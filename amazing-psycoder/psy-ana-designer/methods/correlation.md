# 相关分析 (Correlation)

## 概述

相关分析测量两个连续变量之间的线性关联强度。

**典型场景**: RT 与年龄的关系, 两种任务表现的相关, 问卷各维度间的关联。

## 何时使用

| 条件 | 要求 |
|------|------|
| 变量类型 | 两个连续变量（或有序变量，用 Spearman/Kendall） |
| 关系形态 | 线性关系（检查散点图；非线性时考虑曲线相关或转换） |
| 正态性 | Pearson 要求双变量正态；Spearman/Kendall 无此要求 |
| 独立性 | 每对观测独立（重复测量数据用 rmcorr） |
| 极端值 | Pearson 对极端值敏感；存在极端值时优先 Spearman |
| 样本量 | 无严格下限，但 n < 20 时 CI 很宽；小样本优先 Kendall τ |

## 方法选择

| 方法 | 何时用 | 假设 |
|------|--------|------|
| Pearson r | 两变量连续正态 | 线性关系,无极端值 |
| Spearman ρ | 非正态/有序变量 | 单调关系 |
| Kendall τ | 小样本,多ties | 单调关系 |

## 效应量

| r 值 | 解释 |
|------|------|
| 0.1 | 小 |
| 0.3 | 中 |
| 0.5 | 大 |

r² = 一个变量可被另一个变量解释的方差比例。

## R 代码

```r
# 加载必要包
library(ggplot2)

# 示例数据：模拟被试年龄(age)与反应时(RT)的关系
set.seed(42)
n <- 100
age <- rnorm(n, mean = 35, sd = 12)
RT  <- 500 - 3 * age + rnorm(n, mean = 0, sd = 80)
d   <- data.frame(age, RT)

# -------------------- 1. 描述统计 --------------------
cat("年龄:", round(mean(d$age), 1), "±", round(sd(d$age), 1), "(M ± SD)\n")
cat("RT:", round(mean(d$RT), 1), "±", round(sd(d$RT), 1), "(M ± SD)\n")

# -------------------- 2. 散点图 --------------------
ggplot(d, aes(x = age, y = RT)) +
  geom_point(alpha = 0.5) +
  geom_smooth(method = "lm", se = TRUE, color = "steelblue") +
  labs(title = "年龄与反应时的关系",
       x = "年龄 (岁)", y = "反应时 (ms)") +
  theme_minimal()

# -------------------- 3. 正态性检验 --------------------
# Pearson 的前提：检验双变量正态性
shapiro.test(d$age)
shapiro.test(d$RT)

# -------------------- 4. Pearson 相关 --------------------
res <- cor.test(d$age, d$RT, method = "pearson")
cat("\nPearson r =", round(res$estimate, 3),
    ", t(", res$parameter, ") = ", round(res$statistic, 2),
    ", p = ", format.pval(res$p.value, digits = 3),
    "\n95% CI: [", round(res$conf.int[1], 3), ", ", round(res$conf.int[2], 3), "]\n", sep = "")

# -------------------- 5. 效应量 --------------------
# r 本身就是效应量；同时报告 r²（决定系数）
r <- res$estimate
cat("r² =", round(r^2, 3), "→", round(r^2 * 100, 1), "% 的 RT 方差可被 age 解释\n")

# -------------------- 6. Spearman 相关（非参数备选） --------------------
res_sp <- cor.test(d$age, d$RT, method = "spearman")
cat("\nSpearman ρ =", round(res_sp$estimate, 3),
    ", p =", format.pval(res_sp$p.value, digits = 3), "\n")

# -------------------- 7. Kendall τ（小样本/多ties时推荐） --------------------
res_kt <- cor.test(d$age, d$RT, method = "kendall")
cat("Kendall τ =", round(res_kt$estimate, 3),
    ", p =", format.pval(res_kt$p.value, digits = 3), "\n")

# -------------------- 8. 多变量相关矩阵 --------------------
# 假设有多个变量的情况
d_multi <- data.frame(
  age   = age,
  RT    = RT,
  score = 60 + 0.5 * age + rnorm(n, 0, 10)
)
cor_matrix <- cor(d_multi, method = "pearson")
cor_pvals <- psych::corr.test(d_multi)$p
print(round(cor_matrix, 3))

# -------------------- 9. 重复测量相关 (rmcorr) --------------------
# 当每个被试有多行数据时，用 rmcorr 替代普通 Pearson
# library(rmcorr)
# rmcorr_result <- rmcorr(participant = subject_id, measure1 = var1, measure2 = var2, dataset = df)
```

## APA 报告格式

> Reaction time was negatively correlated with age, r(98)=-.34, p<.001, 95% CI [-.50, -.16].

## 注意事项

- 相关≠因果
- 需检查散点图确认线性关系(非线性时r可能接近0)
- 极端值对r影响巨大
- 被试内重复测量数据不能用普通 Pearson r——每个被试多行,违反独立性。用 **rmcorr (repeated measures correlation)** 替代

## 备选方法

- [简单线性回归](regression.md) — 需要明确区分预测变量和结果变量时
- [rmcorr（重复测量相关）](rmcorr.md) — 被试内重复测量设计的相关分析
- [偏相关](partial-correlation.md) — 需要控制第三个变量时
- [多项式相关/曲线回归](curve-regression.md) — 关系为非线性时
- [Bland-Altman 分析](bland-altman.md) — 评估两种测量方法的一致性而非关联强度
- [信度分析（Cronbach's α / ICC）](reliability.md) — 评估测量工具内部一致性或评分者一致性

