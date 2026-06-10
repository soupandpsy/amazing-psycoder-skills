# McNemar 检验

## 概述

McNemar检验用于**配对二分类数据**,检验前后测或两种条件下分类结果的变化是否对称。

**典型场景**: 治疗前后"符合临床诊断"的比例变化; 两种Stroop版本做对/做错模式的差异。

## 何时使用

| 条件 | 要求 |
|------|------|
| DV类型 | 二分类（是/否、对/错、阳性/阴性） |
| 设计类型 | 配对设计（每个被试接受两种条件或前后测） |
| 样本要求 | 配对样本；被试内两个时间点/条件均需完整数据 |
| 关键假设 | 仅关注不一致对（b和c）；b+c ≥ 10 时可用标准近似，否则需用精确二项检验 |
| 数据格式 | 2×2列联表，对角线为一致结果（a和d），反对角线为变化（b和c） |

## 2×2表解读

```
          条件B
          对    错
条件A 对  a(一致) b(变错)
      错  c(变对)  d(一致)
```

McNemar检验b和c是否对称——即"变对"和"变错"的人是否一样多。

## R代码

```r
mcnemar.test(table(data$pre, data$post))
```

## 报告

> McNemar's test examined whether classification changed from pre to post treatment. Significantly more patients moved from clinical to non-clinical (n=18) than vice versa (n=3), χ²(1)=9.14, p=.002.
