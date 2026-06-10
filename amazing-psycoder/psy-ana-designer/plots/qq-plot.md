# QQ 图 (Quantile-Quantile Plot)

## 概述

QQ图比较数据分位数与理论正态分布分位数。点落在对角线上=数据正态。是正态性检验的视觉辅助。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 正态性假设检验 |
| 分组 | 按条件分面 |
| 配合 | Shapiro-Wilk检验值 |

## R 代码

```r
ggplot(data, aes(sample=rt)) +
  geom_qq() + geom_qq_line(color="red") +
  facet_wrap(~condition) +
  labs(title="Q-Q Plots by Condition") +
  theme_minimal()
```

## 解读

- 点紧密贴合对角线 → 正态 ✓
- 两端偏离对角线（上翘/下垂）→ 重尾分布
- S形偏离 → 偏态分布
- 一端大幅偏离 → 异常值

## 关键参数

| 参数 | 作用 |
|------|------|
| `sample=var` | 检验的变量 |
| `geom_qq_line(color='red')` | 参考对角线 |
| `facet_wrap(~group)` | 分组分面 |
