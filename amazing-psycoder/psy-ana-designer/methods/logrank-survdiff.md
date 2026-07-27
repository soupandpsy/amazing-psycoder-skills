# Log-Rank 检验 / 生存曲线比较

## 概述

Log-Rank检验比较两组或多组的事件时间曲线，是带删失组间比较的候选检验之一。它回答的是整条曲线的加权差异问题，不自动提供领域可解释的效应估计。

**典型场景**: 两种治疗方案下到复发/缓解的时间，或不同招募策略下到研究退出的时间。

**硬排除**: 不得用 Log-Rank/Kaplan–Meier 曲线估计或比较 SSRT；stop-signal 原始试次并不因此成为普通删失生存结局。

## 何时使用

| 条件 | 要求 |
|------|------|
| 研究设计 | 组间设计（两组或多组比较） |
| 因变量类型 | 时间-事件（time-to-event），含删失数据 |
| 样本/信息 | 依据事件数、删失、曲线差异形态、分配比例与目标功效设计；没有通用“每组 20–30”门槛 |
| 核心条件 | 明确定义事件/时间起点、独立或已建模的观察单位、可辩护的删失机制；交叉风险会改变 Log-Rank 的功效和解释，应预先考虑替代 estimand/检验 |

## vs Cox回归

Log-Rank: 给出曲线差异检验；仍应配套报告预先指定的生存概率差、限制平均生存时间差或其他可解释估计与区间
Cox回归: 半参数模型，可加入协变量并估计条件 HR，但依赖其模型结构与诊断

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

> In this illustrative report, a log-rank test compared time-to-relapse curves for an intervention group (n = 45) and a control group (n = 48), χ²(1, N = 93) = 6.45, p = .011. Kaplan–Meier estimates were accompanied by a prespecified absolute survival-probability difference at six months with a confidence interval; censoring counts and follow-up distributions were reported by group.

### 中文报告示例

> 在此示例中，采用 Log-Rank 检验比较干预组（n = 45）与对照组（n = 48）的复发时间曲线，χ²(1, N = 93) = 6.45, p = .011。同时报告六个月无复发概率差及其置信区间，并按组报告删失数量和随访分布。

### 必报信息

- 检验统计量 χ²、自由度
- 样本量 (N)
- p 值及预先指定的、可解释的效应估计与不确定性
- 各组删失/风险集信息；中位生存时间只在可估且符合 estimand 时报告
