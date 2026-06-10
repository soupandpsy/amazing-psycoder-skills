# Reviewer — Python 平台独立审计清单

## Quality Gate（审计入口）

| # | 检查项 | grep 命令 | 失败级别 |
|---|--------|----------|---------|
| 1 | seed 已设 | `grep -q "random\.seed\|np\.random\.seed" script.py` | Critical |
| 2 | 排除日志存在 | `grep -q "Exclusion\|排除" script.py` | Critical |
| 3 | 正态性检验 | `grep -q "shapiro\|normaltest\|probplot" script.py` | Major |
| 4 | 方差齐性检验 | `grep -q "levene\|bartlett" script.py` | Major |
| 5 | 效应量 | `grep -q "cohens_d\|compute_effsize\|eta_squared\|pg\.anova" script.py` | Critical |
| 6 | 多重比较校正 | `grep -q "multipletests\|pairwise_tukeyhsd\|adjust" script.py` | Critical |
| 7 | 环境信息 | `grep -q "sys\.version\|pip freeze\|__version__" script.py` | Major |
| 8 | 无绝对路径 | `! grep -q "/Users/\|/home/\|C:\\\\" script.py` | Major |
| 9 | 列名校验 | `grep -q "issubset\|columns.*assert\|set.*columns" script.py` | Critical |
| 10 | 图表保存 | `grep -q "savefig" script.py` | Minor |
| 11 | 包版本 | `grep -q "__version__\|pip freeze\|pkg_resources" script.py` | Major |
| 12 | 敏感性分析 | `grep -q "Sensitivity\|敏感\|Method A.*Method B" script.py` | Minor |

## 统计反模式 Grep 模式

| # | 反模式 | grep（命中=FAIL） | 严重性 |
|---|--------|------------------|--------|
| 1 | `import *` | `grep -q "import \*" script.py` | Critical |
| 2 | 绝对路径 | `grep -qE "/Users/|C:\\\\\|\~/data" script.py` | Major |
| 3 | `iterrows()` | `grep -q "iterrows()" script.py` | Major |
| 4 | 无 `random_state` | `grep -q "scipy\.stats\." script.py && ! grep -q "random_state" script.py` | Critical |
| 5 | 无 `savefig` | `! grep -q "savefig" script.py` | Minor |
| 6 | `chained_assignment` | `grep -q "chained_assignment" script.py` | Major |
| 7 | 逻辑混合模型用 statsmodels | `grep -q "smf\.logit" script.py` + design=within | Critical |
| 8 | `print(df)` 无 head | `grep -q "print(data\|print(df)" script.py && ! grep -q "\.head\|\.info" script.py` | Minor |
| 9 | `df.apply()` 逐行 | `grep -q "\.apply(lambda" script.py` | Major |

## 模型适配检查

| 设计类型 | 预期模式 | grep 验证 |
|---------|---------|----------|
| 被试内 2 组 | `ttest_rel` 或 `MixedLM` | `grep -q "ttest_rel\|MixedLM\|mixedlm" script.py` |
| 被试间 2 组 | `ttest_ind` | `grep -q "ttest_ind\|f_oneway" script.py` |
| 被试内 3+ 组 | `MixedLM` 或 `rm_anova` | `grep -q "MixedLM\|rm_anova" script.py` |
| 混合设计 | `MixedLM` + 交叉效应 | `grep -q "MixedLM.*groups" script.py` |
| 二分类 DV | `Logit` 或 `glmer` (pymer4) | `grep -q "Logit\|pymer4\|bambi" script.py` |
