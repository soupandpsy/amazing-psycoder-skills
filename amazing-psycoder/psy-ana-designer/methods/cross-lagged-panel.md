# 交叉滞后面板模型 (Cross-Lagged Panel Model / CLPM)

## 概述

CLPM是纵向数据分析中检验**因果方向**的核心方法。通过同时估计X→Y和Y→X的交叉滞后路径,检验是X预测Y的变化,还是Y预测X的变化。

**典型场景**: 焦虑和睡眠质量在3个时间点上的相互预测关系。焦虑(t1)→睡眠(t2),还是睡眠(t1)→焦虑(t2)?

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计类型 | 纵向追踪设计,至少3个时间点(≥3 waves)。2个时间点无法区分因果方向 |
| 因变量类型 | 连续变量。两个构念在每波均需同时测量,且测量间隔相同 |
| 样本量 | SEM要求大样本,一般 N ≥ 200。时间点越多、路径越复杂,所需样本越大 |
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

> A random-intercept cross-lagged panel model examined the bidirectional relationship between anxiety and sleep across 3 waves. The cross-lagged path from anxiety(t1) to sleep(t2) was significant (β=-.18, p=.003), but sleep(t1)→anxiety(t2) was not (β=-.03, p=.61), suggesting anxiety drives sleep disruption rather than vice versa.
