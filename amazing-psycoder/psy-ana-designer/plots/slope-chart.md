# 斜率图 (Slope Chart)

## 概述

斜率图用多条线段连接两个时间点的值,线的斜率直观展示变化方向和幅度。比哑铃图更简洁,适合同时展示大量被试的变化。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 两时间点,多个体/项目 |
| 优势 | 快速识别"谁变最多" |

## R 代码

```r
ggplot(data, aes(x=time, y=value, group=subject_id)) +
  geom_line(aes(color=change_direction), alpha=0.6, linewidth=0.8) +
  geom_point(size=2) +
  scale_color_manual(values=c("increase"="red","decrease"="blue","stable"="grey")) +
  labs(title="Individual Changes", x="Time", y="Score") +
  theme_minimal()
```

## 解读

- 陡峭上升线=大幅增加
- 陡峭下降线=大幅减少
- 平线=无变化
- 颜色编码变化方向→快速识别异常模式

## 关键参数

| 参数 | 作用 |
|------|------|
| `group` | 按个体分组 |
| `color` | 按变化方向着色 |
| `alpha` | 透明度(多线时降低) |
