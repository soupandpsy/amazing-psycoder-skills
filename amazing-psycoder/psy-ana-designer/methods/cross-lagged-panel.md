# 交叉滞后面板模型 (Cross-Lagged Panel Model / CLPM)

## 概述

CLPM 描述纵向变量间的自回归与交叉滞后关联。路径方向提供时间先后下的预测证据，但在没有充分识别假设、干预或自然实验时不能单独确定因果方向。

**典型场景**: 焦虑和睡眠质量在3个时间点上的相互预测关系。焦虑(t1)→睡眠(t2),还是睡眠(t1)→焦虑(t2)?

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计类型 | 纵向追踪；两波可估计有限的交叉滞后关联，三波以上才有更多平稳性/动态结构信息，但波次数量本身不建立因果识别 |
| 因变量类型 | 连续变量。两个构念在每波均需同时测量,且测量间隔相同 |
| 样本信息 | 由波数、可靠性、缺失、随机截距/斜率、效应大小和估计器决定；用设计模拟而非通用 N 门槛 |
| 关键假设 | **平稳性**:交叉滞后路径在不同时间间隔保持稳定;**同步性**:每次测量需在同一时间窗口完成;**测量不变性**:同一构念在不同时间点的测量具有相同结构(建议先检验metric invariance);**无遗留混淆**:模型中已包含主要的第三变量 |

## 模型

```
X(t1) ────→ X(t2) ────→ X(t3)    (自回归路径)
  │   ↘       │   ↘
  │    Y(t1)  │    Y(t2)           (交叉滞后路径)
  ↓           ↓
Y(t1) ────→ Y(t2) ────→ Y(t3)
```

## vs 传统交叉滞后

| 模型 | 特点 |
|------|------|
| 传统CLPM | 被试间+被试内效应混合 |
| **RI-CLPM** (Random Intercept) | **推荐**——分离被试间和被试内变异 |

## R代码 (lavaan)

```r
model <- '
  # 自回归
  X2 ~ X1; X3 ~ X2
  Y2 ~ Y1; Y3 ~ Y2
  # 交叉滞后
  Y2 ~ X1; X2 ~ Y1
  Y3 ~ X2; X3 ~ Y2
  # 同时间相关
  X1 ~~ Y1; X2 ~~ Y2; X3 ~~ Y3
'
fit <- sem(model, data=data)
```

## 报告

> A random-intercept cross-lagged panel model examined bidirectional lagged associations between anxiety and sleep across 3 waves. Anxiety at t1 predicted lower subsequent sleep conditional on the model (β=-.18, p=.003), whereas the reverse path was imprecisely estimated (β=-.03, p=.61). This asymmetry does not by itself establish that anxiety causally drives sleep disruption; that interpretation depends on the stated identification assumptions and sensitivity analyses.
