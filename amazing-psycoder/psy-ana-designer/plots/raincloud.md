# 雨云图 (Raincloud Plot)

## 概述

雨云图整合了三种可视化：小提琴图（密度分布）、箱线图（四分位数+中位数）和散点（个体数据点），在一张图中展示数据的完整信息。

**核心理念**：条形图隐藏个体差异和分布形状，雨云图全部展示。

## 何时使用

| 条件 | 说明 |
|------|------|
| 设计 | 被试内两组比较 |
| DV | 连续变量（RT、分数等） |
| 数据要求 | 每被试每条件有多个试次或均值 |
| 不适用 | 被试间设计（用箱线+散点替代） |

## 图表元素

| 元素 | 作用 |
|------|------|
| 小提琴 (violin) | 展示数据分布的密度形状 |
| 箱线 (boxplot) | 展示中位数、四分位数、范围 |
| 散点 (jitter) | 展示每个被试的数据点 |

## R 代码

```r
ggplot(data, aes(x=condition, y=rt, fill=condition, color=condition)) +
  ggrain::geom_rain(alpha=0.5, point.size=1) +
  scale_fill_brewer(palette="Set2") +
  labs(title="RT by Condition", x="Condition", y="RT (ms)") +
  theme_minimal(base_size=12)
```

## Python 代码

```python
# 手动组合: violin + box + strip
sns.violinplot(data=df, x='condition', y='rt', inner=None)
sns.boxplot(data=df, x='condition', y='rt', width=0.15)
sns.stripplot(data=df, x='condition', y='rt', alpha=0.3, size=3)
# 或 ptitprince.RainCloud()
```

## 输出

保存为 `fig1_raincloud.png`，300dpi，宽6×高5英寸。

## 关键参数

| 参数 | 作用 |
|------|------|
| `alpha` | 小提琴/散点透明度(0.3-0.7) |
| `point.size` | 散点大小 |
| `palette` | 配色方案(推荐Set2) |

## 解读

- 小提琴形状对比=分布差异
- 箱线中位线距离=效应大小
- 散点分散度=个体差异

## 注意事项

被试内设计首选。被试间设计用箱线+散点替代(雨云图的连线逻辑不适用)。
