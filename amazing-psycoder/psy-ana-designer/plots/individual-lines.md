# 个体连线图 (Spaghetti Plot)

## 概述

个体连线图用一条线连接每个被试在两种条件下的数据点，同时叠加红色粗线表示组均值。是展示被试内变化的最直观方式。

## 何时使用

| 条件 | 说明 |
|------|------|
| 设计 | 被试内两组比较 |
| DV | 连续变量 |
| 关键 | 展示个体层面的变化方向和幅度 |

## 图表元素

| 元素 | 作用 |
|------|------|
| 灰色细线（每人一条） | 个体变化轨迹 |
| 红色粗线 | 组均值变化 |
| 红色大点 | 每组均值 |

## R 代码

```r
data_agg %>% 
  ggplot(aes(x=condition, y=mean_rt, group=subject_id)) +
  geom_line(alpha=0.3, linewidth=0.5) +
  geom_point(alpha=0.3, size=1) +
  stat_summary(aes(group=1), fun=mean, geom="line", linewidth=1.5, color="red") +
  stat_summary(fun=mean, geom="point", size=3, color="red") +
  labs(title="Individual RT Changes", x="Condition", y="Mean RT (ms)") +
  theme_minimal(12)
```

## 解读

- 大部分线斜率方向一致 → 条件效应稳健
- 线与组均值反向 → 该被试模式异常
- 线密集/稀疏 → 个体差异大小

## 关键参数

| 参数 | 作用 |
|------|------|
| `group=subject_id` | 按被试分组连线 |
| `alpha` | 个体线透明度(0.2-0.4) |
| `stat_summary(fun=mean)` | 叠加组均值线 |
