# 有序逻辑回归 (Ordinal Logistic Regression)

## 概述

有序逻辑回归处理有序分类因变量,如Likert量表(1-7分)、教育等级、满意度评级。

**典型场景**: 检验实验条件对Likert量表评分(1-7)的影响; 检验年级对学业等级的影响。

## 何时使用

| 条件 | 要求 |
|------|------|
| DV | 有序分类(如Likert 1-7) |
| IV | 连续或分类 |

## 为什么不用普通ANOVA

- Likert数据不是连续变量——是离散有序类别
- 相邻分数差不等距(4→5的难度可能≠1→2的难度)
- 数据被截断(不能低于1,不能高于7)
- 有序逻辑回归不假设等距,只假设顺序

## R代码

```r
library(ordinal)
model <- clm(factor(rating) ~ condition + (1|subject), data=data)
summary(model)
```

## 效应量

OR (Odds Ratio): exp(estimate)。OR>1=更高评分的概率增加。

## 报告

> Ordinal logistic regression examined the effect of condition on Likert ratings (1-7). The congruent condition was associated with higher confidence ratings, OR=1.85, 95%CI [1.42,2.41], p<.001.
