# 中介分析 (Mediation Analysis)

## 概述

中介分析估计由已声明路径模型定义的间接效应。把它解释为因果机制还需要时间顺序、干预/识别假设、无未测混淆和适当的敏感性分析；显著间接效应本身不证明机制。

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

间接效应的不确定性应使用对乘积项分布合适的方法。Bootstrap 区间是常用方案，但并非唯一有效实现；参数化乘积分布、Monte Carlo、贝叶斯后验或设计特定的因果中介方法也可能合适。不要只依赖粗糙的正态近似 Sobel 检验。

- Bootstrap 重采样次数由 Monte Carlo 误差与目标区间精度决定，并记录随机种子
- 计算每次的a×b
- 取2.5%和97.5%分位数为95%CI
- 报告间接效应和区间；是否排除 0 只回答预先声明的检验，不建立因果机制

## 何时使用

| 条件 | 要求 |
|------|------|
| 理论驱动 | 有明确的中介假设(时序、因果逻辑) |
| 设计 | X在M之前,M在Y之前 |
| 样本量 | 由 a/b 路径大小、可靠性、缺失、设计和目标区间精度决定；用模拟/功效分析，不设通用 n 门槛 |

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
| 间接效应占比 | a×b / c | 仅在总效应方向/尺度使该比值稳定且有实质意义时使用；接近 0 或不一致中介时可能失真 |
| 完全标准化间接效应 | a*×b* | 可比跨研究 |

## 报告格式(APA 7th)

> A mediation analysis examined whether attention bias (M) mediated the effect of anxiety (X) on Stroop interference (Y). The indirect effect was significant, a×b=0.15, Bootstrap 95%CI [0.08, 0.23], accounting for 35% of the total effect.

## 常见错误

- ❌ 只用 Baron–Kenny 逐步显著性规则，或把任一单一 CI 算法当作普适答案
- ❌ 只说"中介显著"不报告间接效应大小和CI
- ❌ 截面数据做中介——无法确定时序
- ❌ 不做统计效力分析(小样本Bootstrap不稳定)

## 多个中介

可以同时检验多个中介(并行中介)或链式中介(M1→M2→Y)。用lavaan的多元模型。
