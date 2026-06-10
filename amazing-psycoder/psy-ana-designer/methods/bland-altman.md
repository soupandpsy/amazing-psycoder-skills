# Bland-Altman 分析

## 概述

Bland-Altman图用于评估两种测量方法的**一致性**,而非相关性。这是医学和心理学中方法比较的标准。

**典型场景**: 比较手动RT编码和自动RT编码是否一致; 比较两个版本的Stroop任务是否给出等价的干扰效应。

## 何时使用

Bland-Altman分析适用于评估两种测量方法一致性(agreement)的场景。使用前确认以下条件是否满足:

| 条件 | 要求 |
| --- | --- |
| 设计类型 | 方法比较研究 (method-comparison / agreement study) — 同一批被试同时接受两种测量方法 |
| 因变量类型 | 连续变量 (如反应时、量表得分、生理指标) |
| 样本量要求 | 至少 50 例，推荐 ≥100 例以获得稳定的95%一致限估计 (Bland & Altman, 1986) |
| 关键假设 | 差值服从正态分布; 差值与均值之间无相关(无比例偏倚); 差值方差在测量范围内恒定(方差齐性) |
| 不适用场景 | 两种方法测量的是不同构念; 因变量为分类或等级变量; 新方法为金标准的替代且仅关心新方法误差时(此时应使用测量误差模型) |

## vs 相关分析

相关系数r=0.95≠两种方法可以互换。Bland-Altman图直接回答"两种方法的差异有多大,是否有系统偏差"。

## 指标

- **偏倚 (Bias)**: 两种方法差的均值(±0=完美)
- **95%一致限 (Limits of Agreement)**: Bias ± 1.96×SD_diff。95%的差异应在此范围内。如果这个范围在临床上可接受,则可以互换使用。

## R代码

```r
library(blandr)
blandr.draw(data$method1, data$method2)
blandr.statistics(data$method1, data$method2)
```

## 报告

APA 7th 格式报告示例:

> A Bland-Altman analysis was conducted to assess the agreement between manual and automated RT coding. The mean difference (bias) was 2.3 ms (SD = 5.5), with 95% limits of agreement ranging from -8.5 ms to 13.1 ms. Inspection of the Bland-Altman plot revealed no systematic relationship between the difference and the mean of the two methods (r = .04, p = .713), indicating the absence of proportional bias. The 95% LoA fell within the pre-specified clinically acceptable margin of ±20 ms, supporting the interchangeability of manual and automated coding in this context.

中文格式参考:

> 采用Bland-Altman分析评估手动与自动RT编码的一致性。两种方法差值的均值(偏倚)为2.3 ms (SD = 5.5),95%一致限为[-8.5, 13.1] ms。Bland-Altman图中差值与均值无显著相关(r = .04, p = .713),表明不存在比例偏倚。95%一致限在预先设定的临床可接受范围(±20 ms)之内,支持两种编码方法可互换使用。

**报告要点**:
- 报告偏倚(bias)及其标准差
- 报告95%一致限(95% LoA)的上下界及置信区间
- 检查并报告比例偏倚(差值与均值的相关)
- 结合领域可接受标准讨论一致限是否足够窄
