# 交叉验证 (Cross-Validation)

## 概述

交叉验证估计预测流程在目标数据分布上的泛化表现，而非仅评估训练集拟合。分割单位、预处理嵌套和目标部署分布决定它是否回答正确的预测问题。

**典型场景**: 评估LASSO回归模型对新被试的预测准确率; 比较多个模型的预测性能。

## 何时使用

| 条件 | 要求 |
|------|------|
| 研究设计 | 预测性研究 (非因果推断) |
| 因变量类型 | 连续变量 (回归) 或分类变量 (分类) |
| 信息要求 | 由独立抽样单元数、事件数/类别比例、模型复杂度与目标精度决定；没有通用 `N ≥ 50` 门槛 |
| 分割契约 | 分割必须模拟目标泛化单位（新被试/项目/中心/时间段）；所有调参、特征选择、插补和标准化在训练折内完成 |
| 不适用场景 | 因果效应估计; 时间序列预测 (需用时序交叉验证); 数据存在层次结构但未分层分割 |

## 方法

| 方法 | 特点 | 何时用 |
|------|------|--------|
| k-fold CV | 分 k 份轮流测试 | k 由独立单元数、计算预算与偏差/方差权衡确定 |
| Leave-One-Out (LOOCV) | 每个独立单元留一 | 需评估高方差、计算成本和目标泛化单位，不是小样本自动默认 |
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

> Model predictive performance was evaluated using 10-fold cross-validation with folds split at the participant level, matching the target of prediction for new participants. All preprocessing and tuning occurred within each training fold. The LASSO model yielded RMSE = 45.2, cross-validated R² = .34, and MAE = 34.7, compared with RMSE = 52.1, R² = .28, and MAE = 40.1 for the prespecified comparator. Fold-wise/participant-level uncertainty for the performance difference was reported; no universal “small/medium/large” R² cutoff was imposed.

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
- 若在全部开发数据上重拟合最终模型，应与锁定的预处理/调参流程一起保存；这不会替代独立外部验证
