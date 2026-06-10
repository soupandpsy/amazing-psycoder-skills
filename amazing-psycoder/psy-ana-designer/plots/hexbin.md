# 六边形分箱图 (Hexbin Plot)

## 概述

当散点图数据量极大(>10000点)导致重叠看不清密度时,六边形分箱用颜色表示每个六边形内的点数。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 超大样本散点图(>5000点) |
| 优势 | 颜色编码密度,无重叠问题 |

## R 代码

```r
ggplot(data, aes(x=rt, y=accuracy)) +
  geom_hex(bins=30) +
  scale_fill_viridis_c() +
  labs(title="RT vs Accuracy (N=50,000)", fill="Count") +
  theme_minimal()
```

## vs 散点图

散点图>5000点时严重重叠看不清密度。六边形分箱用颜色编码密度,适合大样本探索。

## 关键参数

| 参数 | 作用 |
|------|------|
| `bins` | 六边形数量(分辨率) |
| `scale_fill_viridis_c()` | 色盲友好颜色梯度 |
