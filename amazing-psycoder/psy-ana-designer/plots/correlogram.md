# 相关图 (Correlogram)

## 概述

相关图将相关矩阵可视化,下半三角=散点图+拟合线,对角=变量名+分布,上半三角=相关系数。一张图展示所有两两关系的完整信息。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 探索性多变量分析(3-8个连续变量) |
| 优势 | 一张图=所有两两散点+相关+分布 |

## R 代码

```r
library(GGally)
ggpairs(data, columns=c("rt","acc","anxiety","age"),
        upper=list(continuous=wrap("cor", size=3)),
        lower=list(continuous=wrap("smooth", alpha=0.3)),
        diag=list(continuous=wrap("densityDiag", alpha=0.5)))
```

## 解读

- 对角: 各变量密度分布
- 下三角: 散点图+loess平滑线
- 上三角: Pearson r + 显著性星号
- 离群点→标记检查

## 关键参数

| 参数 | 作用 |
|------|------|
| `columns` | 选择的变量列号 |
| `upper` | 上三角(推荐cor) |
| `lower` | 下三角(推荐smooth) |
| `diag` | 对角(推荐densityDiag) |
