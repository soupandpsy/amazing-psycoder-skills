# 相关椭圆图 (Correlation Ellipse)

## 概述

在散点图上叠加置信椭圆,展示两变量关系的强度和方向。椭圆越窄越长=相关越强。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 散点图+相关性视觉强化 |
| 优势 | 椭圆形状=相关强度和方向 |

## R 代码

```r
ggplot(data, aes(x=rt, y=accuracy)) +
  geom_point(alpha=0.5) +
  stat_ellipse(level=0.95, color="red", linewidth=1) +
  labs(title="RT vs Accuracy (95% Confidence Ellipse)") +
  theme_minimal()
```

## 解读

- 椭圆窄长=强相关
- 椭圆接近圆=弱相关
- 椭圆倾斜方向=正/负相关
- 椭圆包含约95%的数据点
