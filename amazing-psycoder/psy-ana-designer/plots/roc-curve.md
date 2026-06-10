# ROC 曲线 (ROC Curve)

## 概述

ROC曲线展示二分类模型在所有可能截断点上的灵敏度vs假阳性率。曲线下面积（AUC）量化整体判别力。

## 何时使用

| 条件 | 说明 |
|------|------|
| DV | 二分类（患病/健康,正确/错误） |
| 预测 | 连续分数或概率 |

## R 代码

```r
library(pROC)
roc_obj <- roc(data$diagnosis, data$score)
plot(roc_obj, print.auc=TRUE, auc.polygon=TRUE)
```

## 解读

- AUC=1.0 → 完美分类
- AUC=0.5 → 随机（对角线）
- AUC=0.7-0.8 → 可接受
- AUC>0.9 → 优秀
