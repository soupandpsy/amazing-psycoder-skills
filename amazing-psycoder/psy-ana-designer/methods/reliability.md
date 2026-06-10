# 信度分析 (Reliability Analysis)

## 概述

信度分析评估测量工具的稳定性和一致性。在使用问卷/量表数据前**必须**报告。

**典型场景**: 20题焦虑量表的内部一致性; 两位评分者的一致性。

## 何时使用

| 条件 | 要求 |
|------|------|
| 数据类型 | 连续或有序分类（Likert量表） |
| 题项数量 | 至少3题以上，推荐6-12题 |
| 单维性 | 量表应测量单一构念（或使用分层α/ω） |
| 样本量 | 至少 N ≥ 100，N ≥ 300 更稳定 |
| 缺失值 | 缺失比例 < 5%，否则需多重插补 |
| 反向计分 | 反向题须先反转再分析 |

## 信度类型

| 类型 | 指标 | 何时用 |
|------|------|--------|
| 内部一致性 | Cronbach's α / McDonald's ω | 多题量表 |
| 重测信度 | ICC (two-way random) | 前后测 |
| 评分者信度 | Cohen's κ / ICC | 多人评分 |

## Cronbach's α 解读

| α | 评价 |
|-----|------|
| >0.9 | 优秀 |
| 0.8-0.9 | 好 |
| 0.7-0.8 | 可接受 |
| 0.6-0.7 | 存疑 |
| <0.6 | 不可接受 |

## McDonald's ω vs α

ω (omega) 是基于因子分析的信度,比α更准确(不假设tau等价)。推荐同时报告ω和α。

## R 代码

```r
# 信度分析示例
library(psych)

# 模拟数据：20题焦虑量表，N=200，5点Likert
set.seed(123)
n_items <- 20
n_obs <- 200

# 生成有相关结构的模拟数据
items <- matrix(rnorm(n_obs * n_items), nrow = n_obs)
common <- rnorm(n_obs)
df <- data.frame(lapply(1:n_items, function(i) {
  round(pmin(pmax(1 + 0.5 * common + 0.8 * items[, i], 1), 5))
}))
colnames(df) <- paste0("Q", 1:n_items)

# 1. Cronbach's α
alpha_result <- psych::alpha(df)
cat("Cronbach's α:", round(alpha_result$total$raw_alpha, 3), "\n")

# 2. McDonald's ω（基于单因子模型的信度）
omega_result <- psych::omega(df, nfactors = 1, plot = FALSE)
cat("McDonald's ω (total):", round(omega_result$omega.tot, 3), "\n")

# 3. 如果删除某题后的α
cat("\n如果删除某题后的α:\n")
print(round(alpha_result$alpha.drop[, "raw_alpha"], 3))

# 4. 校正题总相关
cat("\n校正题总相关:\n")
print(round(alpha_result$item.stats$r.drop, 3))

# 5. 描述统计
cat("\n描述统计:\n")
print(psych::describe(df)[, c("mean", "sd", "skew", "kurtosis")])

# 6. 平均项间相关（效应量参考）
cat("\n平均项间相关:", round(alpha_result$total$average_r, 3), "\n")
```

## 报告格式 (APA 7th)

**模板**:

> Internal consistency was evaluated using Cronbach's α and McDonald's ω. The [N]-item [scale name] demonstrated [excellent/good/acceptable] reliability, Cronbach's α = .XX, 95% CI [.XX, .XX], McDonald's ω = .XX. Corrected item-total correlations ranged from .XX to .XX. Descriptive statistics for individual items are presented in Table X.

**示例**:

> Internal consistency was evaluated using Cronbach's α and McDonald's ω. The 20-item Anxiety Scale demonstrated good reliability, Cronbach's α = .87, 95% CI [.84, .90], McDonald's ω = .89. Corrected item-total correlations ranged from .42 to .78. No item removal would have substantially improved α (all α-if-deleted > .85). Descriptive statistics for individual items are presented in Table 1.

**表格示例**:

Table 1  
*Item-Level Descriptive Statistics and Reliability for the Anxiety Scale*

| 题项 | M | SD | 校正题总相关 | α-if-deleted |
|------|---|---|------------|-------------|
| Q1 | 3.24 | 1.12 | .62 | .86 |
| Q2 | 3.51 | 0.98 | .55 | .86 |
| ... | ... | ... | ... | ... |

## 备选方法

- [验证性因子分析 (CFA)](cfa.md) — 评估量表结构效度，检验单维性假设
- [探索性因子分析 (EFA)](efa.md) — 在信度分析前确定因子结构
- [项目分析](item-analysis.md) — 评估单个题项的区分度和难度
- 重测信度 → 使用 [ICC](icc.md)（组内相关系数）
- 评分者信度 → 使用 [Cohen's Kappa](cohens-kappa.md) 或 [Krippendorff's α](krippendorff-alpha.md)
- [Bland-Altman 分析](bland-altman.md) — 两种测量方法的一致性评估

