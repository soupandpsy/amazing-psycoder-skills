# LASSO / 岭回归 (Regularization)

## 概述

LASSO和岭回归通过惩罚项收缩回归系数,防止过拟合。当预测变量多于被试数,或变量间高度相关时特别有用。

**典型场景**: 从50个问卷条目中选出最能预测Stroop效应的子集; 处理>20个高度相关的行为指标。

## 何时使用

| 条件 | 要求 |
|------|------|
| 研究设计 | 观测研究、相关设计、预测建模 |
| 因变量类型 | 连续变量（如反应时、问卷得分、脑电指标） |
| 预测变量 | 多个连续或分类变量，允许预测变量数 > 被试数 |
| 样本要求 | 最终入选变量数建议 < N/10；LASSO选出的变量数受λ控制 |
| 关键假设 | 因变量与预测变量间存在线性关系；观测独立性；无完全共线性（Ridge可处理高度相关，LASSO会从中选一） |

## LASSO vs Ridge

| 方法 | 惩罚 | 效果 | 何时用 |
|------|------|------|--------|
| Ridge | λΣβ² (L2) | 收缩但不归零 | 所有变量都有贡献 |
| LASSO | λΣ\|β\| (L1) | 部分系数→0(变量选择) | 想要精简模型 |
| Elastic Net | λ1Σ\|β\|+λ2Σβ² | 混合 | 不确定时 |

## 交叉验证选λ

```r
library(glmnet)
cv_fit <- cv.glmnet(x, y, alpha=1)  # alpha=1 for LASSO
plot(cv_fit)
coef(cv_fit, s="lambda.min")  # 最优λ下的系数
```

## 报告

### 简要示例

> LASSO regression (λ selected by 10-fold CV) identified 8 of 50 questionnaire items as predictors of Stroop interference. The final model explained 34% of variance, with anxiety and age as the strongest predictors.

### APA 7th 格式报告范例

> We conducted a LASSO regression with 10-fold cross-validation to identify which of 50 questionnaire items predicted Stroop interference (congruent minus incongruent RT, ms). The model selected at λ~min~ retained 8 predictors and explained 34% of the variance in Stroop scores, *R*^2^ = .34, MSE = 1245.61. The strongest predictors were trait anxiety (standardized coefficient β = 0.31) and age (β = −0.26), followed by sleep quality (β = 0.19), education years (β = −0.15), and working memory span (β = −0.12). The remaining three items (physical activity, caffeine intake, and BMI) each contributed |β| < 0.10. Bootstrap resampling (1000 iterations) confirmed that trait anxiety and age were selected in over 80% of resamples, supporting the stability of these predictors.

**中文对照**: 采用10折交叉验证的LASSO回归,从50个问卷条目中筛选Stroop干扰效应的预测变量。模型在λ~min~下保留8个预测变量,解释Stroop得分34%的变异,*R*^2^ = .34, MSE = 1245.61。最强预测变量为特质焦虑(标准化系数β = 0.31)和年龄(β = −0.26),其次是睡眠质量(β = 0.19)、受教育年限(β = −0.15)和工作记忆广度(β = −0.12)。其余三个条目(运动量、咖啡因摄入、BMI)的|β|均 < 0.10。Bootstrap重抽样(1000次)确认特质焦虑和年龄在80%以上的重抽样中被选中,支持这些预测变量的稳定性。

### 报告清单

- 使用的惩罚方法(LASSO / Ridge / Elastic Net)及α值
- λ选择方式(CV折数、λ~min~ 或 λ~1se~)
- 最终模型保留的变量数量及名称
- 模型拟合指标(*R*^2^、MSE 或 deviance)
- 各变量的标准化系数(β)及排序
- Bootstrap稳定性检验结果(如有)

## 注意事项

- LASSO选出的变量不稳定——bootstrap检验选择频率
- 惩罚回归的p值不能直接解释(有选择性偏差)
- 最好结合传统回归: LASSO选出变量,传统回归估计效应和检验
