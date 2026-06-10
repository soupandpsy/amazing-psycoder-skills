# Log-Rank 检验 / 生存曲线比较

## 概述

Log-Rank检验比较两组或多组的**生存曲线**是否有显著差异,是Cox回归的非参数对应。

**典型场景**: ADHD和对照组在Stop-signal任务中的"抑制成功时间"曲线是否不同; 两种治疗方案下"康复时间"的差异。

## 何时使用

| 条件 | 要求 |
|------|------|
| 研究设计 | 组间设计（两组或多组比较） |
| 因变量类型 | 时间-事件（time-to-event），含删失数据 |
| 样本要求 | 两组或多组独立样本；每组建议 ≥ 20-30 例 |
| 核心假设 | 删失与事件独立（非信息性删失）；各组风险函数成比例（比例风险假设） |

## vs Cox回归

Log-Rank: 非参数,只检验"是否有差异",不给效应量
Cox回归: 半参数,给出Hazard Ratio,可加入协变量

## R代码

```r
library(survival)
# Kaplan-Meier曲线
fit <- survfit(Surv(time, event) ~ group, data=data)
plot(fit, col=c("red","blue"), lty=1:2)
# Log-Rank检验
survdiff(Surv(time, event) ~ group, data=data)
```

## 报告

### APA 7th 格式示例

> A log-rank test was conducted to compare survival curves between the ADHD group (n = 45) and the control group (n = 48) on the stop-signal inhibition task. The ADHD group showed significantly slower inhibition compared to the control group, χ²(1, N = 93) = 6.45, p = .011. Kaplan-Meier curves indicated that median inhibition time was 320 ms (95% CI [295, 348]) for the ADHD group and 275 ms (95% CI [252, 301]) for the control group.

### 中文报告示例

> 采用Log-Rank检验比较ADHD组与对照组在停止信号任务中的抑制时间曲线。结果显示，ADHD组的抑制速度显著慢于对照组，χ²(1, N = 93) = 6.45, p = .011。Kaplan-Meier曲线显示，ADHD组中位抑制时间为320 ms，对照组为275 ms。

### 必报信息

- 检验统计量 χ²、自由度
- 样本量 (N)
- p 值（精确到三位小数）
- 各组中位生存时间及95% CI（可选但推荐）
