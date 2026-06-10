# 典型相关分析 (Canonical Correlation Analysis / CCA)

## 概述

CCA分析两组多变量之间的整体关联,是Pearson相关的多元扩展。

**典型场景**: 3个认知任务(RT、准确率、变异性)与4个问卷分数(焦虑、抑郁、压力、疲劳)的整体关联。

## 何时使用

有多个X和多个Y,想知道"这两组变量整体上有多相关",而非逐对检验。

| 条件 | 要求 |
|------|------|
| 设计类型 | 相关设计/观测设计，两组变量均为连续型 |
| 变量集X | 2+连续变量，变量间允许适度相关但避免严重多重共线性 |
| 变量集Y | 2+连续变量，变量间允许适度相关但避免严重多重共线性 |
| 样本量 | 至少 ≥ 变量总数×10（两组变量总数之和×10），推荐 ≥ 200 |
| 变量数比例 | 每组变量数建议 ≤ 5-6，总变量数不宜超过样本量的1/10 |
| 线性假设 | X集与Y集之间关系为线性，各典型变量对之间关系为线性 |
| 多元正态性 | 两组变量联合服从多元正态分布（大样本下可放宽） |
| 组内共线性 | 同一变量集内部无完美共线性（VIF < 10） |

## R代码

```r
library(CCA)
X <- data[,c("rt","accuracy","variability")]
Y <- data[,c("anxiety","depression","stress","fatigue")]
cc <- cc(X, Y)
# 典型相关系数
cc$cor
# 典型载荷
cc$xcoef; cc$ycoef
```

## 报告

### APA 7th 报告格式

> A canonical correlation analysis (CCA) was conducted to examine the overall multivariate relationship between cognitive performance measures (RT, accuracy, RT variability) and mood symptoms (anxiety, depression, stress, fatigue). The overall model was significant, Wilks' Λ = .68, *F*(12, 508.32) = 5.21, *p* < .001.
>
> Two canonical functions emerged as statistically significant. The first canonical correlation was *r*<sub>c</sub> = .52, *p* < .001, accounting for 27.0% of the shared variance between the two variable sets. On the cognitive side, RT loaded most heavily on this function (canonical loading = .85), followed by RT variability (.62) and accuracy (−.48). On the mood side, anxiety showed the strongest loading (.78), followed by stress (.61) and fatigue (.54). This indicates that slower and more variable reaction times were associated with higher anxiety, stress, and fatigue.
>
> The second canonical correlation was *r*<sub>c</sub> = .31, *p* = .012, accounting for an additional 9.6% of shared variance. Accuracy (.72) and depression (.68) were the primary contributors to this function, suggesting that lower accuracy was specifically associated with higher depression scores independent of the first dimension.
>
> Redundancy analysis indicated that the mood variable set explained 18.4% of the variance in the cognitive variables through the first canonical function, and 8.2% through the second. Standardized canonical coefficients and structure coefficients (*r*<sub>s</sub>) are presented in Table X.
