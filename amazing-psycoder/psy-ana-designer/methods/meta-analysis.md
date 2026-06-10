# 元分析 (Meta-analysis)

## 概述

元分析系统地整合多个独立研究的效应量,得出更精确、更具推广性的总体估计。

**典型场景**: 整合15个Stroop研究的干扰效应量; 检验效应是否在不同实验范式间一致。

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计类型 | 系统综述与元分析 (Systematic review and meta-analysis) |
| 因变量类型 | 标准化效应量 (Cohen's d, Hedges' g, OR, r) |
| 样本要求 | 至少2个独立研究, 建议 k ≥ 5 |
| 关键假设 | 研究间独立; 效应量可比较; 无异质性混淆 |

## 模型选择

| 模型 | 假设 | 何时用 |
|------|------|--------|
| 固定效应 | 所有研究估计同一真实效应 | 研究几乎相同 |
| **随机效应** | 真实效应在研究间有变异 | **推荐默认** |

## 关键指标

| 指标 | 含义 |
|------|------|
| 合并效应量 (d/OR/r) | 总体估计 |
| 95%CI | 估计精度 |
| I² | 异质性: 25%低/50%中/75%高 |
| τ² | 研究间方差 |
| 森林图 | 视觉化各研究效应量 |

## 发表偏倚检测

- 漏斗图 + Egger's回归
- 剪补法 (trim-and-fill)
- p-curve分析

## R代码

```r
library(metafor)
res <- rma(yi=effect_sizes, sei=SEs, data=dat, method="REML")
forest(res)
funnel(res)
```

## 报告

APA 7th 格式报告示例:

> A random-effects meta-analysis (Restricted Maximum Likelihood estimation) was conducted to synthesize the interference effect across k = 15 independent Stroop studies (total N = 645). Results revealed a medium overall effect, d = 0.52, 95% CI [0.38, 0.66], z = 7.24, p < .001. However, substantial heterogeneity was observed, Q(14) = 43.75, p < .001, I² = 68%, τ² = 0.09, indicating that 68% of the total variance was attributable to between-study differences rather than sampling error. Moderator analyses examined whether task paradigm (card vs. trial-by-trial) moderated the effect; the between-group test was not significant, Q<sub>B</sub>(1) = 1.23, p = .267. Publication bias was assessed via funnel plot inspection and Egger's regression, which did not suggest significant asymmetry, z = 1.10, p = .271. A trim-and-fill analysis imputed no missing studies, and the adjusted effect remained unchanged. Sensitivity analyses (leave-one-out) confirmed the robustness of the overall estimate, with d ranging from 0.48 to 0.55.
