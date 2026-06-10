# ============================================================
# 分析项目：Stroop 颜色-词义冲突任务
# 统计模型：线性混合模型（statsmodels MixedLM）
# 实验设计：单因素被试内（condition: congruent vs incongruent）
# 因变量：反应时（rt, ms）、正确率（acc, 0/1）
# 生成日期：2026-06-11 | 随机种子：20260609
# ============================================================

# ============================================================
# 第 1 步：环境设置
# 加载所有需要的 Python 库，设置 seaborn 主题和随机种子
# ============================================================
import pandas as pd               # 数据处理：DataFrame, groupby, read_csv
import numpy as np                # 数值计算
import scipy.stats as stats       # 统计检验：shapiro, ttest_rel, probplot
import statsmodels.api as sm      # 统计建模
import statsmodels.formula.api as smf  # 公式接口：mixedlm("rt ~ condition", ...)
import pingouin as pg             # 效应量：compute_effsize()
import matplotlib.pyplot as plt   # 绑图底层
import seaborn as sns             # 统计绑图：violinplot, stripplot
import sys                        # 系统信息

np.random.seed(20260609)                      # 固定随机种子，确保可重复
sns.set_theme(style="whitegrid", palette="Set2")  # seaborn 主题 + 色盲友好调色板

# ============================================================
# 第 2 步：数据导入 + 列名校验
# 缺失必需列时立即报错，避免后续静默失败
# ============================================================
data = pd.read_csv("data/stroop_data.csv")

expected_cols = {"subject_id", "condition", "rt", "acc"}
missing_cols = expected_cols - set(data.columns)
if missing_cols:
    raise ValueError(f"缺少列: {missing_cols}")

print(f"已加载 {len(data)} 行, {len(data.columns)} 列")
print(f"被试数: {data['subject_id'].nunique()}, "
      f"条件: {list(data['condition'].unique())}")

# ============================================================
# 第 3 步：数据清洗（四层排除 + 完整日志）
# ============================================================
print("\n========== 排除日志 ==========")
n_before = len(data)

# 3a. RT 范围过滤 —— 排除过快和过慢的试次
rt_lower, rt_upper = 150, 2000
data = data[(data['rt'] > rt_lower) & (data['rt'] < rt_upper)]
n_rt_excluded = n_before - len(data)
print(f"RT 越界 (<{rt_lower} 或 >{rt_upper} ms): "
      f"{n_rt_excluded} 试次 ({100*n_rt_excluded/n_before:.1f}%)")

# 3b. 仅保留正确试次 —— 错误试次的 RT 不可靠
n_with_acc = len(data)
data_rt = data[data['acc'] == 1].copy()
print(f"错误试次排除: {n_with_acc - len(data_rt)} 试次 "
      f"({100*(n_with_acc-len(data_rt))/n_with_acc:.1f}%)")

# 3c. 被试级排除 —— 正确率过低的被试
accuracy_min = 0.6
subj_acc = data.groupby('subject_id')['acc'].mean()
excluded_subj = subj_acc[subj_acc < accuracy_min].index.tolist()
if excluded_subj:
    print(f"正确率低于 {accuracy_min*100:.0f}% 的被试: "
          f"{len(excluded_subj)} (ID: {excluded_subj})")
    data_rt = data_rt[~data_rt['subject_id'].isin(excluded_subj)]
else:
    print(f"正确率低于 {accuracy_min*100:.0f}% 的被试: 0")

# 3d. 试次级排除 —— 按被试×条件，超过 ±2.5 SD 的极端值
sd_multiplier = 2.5
n_before_sd = len(data_rt)
# 计算每个被试在每个条件下的均值和标准差
data_rt['mean_rt_subj'] = data_rt.groupby(
    ['subject_id', 'condition'])['rt'].transform('mean')
data_rt['sd_rt_subj'] = data_rt.groupby(
    ['subject_id', 'condition'])['rt'].transform('std')
# 标记离群值
data_rt['is_outlier'] = (
    abs(data_rt['rt'] - data_rt['mean_rt_subj']) > sd_multiplier * data_rt['sd_rt_subj'])
n_sd_excluded = data_rt['is_outlier'].sum()
print(f"SD 排除 (>{sd_multiplier} SD): "
      f"{n_sd_excluded} 试次 ({100*n_sd_excluded/n_before_sd:.1f}%)")
data_rt = data_rt[~data_rt['is_outlier']]

print(f"最终数据集: {len(data_rt)} 试次, "
      f"{data_rt['subject_id'].nunique()} 被试")

# ============================================================
# 第 4 步：描述统计
# 按条件分组计算：n、被试数、均值、标准差、标准误、95% CI
# ============================================================
print("\n========== 描述统计 ==========")
desc = data_rt.groupby('condition').agg(
    n=('rt', 'count'),                           # 试次数
    n_subj=('subject_id', 'nunique'),             # 被试数
    mean_rt=('rt', 'mean'),                      # 平均 RT
    sd_rt=('rt', 'std'),                         # RT 标准差
).reset_index()
desc['se_rt'] = desc['sd_rt'] / np.sqrt(desc['n_subj'])           # 标准误
desc['ci95_lo'] = desc['mean_rt'] - stats.t.ppf(
    0.975, desc['n_subj'] - 1) * desc['se_rt']                    # 95% CI 下界
desc['ci95_hi'] = desc['mean_rt'] + stats.t.ppf(
    0.975, desc['n_subj'] - 1) * desc['se_rt']                    # 95% CI 上界
print(desc.round(1).to_string())

