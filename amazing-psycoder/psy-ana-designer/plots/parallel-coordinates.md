# 平行坐标图 (Parallel Coordinates)

## 概述

平行坐标图用多条平行轴展示高维数据,每条线代表一个观测(被试),穿过多条轴展示该观测在所有变量上的值。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 4+连续变量的多变量模式 |
| 优势 | 一张图看所有变量的个体模式 |

## R 代码

```r
library(GGally)
ggparcoord(data, columns=1:5, groupColumn="condition",
           scale="uniminmax", alphaLines=0.3) +
  scale_color_brewer(palette="Set2") +
  labs(title="Multivariate Profiles by Condition") +
  theme_minimal()
```

## 解读

- 平行线→该变量不能区分组
- 交叉线→该变量区分组
- 线束分离→多变量组间差异

## 关键参数

| 参数 | 作用 |
|------|------|
| `columns` | 选择的列范围 |
| `groupColumn` | 分组变量 |
| `scale` | uniminmax/std/globalminmax |
