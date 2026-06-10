# 两因素被试内 ANOVA

## 概述

两因素被试内 ANOVA 用于 2×2 或更复杂的被试内设计。所有被试接受所有条件组合。

**典型场景**: 2(一致性: 一致/不一致) × 2(SOA: 短/长) 的 Stroop 效应比较。

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计 | 被试内, 两个分类IV |
| DV | 连续 |
| 假设 | 每条件组合正态 + 球对称 |

## 关键输出

- **主效应**: A因素的主效应, B因素的主效应
- **交互作用**: A×B交互是否显著
- **简单效应**: 交互显著后,在B的每个水平上检验A的效应

交互显著时,主效应不能直接解释——必须先分析简单效应。

## 效应量: η²p

报告每个效应(主效应A、主效应B、交互A×B)的η²p。

## R 代码

```r
library(tidyverse)
library(afex)
library(rstatix)

# 模拟 2×2 被试内设计数据 (Stroop RT)
set.seed(42)
n <- 30
df <- expand.grid(
  subject = factor(1:n),
  congruency = c("congruent", "incongruent"),
  SOA = c("short", "long")
) %>%
  mutate(
    RT = case_when(
      congruency == "congruent" & SOA == "short"   ~ rnorm(n, 450, 50),
      congruency == "congruent" & SOA == "long"    ~ rnorm(n, 430, 50),
      congruency == "incongruent" & SOA == "short" ~ rnorm(n, 520, 55),
      congruency == "incongruent" & SOA == "long"  ~ rnorm(n, 480, 55)
    )
  )

# 两因素被试内方差分析 (GG校正 + η²p)
model <- aov_ez(
  id = "subject",
  dv = "RT",
  within = c("congruency", "SOA"),
  data = df,
  anova_table = list(correction = "GG", es = "pes")
)
print(model)

# 简单效应分析 (交互显著时)
df %>%
  group_by(SOA) %>%
  anova_test(dv = RT, wid = subject, within = congruency) %>%
  get_anova_table(correction = "GG")

# 描述统计
df %>%
  group_by(congruency, SOA) %>%
  summarise(mean = mean(RT), sd = sd(RT), .groups = "drop")
```

## 报告格式

> A 2×2 repeated measures ANOVA examined the effects of congruency and SOA on RT. The main effect of congruency was significant, F(1,29)=45.2, p<.001, η²p=.61. The congruency×SOA interaction was significant, F(1,29)=8.3, p=.008, η²p=.22. Simple effects revealed...

## 备选方法

- **lmer**: 推荐替代,两因素被试内直接用 `lmer(dv ~ A*B + (1+A*B|subject))`
