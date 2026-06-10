# 因子分析 (Factor Analysis)

## 概述

因子分析用于揭示多个观测变量背后的潜在结构,是量表开发和验证的核心方法。

**典型场景**: 对20题焦虑量表做探索性因子分析(EFA)发现3个因子; 用验证性因子分析(CFA)检验假设的因子结构。

## 何时使用

| 条件 | 要求 |
|------|------|
| 变量类型 | 连续变量（或至少5点以上的Likert量表） |
| 样本量 | 至少100-200例，或每个变量5-10例（N/p ≥ 5） |
| 变量间相关 | 存在适度相关（0.3-0.8），非完全独立也非高度共线 |
| 抽样充分性 | KMO > 0.6；Bartlett 球形检验 p < .05 |
| 因子可解释性 | 提取的因子在理论上可命名、可解释 |
| 研究目的-EFA | 量表开发初期，因子结构未知，需要探索维度 |
| 研究目的-CFA | 已有理论假设或前人因子结构，需要验证 |

## EFA vs CFA

| | EFA | CFA |
|------|-----|-----|
| 目的 | 探索结构 | 验证假设 |
| 何时用 | 量表开发初期 | 有理论假设时 |
| 因子数 | 数据驱动 | 理论驱动 |
| R包 | `psych::fa()` | `lavaan::cfa()` |

## 关键指标

| 指标 | 标准 |
|------|------|
| KMO | >0.6 可接受, >0.8 好 |
| Bartlett 球形检验 | p<.05 |
| 特征值 | >1 (Kaiser准则) |
| 因子载荷 | >0.4 显著 |
| CFI/TLI | >0.90 可接受, >0.95 好 |
| RMSEA | <0.08 可接受, <0.05 好 |
| SRMR | <0.08 好 |

## R 代码

```r
# 因子分析: EFA + CFA
library(psych)      # fa(), KMO(), cortest.bartlett()
library(lavaan)     # cfa()
library(GPArotation) # oblimin 旋转

# --- 1. 数据准备 ---
# 假设 df 是包含量表题项的数据框，item1-item20
items <- df[, grep("^item", names(df))]

# --- 2. 抽样充分性检验 ---
KMO(items)$MSA
cortest.bartlett(cor(items), n = nrow(items))

# --- 3. 确定因子数 ---
# 平行分析
fa.parallel(items, fa = "fa", fm = "ml")

# scree plot 特征值
eigen_vals <- eigen(cor(items))$values
plot(eigen_vals, type = "b", main = "Scree Plot",
     xlab = "Factor Number", ylab = "Eigenvalue")
abline(h = 1, lty = 2)

# --- 4. 探索性因子分析 (EFA) ---
efa <- fa(items, nfactors = 3, rotate = "oblimin", fm = "ml")
print(efa$loadings, cutoff = 0.4, sort = TRUE)
print(efa$Vaccounted)  # 累积方差解释率

# 公因子方差 (communalities)
efa$communality

# 因子得分 (可选)
factor_scores <- factor.scores(items, efa)$scores
df$F1 <- factor_scores[, 1]
df$F2 <- factor_scores[, 2]
df$F3 <- factor_scores[, 3]

# --- 5. 验证性因子分析 (CFA) ---
model_3f <- '
  F1 =~ item1 + item2 + item5 + item8  + item12 + item16
  F2 =~ item3 + item6 + item9 + item11 + item14 + item18
  F3 =~ item4 + item7 + item10 + item13 + item15 + item20
'
fit <- cfa(model_3f, data = df, estimator = "MLR")
summary(fit, fit.measures = TRUE, standardized = TRUE, rsquare = TRUE)

# 效应量: 标准化因子载荷
standardizedSolution(fit)

# 效应量: ω 系数 (复合信度)
compRelSEM(fit)

# 区分效度: HTMT
ave <- semTools::AVE(fit)    # 平均方差提取量
htmt <- semTools::HTMT(fit)  # heterotrait-monotrait ratio
print(htmt)
```

## 报告

### APA 7th 报告格式

> A principal axis factor analysis with oblimin rotation was conducted on the 20 anxiety items. The Kaiser-Meyer-Olkin measure verified sampling adequacy (KMO = .87, "meritorious"), and Bartlett's test of sphericity was significant, χ²(190) = 1845.32, *p* < .001. Parallel analysis suggested a three-factor solution, which explained 58.4% of the total variance.
>
> Factor 1 (Somatic Anxiety) comprised 6 items with loadings from .58 to .82, explaining 24.1% of variance. Factor 2 (Cognitive Anxiety) comprised 6 items with loadings from .55 to .79, explaining 18.7% of variance. Factor 3 (Avoidance Behavior) comprised 5 items with loadings from .52 to .75, explaining 15.6% of variance. Three items with cross-loadings below .40 or cross-loading difference < .20 were removed.
>
> A confirmatory factor analysis using the MLR estimator was conducted to test the hypothesized three-factor model. The model demonstrated adequate fit: robust χ²(167) = 245.31, *p* < .001, CFI = .93, TLI = .92, RMSEA = .06 (90% CI [.05, .08]), SRMR = .06. All standardized factor loadings were significant (*p* < .001) and ranged from .51 to .81. Composite reliability (ω) exceeded .80 for all factors (ω₁ = .88, ω₂ = .86, ω₃ = .84). The three-factor model showed superior fit compared to a unidimensional model, Δχ²(3) = 186.42, *p* < .001. HTMT values were below .85 for all factor pairs, supporting discriminant validity.

## 备选方法

- [主成分分析 (PCA)](./pca.md) — 仅用于降维,不假设潜在因子
- [信度分析 (Reliability)](./reliability.md) — Cronbach's α 和 ω 系数
- [结构方程模型 (SEM)](./sem.md) — 含潜变量路径关系的扩展分析
- [聚类分析 (Cluster Analysis)](./cluster-analysis.md) — 对人分类,非对变量分类
- [多维度尺度分析 (MDS)](./mds.md) — 非参数降维可视化

