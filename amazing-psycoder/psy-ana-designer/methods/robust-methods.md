# 稳健统计方法 (Robust Methods)

## 概述

稳健方法在处理含异常值或重尾分布的数据时比传统方法更可靠,不需要武断地排除数据。

**典型场景**: RT数据含极端慢反应(不能排除——可能是真实认知过程); 小样本且无法验证正态性。

## 方法对照

| 传统方法 | 稳健替代 | R 包 |
|---------|---------|------|
| 均值 | 截尾均值(trimmed mean, 去5-20%) / Winsorized mean | `WRS2` |
| 独立t检验 | Yuen's t-test (trimmed means) | `WRS2::yuen()` |
| 配对t检验 | 配对Yuen或百分位Bootstrap | `WRS2` |
| Pearson相关 | 百分位Bootstrap相关 / Skipped correlation | `WRS2` |
| ANOVA | 稳健ANOVA (trimmed means) | `WRS2::t1way()` |
| 回归 | MM-estimator / Huber M-estimator | `MASS::rlm()` |

## 何时使用

| 条件 | 要求 |
|------|------|
| 数据含异常值且不能排除 | 异常值有理论意义,非实验失误 |
| 分布重尾 | 常见于 RT 数据、生理指标 |
| 小样本无法验证正态性 | n < 30, 正态性检验功效不足 |
| 敏感性分析 | 传统方法与稳健方法结论一致增强信心 |
| 方差齐性不满足 | 稳健方法对方差异质性更宽容 |

## 与排除异常值的对比

排除±2.5SD外的试次是"硬删除",可能丢失信息。稳健方法自动降权极端值,保留更多数据。

## R 代码

```r
# 稳健统计方法示例
library(WRS2)
library(MASS)

# ── 示例数据 ──
set.seed(42)
group1 <- c(rnorm(18, 350, 40), 680, 720)  # RT, 含两个极端慢反应
group2 <- c(rnorm(18, 380, 45), 450, 470)
df <- data.frame(
  rt    = c(group1, group2),
  group = rep(c("A", "B"), each = 20),
  id    = rep(1:20, 2)
)

# ── 1. 截尾均值 ──
mean(group1, trim = 0.20)  # 去掉两端各 20%

# ── 2. Yuen's 独立样本 t 检验 (trimmed means) ──
yuen_result <- yuen(rt ~ group, data = df, tr = 0.20)
print(yuen_result)
# 输出包括: Test statistic (Ty), p-value, trimmed means, 效应量 ξ (xi)

# ── 3. 稳健 ANOVA (trimmed means) ──
t1way_result <- t1way(rt ~ group, data = df, tr = 0.20)
print(t1way_result)

# ── 4. 配对 Yuen ──
yuend(rt ~ group, data = df, tr = 0.20)

# ── 5. 百分位 Bootstrap 相关 ──
x <- rnorm(30)
y <- 0.5 * x + rnorm(30, 0, 1)
y[c(5, 25)] <- c(4.5, -4.0)  # 添加异常值
pbcor_result <- pbcor(x, y, beta = 0.20)
print(pbcor_result)
# 输出包括: Pearson r via bootstrap, p-value, 95% CI

# ── 6. 稳健回归 (MM-estimator) ──
df_reg <- data.frame(x = rnorm(40), y = rnorm(40))
df_reg$y[c(3, 30)] <- c(8, -7)  # 异常值
mm_fit <- MASS::rlm(y ~ x, data = df_reg, method = "MM")
summary(mm_fit)

# ── 效应量: 稳健 Cohen's d (Algina et al., 2005) ──
# 基于 trimmed means 和 Winsorized 方差
akp.effect <- function(m1, m2, s1, s2, n1, n2, tr = 0.20) {
  h   <- floor(tr * n1)
  g   <- n1 - 2 * h
  sw1 <- sqrt(((n1 - 1) * s1^2) / (g - 1))
  sw2 <- sqrt(((n2 - 1) * s2^2) / (g - 1))
  sp  <- sqrt(((n1 - 1) * sw1^2 + (n2 - 1) * sw2^2) / (n1 + n2 - 2))
  (0.642 + tr) * (m1 - m2) / sp  # 校正系数
}
```

## 报告

APA 7th 格式报告示例:

> 因反应时数据呈重尾分布且含极端慢反应(无法以实验失误为由排除), 采用稳健统计分析。对两组截尾均值(trim = 20%)进行 Yuen's 独立样本 t 检验, 结果显示组 A (M<sub>t</sub> = 367.4) 反应显著快于组 B (M<sub>t</sub> = 404.8), T<sub>y</sub> = 2.84, &xi; = 0.42, p = .009, 95% CI [0.11, 0.73]。效应量 &xi; (稳健 Cohen's d) 表示中等效应。作为敏感性分析, 传统独立样本 t 检验结论一致 (t(38) = 2.51, p = .017), 增强了结论可靠性。

## 备选方法

- [传统参数检验](traditional-parametric.md) — 当正态性和方差齐性满足时
- [非参数检验](nonparametric.md) — 转为秩次, 对异常值相对稳健
- [Bootstrap 方法](bootstrap.md) — 不依赖分布假设, 适合小样本
- [混合效应模型](mixed-models.md) — 处理层级数据时比剔除聚合更优
- [贝叶斯稳健回归](bayesian-robust.md) — 使用 Student-t 似然估计替代正态假设


