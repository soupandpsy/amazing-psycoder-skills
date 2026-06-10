# 直方图 (Histogram)

## 概述

直方图将连续变量分箱计数,用柱高表示频率。是检查单变量分布的基础工具。

## 何时使用

| 条件 | 说明 |
|------|------|
| 场景 | 单变量分布检查 |
| DV | 连续变量 |
| 目标 | 判断偏态、多峰、异常值 |

## R 代码

```r
# 基础直方图
ggplot(data, aes(x=rt)) +
  geom_histogram(bins=30, fill="#69b3a2", color="#e9ecef", alpha=0.9) +
  labs(title="RT Distribution", x="RT (ms)", y="Count") +
  theme_minimal()

# 添加均值线
ggplot(data, aes(x=rt)) +
  geom_histogram(bins=30, fill="#69b3a2", alpha=0.8) +
  geom_vline(aes(xintercept=mean(rt)), color="red", linetype="dashed", linewidth=1) +
  labs(title="RT Distribution with Mean", x="RT (ms)", y="Count") +
  theme_minimal()

# 分组直方图 (分面)
ggplot(data, aes(x=rt, fill=condition)) +
  geom_histogram(bins=30, alpha=0.7, position="identity") +
  facet_wrap(~condition, ncol=1) +
  scale_fill_brewer(palette="Set2") +
  labs(title="RT by Condition", x="RT (ms)", y="Count") +
  theme_minimal()

# 分组直方图 (重叠)
ggplot(data, aes(x=rt, fill=condition)) +
  geom_histogram(bins=30, alpha=0.5, position="identity") +
  scale_fill_brewer(palette="Set2") +
  labs(title="RT Distribution Overlay", x="RT (ms)") +
  theme_minimal()
```

## 关键参数

| 参数 | 作用 | 建议 |
|------|------|------|
| `bins` | 分箱数 | 30-50(试次数据),太少=丢信息,太多=噪声 |
| `binwidth` | 箱宽 | 替代bins,更精确控制 |
| `fill` | 填充色 | viridis/brewer色盲友好 |
| `color` | 边框色 | 白色或浅灰 |
| `alpha` | 透明度 | 重叠时0.5 |
| `position` | 位置 | "identity"(重叠)/"dodge"(并排) |

## 解读

- 对称钟形 → 近似正态
- 右尾长 → 正偏态(RT常见)
- 左尾长 → 负偏态
- 双峰 → 可能混合两个过程
