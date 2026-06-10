# 单因素 ANOVA — 被试间 (One-way Between-subjects ANOVA)

## 概述

被试间单因素ANOVA用于比较三组及以上独立样本的均值差异。

**典型场景**：3个年龄组的Stroop效应比较、3种训练方案的成效对比。

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计 | 被试间, 3+组 |
| DV | 连续变量 |
| 假设 | 每组正态+方差齐 |

## 假设与检验

1. **正态性**：每组分别Shapiro-Wilk
2. **方差齐性**：Levene检验。p>0.05→齐,可用常规ANOVA; p<0.05→不齐,用Welch ANOVA
3. **独立性**：每组不同被试

## 效应量

η²p (偏eta方)或 ω² (omega squared)。ω² 比 η²p 更少偏误,报告时优先考虑。

## 事后比较

显著后做两两比较: Tukey HSD (推荐,控制family-wise error) 或 Bonferroni。

## R 代码

```r
library(tidyverse)
library(rstatix)
library(effectsize)
library(car)

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

# --- 假设检验 ---
# 1. 正态性：每组 Shapiro-Wilk
df |>
  group_by(group) |>
  shapiro_test(score)

# 2. 方差齐性：Levene 检验
leveneTest(score ~ group, data = df, center = mean)

# --- 主分析 ---
# 常规 ANOVA（方差齐时）
model <- aov(score ~ group, data = df)
summary(model)

# Welch ANOVA（方差不齐时备选）
oneway.test(score ~ group, data = df, var.equal = FALSE)

# --- 效应量 ---
eta_squared(model, partial = FALSE)   # η²
omega_squared(model, partial = FALSE) # ω²（推荐的校正值）

# --- 事后比较 ---
# Tukey HSD（控制 family-wise error）
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
- **Welch ANOVA**: 方差不齐
- **Kruskal-Wallis**: 非正态

