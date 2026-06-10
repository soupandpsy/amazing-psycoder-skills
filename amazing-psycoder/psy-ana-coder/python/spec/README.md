# Python 分析平台 — API 规范

## Canonical Code Skeleton

所有生成的 Python 脚本必须遵循此 12 步骨架：

```
1. 标题注释     ← 实验名、模型、日期、seed
2. 环境设置     ← import、np.random.seed、全局设置
3. 数据导入     ← pd.read_csv + 列名校验（缺列→raise）
4. 数据清洗     ← RT过滤→正确试次→被试排除→SD排除→缺失处理
5. 排除日志     ← print() 每步排除量+比例
6. 描述统计     ← groupby+agg: n, mean, sd, se, ci95
7. 假设检验     ← Shapiro-Wilk + QQ图 + Levene（按需）
8. 统计建模     ← ttest/scipy.stats/statsmodels（按config选择）
9. 效应量       ← cohens_d/eta_squared（pingouin）
10. 事后比较    ← pairwise_tukeyhsd/statsmodels
11. 图表生成    ← matplotlib + seaborn + plt.savefig
12. 环境信息    ← sys.version + pip freeze
```

---

## API 速查

| 操作 | Python 代码 | 包 |
|------|-----------|-----|
| 数据导入 | `pd.read_csv(path)` | pandas |
| 过滤 | `df[df['col'] > val]` 或 `df.query()` | pandas |
| 分组汇总 | `df.groupby('col').agg({'dv': ['mean','std','count']})` | pandas |
| 创建变量 | `df['new'] = expr` | pandas |
| 管道 | `df.pipe(func1).pipe(func2)` 或链式调用 | pandas |
| 数据重塑 | `pd.pivot_table()` / `pd.melt()` | pandas |
| 配对t检验 | `scipy.stats.ttest_rel(a, b)` | scipy |
| 独立t检验 | `scipy.stats.ttest_ind(a, b)` | scipy |
| 被试内ANOVA | `pg.rm_anova(data, dv, within, subject)` | pingouin |
| 被试间ANOVA | `scipy.stats.f_oneway(*groups)` | scipy |
| 线性混合模型 | `smf.mixedlm("dv ~ cond", data, groups="subj")` | statsmodels |
| 逻辑混合模型 | `smf.logit("dv ~ cond", data)` + 手动 RE | statsmodels |
| 正态性 | `scipy.stats.shapiro(x)` | scipy |
| 方差齐性 | `scipy.stats.levene(*groups)` | scipy |
| Cohen's d | `pg.compute_effsize(x, y, eftype='cohen')` | pingouin |
| η² | `pg.anova(data, dv, between, detailed=True)` | pingouin |
| 事后比较 | `statsmodels.stats.multicomp.pairwise_tukeyhsd()` | statsmodels |
| 雨云图 | `ptitprince.RainCloud()` | ptitprince |
| 小提琴图 | `sns.violinplot()` + `sns.stripplot()` | seaborn |
| 保存图 | `plt.savefig(path, dpi=300, bbox_inches='tight')` | matplotlib |
| 随机种子 | `np.random.seed(n)` | numpy |
| 环境信息 | `!pip freeze` 或 `sys.version` | sys |

---

## 反模式 (12 项)

| # | 反模式 | 替代 |
|---|--------|------|
| 1 | `import *` | `import pandas as pd` |
| 2 | 硬编码路径 | 从 config 读取或 `pathlib.Path` |
| 3 | `df.apply()` 逐行循环 | 向量化操作或 `df.transform()` |
| 4 | 不设 `random_state` | 所有随机函数传入 `random_state={seed}` |
| 5 | `print(df)` 输出全部 | `print(df.head())` 或 `df.info()` |
| 6 | 不检查列存在 | `assert set(cols).issubset(df.columns)` |
| 7 | 排除标准不输出 | print() 每步排除日志 |
| 8 | 多重比较不校正 | `multipletests(pvals, method='bonferroni')` |
| 9 | 无效应量报告 | 所有检验附带 pingouin 效应量 |
| 10 | 图表不保存 | `plt.savefig()` 输出到磁盘 |
| 11 | 不输出环境信息 | `sys.version` + `!pip freeze` |
| 12 | `pd.set_option('mode.chained_assignment', None)` 关闭警告 | 用 `.loc[]` 正确赋值 |

---

## 必装包

