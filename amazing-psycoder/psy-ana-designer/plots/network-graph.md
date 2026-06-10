# 网络图 (Network Graph)

## 概述

网络图展示心理变量之间的偏相关网络。节点=变量，边=偏相关系数。用于症状网络分析、问卷条目网络等。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 心理网络分析(精神病理学) |
| 数据 | 多个连续变量 |

## R 代码

```r
library(qgraph)
network <- estimateNetwork(data, default="EBICglasso")
plot(network, layout="spring", theme="colorblind")
```

## 解读

- 粗/深色边=强偏相关
- 中心节点(多连接)=高Strength中心性
- 绿色边=正相关,红色边=负相关
- 节点间距=连接强度（紧密=强相关）

## 关键参数

| 参数 | 作用 |
|------|------|
| `layout` | spring/circle/fruchtermanreingold |
| `cut` | 边阈值(只显示>cut的边) |
| `theme` | colorblind/classic |
