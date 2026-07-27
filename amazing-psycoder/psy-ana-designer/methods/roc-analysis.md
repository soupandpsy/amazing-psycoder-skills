# ROC 分析 (Receiver Operating Characteristic)

## 概述

ROC分析评估二分类模型的判别能力,通过AUC(曲线下面积)量化分类性能。在临床心理学中广泛用于评估诊断工具。

**典型场景**: 评估焦虑分数对临床诊断的分类准确性; 评估行为指标区分ADHD和对照组的能力。

## 何时使用

| 条件 | 要求 |
|------|------|
| 研究设计 | 诊断/预测验证设计；需明确目标总体、取样方案、预测时点和可辩护的参考标准 |
| 因变量类型 | 二分类(如患病/未患病、阳性/阴性) |
| 自变量类型 | 连续变量或有序分类变量(如量表得分、生物指标) |
| 样本信息 | 由阳性/阴性例数、目标 AUC/敏感度特异度精度、阈值选择和验证方案决定；分别规划两类样本信息 |
| 关键检查 | 参考标准误分类/验证偏倚、病例对照取样、重复/聚类观测、预测器评估时点与目标应用一致；阈值选择必须与验证分开 |
| 扩展/限制 | 多分类、时间结局或聚类数据需要相应 ROC/判别扩展；无可靠参考标准时，普通二分类 ROC 的解释受限；名义预测器需先定义可验证的评分规则 |

## 关键指标

| 指标 | 含义 | 标准 |
|------|------|------|
| AUC | 整体判别力 | 0.5=随机, 0.7=可接受, 0.8=好, 0.9=优秀 |
| Sensitivity | 真阳性率(检出率) | — |
| Specificity | 真阴性率(排错率) | — |
| Youden指数 | Sens+Spec-1 | 确定最优截断点 |

## R代码

```r
library(pROC)
roc_obj <- roc(data$diagnosis, data$score)
auc(roc_obj)
plot(roc_obj)
coords(roc_obj, "best")  # 最优截断点
```

## 报告

APA 7th 格式报告示例:

> A receiver operating characteristic (ROC) analysis was conducted to evaluate the diagnostic accuracy of the anxiety score for identifying clinical anxiety disorder (as determined by structured clinical interview). The area under the ROC curve (AUC) was 0.82, 95% CI [0.75, 0.89], indicating good discriminatory ability between individuals with and without the disorder (Hosmer & Lemeshow, 2000). The optimal cutoff score of 45 was identified using the Youden index (Youden, 1950), yielding a sensitivity of 78% and specificity of 74%. Figure 1 presents the ROC curve.

APA 7th 格式中需报告的关键要素:
- AUC值及其95%置信区间
- 判别能力的定性描述(参考标准: 0.5 = 随机, 0.7–0.8 = 可接受, 0.8–0.9 = 好, ≥ 0.9 = 优秀)
- 最优截断点的确定方法(如Youden指数)及对应的敏感性和特异性
- 参考标准的来源、盲法、误分类风险和缺失验证说明
- 图表编号引用(Figure 1)
