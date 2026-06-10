# 散点图+回归线 (Scatter + Regression)

## 概述

散点图展示两个连续变量的关系，叠加回归线和置信带。

## 何时使用

| 条件 | 说明 |
|------|------|
| 变量 | 两个连续变量 |
| 目标 | 展示线性关系、个体差异 |
| 额外 | 可加颜色/形状区分第三变量 |

## R 代码

```r
ggplot(data, aes(x=anxiety, y=stroop_rt)) +
  geom_point(alpha=0.5, size=2) +
  geom_smooth(method="lm", se=TRUE, color="red") +
  labs(title="Anxiety vs Stroop RT", x="Anxiety Score", y="Stroop RT (ms)") +
  theme_minimal(12)
```

## 解读

- 点均匀散布在回归线两侧 → 线性关系合适
- 漏斗形（方差随X增大） → 异方差,需处理
- 离群点 → 标记被试ID,检查是否合理
