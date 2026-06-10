# Cox 回归 (Cox Proportional Hazards)

## 概述

Cox回归分析"事件发生时间"数据,检验协变量如何影响事件发生的风险率。在心理学中用于分析反应时截止任务。

**典型场景**: Stop-signal任务中,什么因素影响停止成功的"时间"?; 延迟折扣任务中,什么预测"选择立即奖励"的潜伏期?

## 何时使用

| 条件 | 要求 |
|------|------|
| 研究设计 | 纵向/追踪设计（需记录事件发生时间及删失状态） |
| 因变量 | 事件发生时间 + 是否发生（删失） |
| 自变量 | 连续或分类变量 |
| 样本要求 | 每个预测变量至少10个事件（EPV ≥ 10）；总样本量 ≥ 观测变量数 × 10 |
| 关键假设 | 比例风险假设（Schoenfeld残差检验 p > .05）；对数线性假设（连续变量）；无多重共线性 |

## 关键输出

- **Hazard Ratio (HR)**: HR>1=事件发生更快(风险高)
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

> A Cox proportional hazards model was fitted to examine the effect of condition (congruent vs. incongruent) on stop-signal reaction time (SSRT), controlling for age. The proportional hazards assumption was met, χ²(2) = 1.23, p = .541. The overall model was significant, likelihood ratio χ²(2) = 14.67, p < .001. Condition significantly predicted the hazard of successful stopping: participants in the incongruent condition showed a 45% lower hazard of successful stopping compared to the congruent condition, HR = 0.55, 95% CI [0.38, 0.79], p = .001. Age was not a significant predictor, HR = 1.01, 95% CI [0.97, 1.05], p = .612.

**报告要点**：
- 报告比例风险假设检验结果（χ² 与 p 值）
- 报告模型整体拟合（似然比检验或 Wald 检验）
- 每个预测变量报告 HR、95% CI 与 p 值
- HR < 1 解释为"风险更低/事件发生更慢"，HR > 1 解释为"风险更高/事件发生更快"
