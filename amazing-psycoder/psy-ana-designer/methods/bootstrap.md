# Bootstrap 方法

## 概述

Bootstrap 通过从原始数据中**有放回重采样**来估计统计量的抽样分布。不需要假设理论分布,适用范围极广。

**典型场景**: 效应量的置信区间、中介效应的间接效应检验、非标准统计量的推断。

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计 | 被试内或被试间 |
| DV | 连续或分类 |
| 用途 | 效应量CI、中介间接效应、非标准统计量推断 |
| 重采样次数 | ≥5000（报告CI时） |
| 重采样单位 | 需匹配分析单位（被试内→重采样被试） |

## 类型

| 类型 | 方法 | 适用 |
|------|------|------|
| 非参数Bootstrap | 直接从数据重采样 | 通用 |
| 参数Bootstrap | 从拟合的分布采样 | 样本量小但有模型 |
| 残差Bootstrap | 重采样残差 | 回归模型 |

## Bootstrap CI 方法

| 方法 | 特点 |
|------|------|
| Percentile | 简单,非对称可接受 |
| BCa (Bias-Corrected) | **推荐**,校正偏差和偏度 |
| Studentized | 最准确但需SE估计 |

## R 代码

```r
library(boot)

# ==== 1. 配对设计: Cohen's d 的 Bootstrap CI ====
# 对差异分重采样以保留被试内配对结构
set.seed(123)
n <- 30
rt_congruent    <- rnorm(n, mean = 450, sd = 80)
rt_incongruent  <- rnorm(n, mean = 520, sd = 95)
diff_scores     <- rt_incongruent - rt_congruent

boot_d <- function(d, indices) {
  mean(d[indices]) / sd(d[indices])
}

boot_res <- boot(diff_scores, statistic = boot_d, R = 5000)
boot_res
boot.ci(boot_res, type = "perc")   # Percentile CI
boot.ci(boot_res, type = "bca")    # BCa CI (推荐)

# ==== 2. 独立组: Cohen's d 的 Bootstrap CI ====
library(effsize)
set.seed(42)
g1 <- rnorm(35, mean = 10, sd = 3)
g2 <- rnorm(35, mean = 12, sd = 3)
n1 <- length(g1); n2 <- length(g2)

d_boot <- replicate(5000, {
  s1 <- sample(g1, n1, replace = TRUE)
  s2 <- sample(g2, n2, replace = TRUE)
  cohen.d(s1, s2)$estimate
})

cat(sprintf(
  "Cohen's d = %.2f, 95%% CI [%.2f, %.2f]\n",
  cohen.d(g1, g2)$estimate,
  quantile(d_boot, 0.025),
  quantile(d_boot, 0.975)
))

# ==== 3. 中介效应 Bootstrap (间接效应 a×b) ====
library(lavaan)

set.seed(1)
n_obs <- 200
X <- rnorm(n_obs)
M <- 0.5 * X + rnorm(n_obs, sd = 0.8)
Y <- 0.3 * M + 0.4 * X + rnorm(n_obs, sd = 0.7)
med_df <- data.frame(X, M, Y)

model <- '
  M ~ a*X
  Y ~ b*M + cp*X
  indirect := a * b
  total    := a * b + cp
'

fit <- sem(model, data = med_df, se = "bootstrap", bootstrap = 5000)
parameterEstimates(fit, boot.ci.type = "bca.simple", level = 0.95)
```

## 报告

### APA 7th 报告格式 (均值差异)

> 采用 Bootstrap 方法(5000 次重采样)估计配对均值差异的效应量。结果显示，Cohen's d = 0.62, 95% BCa CI = [0.12, 1.10]，置信区间不包含零，表明两条件间差异具有中等以上的效应量。

### APA 7th 报告格式 (中介分析)

> 采用 Bootstrap 方法(5000 次重采样)检验间接效应。结果显示，ab = 0.28, 95% BCa CI = [0.11, 0.47]，置信区间不包含零，表明 M 在 X 与 Y 之间的中介效应显著。

## 注意事项

- 重采样次数≥5000 (报告CI时)
- 重采样单位需匹配分析单位(被试内→重采样被试,非试次)
- Bootstrap不能挽救坏数据——仍需要合理的样本量和实验设计

## 备选方法

- [置换检验](/methods/permutation-test) — 适用于假设检验而非区间估计
- [稳健回归](/methods/robust-regression) — 处理异常值时替代传统回归
- [贝叶斯方法](/methods/bayesian-analysis) — 提供整个后验分布而非点估计区间


