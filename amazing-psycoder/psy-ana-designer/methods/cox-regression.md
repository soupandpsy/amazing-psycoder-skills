# Cox 回归 (Cox Proportional Hazards)

## 概述

Cox回归分析带删失的事件发生时间，检验协变量与条件事件率（hazard）的关系。只有当科学问题的 estimand 确实是 time-to-event 且事件/时间起点/删失机制明确定义时才是候选。

**典型场景**: 治疗开始到复发、研究入组到退出、随访开始到首次症状缓解。

**硬排除**: SSRT 不是普通生存时间，不能把 stop-signal 试次或“停止成功时间”直接送入 Cox 模型来估计 SSRT。按停止信号共识方法预先指定 SSRT 估计，并保留 go RT、SSD、停止成功/失败等原始字段。

## 何时使用

| 条件 | 要求 |
|------|------|
| 研究设计 | 纵向/追踪设计（需记录事件发生时间及删失状态） |
| 因变量 | 事件发生时间 + 是否发生（删失） |
| 自变量 | 连续或分类变量 |
| 信息要求 | 事件数、删失比例、预测变量复杂度和目标精度共同决定样本量；不使用固定 EPV 规则替代设计分析 |
| 关键诊断 | 比例风险、连续变量函数形式、影响点、删失机制与模型稳定性；Schoenfeld 检验/图是证据之一，不以 `p > .05` 宣告假设成立 |
| 依赖结构 | 重复事件、中心/治疗师聚类或多状态过程需相应扩展，不能当作独立单事件样本 |

## 关键输出

- **Hazard Ratio (HR)**: 相对于明确参考组的条件事件率比；方向取决于事件编码，不能自动等同“更好/更坏”
- **生存曲线**: Kaplan-Meier图
- **比例风险检验**: Schoenfeld残差

## R代码

```r
library(survival)
model <- coxph(Surv(time, event) ~ condition + age, data=data)
summary(model)
# 比例风险检验
cox.zph(model)
```

## 报告

APA 7th 格式报告示例：

> In this illustrative report, a Cox proportional hazards model examined time from treatment entry to first relapse, with administrative censoring at the end of follow-up and age included as a prespecified covariate. The intervention group had a lower conditional relapse rate than the control group, HR = 0.55, 95% CI [0.38, 0.79], p = .001. Proportional-hazards diagnostics and sensitivity analyses using an alternative time-varying effect specification were reported alongside the model.

**报告要点**：
- 报告比例风险假设检验结果（χ² 与 p 值）
- 报告模型整体拟合（似然比检验或 Wald 检验）
- 每个预测变量报告 HR、95% CI 与 p 值
- 解释 HR 时明确事件、参考组、时间尺度与条件性；必要时同时报告绝对生存概率或限制平均生存时间等更易解释的量
