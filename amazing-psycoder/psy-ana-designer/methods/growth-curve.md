# 增长曲线模型 (Growth Curve Model)

## 概述

增长曲线模型用于分析随时间变化的数据,估计个体和群体的变化轨迹。

**典型场景**: 被试在5个时间点的N-back表现,检验练习效应和个体差异。

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计 | 纵向, ≥3个时间点 |
| DV | 连续 |
| 关键 | 时间效应 + 个体间变化率差异 |

## 模型

```r
lmer(dv ~ time + (1+time|subject), data=long_data)
```

- 固定效应: time的系数 = 平均变化率
- 随机效应: time的方差 = 变化率的个体差异

## 非线性增长

加入time²检验二次增长(加速/减速变化):
```r
lmer(dv ~ time + I(time^2) + (1+time|subject), data=long_data,
     control = lmerControl(optimizer = "bobyqa"))
```

## 报告

> A growth curve model examined changes in N-back performance across 5 sessions. Performance improved linearly, b=2.3, t(34)=5.12, p<.001, with significant individual differences in change rates (SD_slope=1.8).
