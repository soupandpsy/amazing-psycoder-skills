# 时间序列分析 (ARIMA)

## 概述

ARIMA模型分析单变量时间序列数据,适用于密集纵向测量(如每日日记、EMA生态瞬时评估、生理信号)。

**典型场景**: 30天每日焦虑评分的趋势和周期性分析; 干预前后时间序列的变化(中断时间序列)。

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计类型 | 密集纵向设计（每日日记、EMA、生理信号）或单被试实验设计 |
| 因变量类型 | 连续变量，等间隔时间点重复测量 |
| 样本要求 | 单个序列至少30个时间点；中断时间序列设计建议干预前后各≥12个点 |
| 关键假设 | 差分后序列平稳（ADF检验p<.05）；残差为白噪声（Ljung-Box检验p>.05）；残差近似正态；无缺失值或已妥善插补 |

## ARIMA(p,d,q)

| 参数 | 含义 |
|------|------|
| AR(p) | 自回归阶数:当前值由前p个值预测 |
| I(d) | 差分阶数:做d次差分使序列平稳 |
| MA(q) | 移动平均阶数:当前值由前q个预测误差预测 |

## R代码

```r
library(forecast)
fit <- auto.arima(data$anxiety)
summary(fit)
# 残差诊断
checkresiduals(fit)
# 预测
forecast(fit, h=7)  # 未来7天
plot(forecast(fit, h=7))
```

## 中断时间序列 (ITS)

检验某个干预时点后序列是否发生变化:

```r
model <- lm(outcome ~ time + intervention + time_after, data=data)
```

## 报告

**APA 7th 格式报告示例：**

> A 30-day intensive longitudinal design was used to examine daily anxiety ratings (0–100 visual analog scale) before and after a cognitive training intervention introduced at Day 15. An ARIMA(1,0,2) model was selected via automatic model selection (Hyndman & Khandakar, 2008) and confirmed by residual diagnostics (Ljung-Box test, *p* = .41). The model revealed a significant autoregressive component, AR(1) = 0.62, 95% CI [0.38, 0.86], *p* < .001, indicating that anxiety on a given day was positively predicted by the previous day's score. The moving average parameters were MA(1) = −0.34, 95% CI [−0.58, −0.10], *p* = .006, and MA(2) = 0.21, 95% CI [0.03, 0.39], *p* = .02.
>
> An interrupted time-series analysis examined the intervention effect. The intervention was associated with an immediate level reduction of 3.2 points, *b* = −3.20, 95% CI [−5.17, −1.23], *t*(26) = −3.32, *p* = .002, and a sustained downward trend of −0.15 points per day post-intervention, *b* = −0.15, 95% CI [−0.29, −0.01], *t*(26) = −2.18, *p* = .04. The overall model explained 48% of the variance in daily anxiety ratings (adjusted *R*² = .42).