```bash
pip install pandas numpy scipy statsmodels pingouin matplotlib seaborn ptitprince
```

---

## Canonical Code Skeleton（完整 12 步模板）

以下模板可直接填入 config 字段生成完整 Python 脚本。所有 `{placeholder}` 从 analysis config YAML 读取。

### 步骤 1-2: 环境设置 + 数据导入

```python
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns
import ptitprince as pt
import sys
from pathlib import Path

np.random.seed({seed})

# ── 数据导入 ──
data = pd.read_csv("{data_path}")
expected_cols = ["{subject_col}", "{condition_col}", "{rt_col}", "{acc_col}"]
missing_cols = set(expected_cols) - set(data.columns)
if missing_cols:
    raise ValueError(f"Missing columns: {missing_cols}")
print(f"Loaded {data.shape[0]} rows, {data.shape[1]} cols")
```

### 步骤 3: 数据清洗

```python
n_before = data.shape[0]

# RT 过滤
data = data[(data["{rt_col}"] > {rt_lower}) & (data["{rt_col}"] < {rt_upper})]
n_rt = n_before - data.shape[0]
print(f"RT outliers: {n_rt} ({100*n_rt/n_before:.1f}%)")

# 正确试次
n_with_acc = data.shape[0]
data_rt = data[data["{acc_col}"] == 1].copy()
print(f"Incorrect: {n_with_acc - data_rt.shape[0]} ({100*(n_with_acc - data_rt.shape[0])/n_with_acc:.1f}%)")

# 被试排除（正确率过低）
subj_acc = data.groupby("{subject_col}")["{acc_col}"].mean().reset_index()
subj_acc.columns = ["{subject_col}", "mean_acc"]
excluded_subj = subj_acc[subj_acc["mean_acc"] < {accuracy_min}]
if len(excluded_subj) > 0:
    data_rt = data_rt[~data_rt["{subject_col}"].isin(excluded_subj["{subject_col}"])]
    print(f"Subjects <{accuracy_min*100:.0f}% acc: {len(excluded_subj)}")
else:
    print(f"Subjects <{accuracy_min*100:.0f}% acc: 0")

# SD 排除（被试内 × 条件内）
data_rt["mean_rt"] = data_rt.groupby(["{subject_col}", "{condition_col}"])["{rt_col}"].transform("mean")
data_rt["sd_rt"] = data_rt.groupby(["{subject_col}", "{condition_col}"])["{rt_col}"].transform("std")
data_rt["is_outlier"] = np.abs(data_rt["{rt_col}"] - data_rt["mean_rt"]) > {sd_multiplier} * data_rt["sd_rt"]
n_sd = data_rt["is_outlier"].sum()
print(f"SD exclusion: {n_sd} ({100*n_sd/data_rt.shape[0]:.1f}%)")
data_rt = data_rt[~data_rt["is_outlier"]].copy()
data_rt.drop(columns=["mean_rt", "sd_rt", "is_outlier"], inplace=True)
print(f"Final N = {data_rt.shape[0]}")
```

### 步骤 4: 描述统计

```python
def se(x):
    return np.std(x, ddof=1) / np.sqrt(len(x))

desc = data_rt.groupby("{condition_col}").agg(
    n=("{rt_col}", "count"),
    n_subj=("{subject_col}", "nunique"),
    mean_rt=("{rt_col}", "mean"),
    sd_rt=("{rt_col}", "std"),
    median_rt=("{rt_col}", "median")
).reset_index()

desc["se_rt"] = desc["sd_rt"] / np.sqrt(desc["n_subj"])
desc["ci95_lo"] = desc["mean_rt"] - stats.t.ppf(0.975, desc["n_subj"] - 1) * desc["se_rt"]
desc["ci95_hi"] = desc["mean_rt"] + stats.t.ppf(0.975, desc["n_subj"] - 1) * desc["se_rt"]

print(desc.to_string(index=False))
```

### 步骤 5: 假设检验

