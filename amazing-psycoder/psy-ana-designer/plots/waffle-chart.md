# 华夫图 (Waffle Chart)

## 概述

华夫图用方格矩阵表示比例,每个方格代表1%或固定数量。比饼图更准确地传达比例信息。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 展示组成比例(替代饼图) |
| 优势 | 1方格=固定单位,直观准确 |

## R 代码

```r
library(waffle)
parts <- c(Congruent=60, Incongruent=40)
waffle(parts, rows=10, colors=c("#69b3a2","#404080"),
       title="Trial Type Distribution")
```

## vs 饼图

华夫图比饼图更准确(人类不擅长比较角度和面积)。每个方格=离散单位,容易计数。

## 关键参数

| 参数 | 作用 |
|------|------|
| `rows` | 行数(控制格子大小) |
| `colors` | 颜色向量 |
| `title` | 标题 |
