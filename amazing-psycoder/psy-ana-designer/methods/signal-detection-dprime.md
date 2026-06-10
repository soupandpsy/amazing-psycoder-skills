# 信号检测论 (Signal Detection Theory / d')

## 概述

信号检测论将反应分解为**辨别力(d')**和**反应偏向(c)**两个独立指标。解决准确率指标混淆辨别力和偏向的问题。

**典型场景**: Go/No-go、N-back、记忆再认等范式中,将准确率分解为d'和c。

## 何时使用

| 条件 | 要求 |
|------|------|
| 实验设计 | 包含信号试次(信号出现)和噪音试次(信号未出现)的检测任务 |
| 因变量 | 二分类反应("是"/"否" 或 "信号"/"噪音") |
| 理论基础 | 信号检测论框架, 需计算击中率(Hit)和虚报率(FA) |
| 样本量 | 每个条件至少20试次, 以保证Hit率和FA率估计稳定 |
| 数据前提 | 可计算击中率和虚报率的分类数据; 极端值(0或1)需校正 |

## 关键指标

| 指标 | 公式 | 含义 |
|------|------|------|
| **d' (d-prime)** | z(Hit) - z(FA) | 辨别力:区分信号和噪音的能力 |
| **c (criterion)** | -0.5*(z(Hit)+z(FA)) | 反应偏向: c>0保守, c<0宽松 |

- Hit = 信号出现时的"是"反应率
- FA = 信号未出现时的"是"反应率(虚报)

## 为什么用d'而非准确率

两个被试准确率都是85%,但:
- A: Hit=90%, FA=20% → d'=2.08, 偏向宽松
- B: Hit=85%, FA=5% → d'=2.76, 偏向保守

准确率相同但d'差异大。单纯用准确率会混淆辨别力和反应偏向。

## 校正极端值

Hit或FA为0或1时,z值无穷大。常用校正:
- **log-linear**: Hit=(#Hit+0.5)/(#Signal+1)
- **1/(2N)**: 极值替换为 1/(2×试次数)

## R 代码

```r
# 信号检测论: d' 和 c 的计算
library(tidyverse)
library(effsize)  # 用于 Cohen's d

# ---- 示例数据 ----
# 每个被试的 Hit 和 FA 来自实验原始反应数据
df <- tibble(
  subject   = 1:30,
  group     = rep(c("ADHD", "Control"), each = 15),
  n_signal  = 50,   # 信号试次总数
  n_noise   = 50,   # 噪音试次总数
  n_hit     = c(sample(30:45, 15, replace = TRUE), sample(35:48, 15, replace = TRUE)),
  n_fa      = c(sample(10:25, 15, replace = TRUE), sample(3:12,  15, replace = TRUE))
)

# ---- 核心函数: 计算 d' 和 c ----
calc_dprime <- function(hit, fa, n_signal, n_noise, correction = "loglinear") {
  # Log-linear 校正避免极端值
  if (correction == "loglinear") {
    hit_rate <- (hit + 0.5) / (n_signal + 1)
    fa_rate  <- (fa  + 0.5) / (n_noise  + 1)
  } else if (correction == "halfN") {
    half_hit <- 1 / (2 * n_signal)
    half_fa  <- 1 / (2 * n_noise)
    hit_rate <- pmax(pmin(hit / n_signal, 1 - half_hit), half_hit)
    fa_rate  <- pmax(pmin(fa  / n_noise,  1 - half_fa),  half_fa)
  } else {
    hit_rate <- hit / n_signal
    fa_rate  <- fa  / n_noise
  }

  d_prime <- qnorm(hit_rate) - qnorm(fa_rate)
  c_bias  <- -0.5 * (qnorm(hit_rate) + qnorm(fa_rate))

  tibble(hit_rate, fa_rate, d_prime, c_bias)
}

# ---- 批量计算 ----
results <- df |>
  mutate(calc_dprime(n_hit, n_fa, n_signal, n_noise)) |>
  select(subject, group, hit_rate, fa_rate, d_prime, c_bias)

# ---- 组水平描述统计 ----
results |>
  group_by(group) |>
  summarise(
    n            = n(),
    mean_dprime  = mean(d_prime),
    sd_dprime    = sd(d_prime),
    mean_c       = mean(c_bias),
    sd_c         = sd(c_bias),
    .groups      = "drop"
  )

# ---- 独立样本 t 检验 + 效应量 ----
# d' 组间比较
t_dprime <- t.test(d_prime ~ group, data = results)
print(t_dprime)

cohens_d_dprime <- cohen.d(d_prime ~ group, data = results)
print(cohens_d_dprime)

# c 组间比较
t_c <- t.test(c_bias ~ group, data = results)
print(t_c)

# ---- 可视化 ----
ggplot(results, aes(x = group, y = d_prime, fill = group)) +
  geom_boxplot(outlier.shape = NA, alpha = 0.5) +
  geom_jitter(width = 0.1, size = 2) +
  labs(
    title  = "信号检测论: 辨别力 (d') 组间比较",
    y      = "d' (辨别力)",
    x      = NULL
  ) +
  theme_minimal()
```

## 报告

**APA 7th 报告模板 (中文)**：

> 采用信号检测论分析辨别力与反应偏向。ADHD组辨别力显著低于对照组（d' = 1.45 ± 0.38 vs. 2.32 ± 0.41），独立样本 t 检验结果显著，t(58) = 4.21, p < .001, Cohen's d = 1.10, 95% CI [0.82, 1.38]。两组在反应偏向上无显著差异（c = 0.12 ± 0.15 vs. 0.08 ± 0.17），t(58) = 0.76, p = .450。

**APA 7th Report Template (English)**:

> Signal detection analysis was conducted to separate sensitivity (d') from response bias (c). The ADHD group showed significantly lower sensitivity (d' = 1.45, SD = 0.38) compared to the control group (d' = 2.32, SD = 0.41), t(58) = 4.21, p < .001, Cohen's d = 1.10, 95% CI [0.82, 1.38]. No significant group difference was found in response criterion (c = 0.12, SD = 0.15 vs. c = 0.08, SD = 0.17), t(58) = 0.76, p = .450.

**报告要点**：
- 同时报告 d' 和 c 的均值、标准差
- 报告推断统计（t值、自由度、p值）及效应量（Cohen's d, 95% CI）
- 若使用校正方法（log-linear / 1/(2N)），应在方法部分说明

## 备选方法

- [ROC分析 (Receiver Operating Characteristic)](../methods/roc-analysis.md) — 信号检测论的扩展，适用于多水平置信度评定
- [线性混合模型 (Linear Mixed Model)](../methods/linear-mixed-model.md) — 当需同时建模被试和项目随机效应时
- [逻辑混合模型 (Logistic GLMM)](../methods/logistic-mixed-model.md) — 当自变量为分类或连续变量时，直接建模"是/否"反应概率
- A' (A-prime) — 非参数信号检测指标，不假设等方差正态分布（在非参数检验中涉及）
