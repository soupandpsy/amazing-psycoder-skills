# 双标图 (Biplot)

## 概述

双标图是PCA/因子分析的标准可视化。点=观测(被试),箭头=变量(载荷)。同时展示数据结构和变量关系。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | PCA/EFA/CFA结果可视化 |
| 展示 | 前两个主成分+变量载荷 |

## R 代码

```r
library(factoextra)
pca <- prcomp(data[,vars], scale=TRUE)
fviz_pca_biplot(pca, repel=TRUE, col.var="#69b3a2", col.ind="grey60")
```

## 解读

- 箭头方向=变量在PC空间的投影方向
- 箭头长度=该变量被前两个PC解释的比例(cos²)
- 同方向箭头=正相关变量
- 反方向箭头=负相关变量
- 点聚类=被试亚群

## 关键参数

| 参数 | 作用 |
|------|------|
| `repel` | TRUE=标签不重叠 |
| `col.var` | 箭头颜色 |
| `col.ind` | 个体点颜色 |
