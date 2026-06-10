# Ex-Gaussian 分布拟合

## 概述

Ex-Gaussian分布将RT分解为三个有心理学意义的参数:μ(决策速度)、σ(决策变异性)、τ(注意 lapse/极端慢反应)。是RT分析的**黄金标准**之一。

**典型场景**: ADHD研究中,高τ值(更多的极端慢反应)是核心行为标记,而μ和σ可能与对照组无差异。

## 何时使用

| 条件 | 要求 |
|------|------|
| 实验设计 | 被试间或被试内设计;需至少两组或两个条件进行比较 |
| 因变量类型 | 反应时(RT),连续正数变量,单位通常为毫秒 |
| 样本量要求 | 每组/每条件 ≥ 50个有效试次;每组被试 ≥ 20人以获得稳定参数估计 |
| 关键假设 | RT服从Ex-Gaussian分布(高斯 + 指数卷积);拟合算法收敛(需检查convergence);剔除无效试次(预期反应、过快反应<150ms);各组分布形态可比 |

## 三个参数

| 参数 | 心理学解释 | 典型值(ms) |
|------|-----------|----------|
| μ (mu) | 高斯成分的均值 — 信息处理速度 | 300-500 |
| σ (sigma) | 高斯成分的SD — 决策稳定性 | 50-150 |
| τ (tau) | 指数成分 — 注意波动/极端慢反应 | 50-300 |

## 为什么用Ex-Gaussian

普通均值/中位数无法区分"整体变慢"和"偶尔走神":
- 被试A: 整体RT慢200ms, 但不变异 → μ大, τ正常
- 被试B: 正常速度但有10%的试次极慢 → μ正常, τ大
两个被试的均值RT可能相同,但认知过程完全不同。

## R代码

```r
library(retimes)  # 或 brms
fit <- timefit(data$rt)
# 检查拟合是否成功
if (fit@ convergence != 0) {
  stop("Ex-Gaussian fitting failed to converge. Try brms with exgaussian() family.")
}
summary(fit)  # mu, sigma, tau

# 备选: 贝叶斯 Ex-Gaussian (brms, 更稳健)
# fit_brm <- brm(rt ~ 1 + (1|subject), data = data,
#                family = exgaussian(), cores = 4)
```

## 报告格式 (APA 7th)

**方法部分**:

> Reaction times (RTs) were analyzed using the Ex-Gaussian distribution, which decomposes the RT distribution into three parameters: mu (μ, the mean of the Gaussian component, reflecting decision speed), sigma (σ, the standard deviation of the Gaussian component, reflecting decision variability), and tau (τ, the mean of the exponential component, reflecting attentional lapses/slow responses). Parameters were estimated separately for each participant and each condition using maximum likelihood estimation via the `retimes` package in R (Massidda, 2013). Only correct trials with RTs between 150 ms and 2.5 SD above each participant's condition mean were included. Model convergence was verified for all individual fits (convergence = 0). The resulting parameter estimates (μ, σ, τ) were then submitted to separate independent-samples t-tests (or repeated-measures ANOVAs for within-subjects designs) comparing groups/conditions.

**结果部分**:

> Ex-Gaussian parameters were estimated to decompose the RT distributions. For the tau (τ) parameter, reflecting the exponential tail of the distribution, the ADHD group (M = 180.25 ms, SD = 52.10) showed significantly larger values than the control group (M = 95.30 ms, SD = 38.75), t(58) = 4.32, p < .001, Cohen's d = 1.13, 95% CI [0.55, 1.69]. This indicates a greater proportion of extremely slow responses in the ADHD group. For the mu (μ) parameter, reflecting the Gaussian mean (decision speed), no significant difference was found between the ADHD group (M = 425.60 ms, SD = 68.40) and the control group (M = 410.20 ms, SD = 59.15), t(58) = 0.97, p = .336, d = 0.25, 95% CI [-0.26, 0.76]. For the sigma (σ) parameter, reflecting decision variability, no significant difference was found between the ADHD group (M = 98.50 ms, SD = 28.30) and the control group (M = 94.10 ms, SD = 24.90), t(58) = 0.43, p = .669, d = 0.11, 95% CI [-0.40, 0.62]. Together, these results suggest that the overall RT slowing observed in ADHD is primarily driven by increased attentional lapses (higher τ) rather than a general slowing of information processing speed (μ) or increased moment-to-moment variability (σ).

**表格建议**:

| 参数 | ADHD组 M (SD) | 对照组 M (SD) | t(58) | p | Cohen's d | 95% CI of d |
|------|--------------|---------------|-------|---|-----------|-------------|
| μ (mu) | 425.60 (68.40) | 410.20 (59.15) | 0.97 | .336 | 0.25 | [-0.26, 0.76] |
| σ (sigma) | 98.50 (28.30) | 94.10 (24.90) | 0.43 | .669 | 0.11 | [-0.40, 0.62] |
| τ (tau) | 180.25 (52.10) | 95.30 (38.75) | 4.32 | <.001 | 1.13 | [0.55, 1.69] |

> *Note.* N = 60 (30 per group). RTs are in milliseconds. Ex-Gaussian parameters were estimated individually for each participant using maximum likelihood estimation. p-values are two-tailed. CI = confidence interval.
