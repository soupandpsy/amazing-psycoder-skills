# 非参数检验 (Nonparametric Tests)

## 概述

非参数检验不假设数据分布,用于数据严重偏离正态且转换无效的情况。

## 方法对照

| 参数方法 | 非参数替代 | 检验的假设 |
|---------|----------|----------|
| 配对t检验 | Wilcoxon符号秩 | 差值的对称分布 |
| 独立t检验 | Mann-Whitney U | 两组分布形状相似 |
| 被试内ANOVA | Friedman | 排序一致性 |
| 被试间ANOVA | Kruskal-Wallis | 各组分布形状相似 |

## 何时使用

| 条件 | 要求 |
|------|------|
| 正态性检验 | Shapiro-Wilk p < .001，QQ图明显弯曲 |
| 数据转换后仍非正态 | log、sqrt、Box-Cox 转换后仍不满足正态性 |
| 小样本 | 每条件 n < 20 且不能假设正态分布 |
| 极端异常值 | 存在极端异常值且不能从数据中排除 |

## 代价

- 统计效力低于参数方法 (正态数据时约95%)
- 不能直接估计效应量的大小 (只能判断"是否有差异")
- 较难扩展到复杂设计 (多因素、协变量)

## R 代码

```r
library(rstatix)
library(ggplot2)

# ── 示例数据 ──────────────────────────────────────────
set.seed(42)
df_long <- data.frame(
  id      = rep(1:20, times = 2),
  cond    = rep(c("pre", "post"), each = 20),
  score   = c(rlnorm(20, 3, 0.5), rlnorm(20, 3.2, 0.5))
)

df_indep <- data.frame(
  group = rep(c("control", "treatment"), each = 15),
  value = c(rlnorm(15, 3, 0.6), rlnorm(15, 3.6, 0.6))
)

# ── 1. 配对 Wilcoxon 符号秩检验 ──────────────────────
wilcox_res <- wilcox_test(df_long, score ~ cond, paired = TRUE)
wilcox_eff <- df_long %>%
  wilcox_effsize(score ~ cond, paired = TRUE)
wilcox_res
wilcox_eff   # r = Z / sqrt(N)

# ── 2. Mann-Whitney U 检验 (独立两组) ────────────────
mwu_res <- wilcox_test(df_indep, value ~ group)
mwu_eff <- df_indep %>%
  wilcox_effsize(value ~ group)
mwu_res
mwu_eff

# ── 3. Friedman 检验 (被试内多条件) ──────────────────
df_fried <- data.frame(
  id    = rep(1:15, times = 3),
  cond  = rep(c("A", "B", "C"), each = 15),
  score = c(rlnorm(15, 3, 0.4), rlnorm(15, 3.5, 0.4), rlnorm(15, 3.9, 0.4))
)
fried_res <- friedman_test(df_fried, score ~ cond | id)
fried_eff <- df_fried %>%
  friedman_effsize(score ~ cond | id)
fried_res
fried_eff     # Kendall's W

# 事后两两比较 (配对 Wilcoxon + Bonferroni 校正)
pwc_fried <- df_fried %>%
  pairwise_wilcox_test(score ~ cond, paired = TRUE,
                       p.adjust.method = "bonferroni")
pwc_fried

# ── 4. Kruskal-Wallis 检验 (被试间多组) ──────────────
df_kw <- data.frame(
  group = rep(c("G1", "G2", "G3"), each = 12),
  value = c(rlnorm(12, 3, 0.5), rlnorm(12, 3.4, 0.5), rlnorm(12, 4, 0.5))
)
kw_res <- kruskal_test(df_kw, value ~ group)
kw_eff <- df_kw %>%
  kruskal_effsize(value ~ group)
kw_res
kw_eff        # eta²[H] (epsilon-squared)

# 事后两两比较 (Dunn 检验 + Bonferroni)
pwc_kw <- df_kw %>%
  dunn_test(value ~ group, p.adjust.method = "bonferroni")
pwc_kw

# ── 可视化 ───────────────────────────────────────────
ggplot(df_kw, aes(x = group, y = value)) +
  geom_boxplot(outlier.shape = NA) +
  geom_jitter(width = 0.15, alpha = 0.6) +
  labs(title = "Kruskal-Wallis: 各组分布比较",
       x = "组别", y = "观测值") +
  theme_minimal()
```

## 报告格式 (APA 7th)

**Wilcoxon 符号秩检验示例：**

> A Wilcoxon signed-rank test indicated that post-test scores (Mdn = 28.5) were significantly higher than pre-test scores (Mdn = 19.2), V = 345, p = .003, r = .66.

**Mann-Whitney U 检验示例：**

> A Mann-Whitney U test revealed that the treatment group (Mdn = 45.3, n = 30) scored significantly higher than the control group (Mdn = 32.1, n = 28), U = 287, p = .021, r = .42.

**Friedman 检验示例：**

> A Friedman test showed a significant difference among the three conditions, χ²(2) = 12.34, p = .002, Kendall's W = .41. Post-hoc pairwise Wilcoxon signed-rank tests with Bonferroni correction revealed significant differences between condition A and C (p = .004), but not between A and B (p = .312).

**Kruskal-Wallis 检验示例：**

> A Kruskal-Wallis H test indicated a significant effect of group on performance, H(2) = 11.56, p = .003, ε² = .26. Dunn's post-hoc tests with Bonferroni correction showed that G3 (Mdn = 52.0) scored significantly higher than G1 (Mdn = 31.5, p = .002). No other comparisons reached significance (all p > .05).

## 备选方法

- [稳健统计方法](robust.md) — 当数据含异常值但不想完全转向秩次检验时，可使用截尾均值或 M 估计
- [Bootstrap](bootstrap.md) — 重抽样方法，不依赖分布假设，适用于置信区间估计
- [数据转换](transformation.md) — 若轻微偏离正态，先尝试 log / sqrt / Box-Cox 转换再使用参数方法
- [贝叶斯方法](bayesian.md) — 可容纳非正态分布，直接对参数的后验分布建模，不对数据分布做严格假设
