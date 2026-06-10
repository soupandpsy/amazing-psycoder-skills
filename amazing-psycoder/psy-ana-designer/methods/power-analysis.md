# 统计效力分析 (Power Analysis)

## 概述

效力分析在数据收集**之前**确定所需样本量,或在收集**之后**评估已有效应可检测的最小效应量。心理学预注册和伦理审查的必需品。

**典型场景**: "我需要多少被试才能检测到 d=0.5 的效应?" "n=30 时我能检测到多小的效应?"

## 何时使用

| 条件 | 要求 |
|------|------|
| 研究设计已确定 | 自变量/因变量、实验设计类型(被试间/被试内/混合)已明确 |
| 效应量可估计 | 可从文献、元分析或预实验中获取预期的效应量(Cohen's d, η², r 等) |
| 统计检验已选定 | 已确定将使用的统计方法(t检验、ANOVA、回归、混合模型等) |
| 伦理或资源约束存在 | 需要向伦理委员会提交样本量理由,或受限于预算/时间 |
| 预注册要求 | 期刊或平台要求预注册时注明样本量规划依据 |

> 若上述条件不满足(例如无效应量估计),应使用**敏感性分析**(sensitivity analysis):固定 α、power 和 n,反推可检测的最小效应量。

## 四种效力分析

| 类型 | 给定 | 求 |
|------|------|-----|
| A Priori | α, power, effect size | 所需 n |
| Sensitivity | α, power, n | 可检测的最小效应 |
| Post-hoc | α, n, effect size | 已有研究的power |
| 样本量规划 | 预算/时间约束 | 最优被试数 |

## 常用工具

| 方法 | R包 |
|------|-----|
| t检验/ANOVA | `pwr` |
| 混合模型 | `simr` (基于模拟) |
| 通用 | `powerAnalyzeR` |

## 典型值

- α = 0.05 (标准)
- Power = 0.80 (推荐) 或 0.90 (严格)
- d = 0.2 (小), 0.5 (中), 0.8 (大)
- η²p = 0.01 (小), 0.06 (中), 0.14 (大)

## R 代码

### 安装与加载

```r
install.packages("pwr")
library(pwr)
```

### A Priori 效力分析 (求所需样本量)

双样本独立 t 检验,预期 Cohen's d = 0.5,α = 0.05,power = 0.80:

```r
result <- pwr.t.test(
  d         = 0.5,
  sig.level = 0.05,
  power     = 0.80,
  type      = "two.sample",
  alternative = "two.sided"
)
result
# n = 63.77 → 每组需 64 名被试,共 128 名
```

单因素被试间 ANOVA (4 组),预期 f = 0.25 (中等效应),α = 0.05,power = 0.80:

```r
pwr.anova.test(
  k         = 4,
  f         = 0.25,
  sig.level = 0.05,
  power     = 0.80
)
# n = 44.60 → 每组需 45 名被试,共 180 名
```

相关系数检验,预期 r = 0.30:

```r
pwr.r.test(
  r         = 0.30,
  sig.level = 0.05,
  power     = 0.80,
  alternative = "two.sided"
)
# n = 84.07 → 需 85 名被试
```

### Sensitivity 分析 (给定 n 求可检测的最小效应量)

```r
# 已知每组仅能招募 30 名被试,求可检测的最小 d
pwr.t.test(
  n          = 30,
  sig.level  = 0.05,
  power      = 0.80,
  type       = "two.sample",
  alternative = "two.sided"
)
# d = 0.74 → 仅能检测到大效应
```

### Post-hoc 效力分析 (已收集数据后评估 power)

```r
# 已有研究:每组 n=25,d=0.4,评估其 power
pwr.t.test(
  n          = 25,
  d          = 0.4,
  sig.level  = 0.05,
  type       = "two.sample",
  alternative = "two.sided"
)
# power = 0.31 → 效力严重不足
```

### 效应量换算

```r
# Cohen's d → f (ANOVA用)
d <- 0.5
f <- d / 2
f  # 0.25

# η² → f (ANOVA用)
eta_sq <- 0.06
f <- sqrt(eta_sq / (1 - eta_sq))
f  # 0.253
```

### 混合模型效力分析 (simr)

```r
# install.packages("simr")
library(simr)

# 使用已有模型对象进行基于模拟的效力估计
# model <- lmer(RT ~ condition + (1 | subject), data = pilot_data)
# powerSim(model, nsim = 200, test = fixed("condition"))
```

## 报告

> An a priori power analysis (α=.05, power=.80) indicated that N=34 is required to detect a medium within-subjects effect (d_z=0.5) with a two-tailed paired t-test.

## 备选方法

- [等价性检验 (Equivalence Testing)](./equivalence-testing.md) — 当研究目标是证明"无效应"或"效应可忽略"，而非检测差异
- [贝叶斯因子 (Bayes Factor)](./bayes-factor.md) — 当需要持续收集数据直到证据充分(而非预先固定样本量)
- [效应量估计 (Effect Size Estimation)](./effect-size.md) — 当已有时数据,需要估计效应量及其置信区间
- [样本量规划 (Sample Size Planning)](./sample-size-planning.md) — 当约束来自预算/时间而非统计效力


