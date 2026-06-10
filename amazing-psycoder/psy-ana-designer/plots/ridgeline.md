# 山脊图 (Ridgeline Plot)

## 概述

山脊图是多个密度图沿Y轴堆叠,比较3+组或3+时间点的分布形状。当需要比较的条件>=3时,比多个直方图更紧凑优雅。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 3+组分布比较,纵向多时间点 |
| DV | 连续 |
| 优势 | 节省空间,分布变化一目了然 |

## R 代码

```r
library(ggridges)
ggplot(data, aes(x=rt, y=condition, fill=condition)) +
  geom_density_ridges(alpha=0.7, scale=1.5) +
  scale_fill_viridis_d() +
  labs(title="RT Distribution by Condition", x="RT (ms)", y="Condition") +
  theme_ridges()
```

## 解读

- 峰向右移 → 条件间RT增加
- 峰变宽 → 变异性增大
- 多峰 → 可能混合亚群
- 重叠程度 → 条件间差异大小

## 关键参数

| 参数 | 作用 |
|------|------|
| `scale` | 重叠程度(>1=更大重叠) |
| `quantile_lines` | TRUE=加中位线 |
| `fill` | 颜色映射 |
