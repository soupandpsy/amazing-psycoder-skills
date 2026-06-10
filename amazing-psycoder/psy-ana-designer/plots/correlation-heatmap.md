# 相关矩阵热图 (Correlation Heatmap)

## 概述

热图用颜色编码多个变量间的相关系数矩阵，一目了然地展示所有两两相关。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 4+连续变量的相关矩阵 |
| 目标 | 快速识别强相关和弱相关 |

## R 代码

```r
library(corrplot)
cor_matrix <- cor(data[,vars], method="pearson")
corrplot(cor_matrix, method="color", type="upper",
         addCoef.col="black", tl.col="black", tl.cex=0.8)
```

## 解读

- 深色=强相关（正或负）
- 浅色=弱相关
- 对角线=1（自己与自己）
- 矩阵对称

## 关键参数

| 参数 | 作用 |
|------|------|
| `method` | color/circle/number |
| `type` | upper/lower/full |
| `addCoef.col` | 相关系数文字颜色 |
