# 配对 t 检验 (Paired Samples t-test)

## 概述

配对 t 检验用于比较同一组被试在两种条件下的均值差异，是心理学实验中最常用的统计方法。

**典型场景**：Stroop 一致 vs 不一致 RT、干预前后成绩对比。

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计 | 被试内 (within-subjects) |
| 条件数 | 恰好 2 个 |
| DV | 连续变量 (RT/分数/评分) |
| 数据要求 | 差值近似正态 |

## 假设与检验

1. **差值正态性**：两种条件的差值服从正态分布。注意不是原始数据正态，是**差值**正态
2. **无极端异常值**：极端差值会严重扭曲 t 值和效应量

R: `shapiro.test(diff)`  Python: `scipy.stats.shapiro(diff)`

**违反时**：轻度非正态→t检验对n>30稳健；严重非正态→Wilcoxon符号秩检验。

## 效应量：Cohen's d_z

| 大小 | d_z |
|------|-----|
| 小 | 0.2 |
| 中 | 0.5 |
| 大 | 0.8 |

d_z = 均值差 / 差值的SD。配对设计中推荐 d_z 而非 d_av——d_z 反映被试内效应一致性，通常大于 d_av。Stroop 典型 d_z≈0.4-0.6。

R: `effectsize::repeated_measures_d(dv ~ cond \| subject, data)`
Python: `pingouin.compute_effsize(x, y, paired=True, eftype='cohen')`

## 样本量参考 (80% power)

| d_z | 所需被试 |
|-----|---------|
| 0.2 | ~200 |
| 0.5 | ~34 |
| 0.8 | ~15 |

## R 代码

```r
# 加载必要包
library(tidyverse)
library(effectsize)
library(ggdist)

# 模拟 Stroop 实验数据 (一致 vs 不一致)
set.seed(42)
n <- 30
df_wide <- tibble(
  id          = 1:n,
  congruent   = rnorm(n, mean = 450, sd = 80),
  incongruent = rnorm(n, mean = 520, sd = 95)
)

# 转为长格式
df <- df_wide |>
  pivot_longer(-id, names_to = "condition", values_to = "rt") |>
  mutate(condition = factor(condition, levels = c("congruent", "incongruent")))

# 1. 配对 t 检验
t_res <- t.test(rt ~ condition, data = df, paired = TRUE)
t_res

# 2. 效应量 (Cohen's d_z)
d_res <- repeated_measures_d(rt ~ condition | subject_id, data = df)
d_res

# 3. 均值差 + 95% CI
diff_vals <- df_wide$incongruent - df_wide$congruent
ci_diff   <- t.test(diff_vals)$conf.int
sprintf("Mean diff = %.2f, 95%% CI [%.2f, %.2f]",
        mean(diff_vals), ci_diff[1], ci_diff[2])

# 4. 差值正态性检验
shapiro.test(diff_vals)

# 5. 雨云图 + 个体连线图
ggplot(df, aes(x = condition, y = rt, fill = condition)) +
  stat_halfeye(adjust = 0.5, width = 0.6, justification = -0.2,
               point_colour = NA) +
  geom_boxplot(width = 0.15, outlier.color = NA, alpha = 0.5) +
  geom_line(aes(group = id), color = "grey60", alpha = 0.4) +
  geom_point(aes(group = id), size = 2, alpha = 0.7) +
  scale_fill_manual(values = c("#56B4E9", "#E69F00")) +
  labs(x = "Condition", y = "Response Time (ms)",
       title = "Paired t-test: Congruent vs Incongruent") +
  theme_minimal(base_size = 14) +
  theme(legend.position = "none")
```

## APA 7th 报告格式

> A paired-samples t-test compared RT in congruent (M=450, SD=80) and incongruent (M=520, SD=95) conditions. Results: t(29)=5.32, p<.001, Cohen's d_z=0.97, 95% CI [0.65,1.29].

## 输出
1. t值、df、p值
2. 均值差 + 95%CI
3. Cohen's d_z + 95%CI
4. 差值正态性检验
5. 雨云图 + 个体连线图

## 常见错误
- ❌ 用独立t检验做被试内比较（丢失配对，效力大降）
- ❌ 检验原始正态而非差值正态
- ❌ 报告 d_av 而非 d_z

## 备选方法
- **lmer**: 需利用全部试次、处理随机效应时
- **Wilcoxon符号秩**: 差值非正态
- **BayesFactor**: 需量化H0支持度