```python
# Shapiro-Wilk（按条件）
for cond in data_rt["{condition_col}"].unique():
    vals = data_rt[data_rt["{condition_col}"] == cond]["{rt_col}"]
    W, p = stats.shapiro(vals)
    verdict = "PASS" if p > 0.05 else "FAIL"
    print(f"Shapiro-Wilk ({cond}): W={W:.4f}, p={p:.4f} [{verdict}]")

# Q-Q 图
fig, axes = plt.subplots(1, data_rt["{condition_col}"].nunique(), figsize=(5*data_rt["{condition_col}"].nunique(), 4))
if data_rt["{condition_col}"].nunique() == 1:
    axes = [axes]
for ax, (cond, grp) in zip(axes, data_rt.groupby("{condition_col}")):
    stats.probplot(grp["{rt_col}"], dist="norm", plot=ax)
    ax.set_title(f"Q-Q: {cond}")
plt.tight_layout()
plt.show()

# Levene 方差齐性检验
groups = [grp["{rt_col}"].values for _, grp in data_rt.groupby("{condition_col}")]
W, p = stats.levene(*groups)
print(f"Levene: W={W:.4f}, p={p:.4f}" + (" [PASS]" if p > 0.05 else " [FAIL]"))
```

### 步骤 6: 统计模型

```python
# 根据 config model.type 选择以下之一：

# ── 配对 t 检验 ──
# data_agg = data_rt.groupby(["{subject_col}", "{condition_col}"])["{rt_col}"].mean().reset_index()
# conds = data_agg["{condition_col}"].unique()
# t, p = stats.ttest_rel(
#     data_agg[data_agg["{condition_col}"] == conds[0]]["{rt_col}"],
#     data_agg[data_agg["{condition_col}"] == conds[1]]["{rt_col}"]
# )
# print(f"Paired t-test: t={t:.4f}, df={len(data_agg)//2 - 1}, p={p:.4f}")

# ── 被试内 ANOVA (pingouin) ──
# aov = pg.rm_anova(data=data_rt, dv="{rt_col}", within="{condition_col}", subject="{subject_col}", detailed=True)
# print(aov)

# ── 线性混合模型 (statsmodels) ──
# model = smf.mixedlm("{rt_col} ~ {fixed_effects}", data=data_rt, groups=data_rt["{subject_col}"],
#                      re_formula="1 + {condition_col}").fit(reml=True)
# print(model.summary())

# ── 逻辑混合模型 (statsmodels) ──
# import statsmodels.api as sm
# model = smf.logit("{acc_col} ~ {fixed_effects}", data=data).fit()
# print(model.summary())

# ── Gamma 混合模型 (statsmodels) ──
# model = smf.mixedlm("{rt_col} ~ {fixed_effects}", data=data_rt, groups=data_rt["{subject_col}"],
#                      re_formula="1 + {condition_col}").fit(reml=True)
# print(model.summary())
```

### 步骤 7: 效应量

```python
# 根据 config model.type 选择：

# ── Cohen's d (配对) ──
# conds = data_agg["{condition_col}"].unique()
# d = pg.compute_effsize(
#     data_agg[data_agg["{condition_col}"] == conds[0]]["{rt_col}"],
#     data_agg[data_agg["{condition_col}"] == conds[1]]["{rt_col}"],
#     paired=True, eftype="cohen"
# )
# print(f"Cohen's d = {d:.4f}")

# ── η² (ANOVA) ──
# aov = pg.rm_anova(data=data_rt, dv="{rt_col}", within="{condition_col}", subject="{subject_col}", detailed=True)
# ng2 = aov["ng2"].values[0]
# print(f"Generalized η² = {ng2:.4f}")

# ── R² (混合模型) ──
# null_model = smf.mixedlm("{rt_col} ~ 1", data=data_rt, groups=data_rt["{subject_col}"]).fit(reml=True)
# r2_marg = 1 - model.llf / null_model.llf
# print(f"Marginal R² (pseudo) = {r2_marg:.4f}")

# ── Odds Ratio (逻辑回归) ──
# or_vals = np.exp(model.params)
# ci = np.exp(model.conf_int())
# print("Odds Ratios:")
# print(pd.DataFrame({"OR": or_vals, "CI_low": ci.iloc[:, 0], "CI_high": ci.iloc[:, 1]}))
```

### 步骤 8: 事后比较

```python
# ── Tukey HSD (statsmodels) ──
# tukey = pairwise_tukeyhsd(data_rt["{rt_col}"], data_rt["{condition_col}"], alpha=0.05)
# print(tukey)

# ── pingouin 配对事后（含多重比较校正） ──
# posthoc = pg.pairwise_ttests(data=data_rt, dv="{rt_col}", within="{condition_col}",
#                               subject="{subject_col}", padjust="{correction}")
# print(posthoc[["Contrast", "A", "B", "T", "dof", "p-unc", "p-corr"]].to_string(index=False))
```

