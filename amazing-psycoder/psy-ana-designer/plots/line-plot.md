# 折线图 (Line Plot)

## 概述

折线图是最基础的时间序列可视化，用线段连接连续时间点的数据。适合展示趋势和变化。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 单变量随时间变化 |
| 数据 | 时间 × 连续值 |

## R 代码

```r
ggplot(data, aes(x=time, y=value)) +
  geom_line(color="#69b3a2", linewidth=1) +
  geom_point(size=2, color="#69b3a2") +
  labs(title="Value Over Time", x="Time", y="Value") +
  theme_minimal()

# 多组折线
ggplot(data, aes(x=time, y=value, color=group)) +
  geom_line(linewidth=1) +
  scale_color_brewer(palette="Set2") +
  labs(title="Group Trends", x="Time", y="Value") +
  theme_minimal()
```

## 关键参数

| 参数 | 作用 |
|------|------|
| `linewidth` | 线宽(默认0.5) |
| `linetype` | 线型(solid/dashed/dotted) |
| `color` | 分组变量映射颜色 |

## 解读

- 上升趋势→随时间增加
- 转折点→干预/事件影响
- 多条线间距变化→组间差异变化

## 注意事项

X轴需排序。多条线时颜色不超过6种(否则难区分)。
