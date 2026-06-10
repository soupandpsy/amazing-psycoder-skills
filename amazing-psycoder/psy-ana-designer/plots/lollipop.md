# 棒棒糖图 (Lollipop Chart)

## 概述

棒棒糖图用细线+圆点替代条形图的柱子,保留数值比较功能但减少了"墨水"。是条形图的优雅替代。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 排序的多项对比 |
| 优势 | 比条形图更简洁,点+线=最少墨水 |

## R 代码

```r
ggplot(data, aes(x=reorder(condition, mean_rt), y=mean_rt)) +
  geom_segment(aes(xend=condition, yend=0), color="grey", linewidth=1) +
  geom_point(size=4, color="#69b3a2") +
  coord_flip() +
  labs(title="Mean RT by Condition", x="Condition", y="Mean RT (ms)") +
  theme_minimal()
```

## vs 条形图

棒棒糖图用点标记数值,线连接点和基线。同样展示数值大小,但视觉上更轻量。适合≥5组的排序比较。

## 关键参数

| 参数 | 作用 |
|------|------|
| `geom_segment(xend,yend=0)` | 从0到值的线段 |
| `coord_flip()` | 水平展示(推荐) |
| `reorder()` | 按值排序 |
