# 单因素 ANOVA — 被试内 (One-way Repeated Measures ANOVA)

## 概述

被试内单因素ANOVA用于比较同一组被试在3个及以上条件下的均值差异。是配对t检验的扩展。

**典型场景**：3种难度Stroop的RT比较、4种记忆负荷的准确率比较。

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计 | 被试内, 3+条件 |
| DV | 连续变量 |
| 假设 | 正态+球对称 |

## 假设与检验

1. **正态性**：每条件数据近似正态
2. **球对称 (Sphericity)**：所有条件对的差值方差相等。Mauchly检验。p<0.05→违反→Greenhouse-Geisser校正
3. **无极端异常值**

## 效应量: η²p (偏eta方)

| 大小 | η²p |
|------|-----|
| 小 | 0.01 |
| 中 | 0.06 |
| 大 | 0.14 |

η²p = 条件效应解释的方差比例（排除被试间变异）。

## 事后比较

ANOVA显著后必须做两两比较:
- Bonferroni: 最保守
- Tukey HSD: 适用所有两两
- FDR: 探索性分析

**关键**: 事后比较的p值必须经过多重比较校正。

## 备选方法
- **lmer**: 推荐替代,效力更高,处理不平衡更好
- **Friedman**: 非正态或严重违反球对称
- **GG校正ANOVA**: 球对称违反但正态时

## R 代码

```r
# 加载必要库
library(tidyverse)
library(rstatix)      # 便于ANOVA、效应量、事后检验
library(afex)         # 自动应用GG/HF校正的重复测量ANOVA

# ============================================
# 示例数据: 30名被试在3个条件下的反应时 (ms)
# ============================================
set.seed(42)
n <- 30
df <- data.frame(
  id       = factor(rep(1:n, 3)),
  cond     = factor(rep(c("easy", "medium", "hard"), each = n)),
  rt       = c(rnorm(n, 400, 50),
               rnorm(n, 480, 55),
               rnorm(n, 580, 65))
)
head(df)

# ============================================
# 描述统计
# ============================================
df %>%
  group_by(cond) %>%
  summarise(M = mean(rt), SD = sd(rt), N = n())

# ============================================
# 重复测量ANOVA (afex: 自动输出GG/HF校正结果)
# ============================================
aov_res <- aov_car(rt ~ cond + Error(id/cond), data = df)
summary(aov_res)
nice(aov_res)  # 整齐的输出表

# ============================================
# 球对称检验 (Mauchly's Test)
# ============================================
aov_ez <- anova_test(data = df, dv = rt, wid = id, within = cond)
aov_ez  # 自动包含Mauchly检验与GG校正后的p值

# ============================================
# 效应量: 偏η² (partial eta-squared)
# ============================================
get_anova_table(aov_ez, correction = TRUE)  # 含η²p

# 或手工提取:
eta_sq <- aov_ez$ANOVA[["ges"]]            # 广义偏eta方
cat(sprintf("Generalized η² = %.3f\n", eta_sq))

# ============================================
# 事后两两比较 (Bonferroni校正)
# ============================================
pairwise_t_test(data = df, rt ~ cond, paired = TRUE,
                p.adjust.method = "bonferroni") %>%
  select(-.y.)

# 报告Cohen's d作为效应量
df %>%
  pairwise_t_test(rt ~ cond, paired = TRUE,
                  p.adjust.method = "bonferroni") %>%
  mutate(cohens_d = statistic / sqrt(n))  # 配对Cohen's d近似

# ============================================
# 备选: 手工lm模型 (用于lme4替代)
# ============================================
# library(lme4)
# library(lmerTest)
# m_lmer <- lmer(rt ~ cond + (1 | id), data = df)
# anova(m_lmer)
```

## 报告格式

> A one-way repeated measures ANOVA examined RT across three difficulty levels (easy/medium/hard). Mauchly's test indicated violation of sphericity (p=.02), so Greenhouse-Geisser correction was applied. The main effect was significant, F(1.6, 46.4)=12.34, p<.001, η²p=.30.
