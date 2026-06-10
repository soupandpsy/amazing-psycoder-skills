# 气泡图 (Bubble Chart)

## 概述

气泡图是散点图的扩展,用点的大小表示第三个连续变量。适合展示3个变量的关系。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 3个连续变量的关系 |
| 第三变量 | 用点大小(size)表示 |

## R 代码

```r
ggplot(data, aes(x=rt, y=accuracy, size=sample_size, color=condition)) +
  geom_point(alpha=0.6) +
  scale_size(range=c(1, 10), name="Sample Size") +
  labs(title="RT vs Accuracy by Sample Size") +
  theme_minimal()
```

## 关键参数

| 参数 | 作用 |
|------|------|
| `size` | 映射第三变量的点大小 |
| `scale_size(range=c(a,b))` | 点大小范围 |
| `alpha` | 透明度 |
