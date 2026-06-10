# Cleveland 点图 (Cleveland Dot Plot)

## 概述

Cleveland点图用排序后的点展示多组数值,是条形图的最佳替代。心理学论文中应优先考虑。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 多组排序比较(≥5组) |
| 优势 | 精准读取数值,易比较排序 |

## R 代码

```r
ggplot(data, aes(x=mean_rt, y=reorder(condition, mean_rt))) +
  geom_point(size=4, color="#69b3a2") +
  geom_errorbarh(aes(xmin=mean_rt-se, xmax=mean_rt+se), height=0.2) +
  labs(title="Mean RT by Condition", x="Mean RT (ms)", y="Condition") +
  theme_minimal()
```

## 解读

- 点水平位置=均值
- 误差线=SE/CI
- 从上到下排序=从高到低
- 点间距=条件间差异

## 关键参数

| 参数 | 作用 |
|------|------|
| `reorder(var, val)` | 按值排序Y轴 |
| `geom_errorbarh` | 水平误差线 |
