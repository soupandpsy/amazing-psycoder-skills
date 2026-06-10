# 分位数回归 (Quantile Regression)

## 概述

分位数回归建模DV的**特定分位数**(如中位数、第10百分位)而非均值,揭示效应在不同RT段上的差异。

**典型场景**: Stroop效应在快反应(第25百分位)和慢反应(第75百分位)上是否不同? 揭示条件效应是否集中在特定RT段。

## 何时使用

| 条件 | 要求 |
|------|------|
| 实验设计 | 被试内或被试间设计,比较两个或多个实验条件 |
| 因变量类型 | 连续变量,通常为反应时(RT),也可用于其他连续指标(如眼动指标、生理数据) |
| 样本量 | 每组至少100个观测;分位数估计对极端分位数(τ < 0.10 或 τ > 0.90)需要更大样本(200+) |
| 核心假设 | 条件效应可能在DV分布的不同位置存在差异;关注效应异质性而非仅在均值上的差异 |

## 为什么不用均值回归

均值回归假设效应在所有RT水平上恒定。但真实数据中,条件效应可能在快反应上小(自动加工)、慢反应上大(受控加工失败)。分位数回归直接检验这个假设。

## R代码

```r
library(quantreg)
model <- rq(rt ~ condition, tau=c(0.25, 0.50, 0.75), data=data)
summary(model)
# 效应随分位数变化图
plot(summary(model))
```

## 报告

### APA 7th 格式报告示例

> A quantile regression was conducted to examine whether the congruency effect varied across the reaction time distribution. Reaction time (RT) was regressed on congruency condition (congruent vs. incongruent) at three quantiles: τ = .25 (fast responses), τ = .50 (median responses), and τ = .75 (slow responses). Results revealed a significant effect of congruency at all three quantiles, with the effect increasing monotonically from the lower to the upper tail. Specifically, at τ = .25, the congruency effect was 25 ms (95% CI [18, 32]), *b* = 25.00, *SE* = 3.57, *t*(98) = 7.00, *p* < .001. At the median (τ = .50), the effect was 42 ms (95% CI [35, 49]), *b* = 42.00, *SE* = 3.57, *t*(98) = 11.76, *p* < .001. At τ = .75, the effect reached 65 ms (95% CI [55, 75]), *b* = 65.00, *SE* = 5.10, *t*(98) = 12.75, *p* < .001. A Wald test confirmed that the regression coefficients differed significantly across quantiles, χ²(2, *N* = 99) = 15.32, *p* < .001, indicating that slower trials were disproportionately affected by the congruency manipulation. Standard errors were estimated via the bootstrap method with 500 replications. All analyses were performed in R using the *quantreg* package (Version 5.97; Koenker, 2023).
