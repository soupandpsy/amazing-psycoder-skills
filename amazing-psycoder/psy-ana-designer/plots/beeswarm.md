# 蜜蜂群图 (Beeswarm Plot)

## 概述

蜜蜂群图将每个数据点排列在分类轴两侧,点不重叠,比jitter散点更清晰。适合展示每个被试的数据且有中等数量的观测。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 展示所有个体数据,避免重叠 |
| 观测数 | 10-200每条件(太多会溢出) |

## R 代码

```r
library(ggbeeswarm)
ggplot(data, aes(x=condition, y=rt, color=condition)) +
  geom_beeswarm(size=2, alpha=0.7, cex=2) +
  stat_summary(fun=mean, geom="point", size=4, color="red", shape=18) +
  labs(title="RT by Condition", x="Condition", y="RT (ms)") +
  theme_minimal() + theme(legend.position="none")
```

## 关键参数

| 参数 | 作用 |
|------|------|
| `cex` | 点间距(越大越分散) |
| `size` | 点大小 |
| `priority` | 排列优先级("ascending"/"descending"/"random") |

## vs 雨云图

雨云图有密度层展示分布形状,蜜蜂群图只展示个体点。点<50时蜜蜂群图更清晰,>100时雨云图更好。
