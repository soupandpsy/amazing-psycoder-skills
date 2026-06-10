# 堆叠面积图 (Stacked Area Chart)

## 概述

堆叠面积图展示多个类别随时间的组成变化。X轴=时间,Y轴=累计量,颜色=类别。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 时间序列 + 组成比例 |
| 数据 | 时间 × 类别 × 数值 |

## R 代码

```r
ggplot(data, aes(x=time, y=count, fill=category)) +
  geom_area(alpha=0.8, position="fill") +  # position="fill"=比例化
  scale_fill_viridis_d() +
  labs(title="Composition Change Over Time", x="Time", y="Proportion") +
  theme_minimal()
```

## 解读

- 带宽度变化=某类别比例增减
- 色带平行=比例稳定
- position="stack"(绝对量) vs "fill"(比例)