### 步骤 9: 敏感性分析

```python
# 方法 A vs 方法 B 一致性检查
# ── 方法 A: 配对 t 检验 ──
data_agg = data_rt.groupby(["{subject_col}", "{condition_col}"])["{rt_col}"].mean().reset_index()
conds = data_agg["{condition_col}"].unique()
t_val, p_a = stats.ttest_rel(
    data_agg[data_agg["{condition_col}"] == conds[0]]["{rt_col}"],
    data_agg[data_agg["{condition_col}"] == conds[1]]["{rt_col}"]
)
d_val = pg.compute_effsize(
    data_agg[data_agg["{condition_col}"] == conds[0]]["{rt_col}"],
    data_agg[data_agg["{condition_col}"] == conds[1]]["{rt_col}"],
    paired=True, eftype="cohen"
)
print(f"A (t-test): t={t_val:.2f}, p={p_a:.4f}, d={d_val:.2f}")

# ── 方法 B: 线性混合模型 ──
model = smf.mixedlm("{rt_col} ~ C({condition_col})", data=data_rt, groups=data_rt["{subject_col}"]).fit(reml=True)
p_b = model.pvalues.iloc[1]
print(f"B (lmer): p={p_b:.4f}")
agree = "YES ✓" if (p_a < 0.05) == (p_b < 0.05) else "NO ✗"
print(f"Agree: {agree}")
```

### 步骤 10: 图表

```python
# ── 雨云图 (ptitprince) ──
fig, ax = plt.subplots(figsize=(6, 5))
pt.RainCloud(x="{condition_col}", y="{rt_col}", data=data_rt, palette="Set2",
             bw=0.2, width_viol=0.6, ax=ax, orient="v", alpha=0.5, point_size=2)
ax.set_title("{experiment_name}")
sns.despine()
plt.tight_layout()
plt.savefig(Path("{save_path}") / "fig1_raincloud.png", dpi=300, bbox_inches="tight")
plt.show()

# ── 个体连线图 ──
fig, ax = plt.subplots(figsize=(6, 5))
# 折线
for subj, grp in data_agg.groupby("{subject_col}"):
    ax.plot(grp["{condition_col}"], grp["{rt_col}"], alpha=0.3, linewidth=0.5, color="gray")
# 个体点
sns.stripplot(x="{condition_col}", y="{rt_col}", data=data_agg, alpha=0.3, size=4, ax=ax)
# 组均值折线
means = data_agg.groupby("{condition_col}")["{rt_col}"].mean()
ax.plot(means.index, means.values, linewidth=2, color="red", marker="o", markersize=8)
ax.set_title("Individual Changes")
sns.despine()
plt.tight_layout()
plt.savefig(Path("{save_path}") / "fig2_individual.png", dpi=300, bbox_inches="tight")
plt.show()
```

### 步骤 11: 环境信息

```python
import datetime, platform, importlib

print(f"Generated: {datetime.datetime.now().isoformat()}")
print(f"Python: {sys.version}")
print(f"Platform: {platform.platform()}")

pkgs = ["pandas", "numpy", "scipy", "statsmodels", "pingouin", "matplotlib", "seaborn", "ptitprince"]
for pkg_name in pkgs:
    try:
        mod = importlib.import_module(pkg_name)
        ver = getattr(mod, "__version__", "unknown")
        print(f"  {pkg_name}: {ver}")
    except ImportError:
        print(f"  {pkg_name}: NOT INSTALLED")
```

### 步骤 12: Jupyter / Quarto 报告模板

```yaml
---
title: "{experiment_name} — Analysis Report"
author: "psy-ana-coder"
date: "{date}"
format:
  html:
    toc: true
    toc_float: true
    theme: flatly
jupyter: python3
---

## Exclusion Summary

| Step          | Trials   | %          |
|---------------|----------|------------|
| RT cutoffs    | {n_rt}   | {rt_pct}%  |
| SD exclusion  | {n_sd}   | {sd_pct}%  |
| **Final**     | {n_final}| —          |

## Descriptive Statistics

```{{python}}
print(desc.to_markdown(index=False))
```

## Model Results

```{{python}}
print(model.summary())
```

## Figures

![Raincloud]({{save_path}}/fig1_raincloud.png)

![Individual Lines]({{save_path}}/fig2_individual.png)

## Environment

- Python {python_version}
```
