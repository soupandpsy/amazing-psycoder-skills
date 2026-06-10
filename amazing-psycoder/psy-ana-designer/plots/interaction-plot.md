# 交互作用图 (Interaction Plot)

## 概述

交互图用分组折线展示两因素的交互效应，是理解交互作用最直观的方式。

## 何时使用

| 条件 | 说明 |
|------|------|
| 设计 | 两因素设计（被试内/间/混合） |
| 关键 | 折线不平行→交互存在 |

## 图表元素

| 元素 | 作用 |
|------|------|
| 分组折线 | 每个水平的一条均值折线 |
| 误差棒 | SE或CI |
| 颜色/线型 | 区分不同水平 |

## R 代码

```r
ggplot(data_agg, aes(x=factorA, y=mean_rt, color=factorB, group=factorB)) +
  stat_summary(fun=mean, geom="line", linewidth=1) +
  stat_summary(fun=mean, geom="point", size=3) +
  stat_summary(fun.data=mean_se, geom="errorbar", width=0.1) +
  labs(title="Interaction Plot", x="Factor A", y="Mean RT (ms)") +
  theme_minimal(12)
```

## 解读

- **平行线** → 无交互
- **交叉线** → 强交互（交叉交互）
- **不平行但不交叉** → 弱交互（ ordinal交互）
- 交互显著时，主效应的解释需谨慎

## 关键参数

| 参数 | 作用 |
|------|------|
| `group=factorB` | 按第二个因素分组 |
| `fun.data=mean_se` | 误差棒用SE |
| `width` | 误差棒宽度(0.1) |
