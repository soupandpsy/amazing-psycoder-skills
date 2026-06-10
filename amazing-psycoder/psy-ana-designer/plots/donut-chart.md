# 环形图 (Donut Chart)

## 概述

环形图是饼图的变体,中心为空,用环的弧长表示比例。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 2-5个类别的比例展示 |
| ⚠️ | 不推荐用于精确比较(条形图更准确) |

## R 代码

```r
library(ggplot2)
data <- data.frame(category=c("A","B","C"), count=c(30,45,25))
data$fraction <- data$count/sum(data$count)
data$ymax <- cumsum(data$fraction)
data$ymin <- c(0, head(data$ymax, n=-1))

ggplot(data, aes(ymax=ymax, ymin=ymin, xmax=4, xmin=3, fill=category)) +
  geom_rect(color="white", linewidth=1) +
  coord_polar(theta="y") +
  xlim(c(2,4)) +
  scale_fill_brewer(palette="Set2") +
  theme_void() + theme(legend.position="right")
```

## 争议

人眼不擅长比较角度和弧长。条形图更适合精确比较。环形图仅推荐用于展示2-3个类别的粗略比例。

## 关键参数

| 参数 | 作用 |
|------|------|
| `xlim(c(2,4))` | 环的内外半径 |
| `coord_polar(theta='y')` | 转为极坐标 |
