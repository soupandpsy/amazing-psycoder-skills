# 潜在类别/剖面分析 (LCA/LPA)

## 概述

LCA/LPA是基于模型的聚类方法,通过拟合指标确定最优类别数,将被试分为互斥的潜在亚群。是"以人为中心"的方法。

**典型场景**: 基于焦虑、抑郁、压力分数发现心理健康的三个亚型; 基于Stroop、Flanker、N-back表现发现认知控制的两种模式。

## 何时使用

| 条件 | 要求 |
|------|------|
| 研究设计类型 | 以人为中心(person-centered)；基于被试间变量将被试分为互斥亚群 |
| 因变量类型 | LCA: 二分类或多分类指标；LPA: 连续指标（通常标准化） |
| 最低样本量 | ≥300；类别数或指标数较多时需≥500–1000 |
| 指标数量 | ≥3个观测指标，通常4–10个 |
| 关键假设 | 局部独立性（给定类别后指标互不相关）；多变量正态性（LPA）；无系统缺失模式 |
| 类别确定 | 综合BIC/aBIC、Entropy(>.80)、LMR-LRT/BLRT(p<.05)与理论可解释性 |
| 常见陷阱 | 仅凭拟合指标选类别而忽视理论意义；样本量不足导致假类别；忽视局部独立性违背 |

## LCA vs LPA

| 方法 | 指标 | 何时用 |
|------|------|--------|
| LCA | 分类指标 | 类别型观测变量 |
| LPA | 连续指标 | 连续型观测变量 |

## 模型选择

| 指标 | 标准 |
|------|------|
| BIC | 越低越好 |
| aBIC | 越低越好 |
| Entropy | >0.8好 |
| LMR-LRT | p<.05→k类比k-1类好 |
| BLRT | 同上,更准确但计算慢 |

## R代码

```r
library(mclust)  # LPA
model <- Mclust(data[,c("anxiety","depression","stress")])
summary(model)
plot(model, what="BIC")

# 或 tidyLPA
library(tidyLPA)
data %>% select(anxiety, depression, stress) %>%
  estimate_profiles(1:5) %>% plot_profiles()
```

## 报告格式 (APA 7th)

**方法部分 (Method)**

> We conducted latent profile analysis (LPA) using Mplus 8.8 (Muthén & Muthén, 2017) to identify distinct subgroups of participants based on their scores on the Depression Anxiety Stress Scales (DASS-21; Lovibond & Lovibond, 1995). Models with one through six latent profiles were estimated using robust maximum likelihood estimation with 500 random start values. Model fit was evaluated using the Bayesian information criterion (BIC), sample-size adjusted BIC (aBIC), entropy, and the Lo–Mendell–Rubin adjusted likelihood ratio test (LMR-LRT). The final model was selected based on a combination of fit indices, classification quality, and theoretical interpretability of the profiles (Nylund-Gibson & Choi, 2018).

**结果部分 (Results)**

> Table 1 presents the fit indices for the one- through six-profile models. The three-profile solution demonstrated the best balance of fit and parsimony: BIC = 4521.34, aBIC = 4480.12, entropy = 0.86, and a significant LMR-LRT (p = .002) indicating that the three-profile model fit significantly better than the two-profile model. Although the four-profile model yielded a slightly lower BIC (4491.20), the LMR-LRT was nonsignificant (p = .21) and one additional profile contained only 5% of the sample, suggesting over-extraction.
>
> Profile 1 ("Low Distress," n = 132, 44.0%) was characterized by low scores across all three subscales (M_anxiety = 3.21, SD = 2.10; M_depression = 2.89, SD = 1.95; M_stress = 4.12, SD = 2.30). Profile 2 ("Moderate Anxiety," n = 96, 32.0%) showed elevated anxiety (M = 12.45, SD = 3.21) with relatively lower depression (M = 5.67, SD = 2.80) and stress (M = 8.90, SD = 3.10). Profile 3 ("High Comorbid," n = 72, 24.0%) exhibited high scores on all three dimensions (M_anxiety = 18.23, SD = 4.10; M_depression = 16.78, SD = 3.85; M_stress = 19.45, SD = 4.20). A one-way ANOVA confirmed significant differences across profiles on all indicator variables (all ps < .001, η² = .62–.78). Figure 1 displays the profile plot with standardized means.

**表格建议 (Suggested Table)**

| Model | BIC | aBIC | Entropy | LMR-LRT p | 最小类别占比 |
|-------|-----|------|---------|-----------|-------------|
| 1-class | 4820.45 | 4805.12 | — | — | — |
| 2-class | 4650.30 | 4620.55 | .82 | .010 | 38% |
| **3-class** | **4521.34** | **4480.12** | **.86** | **.002** | **24%** |
| 4-class | 4491.20 | 4445.80 | .84 | .210 | 5% |
| 5-class | 4475.60 | 4420.15 | .81 | .350 | 4% |

*Note.* Boldface indicates the selected model. BIC = Bayesian information criterion; aBIC = sample-size adjusted BIC; LMR-LRT = Lo–Mendell–Rubin adjusted likelihood ratio test.
