# 交叉验证 (Cross-Validation)

## 概述

交叉验证评估预测模型在**新数据**上的泛化能力,而非仅在训练数据上的拟合度。是机器学习方法评估的黄金标准。

**典型场景**: 评估LASSO回归模型对新被试的预测准确率; 比较多个模型的预测性能。

## 何时使用

| 条件 | 要求 |
|------|------|
| 研究设计 | 预测性研究 (非因果推断) |
| 因变量类型 | 连续变量 (回归) 或分类变量 (分类) |
| 样本量要求 | k-fold: 中等及以上 (N ≥ 50); LOOCV: 小样本可用 |
| 关键假设 | 数据独立同分布; k-fold分割需在被试级别进行 (非试次级别) |
| 不适用场景 | 因果效应估计; 时间序列预测 (需用时序交叉验证); 数据存在层次结构但未分层分割 |

## 方法

| 方法 | 特点 | 何时用 |
|------|------|--------|
| k-fold CV | 分k份,轮流测试 | 标准,k=5或10 |
| Leave-One-Out (LOOCV) | 每被试留一 | 小样本 |
| 重复k-fold | 多次随机分 | 评估稳定性 |

## R代码

```r
library(caret)
# 10-fold CV for linear model
train_control <- trainControl(method="cv", number=10)
model <- train(rt ~ ., data=data, method="lm", trControl=train_control)
print(model$results)  # RMSE, R², MAE
```

## 报告

APA 7th 格式报告示例 (回归模型):

> Model predictive performance was evaluated using 10-fold cross-validation, with folds split at the participant level to preserve independence. Prediction accuracy was assessed via root mean square error (RMSE) and explained variance (R²). The LASSO regression model demonstrated superior generalization (RMSE = 45.2, R² = .34, MAE = 34.7) compared to the full ordinary least squares model (RMSE = 52.1, R² = .28, MAE = 40.1). Cross-validated R² values indicated that the LASSO model accounted for 34% of the variance in out-of-sample reaction times, exceeding the conventional threshold for medium effect size in predictive modeling (R² > .13). These results suggest that regularized regression provides more robust predictions for novel participants than the unpenalized model.

APA 7th 格式报告示例 (分类模型):

> Classification performance was evaluated using stratified 10-fold cross-validation. The random forest classifier achieved a mean cross-validated AUC of .82 (95% CI [.78, .86]), sensitivity of .74, and specificity of .81, outperforming logistic regression (AUC = .76, 95% CI [.71, .81]).

报告清单:
- [ ] 明确交叉验证方法 (k-fold / LOOCV / 重复k-fold) 及 k 值
- [ ] 说明分割策略 (被试级别 / 试次级别 / 分层)
- [ ] 报告主要性能指标 (RMSE / R² / AUC / 准确率等)
- [ ] 若涉及模型比较, 报告各模型性能差异
- [ ] 给出关键指标的置信区间 (推荐)

## 注意事项

- CV估计的是预测性能,不是因果效应
- 被试内设计中,k-fold需在被试级别分(非试次)
- 最终模型应在全部数据上重新拟合后报告
