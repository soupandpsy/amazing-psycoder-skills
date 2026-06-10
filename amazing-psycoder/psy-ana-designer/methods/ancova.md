# 协方差分析 (ANCOVA)

## 概述

ANCOVA 在比较组间差异时控制一个或多个连续协变量的影响,提高统计效力和精度。

**典型场景**: 比较两种训练方法的效果,控制前测成绩的影响。控制年龄比较两组 Stroop 效应。

## 何时使用

| 条件 | 要求 |
|------|------|
| DV | 连续 |
| IV | 分类 |
| 协变量 | 连续,与DV线性相关 |

## 为什么用ANCOVA

- 减少误差方差→提高统计效力
- 校正组间初始差异(准实验设计)
- 调整均值→更准确地估计处理效应

## 关键假设

1. **协变量与DV线性相关**
2. **回归斜率同质性**: 各组间协变量-DV的回归斜率相同(最重要假设)。违背→不能用标准ANCOVA

## R 代码

```r
# 加载必要包
library(car)         # Anova() Type III SS
library(effectsize)  # eta_squared() 效应量
library(emmeans)     # 估计边际均值 (adjusted means)
library(ggplot2)     # 可视化

# ── 模拟数据 ──────────────────────────────────────────
set.seed(123)
n <- 90
group <- factor(rep(c("A", "B", "C"), each = 30))
age <- round(rnorm(n, mean = 25, sd = 5), 1)
# DV: Stroop干扰效应(ms), 控制age的影响
stroop <- 50 +
  ifelse(group == "A", 15, ifelse(group == "B", 28, 2)) +
  0.8 * age + rnorm(n, 0, 10)
df <- data.frame(group, age, stroop)

# ── 1. 检查回归斜率同质性 ──────────────────────────────
# 交互项不显著 → 假设成立
homogeneity <- aov(stroop ~ group * age, data = df)
summary(homogeneity)

# ── 2. 拟合 ANCOVA 模型 ────────────────────────────────
model <- aov(stroop ~ group + age, data = df)

# Type III SS（推荐，处理不平衡设计）
Anova(model, type = "III")

# ── 3. 效应量 ─────────────────────────────────────────
eta_squared(model, partial = TRUE)

# ── 4. 估计边际均值（adjusted means）───────────────────
emm <- emmeans(model, ~ group)
emm
pairs(emm, adjust = "bonferroni")  # 事后比较

# ── 5. 可视化 ─────────────────────────────────────────
ggplot(df, aes(x = age, y = stroop, color = group)) +
  geom_point(alpha = 0.6) +
  geom_smooth(method = "lm", se = FALSE, linewidth = 1.2) +
  labs(
    title = "ANCOVA: Stroop干扰效应 ~ 组别 + 年龄",
    x = "年龄 (岁)", y = "Stroop 干扰效应 (ms)",
    color = "组别"
  ) +
  theme_minimal()
```

## 报告

> ANCOVA compared Stroop interference between groups controlling for age. The group effect was significant after adjustment, F(2,96)=5.32, p=.006, η²p=.10. Adjusted means: Group A=65ms, Group B=78ms, Group C=52ms.

## 备选方法

- 无协变量或协变量不满足假设 → [单因素方差分析 (One-way ANOVA)](anova.md)
- 多个DV → [多元协方差分析 (MANCOVA)](mancova.md)
- 协变量与DV非线性 → [分层回归 (Hierarchical Regression)](hierarchical-regression.md)
- 组间初始差异大且无法用协变量校正 → [倾向得分匹配 (Propensity Score Matching)](propensity-score-matching.md)
- 重复测量设计 → [重复测量ANCOVA](repeated-measures-ancova.md)
