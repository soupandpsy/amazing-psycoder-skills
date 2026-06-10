# 树图 (Treemap)

## 概述

树图用嵌套矩形展示层次数据的组成比例。面积=数值大小。适合展示多层级组成。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 层次比例数据 |
| 优势 | 比饼图更有效利用空间 |

## R 代码

```r
library(treemap)
treemap(data,
        index=c("category","subcategory"),
        vSize="value",
        vColor="value",
        type="value",
        palette="YlGnBu",
        title="Hierarchical Composition")
```

## vs 饼图

树图比饼图更高效地利用空间,可以展示多层级的层次结构。适合>5个类别。

## 关键参数

| 参数 | 作用 |
|------|------|
| `index` | 层级分类变量 |
| `vSize` | 面积变量 |
| `vColor` | 颜色变量 |
| `palette` | 配色方案 |
