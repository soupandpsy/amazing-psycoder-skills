# 多元方差分析 (MANOVA)

## 概述

MANOVA 在多个因变量上同时检验组间差异。当DV之间相关时,比分别做多个ANOVA更有效力且控制整体假阳性。

**典型场景**: 检验焦虑组和对照组在RT、准确率、RT变异性三个DV上的综合差异。

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计类型 | 组间设计（一个分类IV，多个连续DV） |
| DV | 2+连续变量，中等相关（r ≈ 0.3–0.7）；相关过高（r > 0.8）可考虑降维，相关过低（r < 0.2）则多个ANOVA亦可 |
| IV | 1个或以上分类变量（单因素或多因素） |
| 样本量 | 每组每DV ≥ 20，总样本 ≥ 组数 × DV数 × 20；组间样本量尽量平衡 |
| 假设 | 多元正态性（每组的DV联合分布近似多元正态）、方差-协方差矩阵齐性（Box's M 检验 p > .001）、观测独立性、无多元异常值 |

## vs 多个ANOVA

- 多个ANOVA: 每个DV一个 → 假阳性累积(3个DV→~14%至少一个假显著)
- MANOVA: 一个检验覆盖所有DV → 控制整体假阳性
- MANOVA可以检测到单个ANOVA检测不到的差异(DV组合的线性模式)

## 关键输出

| 统计量 | 推荐场景 |
|--------|---------|
| Pillai's Trace | 最稳健,假设违反时优先 |
| Wilks' Λ | 最常用 |

## R 代码

```r
# 加载必要的包
library(car)        # 用于MANOVA和Box's M检验
library(effectsize) # 用于效应量计算

# ---- 模拟数据 ----
# 场景: 焦虑组 vs 对照组，在RT、准确率、RT变异性上的综合差异
set.seed(123)
n_per_group <- 40
group <- factor(rep(c("焦虑组", "对照组"), each = n_per_group))

RT <- c(rnorm(n_per_group, mean = 520, sd = 80),
        rnorm(n_per_group, mean = 450, sd = 75))

accuracy <- c(rnorm(n_per_group, mean = 0.78, sd = 0.10),
              rnorm(n_per_group, mean = 0.88, sd = 0.08))

RT_variability <- c(rnorm(n_per_group, mean = 120, sd = 30),
                    rnorm(n_per_group, mean = 90, sd = 25))

df <- data.frame(group, RT, accuracy, RT_variability)

# ---- 描述统计 ----
cat("=== 描述统计 ===\n")
print(aggregate(cbind(RT, accuracy, RT_variability) ~ group, data = df, FUN = mean))

# ---- 假设检验: Box's M (方差-协方差矩阵齐性) ----
cat("\n=== Box's M 检验 ===\n")
box_m <- boxM(cbind(RT, accuracy, RT_variability) ~ group, data = df)
print(box_m)

# ---- MANOVA ----
dv_matrix <- cbind(df$RT, df$accuracy, df$RT_variability)
manova_fit <- manova(dv_matrix ~ group, data = df)

cat("\n=== MANOVA (Pillai's Trace) ===\n")
print(summary(manova_fit, test = "Pillai"))

cat("\n=== MANOVA (Wilks' Λ) ===\n")
print(summary(manova_fit, test = "Wilks"))

# ---- 效应量 (偏η²) ----
cat("\n=== 效应量 ===\n")
print(eta_squared(manova_fit, partial = TRUE))

# ---- 事后单变量ANOVA (Bonferroni校正) ----
cat("\n=== 事后单变量ANOVA ===\n")
dv_names <- c("RT", "accuracy", "RT_variability")
for (dv in dv_names) {
  cat("\n---", dv, "---\n")
  aov_fit <- aov(as.formula(paste(dv, "~ group")), data = df)
  print(summary(aov_fit))
}
```

## 报告格式 (APA 7th)

**方法部分**（简要报告）:

> A one-way multivariate analysis of variance (MANOVA) was conducted to examine the effect of group (anxiety group vs. control group) on three dependent variables: reaction time (RT), accuracy, and RT variability. Assumptions were checked prior to analysis. Box's M test for homogeneity of variance-covariance matrices was non-significant, *M* = 18.23, *p* = .214, indicating the assumption was tenable. Multivariate normality was assessed via Shapiro-Wilk tests on each DV per group; no severe violations were detected.

**结果部分**:

> Using Pillai's Trace, the multivariate effect of group was significant, *V* = 0.45, *F*(3, 76) = 11.23, *p* < .001, partial η² = .31. Follow-up univariate ANOVAs with Bonferroni-adjusted alpha (.05/3 = .017) revealed that the anxiety group had significantly slower RT, *F*(1, 78) = 18.45, *p* < .001, η²_p = .19; lower accuracy, *F*(1, 78) = 22.10, *p* < .001, η²_p = .22; and higher RT variability, *F*(1, 78) = 15.67, *p* < .001, η²_p = .17. Descriptive statistics and full model results are presented in Table X.

**APA 7th 要点**:
- 报告检验统计量名称（Pillai's Trace / Wilks' Λ）、值、*F*值、假设自由度和误差自由度、*p*值、效应量（partial η²）。
- 若 Pillai's 和 Wilks' 均报告，需说明选择依据（如"因样本量不等，报告 Pillai's Trace"）。
- 事后单变量分析须注明多重比较校正方法及调整后的 alpha 水平。

## 局限

- 需要较大样本(每DV每条件≥20)
- 假设比ANOVA更难满足
- 显著后仍需单变量ANOVA解读——报告时需多重比较校正

## 备选方法

- [单因素ANOVA](anova.md) — DV只有一个时使用
- [MANCOVA](mancova.md) — 需要控制协变量时使用
- [判别分析](discriminant-analysis.md) — 关注变量组合如何区分组别时使用
- [重复测量ANOVA](repeated-measures-anova.md) — 同组被试多时间点时使用
- [线性判别分析(LDA)](lda.md) — 分类目的时优先考虑

