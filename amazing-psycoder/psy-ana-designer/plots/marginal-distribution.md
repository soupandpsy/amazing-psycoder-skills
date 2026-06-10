# 边缘分布图 (Marginal Distribution)

## 概述

在散点图的X轴和Y轴边缘添加直方图或密度图,同时展示两变量关系和各自的分布。是APA推荐的高信息密度图表。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 两连续变量的相关+分布 |
| 优势 | 一张图展示关系+各自分布 |

## R 代码

```r
library(ggExtra)
p <- ggplot(data, aes(x=anxiety, y=stroop_rt)) +
  geom_point(alpha=0.5, size=2, color="#69b3a2") +
  geom_smooth(method="lm", se=TRUE, color="red") +
  theme_minimal()
ggMarginal(p, type="density", fill="#69b3a2", alpha=0.5)
# type="histogram" for histograms
```

## 解读

- 主图: 两变量关系(散点+回归线)
- 顶部: X变量分布
- 右侧: Y变量分布
- 分布偏离正态→考虑转换或非参数方法
