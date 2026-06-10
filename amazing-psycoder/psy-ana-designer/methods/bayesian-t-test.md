# 贝叶斯 t 检验 (Bayesian t-test)

## 概述

贝叶斯t检验量化了H1和H0的相对证据强度。不输出p值,输出**贝叶斯因子(BF10)**。

## 何时使用

- 需要量化"没有差异"的证据 (传统t检验不能)
- 小样本(传统方法效力不足)
- 预注册分析计划中预先指定
- 需要连续监控证据(序贯分析)

## BF10 解读

| BF10 | 证据强度 | 含义 |
|------|---------|------|
| >100 | 极端 | H1极强支持 |
| 30-100 | 非常强 | H1强支持 |
| 10-30 | 强 | H1支持 |
| 3-10 | 中等 | H1中等支持 |
| 1/3-3 | 弱 | 数据不敏感 |
| 1/10-1/3 | 中等 | H0中等支持 |
| 1/30-1/10 | 强 | H0强支持 |

## R代码

```r
library(BayesFactor)
bf <- ttestBF(formula = rt ~ condition, data = data_agg, paired = TRUE)
print(bf)  # BF10
```

## 报告格式

> A Bayesian paired t-test compared the two conditions. The Bayes factor (BF10=5.32) provided moderate evidence for H1 over H0.

## 报告

APA 第七版格式报告示例(以贝叶斯配对t检验为例):

**方法部分**：使用贝叶斯配对t检验(BayesFactor R包, 默认先验: 柯西分布, scale = √2/2), 以BF10作为贝叶斯因子, 报告后验分布的中位数及95%最高密度区间(HDI)。

**结果部分示例**：

> 对两种实验条件下的反应时进行贝叶斯配对t检验。结果显示, 贝叶斯因子BF10 = 5.32, 为H1(存在差异)相对于H0(无差异)提供了中等程度的证据(Jeffreys, 1961)。后验分布的中位数为 δ = 0.48, 95% HDI [0.12, 0.85], 效应量对应中等偏小水平。先验设定为柯西分布(scale = √2/2), 稳健性检验显示, 在r = 0.5至1.0的先验范围内, BF10的变化不超过12%, 结论较为稳健。

**模板(英文)**：

> A Bayesian paired t-test was conducted to compare response times between the two conditions. The analysis yielded a Bayes factor BF10 = [value], providing [anecdotal/substantial/strong/very strong/decisive] evidence in favor of H[1/0]. The posterior median for the standardized effect size was δ = [value], 95% credible interval [[lower], [upper]]. A default Cauchy prior (scale = √2/2) was used for the effect size under H1.

## 注意事项

- BF10>3 不代表"效应存在"——是连续证据,不是二值决策
- 仍需报告效应量(后验分布的均值+95%可信区间)
- 先验设置影响BF值(默认Cauchy scale=√2/2)
