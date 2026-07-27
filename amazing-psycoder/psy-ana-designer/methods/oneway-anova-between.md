# 单因素 ANOVA — 被试间 (One-way Between-subjects ANOVA)

## 概述

被试间单因素ANOVA用于比较三组及以上独立样本的均值差异。

**典型场景**：3个年龄组的Stroop效应比较、3种训练方案的成效对比。

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计 | 被试间, 3+组 |
| DV | 连续变量 |
| 假设 | 独立观测；所选均值模型的残差/方差结构与推断方法相容 |

## 假设与检验

1. **分布/影响诊断**：结合模型残差、样本结构和影响点评估，不用每组 Shapiro p 值机械决定方法
2. **方差结构**：预先选择常规或 Welch/稳健模型；Levene 可提供描述性证据，但不作数据驱动切换开关
3. **独立性**：每组不同被试

## 效应量

η²p (偏eta方)或 ω² (omega squared)。ω² 比 η²p 更少偏误,报告时优先考虑。

## 事后比较

事后或计划比较必须先声明 claim family。Tukey、Holm/Bonferroni、层级检验或不校正各自回答不同的比较计划；不能仅因 omnibus p 值显著就自动生成所有两两比较。

## R 代码

```r
library(tidyverse)
library(rstatix)
library(effectsize)

# --- 读入数据 ---
# 长格式：一列 group（因子），一列 score（连续DV）
df <- read_csv("data.csv") |>
  mutate(group = factor(group))

# --- 描述统计 ---
df |>
  group_by(group) |>
  summarise(
    n    = n(),
    M    = mean(score),
    SD   = sd(score),
    .groups = "drop"
  )

# --- 主分析 ---
# 以下两种不是由同一数据上的 Levene p 值自动二选一；按确认的方差模型生成其一。
model <- aov(score ~ group, data = df)
summary(model)

# 异方差 estimand/推断计划的候选实现
oneway.test(score ~ group, data = df, var.equal = FALSE)

# --- 效应量 ---
eta_squared(model, partial = FALSE)   # η²
omega_squared(model, partial = FALSE) # ω²（推荐的校正值）

# --- 已声明的比较族（仅在 config 指定 all-pairwise Tukey 时）---
TukeyHSD(model)

# 或 rstatix 版本（含效应量，推荐在报告时使用）
df |>
  tukey_hsd(score ~ group) |>
  as_tibble()
```

## 报告

APA 7th 标准格式：

> A one-way between-subjects ANOVA was conducted to compare the effect of **[IV]** on **[DV]** for **[描述三组+组别]** .
>
> There was a [significant / non-significant] effect of **[IV]** on **[DV]** at the *p* < .05 level for the three conditions [*F*(*df*₁, *df*₂) = *F*值, *p* = *p*值, η² = .xx].
>
> Post hoc comparisons using the Tukey HSD test indicated that the mean score for **[条件A]** (*M* = *M*值, *SD* = *SD*值) was significantly [higher / lower / different] than **[条件B]** (*M* = *M*值, *SD* = *SD*值), *p* = .xxx. [No other comparisons / …] were statistically significant.

## 备选方法
- **Welch ANOVA**: 当预先声明的 estimand 和异方差均值模型相符
- **Kruskal-Wallis**: 当目标是秩/分布差异且独立同形等解释条件适用；不是“正态性检验失败后的自动替代”
