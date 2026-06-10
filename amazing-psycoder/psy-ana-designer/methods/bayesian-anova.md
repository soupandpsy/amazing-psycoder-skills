# 贝叶斯 ANOVA

## 概述

贝叶斯ANOVA是传统ANOVA的贝叶斯替代,量化每个效应的证据强度(贝叶斯因子),而非仅给出p值。

**典型场景**: 需要报告"无差异"的证据; 小样本(传统ANOVA效力不足); 预注册分析中预先指定。

## 何时使用

| 条件 | 要求 |
|------|------|
| 实验设计 | 被试内设计（单因素或多因素重复测量） |
| 因变量类型 | 连续变量（如反应时、正确率） |
| 样本量要求 | 小样本可用；传统ANOVA效力不足时尤适用 |
| 核心前提 | 设定合理先验分布（默认Cauchy先验，r scale参数需报告）；序贯分析需预先注册停止规则 |

## 与传统ANOVA对比

| 传统ANOVA | 贝叶斯ANOVA |
|-----------|------------|
| p<.05→拒绝H0 | BF10→量化H1/H0相对证据 |
| 不显著≠无效应 | BF01量化H0证据 |
| 不能监控证据累积 | 支持序贯分析 |
| 对样本量敏感 | 小样本仍可用 |

## R代码

```r
library(BayesFactor)
bf <- anovaBF(rt ~ condition, data=data_agg, whichRandom="subject")
plot(bf)  # 每个效应的BF
```

## 报告（APA 7th 格式）

### 正文报告示例

> A Bayesian repeated-measures ANOVA was conducted to examine the effect of condition (2 levels: congruent, incongruent) on reaction time (RT). The analysis used the `BayesFactor` package in R (Morey & Rouder, 2018) with default Cauchy priors (r scale = 0.5) on the fixed effects and a Jeffreys prior on the random effect of subject. The model including condition was strongly preferred over the null model, BF<sub>10</sub> = 15.30, indicating that the data are approximately 15 times more likely under the alternative hypothesis than under the null. The inclusion Bayes factor for condition, averaged across all candidate models, was BF<sub>incl</sub> = 12.80, providing strong evidence for an effect of condition on RT (Jeffreys, 1961). Posterior estimates indicated a mean RT difference of 45 ms, 95% credible interval [28, 62].

### 报告要素

- **先验设定**: 明确报告先验分布类型及参数（如 Cauchy prior, r scale = 0.5）
- **贝叶斯因子**: 报告 BF<sub>10</sub>（支持H1的证据）或 BF<sub>01</sub>（支持H0的证据），并注明解释标准
- **纳入贝叶斯因子**: 报告 BF<sub>incl</sub>，反映每个因子跨模型的平均证据
- **后验分布**: 如可能，报告效应量的后验均值及95%可信区间
- **证据强度解释**: BF > 3 = 中等证据，BF > 10 = 强证据，BF > 100 = 极强证据（Jeffreys, 1961）

## 注意事项

- 先验设置影响BF值——报告先验,做灵敏度分析
- BF10>3 = 中等证据, >10 = 强证据
- 超过10个被试内条件时计算可能很慢
