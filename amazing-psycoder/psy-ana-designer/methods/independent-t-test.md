# 独立 t 检验 (Independent Samples t-test)

## 概述

独立 t 检验用于比较两组独立样本的均值差异。在心理学中用于被试间设计。

**典型场景**：实验组 vs 控制组、A组 vs B组（不同被试）、不同人群比较。

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计 | 被试间 (between-subjects) |
| 条件数 | 恰好 2 个 |
| DV | 连续变量 |
| 数据要求 | 每组数据近似正态，方差齐或不齐 |

## 假设与检验

1. **独立性**：两组被试互相独立
2. **正态性**：每组数据近似正态。Shapiro-Wilk 分组检验
3. **方差齐性**：Levene检验。p>0.05→方差齐→Student's t; p<0.05→方差不齐→Welch's t

**Welch t-test 是默认推荐**：不假设方差齐性，自由度校正。大多数情况下 Welch 比 Student's t 更安全。

## 效应量：Cohen's d

| 大小 | d |
|------|-----|
| 小 | 0.2 |
| 中 | 0.5 |
| 大 | 0.8 |

Cohen's d = (M1-M2) / pooled_SD。独立设计中 d 是标准化均值差。

## R 代码

```r
# 独立 t 检验 - 完整分析流程
library(effectsize)   # cohens_d()
library(car)          # leveneTest()

# 示例数据：实验组 vs 控制组
exp_group  <- c(88, 92, 85, 90, 87, 93, 89, 91, 86, 94, 90, 88)
ctrl_group <- c(78, 80, 82, 79, 81, 77, 83, 80, 78, 82, 79, 81)
n_exp  <- length(exp_group)
n_ctrl <- length(ctrl_group)

# 描述统计
cat(sprintf("实验组: M = %.2f, SD = %.2f, n = %d\n",
  mean(exp_group), sd(exp_group), n_exp))
cat(sprintf("控制组: M = %.2f, SD = %.2f, n = %d\n",
  mean(ctrl_group), sd(ctrl_group), n_ctrl))

# 1. 正态性检验 (Shapiro-Wilk, 分组)
shap_exp  <- shapiro.test(exp_group)
shap_ctrl <- shapiro.test(ctrl_group)
cat(sprintf("\n正态性检验:\n  实验组 W = %.3f, p = %.3f\n  控制组 W = %.3f, p = %.3f\n",
  shap_exp$statistic, shap_exp$p.value,
  shap_ctrl$statistic, shap_ctrl$p.value))

# 2. 方差齐性检验 (Levene)
df_long <- data.frame(
  value = c(exp_group, ctrl_group),
  group = factor(rep(c("exp", "ctrl"), c(n_exp, n_ctrl)))
)
lev <- leveneTest(value ~ group, data = df_long)
cat(sprintf("\nLevene 方差齐性检验: F(1,%d) = %.3f, p = %.3f\n",
  lev$Df[2], lev$`F value`[1], lev$`Pr(>F)`[1]))

# 3. 独立 t 检验（Welch 默认，不假设方差齐性）
t_result <- t.test(exp_group, ctrl_group, var.equal = FALSE)
cat(sprintf("\nWelch t-test:\n  t(%.2f) = %.3f, p = %.4f\n",
  t_result$parameter, t_result$statistic, t_result$p.value))
cat(sprintf("  均值差 = %.3f, 95%% CI [%.3f, %.3f]\n",
  t_result$estimate[1] - t_result$estimate[2],
  t_result$conf.int[1], t_result$conf.int[2]))

# 4. 效应量 Cohen's d
d_result <- cohens_d(exp_group, ctrl_group)
cat(sprintf("\nCohen's d = %.3f, 95%% CI [%.3f, %.3f]\n",
  d_result$Cohens_d, d_result$CI_low, d_result$CI_high))
```

## APA 7th 报告格式

> An independent-samples t-test compared the experimental group (M=520, SD=95) and control group (M=450, SD=80). Results: t(58)=3.15, p=.003, Cohen's d=0.81, 95% CI [0.38,1.24].

## 备选方法
- **Mann-Whitney U**: 非正态
- **Welch's ANOVA**: 三组+
