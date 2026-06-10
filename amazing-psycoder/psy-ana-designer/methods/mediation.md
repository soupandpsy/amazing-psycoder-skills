# 中介分析 (Mediation Analysis)

## 概述

中介分析检验X通过中介变量M影响Y的**间接路径**。是心理学中检验"机制"的核心方法。

**典型场景**: 焦虑(X)通过注意偏向(M)影响Stroop干扰效应(Y)。注意偏向是中介变量。

## 模型

```
X ──c'──→ Y     (直接效应)
  ↘     ↗
    M          (间接效应: a×b)
```

- **路径a**: X→M (X对中介的效应)
- **路径b**: M→Y (中介对Y的效应,控制X)
- **间接效应 (a×b)**: X通过M影响Y的效应
- **直接效应 (c')**: X对Y的直接效应(控制M)
- **总效应 (c)**: 直接+间接 = c' + a×b

## Bootstrap 置信区间

**必须用Bootstrap**检验间接效应,不能依赖Sobel检验。因为a×b的抽样分布非正态。

- Bootstrap重采样(通常5000次)
- 计算每次的a×b
- 取2.5%和97.5%分位数为95%CI
- **95%CI不跨0** → 中介效应显著

## 何时使用

| 条件 | 要求 |
|------|------|
| 理论驱动 | 有明确的中介假设(时序、因果逻辑) |
| 设计 | X在M之前,M在Y之前 |
| 样本量 | Bootstrap中介分析通常需n≥100 |

## R代码

```r
library(lavaan)
model <- '
  M ~ a*X       # 路径a
  Y ~ b*M + c*X # 路径b和c
  indirect := a*b
  total := c + a*b
'
fit <- sem(model, data=data, se="bootstrap", bootstrap=5000)
summary(fit, fit.measures=TRUE)
parameterEstimates(fit, ci=TRUE)
```

## 效应量

| 指标 | 公式 | 解释 |
|------|------|------|
| 间接效应占比 | a×b / c | 总效应中被中介解释的比例 |
| 完全标准化间接效应 | a*×b* | 可比跨研究 |

## 报告格式(APA 7th)

> A mediation analysis examined whether attention bias (M) mediated the effect of anxiety (X) on Stroop interference (Y). The indirect effect was significant, a×b=0.15, Bootstrap 95%CI [0.08, 0.23], accounting for 35% of the total effect.

## 常见错误

- ❌ 用逐步法(Baron & Kenny,1986)而不用Bootstrap——统计效力低
- ❌ 只说"中介显著"不报告间接效应大小和CI
- ❌ 截面数据做中介——无法确定时序
- ❌ 不做统计效力分析(小样本Bootstrap不稳定)

## 多个中介

可以同时检验多个中介(并行中介)或链式中介(M1→M2→Y)。用lavaan的多元模型。