# ============================================================
# 第 5 步：统计假设检验
# Shapiro-Wilk 正态性检验 + Q-Q 图，按条件分别检验
# ============================================================
print("\n========== 假设检验 ==========")
for cond in data_rt['condition'].unique():
    subset = data_rt[data_rt['condition'] == cond]['rt']
    W, p = stats.shapiro(subset)
    verdict = "通过" if p > 0.05 else "未通过"
    print(f"  {cond}: W = {W:.3f}, p = {p:.3f} [{verdict}]")

# Q-Q 图：点贴近对角线 = 数据近似正态
fig, axes = plt.subplots(
    1, data_rt['condition'].nunique(), figsize=(10, 4))
if data_rt['condition'].nunique() == 1:
    axes = [axes]  # 确保 axes 可迭代
for ax, (cond, grp) in zip(axes, data_rt.groupby('condition')):
    stats.probplot(grp['rt'], dist="norm", plot=ax)
    ax.set_title(f"Q-Q 图: {cond}")
plt.tight_layout()
plt.savefig("output/fig_qq.png", dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# 第 6 步：统计建模
# 线性混合模型：rt ~ condition + 随机效应(被试)
# 固定效应: condition（一致 vs 不一致的 RT 差异）
# 随机效应: 每个被试有自己的基线 RT + 条件效应
# ============================================================
print("\n========== 统计模型 ==========")
model = smf.mixedlm(
    "rt ~ condition",                    # 固定效应公式
    data_rt,                             # 试次级数据（不聚合）
    groups=data_rt["subject_id"],        # 随机截距：按被试分组
    re_formula="~condition"              # 随机斜率：每被试的条件效应
)
result = model.fit(method="lbfgs")       # L-BFGS 优化器
print(result.summary())

# ============================================================
# 第 7 步：效应量
# 使用 pingouin 计算被试内 Cohen's d（基于被试×条件均值）
# ============================================================
print("\n========== 效应量 ==========")
# 聚合到被试×条件均值
data_agg = data_rt.groupby(
    ['subject_id', 'condition'])['rt'].mean().reset_index()
conditions = data_rt['condition'].unique()
eff = pg.compute_effsize(
    data_agg[data_agg['condition'] == conditions[0]]['rt'],
    data_agg[data_agg['condition'] == conditions[1]]['rt'],
    paired=True,         # 被试内设计必须指定 paired=True
    eftype='cohen'       # Cohen's d
)
print(f"Cohen's d (被试内): {eff:.3f}")
print("解释: 0.2 = 小, 0.5 = 中, 0.8 = 大")

# ============================================================
# 第 8 步：敏感性分析
# 用配对 t 检验（方法 A）与混合模型（方法 B）比较
# 如果两者结论一致 → 结果稳健
# ============================================================
print("\n========== 敏感性分析 ==========")
c1 = data_agg[data_agg['condition'] == conditions[0]]['rt'].values
c2 = data_agg[data_agg['condition'] == conditions[1]]['rt'].values

# 方法 A：配对 t 检验
t_stat, t_p = stats.ttest_rel(c1, c2)
d_val = pg.compute_effsize(c1, c2, paired=True, eftype='cohen')
print(f"方法 A (配对 t 检验): t = {t_stat:.2f}, p = {t_p:.4f}, d = {d_val:.2f}")

# 方法 B：线性混合模型
lmer_p = result.pvalues.iloc[1]  # condition 的 p 值
print(f"方法 B (MixedLM): p = {lmer_p:.4f}")

agree = ("是 —— 结论稳健"
         if (t_p < 0.05) == (lmer_p < 0.05)
         else "否 —— 需进一步检查")
print(f"两种方法结论一致: {agree}")

# ============================================================
# 第 9 步：图表生成
# 图 1：小提琴 + 散点（雨云图的 Python 等价实现）
# 图 2：个体连线图
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 图 1: 小提琴图 + 散点 —— 展示完整分布 + 个体数据点
sns.violinplot(data=data_rt, x='condition', y='rt',
               inner=None, ax=axes[0])
sns.stripplot(data=data_rt, x='condition', y='rt',
              alpha=0.3, size=3, ax=axes[0])
axes[0].set_title("Stroop: 各条件反应时")
axes[0].set_ylabel("反应时 (ms)")

# 图 2: 个体连线图 —— 灰色线 = 个体变化, 红色线 = 组均值
for subj in data_agg['subject_id'].unique():
    subj_data = data_agg[data_agg['subject_id'] == subj]
    axes[1].plot(
        subj_data['condition'].map({c: i for i, c in enumerate(conditions)}),
        subj_data['rt'],
        alpha=0.3, linewidth=0.5, color='gray')
means = data_agg.groupby('condition')['rt'].mean()
axes[1].plot(range(len(means)), means.values, 'r-', linewidth=2)
axes[1].set_title("Stroop: 个体 RT 变化")
axes[1].set_ylabel("平均反应时 (ms)")
axes[1].set_xticks(range(len(conditions)))
axes[1].set_xticklabels(conditions)

plt.tight_layout()
plt.savefig("output/fig_stroop.png", dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# 第 10 步：环境信息 —— 确保分析完全可重复
# ============================================================
print("\n========== 环境信息 ==========")
print(f"分析生成时间: {pd.Timestamp.now()}")
print(f"Python 版本: {sys.version}")
for pkg in ['pandas', 'numpy', 'scipy', 'statsmodels',
             'pingouin', 'matplotlib', 'seaborn']:
    mod = __import__(pkg)
    print(f"  {pkg}: {mod.__version__}")
