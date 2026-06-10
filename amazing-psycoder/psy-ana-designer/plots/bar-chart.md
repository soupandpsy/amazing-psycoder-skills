# 条形图 (Bar Chart)

## 概述

条形图用柱高表示均值，误差棒表示SE/CI。是心理学论文中最常见但也最有争议的图表——隐藏了个体差异和分布形状。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 被试间设计,多组均值比较 |
| DV | 连续（均值+误差） |
| ⚠️ | 被试内设计不推荐——隐藏个体变化 |

## R 代码

```r
# 先计算均值和SE
desc <- data %>% group_by(condition) %>%
  summarise(mean=mean(rt), se=sd(rt)/sqrt(n()), .groups="drop")

ggplot(desc, aes(x=condition, y=mean, fill=condition)) +
  geom_col(width=0.6) +
  geom_errorbar(aes(ymin=mean-se, ymax=mean+se), width=0.15) +
  scale_fill_brewer(palette="Set2") +
  labs(title="Mean RT by Condition", x="Condition", y="Mean RT (ms)") +
  theme_minimal() + theme(legend.position="none")
```

## 争议

- 隐藏分布形状（正态和双峰可以有相同均值和SE）
- 隐藏个体数据点
- 被试内设计用条形图 = 信息损失
- 推荐替代: 雨云图(被试内)、箱线+散点(被试间)

## 关键参数

| 参数 | 作用 |
|------|------|
| `width` | 柱宽(0.4-0.8) |
| `position` | dodge(并排)/stack(堆叠)/fill(比例) |
| `stat` | identity(给定值)/count(自动计数) |
