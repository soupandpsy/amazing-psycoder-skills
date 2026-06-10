# ROC 分析 (Receiver Operating Characteristic)

## 概述

ROC分析评估二分类模型的判别能力,通过AUC(曲线下面积)量化分类性能。在临床心理学中广泛用于评估诊断工具。

**典型场景**: 评估焦虑分数对临床诊断的分类准确性; 评估行为指标区分ADHD和对照组的能力。

## 何时使用

| 条件 | 要求 |
|------|------|
| 研究设计 | 横断面设计或病例-对照设计,需有金标准诊断作为参考 |
| 因变量类型 | 二分类(如患病/未患病、阳性/阴性) |
| 自变量类型 | 连续变量或有序分类变量(如量表得分、生物指标) |
| 样本量要求 | 两组各不少于30例,总样本量建议 ≥ 100 |
| 关键假设 | 金标准独立于预测变量; 观测值相互独立; 预测变量在两组间有足够的变异 |
| 不适用情形 | 因变量为多分类或连续变量; 无可靠金标准; 预测变量为纯分类名义变量 |

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
- 金标准/参考标准的来源说明
- 图表编号引用(Figure 1)
