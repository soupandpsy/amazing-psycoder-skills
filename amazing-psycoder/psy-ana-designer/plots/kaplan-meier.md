# Kaplan-Meier 生存曲线

## 概述

Kaplan-Meier曲线展示事件发生时间的概率，适合分析Stop-signal任务、延迟折扣等"时间→事件"数据。

## 何时使用

| 条件 | 说明 |
|------|------|
| DV | 事件发生时间+是否发生（删失） |
| 分组 | 1-4组比较 |

## R 代码

```r
library(survival)
fit <- survfit(Surv(time, event) ~ group, data=data)
plot(fit, col=c("red","blue"), lty=1:2, lwd=2,
     xlab="Time (ms)", ylab="Survival Probability")
legend("topright", legend=levels(data$group), col=c("red","blue"), lty=1:2)
```

## 解读

- 曲线下降快 → 事件发生早
- 曲线分离 → 组间差异
- 平坦段 → 该时期无事件
- "+"标记 → 删失观测

## 关键参数

| 参数 | 作用 |
|------|------|
| `Surv(time,event)` | 生存对象 |
| `col` | 分组颜色 |
| `lty` | 线型区分 |
