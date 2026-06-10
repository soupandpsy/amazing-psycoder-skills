# 多水平/跨层模型 (Multilevel Modeling)

## 概述

多水平模型处理嵌套数据结构。心理学中最常见的嵌套:试次嵌套于被试,被试嵌套于班级,班级嵌套于学校。

**典型场景**: 学生(Level-1)嵌套于班级(Level-2),检验班级氛围(Level-2)对学生成绩(Level-1)的影响。

## 何时使用

| 条件 | 要求 |
|---|---|
| 研究设计类型 | 嵌套设计（试次嵌套于被试、被试嵌套于班级/学校）、重复测量设计 |
| 因变量类型 | 连续变量（反应时、成绩、量表得分等） |
| 样本量要求 | Level-2 单元数 ≥ 30（如 30 个班级），每单元 Level-1 观测数 ≥ 5；样本不足时 ICC 和随机效应估计可能不稳定 |
| 关键前提 | 数据存在显著嵌套结构（ICC > 0.05）；Level-1 变量组均值中心化，Level-2 变量总均值中心化 |

## 何时用（vs lmer）

其实 lmer 就是多水平模型的特例。当你的数据有明确层级(重复测量/嵌套)且需要区分组内和组间效应时,多水平术语更有用:

- 被试内效应(Level-1): 条件效应
- 被试间效应(Level-2): 组别、人口学变量
- 跨层交互: Level-2变量调节Level-1效应

## 模型

```r
lmer(rt ~ condition * group + (1+condition|subject), data=data)
```

## 关键：中心化

- Level-1变量: 组均值中心化 (centered within cluster)
- Level-2变量: 总均值中心化 (grand mean centered)
- 不做中心化会导致组间和组内效应混淆

## ICC (Intraclass Correlation Coefficient)

ICC = 组间方差/(组间方差+组内方差),衡量嵌套结构的必要性。ICC > 0.05 → 需要用多水平模型。

## 报告（APA 7th 格式）

多水平模型报告应包含模型设定、固定效应、随机效应及模型比较信息。以下为 APA 7th 格式示例：

**Model specification.** A multilevel model was fitted to examine the effect of condition (Level-1 within-subject factor: congruent vs. incongruent) and group (Level-2 between-subject factor: control vs. treatment) on reaction time (RT). The model included random intercepts and random slopes for condition by subject. Level-1 predictor (condition) was group-mean centered; Level-2 predictor (group) was grand-mean centered. Estimation was performed using restricted maximum likelihood (REML) via the `lme4` package in R.

**Fixed effects.** The intercept was significant, *b* = 450.3, *SE* = 18.7, *t*(58) = 24.08, *p* < .001. The main effect of condition was significant, *b* = 30.5, *SE* = 5.2, *t*(58) = 5.87, *p* < .001, with slower RTs in the incongruent condition. The main effect of group was not significant, *b* = 12.8, *SE* = 22.4, *t*(58) = 0.57, *p* = .571. The cross-level interaction between condition and group was significant, *b* = 15.2, *SE* = 4.4, *t*(58) = 3.45, *p* < .001, indicating that the condition effect differed by group: the congruency effect was larger in the treatment group than in the control group.

**Random effects.** The random intercept variance was 2450.6 (*SD* = 49.5) and the random slope variance for condition was 320.4 (*SD* = 17.9), with a correlation between intercept and slope of −.32. The residual variance was 1800.2 (*SD* = 42.4). The ICC was .12, confirming that 12% of the variance in RT was attributable to between-subject differences, justifying the multilevel approach.

**Model comparison.** Adding the cross-level interaction significantly improved model fit over the main-effects-only model, χ²(1) = 11.89, *p* < .001, ΔAIC = −9.9.
