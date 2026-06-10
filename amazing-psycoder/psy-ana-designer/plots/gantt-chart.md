# 甘特图 (Gantt Chart)

## 概述

甘特图用横向条形图展示实验流程时间线,每个任务/阶段用条形长度表示持续时间。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 展示实验设计的时间结构 |
| 用途 | 方法部分的视觉辅助 |

## R 代码

```r
library(ggplot2)
ggplot(data, aes(x=start_time, xend=end_time, y=task, color=phase)) +
  geom_segment(linewidth=6) +
  labs(title="Experiment Timeline", x="Time (minutes)", y="Task") +
  theme_minimal()
```

## 关键参数

| 参数 | 作用 |
|------|------|
| `x`/`xend` | 任务起止时间 |
| `y` | 任务名称 |
| `color` | 阶段颜色分组 |
| `linewidth` | 条形宽度(6-10合适) |

## 解读

- 条形长度=任务持续时间
- 条形重叠=并行任务
- 颜色分组=实验阶段

## 注意事项

适合方法论部分的实验流程图。精确时间需标注数值。
