# 多元线性回归 (Multiple Regression)

## 概述

多元回归用一个或多个连续型预测变量来预测连续型结果变量。在心理学中广泛用于分析多个因素对行为的共同影响。

**典型场景**: 用年龄、教育年限、焦虑分数预测 Stroop 干扰效应。

## 何时使用

| 条件 | 要求 |
|------|------|
| DV | 连续 |
| IV | 连续或分类(需虚拟编码) |
| 目标 | 预测/解释 DV 的方差 |

## 关键输出

- **R²**: 模型整体解释的方差比例
- **ΔR²**: 加入某变量后方差增量(层次回归)
- **β权重**: 标准化回归系数(可比变量间相对重要性)
- **b**: 非标准化系数(用于预测)
- **VIF**: 多重共线性诊断(VIF>5→共线性问题)

## 层次回归 (Hierarchical Regression)

分步进入变量,检验每一步的ΔR²是否显著:

Step 1: 控制变量 (年龄、性别) → R²=.05
Step 2: 主要预测变量 (焦虑) → ΔR²=.12, p<.001
Step 3: 交互项 → ΔR²=.03, p=.04

## R 代码

```r
# 多元线性回归 — 完整分析流程
library(car)       # vif() 共线性诊断
library(lm.beta)   # lm.beta() 标准化系数

# ---- 模拟数据 ----
set.seed(123)
n <- 100
data <- data.frame(
  age       = rnorm(n, mean = 35, sd = 10),
  education = sample(8:20, n, replace = TRUE),
  anxiety   = rnorm(n, mean = 50, sd = 10)
)
# 构造 DV，加入真实效应 + 噪声
data$stroop <- 50 + 0.5 * data$age - 1.5 * data$education +
               0.8 * data$anxiety + rnorm(n, 0, 8)

# ---- 1. 描述统计与相关矩阵 ----
summary(data)
round(cor(data[, c("age", "education", "anxiety", "stroop")]), 3)

# ---- 2. 多元回归 ----
model <- lm(stroop ~ age + education + anxiety, data = data)
summary(model)

# ---- 3. 标准化回归系数 (β 权重) ----
lm.beta::lm.beta(model)

# ---- 4. 多重共线性诊断 (VIF) ----
car::vif(model)          # VIF < 5 表示无严重共线性

# ---- 5. 效应量: Cohen's f² ----
r2 <- summary(model)$r.squared
f2 <- r2 / (1 - r2)
cat(sprintf("Cohen's f² = %.3f (%s)\n", f2,
    ifelse(f2 < 0.15, "small",
    ifelse(f2 < 0.35, "medium", "large"))))
# f²: 0.02 = small, 0.15 = medium, 0.35 = large

# ---- 6. 层次回归 (Hierarchical Regression) ----
model_step1 <- lm(stroop ~ age, data = data)
model_step2 <- lm(stroop ~ age + education + anxiety, data = data)

# ΔR² 显著性检验
anova(model_step1, model_step2)

# 各步骤 R²
cat("Step 1 R²:", round(summary(model_step1)$r.squared, 3), "\n")
cat("Step 2 R²:", round(summary(model_step2)$r.squared, 3), "\n")
cat("ΔR²:",
    round(summary(model_step2)$r.squared - summary(model_step1)$r.squared, 3), "\n")

# ---- 7. Durbin-Watson 自相关检验 ----
car::durbinWatsonTest(model)

# ---- 8. 残差诊断图 ----
par(mfrow = c(2, 2))
plot(model)
par(mfrow = c(1, 1))
```

## 报告格式

> A hierarchical multiple regression predicted Stroop interference. Age and gender were entered at Step 1 (R²=.05), followed by anxiety at Step 2 which significantly improved prediction (ΔR²=.12, p<.001). In the final model, anxiety was the strongest predictor, β=.35, t(96)=3.78, p<.001.

## 假设

- 线性关系 (散点图检查)
- 残差正态
- 残差方差齐性
- 无严重多重共线性 (VIF<5)
- 无自相关 (Durbin-Watson≈2)

## 备选方法

| 方法 | 适用场景 |
|------|----------|
| [逐步回归 (Stepwise Regression)](./stepwise-regression.md) | 预测变量较多，需自动筛选时；注意过拟合风险 |
| [岭回归 (Ridge Regression)](./ridge-regression.md) | 严重多重共线性 (VIF > 10) 时替代 OLS |
| [LASSO 回归](./lasso-regression.md) | 同时进行变量选择与正则化，适合高维数据 |
| [逻辑回归 (Logistic Regression)](./logistic-regression.md) | DV 为二分变量时替代多元回归 |
| [分层线性模型 (HLM)](./hlm.md) | 数据存在嵌套结构（如学生嵌套于班级）时替代多元回归 |
| [调节效应分析 (Moderation)](./moderation.md) | 检验变量间的交互效应 |
| [中介分析 (Mediation)](./mediation.md) | 检验自变量通过中介变量影响因变量的间接路径 |
