# 密度图 (Density Plot)

## 概述

密度图展示连续变量的平滑分布曲线，适合比较多个条件的分布形状。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 比较分布形状 |
| 用途 | 检查多峰、偏态、组间分布差异 |

## R 代码

```r
ggplot(data, aes(x=rt, fill=condition, color=condition)) +
  geom_density(alpha=0.3) +
  labs(title="RT Distribution by Condition", x="RT (ms)", y="Density") +
  theme_minimal()
```

## 解读

- 单峰对称 → 近似正态
- 右尾长 → 正偏态（RT常见）
- 双峰 → 可能混合了两个过程
- 多组密度不重叠 → 组间差异大

## 关键参数

| 参数 | 作用 |
|------|------|
| `adjust` | 带宽乘数(>1平滑,<1细节多) |
| `alpha` | 透明度(重叠时0.3-0.5) |
| `bw` | 带宽(替代adjust) |
