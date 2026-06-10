# 交叉随机效应 (Crossed Random Effects)

## 概述

当实验同时抽样**被试**和**刺激**时,两者都是随机效应,需在模型中同时建模。这是心理语言学的**标准做法**,也适用于任何以刺激为随机样本的设计。

**典型场景**: 30个被试对50个面孔图片做情绪判断。被试和图片都是随机样本→需交叉随机效应。

## 何时使用

| 条件 | 要求 |
|------|------|
| 实验设计 | 被试内设计（within-subjects），同时包含被试和刺激两个随机抽样维度 |
| 因变量类型 | 连续变量（如反应时、评分、注视时间等） |
| 自变量类型 | 分类变量（如实验条件），可包含被试内和被试间因素 |
| 最低样本量 | 被试 ≥ 20，刺激 ≥ 20；建议被试 ≥ 30、刺激 ≥ 30 以保证方差成分估计稳定 |
| 被试与刺激关系 | 交叉（crossed），非嵌套（non-nested）：每个被试接触多个刺激，每个刺激被多个被试评定 |
| 关键假设 | 被试和刺激均为来自对应总体的随机样本；随机效应的正态性和方差齐性 |
| 不适用情况 | 刺激为固定效应（如仅使用2张图片）或刺激嵌套于被试（如每个被试使用不同的刺激集） |

## 为什么必须做

如果只建模被试随机效应而忽略刺激:
- 刺激间的系统差异被当作误差→假阳性膨胀
- 统计推断只能推广到"这些被试"而不能同时推广到"这些刺激+其他类似刺激"

## 模型

```r
lmer(rt ~ condition + (1|subject) + (1+condition|item), data=data)
```

**关键**: 这是交叉效应,非嵌套。被试和刺激之间没有层级关系。

## 何时需要

- 语言研究: 被试×词汇/句子
- 面孔/图片研究: 被试×刺激图片
- 社会认知: 被试×社交场景

## 报告

> A linear mixed model with crossed random effects of subjects and items examined the condition effect on RT. The effect was significant, b=35.2, SE=12.1, t=2.91, with random intercepts by subject (SD=85) and by-item random slopes (SD=15).

## 报告格式 (APA 7th)

**方法部分示例：**

> We analyzed the data using linear mixed-effects models with crossed random effects, as both participants and stimuli were treated as random samples from their respective populations. The model included condition as a fixed effect, with random intercepts for participants and random intercepts and slopes for condition by stimuli. Model parameters were estimated using restricted maximum likelihood (REML) with the `lme4` package (Version 1.1-35.1; Bates et al., 2015) in R (Version 4.4.0; R Core Team, 2024). Significance of fixed effects was assessed via Satterthwaite-approximated degrees of freedom using the `lmerTest` package (Version 3.1-3; Kuznetsova et al., 2017).
>
> The maximal random-effects structure justified by the design (Barr et al., 2013) was specified as: `dv ~ condition + (1 | participant) + (1 + condition | stimulus)`. When the maximal model failed to converge, we simplified the random-effects structure by removing the correlation term first, then the slope term if non-convergence persisted (Bates et al., 2015).

**结果部分示例：**

> A linear mixed-effects model with crossed random effects of participants and stimuli revealed a significant effect of condition on response times, *b* = 35.2, *SE* = 12.1, *t*(52.7) = 2.91, *p* = .005. The random-effects structure included a random intercept for participants (variance = 7225, *SD* = 85.0) and random intercepts and slopes for condition by stimuli (intercept variance = 1024, *SD* = 32.0; slope variance = 225, *SD* = 15.0; correlation between intercept and slope = -.12). The model explained 34% of the total variance in response times (conditional *R*² = .34; marginal *R*² = .12; Nakagawa & Schielzeth, 2013).

**参考文献格式（APA 7th）：**

> Barr, D. J., Levy, R., Scheepers, C., & Tily, H. J. (2013). Random effects structure for confirmatory hypothesis testing: Keep it maximal. *Journal of Memory and Language*, *68*(3), 255–278. https://doi.org/10.1016/j.jml.2012.11.001
>
> Bates, D., Machler, M., Bolker, B., & Walker, S. (2015). Fitting linear mixed-effects models using lme4. *Journal of Statistical Software*, *67*(1), 1–48. https://doi.org/10.18637/jss.v067.i01
>
> Kuznetsova, A., Brockhoff, P. B., & Christensen, R. H. B. (2017). lmerTest package: Tests in linear mixed effects models. *Journal of Statistical Software*, *82*(13), 1–26. https://doi.org/10.18637/jss.v082.i13
>
> Nakagawa, S., & Schielzeth, H. (2013). A general and simple method for obtaining *R*² from generalized linear mixed-effects models. *Methods in Ecology and Evolution*, *4*(2), 133–142. https://doi.org/10.1111/j.2041-210x.2012.00261.x
