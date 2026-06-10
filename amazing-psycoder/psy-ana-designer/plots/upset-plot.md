# Upset 图 (UpSet Plot)

## 概述

Upset图展示多个集合的交集大小,是韦恩图的现代替代。适合展示多个分类条件的组合模式(如多个症状共存)。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 3+集合的交集可视化 |
| 数据类型 | 每个观测属于0或多个类别 |

## R 代码

```r
library(UpSetR)
upset(data, sets=c("anxiety","depression","stress","fatigue"),
      order.by="freq", main.bar.color="#69b3a2",
      sets.bar.color="#404080")
```

## vs 韦恩图

- 韦恩图: 2-3个集合清晰,>4无法阅读
- Upset: 任意数量集合,按频率排序,清晰

## 关键参数

| 参数 | 作用 |
|------|------|
| `sets` | 集合名称向量 |
| `order.by` | freq(按频率排序)/degree |
| `main.bar.color` | 主柱颜色 |
