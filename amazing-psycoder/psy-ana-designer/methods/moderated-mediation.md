# 有调节的中介 (Moderated Mediation)

## 概述

有调节的中介检验中介效应是否随调节变量的水平而变化——结合了中介和调节的逻辑。

**典型场景**: 焦虑(X)→注意偏向(M)→Stroop(Y)的中介路径,在工作记忆容量(W)高低组上是否有差异?

## 何时使用

| 条件 | 要求 |
|------|------|
| 研究设计 | 实验或准实验设计，包含自变量(X)、中介变量(M)、因变量(Y)及至少一个调节变量(W) |
| 因变量类型 | 连续变量（如反应时、正确率、量表得分） |
| 样本量 | 建议 N ≥ 200；采用 Bootstrap 法时样本量越大，置信区间越稳定 |
| 中介路径前提 | X→M 或 M→Y（或两者）的中介路径已在理论或预实验中确立 |
| 关键假设 | (1) 变量间存在线性关系；(2) 无严重多重共线性；(3) 调节变量与中介路径的交互项有理论依据；(4) Bootstrap 置信区间不跨零作为显著性判断依据 |

## 关键概念

- **条件间接效应**: 在W的不同水平上,a×b是否不同?
- **调节的中介指标 (Index of Moderated Mediation)**: 量化中介效应随W变化的程度。Bootstrap CI不跨0→有调节的中介显著

## 两种类型

| 类型 | 定义 | 检验 |
|------|------|------|
| 第一阶段调节 | W调节X→M路径 | W×X预测M |
| 第二阶段调节 | W调节M→Y路径 | W×M预测Y |

## R代码

```r
library(lavaan)
model <- '
  M ~ a1*X + a2*W + a3*X:W    # 第一阶段被W调节
  Y ~ b*M + c*X
  indirect.low := (a1+a3*(-1))*b    # W低时
  indirect.high := (a1+a3*(1))*b    # W高时
  diff := indirect.high - indirect.low  # 差异
'
fit <- sem(model, data=data, se="bootstrap", bootstrap=5000)
```

## 报告格式

> Moderated mediation examined whether working memory capacity (W) moderated the indirect effect of anxiety on Stroop through attention bias. The index of moderated mediation was significant, index=0.12, Bootstrap 95%CI [0.04, 0.21], indicating that the mediation pathway was stronger at higher working memory levels.

## 报告

### APA 7th 格式示例

> A moderated mediation model (Model 7; Hayes, 2018) was tested using structural equation modeling with 5,000 bootstrap resamples. Anxiety (X) was the independent variable, attention bias (M) the mediator, Stroop interference score (Y) the dependent variable, and working memory capacity (W) the moderator of the X→M path. Results indicated a significant index of moderated mediation, *index* = 0.12, 95% CI [0.04, 0.21]. The conditional indirect effect was significant at high levels of working memory (+1 SD), *ab* = 0.18, 95% CI [0.08, 0.30], but not at low levels (−1 SD), *ab* = 0.02, 95% CI [−0.05, 0.10]. These findings suggest that the indirect effect of anxiety on Stroop performance via attention bias is contingent upon working memory capacity, such that the mediation pathway is stronger for individuals with higher working memory levels.

### APA 表格建议

在正文中报告以下关键指标：

| 效应 | 估计值 | SE | Bootstrap 95% CI |
|------|--------|-----|--------------------|
| 被调节的中介指标 (Index) | 0.12 | 0.04 | [0.04, 0.21] |
| 条件间接效应 (W = −1 SD) | 0.02 | 0.04 | [−0.05, 0.10] |
| 条件间接效应 (W = +1 SD) | 0.18 | 0.06 | [0.08, 0.30] |
