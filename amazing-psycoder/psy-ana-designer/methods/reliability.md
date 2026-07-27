# 信度分析 (Reliability Analysis)

## 概述

信度分析评估特定总体、用途和测量模型下的分数一致性/稳定性。需要对量表分数作实质推断时通常应报告合适的信度证据，但指标必须匹配用途，不能把 α 当作所有测量的通用质量证书。

**典型场景**: 20题焦虑量表的内部一致性; 两位评分者的一致性。

## 何时使用

| 条件 | 要求 |
|------|------|
| 数据类型 | 连续或有序分类（Likert量表） |
| 题项数量 | 由构念覆盖、模型识别与测量精度决定；题项更多并不自动提高内容效度 |
| 单维性 | 量表应测量单一构念（或使用分层α/ω） |
| 样本信息 | 由题项数、响应分布、层级/评分者结构和目标区间精度决定；报告区间或用模拟评估 |
| 缺失值 | 按缺失机制、层级和 estimand 制定策略；不存在“超过 5% 就必须多重插补”的通用规则 |
| 反向计分 | 反向题须先反转再分析 |

## 信度类型

| 类型 | 指标 | 何时用 |
|------|------|--------|
| 内部一致性 | Cronbach's α / McDonald's ω | 多题量表 |
| 重测信度 | ICC (two-way random) | 前后测 |
| 评分者信度 | Cohen's κ / ICC | 多人评分 |

## Cronbach's α 解读

报告 α 的估计、不确定性、题项/总体/用途和假设。可接受程度取决于决策后果、分数用途和构念宽度；固定的 `.7/.8/.9` 标签不是通用判据，极高 α 也可能反映题项冗余。

## McDonald's ω vs α

ω 基于声明的因子模型，可在该模型合适时放松 α 的 tau-equivalence 假设；模型错配时并不自动“更准确”。根据测量结构和用途选择 α、ω、ICC、广义信度或其他指标，不要求仪式性地全部报告。

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

- 验证性因子分析 (CFA) — 评估量表结构效度，检验单维性假设
- 探索性因子分析 (EFA) — 在信度分析前确定因子结构
- 项目分析 — 评估单个题项的区分度和难度
- 重测信度 → 使用 ICC（组内相关系数）
- 评分者信度 → 使用 Cohen's Kappa 或 Krippendorff's α
- [Bland-Altman 分析](bland-altman.md) — 两种测量方法的一致性评估
