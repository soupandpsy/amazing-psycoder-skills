# 森林图 (Forest Plot)

## 概述

森林图是元分析的标准可视化。每个研究用一条水平线表示效应量和CI，菱形表示合并效应量。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 元分析 |
| 变量 | 效应量+SE/CI |

## R 代码

```r
library(metafor)
res <- rma(yi=yi, sei=sei, data=dat)
forest(res, slab=paste(Author, Year),
       xlab="Cohen's d", mlab="RE Model")
```

## 解读

- 线跨过0（或1 for OR）→ 该研究不显著
- 菱形完全在0一侧 → 总体效应显著
- 线长度=CI宽度=估计精度

## 关键参数

| 参数 | 作用 |
|------|------|
| `slab` | 研究标签 |
| `xlab` | X轴标签(效应量名称) |
| `mlab` | 合并效应量标签 |
