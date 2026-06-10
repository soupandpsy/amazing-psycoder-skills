# 哑铃图 (Dumbbell Chart)

## 概述

哑铃图用线段连接两点的值,两端用圆点标记。非常适合展示前后变化或两组比较,尤其当需要同时展示多个项目的比较时。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 前后测比较,两组均值比较(多项) |
| 目标 | 展示变化幅度和方向 |

## R 代码

```r
library(ggalt)
ggplot(data, aes(x=pre, xend=post, y=subject)) +
  geom_dumbbell(size=2, color="#e3e2e1",
                colour_x="#5b8124", colour_xend="#bad744",
                dot_guide=TRUE, dot_guide_size=0.25) +
  labs(title="Pre-Post Change", x="Score", y="Subject") +
  theme_minimal()
```

## 解读

- 线长=变化幅度
- 左端点=前测,右端点=后测
- 颜色翻转(左>右)=分数下降
- 多条线平行=变化一致;分散=个体差异大

## 关键参数

| 参数 | 作用 |
|------|------|
| `size` | 线宽 |
| `colour_x`/`colour_xend` | 起终点颜色 |
| `dot_guide` | TRUE=加纵向虚线引导 |
