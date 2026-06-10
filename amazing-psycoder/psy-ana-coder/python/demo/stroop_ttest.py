# ============================================================
# 分析项目：Stroop 颜色-词义冲突任务
# 统计模型：配对 t 检验（被试内，基于每被试每条件的均值）
# 实验设计：单因素被试内（condition: congruent vs incongruent）
# 因变量：反应时（rt, ms）
# 生成日期：2026-06-11 | 随机种子：20260610
# ============================================================

# ============================================================
# 第 1 步：环境设置
# 加载需要的库，设置绘图主题和随机种子
# ============================================================
import pandas as pd               # 数据处理
import numpy as np                # 数值计算
import scipy.stats as stats       # 统计检验：shapiro, ttest_rel, probplot
import pingouin as pg             # 效应量：compute_effsize()
import matplotlib.pyplot as plt   # 绑图
import seaborn as sns             # 统计绑图
import sys                        # 系统信息

np.random.seed(20260610)                      # 固定随机种子
sns.set_theme(style="whitegrid", palette="Set2")

# ============================================================
# 第 2 步：数据导入 + 列名校验
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

# 3a. RT 范围过滤
rt_lower, rt_upper = 150, 2000
data = data[(data['rt'] > rt_lower) & (data['rt'] < rt_upper)]
print(f"RT 越界 (<{rt_lower} 或 >{rt_upper} ms): "
      f"{n_before - len(data)} 试次 "
      f"({100*(n_before-len(data))/n_before:.1f}%)")

# 3b. 仅保留正确试次
n_with_acc = len(data)
data_rt = data[data['acc'] == 1].copy()
print(f"错误试次排除: {n_with_acc - len(data_rt)} 试次 "
      f"({100*(n_with_acc-len(data_rt))/n_with_acc:.1f}%)")

# 3c. 被试级排除
accuracy_min = 0.6
subj_acc = data.groupby('subject_id')['acc'].mean()
excluded_subj = subj_acc[subj_acc < accuracy_min].index.tolist()
if excluded_subj:
    print(f"正确率低于 {accuracy_min*100:.0f}% 的被试: "
          f"{len(excluded_subj)} (ID: {excluded_subj})")
    data_rt = data_rt[~data_rt['subject_id'].isin(excluded_subj)]
else:
    print(f"正确率低于 {accuracy_min*100:.0f}% 的被试: 0")

# 3d. 试次级排除（按被试×条件）
sd_multiplier = 2.5
n_before_sd = len(data_rt)
data_rt['mean_rt_subj'] = data_rt.groupby(
    ['subject_id', 'condition'])['rt'].transform('mean')
data_rt['sd_rt_subj'] = data_rt.groupby(
    ['subject_id', 'condition'])['rt'].transform('std')
data_rt['is_outlier'] = (
    abs(data_rt['rt'] - data_rt['mean_rt_subj']) > sd_multiplier * data_rt['sd_rt_subj'])
print(f"SD 排除 (>{sd_multiplier} SD): "
      f"{data_rt['is_outlier'].sum()} 试次 "
      f"({100*data_rt['is_outlier'].sum()/n_before_sd:.1f}%)")
data_rt = data_rt[~data_rt['is_outlier']]

print(f"最终数据集: {len(data_rt)} 试次, "
      f"{data_rt['subject_id'].nunique()} 被试")

# ============================================================
# 第 4 步：聚合到被试均值
# 配对 t 检验分析的是每被试每条件的均值，而非原始试次
# ============================================================
data_agg = data_rt.groupby(
    ['subject_id', 'condition'])['rt'].mean().reset_index()

# ============================================================
# 第 5 步：描述统计（基于被试均值）
# ============================================================
print("\n========== 描述统计 ==========")
desc = data_agg.groupby('condition').agg(
    n=('rt', 'count'),                     # 被试数
    mean_rt=('rt', 'mean'),                # 平均 RT
    sd_rt=('rt', 'std'),                   # 被试间标准差
).reset_index()
desc['se_rt'] = desc['sd_rt'] / np.sqrt(desc['n'])
desc['ci95_lo'] = desc['mean_rt'] - stats.t.ppf(
    0.975, desc['n'] - 1) * desc['se_rt']
