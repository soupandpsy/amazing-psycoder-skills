# 环形条形图 (Circular Barplot)

## 概述

环形条形图将条形排列在圆形坐标系中,适合展示大量类别的排序比较。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 多类别排序(>10类),需要醒目展示 |
| ⚠️ | 不适合精确读数(角度难比较) |

## R 代码

```r
ggplot(data, aes(x=reorder(label, value), y=value)) +
  geom_bar(stat="identity", fill="#69b3a2", alpha=0.8) +
  coord_polar(start=0) +
  ylim(-max(data$value)*0.2, max(data$value)) +
  theme_void()
```

## vs 普通条形图

环形条形图美观但精确度低。推荐只在展示类别的**相对排名**(而非精确值)时使用。

## 关键参数

| 参数 | 作用 |
|------|------|
| `coord_polar(start=0)` | 起始角度 |
| `ylim` | Y轴范围(需包含负值以留空中心) |
