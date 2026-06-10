# 树状图 (Dendrogram)

## 概述

树状图展示层次聚类的结果,用树枝结构表示数据点的分组关系。是聚类分析的必要可视化。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 层次聚类结果 |
| 用途 | 确定最佳聚类数(剪枝高度) |

## R 代码

```r
hc <- hclust(dist(data[,vars]), method="ward.D2")
plot(hc, hang=-1, labels=FALSE, main="Hierarchical Clustering")
rect.hclust(hc, k=3, border="red")  # 标注3类
```

## 解读

- 纵轴=合并距离(越高=越不相似)
- 横轴=观测/聚类
- 低处合并=相似度高
- 高处横切线→确定聚类数

## 关键参数

| 参数 | 作用 |
|------|------|
| `method` | 聚类方法(ward.D2/complete/average) |
| `hang` | 标签悬挂位置(-1=对齐) |
| `k` | 剪枝类别数 |
