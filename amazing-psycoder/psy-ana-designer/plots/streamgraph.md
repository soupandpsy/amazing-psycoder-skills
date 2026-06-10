# 流图 (Streamgraph)

## 概述

流图是堆叠面积图的变体,中心对称排列,用流动的形状展示组成随时间的变化。比堆叠面积图更具美感。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 多类别随时间变化的组成 |
| 数据 | 时间 × 类别 × 数值 |

## R 代码

```r
library(streamgraph)
streamgraph(data, key="category", value="count", date="year") %>%
  sg_fill_brewer("Set2") %>%
  sg_legend(show=TRUE)
```

## vs 堆叠面积图

流图中心对称,视觉上更平衡,但读数值不如堆叠面积图精确。适合展示整体趋势而非精确值。

## 关键参数

| 参数 | 作用 |
|------|------|
| `key` | 类别列 |
| `value` | 数值列 |
| `date` | 时间列 |