desc['ci95_hi'] = desc['mean_rt'] + stats.t.ppf(
    0.975, desc['n'] - 1) * desc['se_rt']
print(desc.round(1).to_string())

# ============================================================
# 第 6 步：统计假设检验
# 配对 t 检验的关键假设：两种条件的差值服从正态分布
# 注意：检查的是差值正态性，而非原始数据的正态性！
# ============================================================
print("\n========== 假设检验 ==========")
conditions = data_rt['condition'].unique()
c1 = data_agg[data_agg['condition'] == conditions[0]]['rt'].values
c2 = data_agg[data_agg['condition'] == conditions[1]]['rt'].values
diff = c2 - c1  # 每被试的差值

# Shapiro-Wilk 差值正态性检验
W, p = stats.shapiro(diff)
verdict = "通过" if p > 0.05 else "未通过"
print(f"差值正态性检验: W = {W:.3f}, p = {p:.3f} [{verdict}]")

# Q-Q 图：差值正态性可视化
fig, ax = plt.subplots(figsize=(5, 4))
stats.probplot(diff, dist="norm", plot=ax)
ax.set_title("Q-Q 图: RT 差值（不一致 − 一致）\n点贴近红线 = 差值近似正态")
plt.tight_layout()
plt.savefig("output/fig_qq.png", dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# 第 7 步：统计检验
# 配对 t 检验：比较同一批被试在两种条件下的均值差异
# ============================================================
print("\n========== 配对 t 检验 ==========")
t_stat, t_p = stats.ttest_rel(c1, c2)
mean_diff = np.mean(diff)
ci = stats.t.interval(
    0.95, len(diff) - 1,
    loc=mean_diff,
    scale=stats.sem(diff))  # 差值的 95% CI
print(f"t({len(diff) - 1}) = {t_stat:.2f}, p = {t_p:.4f}")
print(f"均值差: {mean_diff:.1f} ms [{ci[0]:.1f}, {ci[1]:.1f}]")

# ============================================================
# 第 8 步：效应量
# Cohen's dz（被试内设计推荐）：差值均值 / 差值标准差
# ============================================================
print("\n========== 效应量 ==========")
dz = pg.compute_effsize(c1, c2, paired=True, eftype='cohen')
print(f"Cohen's dz = {dz:.2f}")
print("解释: 0.2 = 小, 0.5 = 中, 0.8 = 大")

# ============================================================
# 第 9 步：图表生成
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 图 1: 小提琴 + 散点（雨云图的 Python 实现）
sns.violinplot(data=data_agg, x='condition', y='rt',
               inner=None, ax=axes[0])
sns.stripplot(data=data_agg, x='condition', y='rt',
              alpha=0.3, size=3, ax=axes[0])
axes[0].set_title("Stroop: 各条件反应时")
axes[0].set_ylabel("平均反应时 (ms)")

# 图 2: 个体连线图 —— 灰色线 = 个体, 红色线 = 组均值趋势
for subj in data_agg['subject_id'].unique():
    subj_data = data_agg[data_agg['subject_id'] == subj]
    axes[1].plot([0, 1], subj_data['rt'].values,
                 alpha=0.3, linewidth=0.5, color='gray')
means = data_agg.groupby('condition')['rt'].mean()
axes[1].plot([0, 1], means.values, 'r-', linewidth=2)
axes[1].set_title("Stroop: 个体 RT 变化")
axes[1].set_ylabel("平均反应时 (ms)")
axes[1].set_xticks([0, 1])
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
for pkg in ['pandas', 'numpy', 'scipy', 'pingouin', 'matplotlib', 'seaborn']:
    mod = __import__(pkg)
    print(f"  {pkg}: {mod.__version__}")
