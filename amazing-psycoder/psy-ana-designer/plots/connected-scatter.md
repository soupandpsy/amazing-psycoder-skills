# 连接散点图 (Connected Scatter Plot)

## 概述

连接散点图将时间序列数据的点用线段连接,同时展示两个变量的关系演变。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 两变量随时间共同变化 |
| 优势 | 展示轨迹,而非仅起点和终点 |

## R 代码

```r
ggplot(data, aes(x=rt, y=accuracy)) +
  geom_path(arrow=arrow(), color="grey70") +
  geom_point(aes(color=time), size=3) +
  scale_color_viridis_c() +
  labs(title="RT-Accuracy Trajectory Over Time") +
  theme_minimal()
```

## vs 普通散点图

连接散点图增加了时间维度(路径方向),展示'如何从A到B'而非仅A和B的位置。

## 关键参数

| 参数 | 作用 |
|------|------|
| `geom_path` | 保持行顺序连接 |
| `arrow()` | 添加箭头指示方向 |
| `scale_color_viridis_c()` | 颜色编码时间 |
