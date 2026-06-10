# 时间序列图 (Time Series Plot)

## 概述

时间序列图展示变量随时间的变化，适合纵向数据、密集追踪数据。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 纵向追踪、EMA生态瞬时评估 |
| 关键 | 展示趋势、周期、干预断点 |

## R 代码

```r
ggplot(data, aes(x=time, y=score, group=subject_id)) +
  geom_line(alpha=0.3, linewidth=0.3) +
  stat_summary(aes(group=1), fun=mean, geom="line", linewidth=1.5, color="red") +
  geom_vline(xintercept=intervention_day, linetype="dashed") +
  labs(title="Daily Anxiety Scores", x="Day", y="Score") +
  theme_minimal()
```

## 解读

- 均值线趋势 → 群体变化方向
- 灰色个体线 → 个体差异
- 虚线后的变化 → 干预效果

## 关键参数

| 参数 | 作用 |
|------|------|
| `geom_line(aes(group=id))` | 个体轨迹 |
| `stat_summary(fun=mean)` | 群体均值 |
| `geom_vline(xintercept)` | 干预断点线 |
