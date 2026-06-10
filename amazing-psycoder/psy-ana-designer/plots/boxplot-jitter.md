# 箱线图+散点 (Boxplot + Jitter)

## 概述

箱线图展示数据的四分位分布，叠加散点展示个体数据点。适合被试间设计或多组比较。

## 何时使用

| 条件 | 说明 |
|------|------|
| 设计 | 被试间设计或多组比较 |
| DV | 连续变量 |
| 组数 | 2-6组（更多时分面） |

## 图表元素

| 元素 | 作用 |
|------|------|
| 箱体 | IQR（25%-75%），中位线 |
| 须线 | 1.5×IQR范围 |
| 散点 (jitter) | 每个被试的数据点 |

## R 代码

```r
ggplot(data, aes(x=group, y=rt, fill=group)) +
  geom_boxplot(alpha=0.5, outlier.shape=NA) +
  geom_jitter(width=0.1, alpha=0.3, size=1) +
  scale_fill_brewer(palette="Set2") +
  labs(title="RT by Group", x="Group", y="RT (ms)") +
  theme_minimal(12) + theme(legend.position="none")
```

## vs 雨云图

雨云图增加了小提琴密度层，更适合被试内设计。箱线+散点简洁清晰，适合被试间或多组。

## 关键参数

| 参数 | 作用 |
|------|------|
| `width` | 箱宽(0.3-0.6) |
| `outlier.shape` | NA=隐藏异常值 |
| `notch` | TRUE=中位数缺口比较 |
