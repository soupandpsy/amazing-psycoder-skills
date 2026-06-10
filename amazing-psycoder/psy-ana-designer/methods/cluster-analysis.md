# 聚类分析 (Cluster Analysis)

## 概述

聚类分析基于多个变量将被试分成同质的子群体,常用于发现行为模式。

**典型场景**: 基于RT、准确率和问卷分数将被试分为"高效"和"谨慎"两类; 发现焦虑的不同表现亚型。

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计 | 被试间 |
| DV | 多个连续变量（需标准化） |
| 目标 | 发现同质子群体（探索性） |
| 样本量 | n ≥ 50，变量数 < n/5 |
| 数据要求 | 标准化变量，缺失值已处理 |

## 方法

| 方法 | 特点 | R包 |
|------|------|-----|
| K-means | 预指定k个类 | `stats::kmeans()` |
| 层次聚类 | 不需预指定,树状图可视化 | `stats::hclust()` |
| 潜在类别分析(LCA) | 基于模型,提供拟合指标 | `poLCA` |

## 如何确定k

| 方法 | 指标 |
|------|------|
| 肘部法 (Elbow) | 组内SS的拐点 |
| 轮廓系数 (Silhouette) | 越接近1越好 |
| BIC (LCA) | 越低越好 |

## R 代码

```r
# 聚类分析完整示例
library(tidyverse)
library(cluster)      # 轮廓系数
library(factoextra)   # 聚类可视化
library(effectsize)   # 效应量（eta-squared）

# ============================================
# 1. 数据准备与标准化
# ============================================
set.seed(123)
df <- read.csv("data.csv")  # 替换为实际数据文件
vars <- df %>% select(RT, accuracy, anxiety, depression)
vars_scaled <- scale(vars)  # 标准化（均值为0，标准差为1）

# ============================================
# 2. 确定最佳聚类数 k
# ============================================
# 肘部法：寻找组内平方和（WSS）的拐点
fviz_nbclust(vars_scaled, kmeans, method = "wss") +
  labs(title = "肘部法确定最佳 k")

# 轮廓系数法：越接近 1 越好
fviz_nbclust(vars_scaled, kmeans, method = "silhouette") +
  labs(title = "轮廓系数法确定最佳 k")

# ============================================
# 3. 执行 K-means 聚类（假设 k = 3）
# ============================================
k <- 3
km <- kmeans(vars_scaled, centers = k, nstart = 25)
df$cluster <- factor(km$cluster)

# 聚类结果可视化（PCA 降维投影）
fviz_cluster(km, data = vars_scaled,
             ellipse.type = "norm",
             palette = "jco",
             ggtheme = theme_minimal(),
             main = paste0("K-means 聚类结果 (k = ", k, ")"))

# ============================================
# 4. 聚类特征描述
# ============================================
cluster_profile <- df %>%
  group_by(cluster) %>%
  summarise(
    n = n(),
    across(c(RT, accuracy, anxiety, depression),
           list(M = mean, SD = sd), .names = "{.col}_{.fn}")
  )
print(cluster_profile)

# ============================================
# 5. 聚类质量指标：轮廓系数
# ============================================
sil <- silhouette(km$cluster, dist(vars_scaled))
cat(sprintf("平均轮廓系数: %.3f\n", mean(sil[, 3])))

# ============================================
# 6. 外部效度验证：聚类间差异检验 + 效应量
# ============================================
# ANOVA 检验焦虑分数在聚类间是否有差异
anova_res <- aov(anxiety ~ cluster, data = df)
summary(anova_res)

# 效应量：eta-squared（广义 eta-squared 适用于被试间设计）
eta_sq <- eta_squared(anova_res, partial = FALSE)
cat(sprintf("eta-squared = %.3f (%.2f%% CI [%.3f, %.3f])\n",
            eta_sq$Eta2, 95,
            eta_sq$CI_low, eta_sq$CI_high))

# 事后多重比较（Tukey HSD）
TukeyHSD(anova_res)

# ============================================
# 7.（可选）层次聚类
# ============================================
dist_mat <- dist(vars_scaled, method = "euclidean")
hc <- hclust(dist_mat, method = "ward.D2")
fviz_dend(hc, k = k, rect = TRUE,
          main = "层次聚类树状图（Ward 法）")
```

## 报告

> K-means clustering (k=3, silhouette=0.42) identified three response patterns: fast-accurate (45%), slow-accurate (32%), and fast-inaccurate (23%). Groups differed on anxiety scores, F(2,97)=8.34, p<.001.

## 注意事项

- 聚类是探索性方法——结果需在独立样本中验证
- 变量需标准化(否则单位大的变量主导聚类)
- 不同的k和算法可能得出不同结果——报告稳定性

## 备选方法

- [判别分析](./discriminant-analysis.md) — 已知分组标签时用于预测组别归属
- [因子分析](./factor-analysis.md) — 降维发现潜在维度结构，而非将被试分组
- [潜在剖面分析](./latent-profile-analysis.md) — 连续变量的模型化聚类，提供拟合指标
- [混合效应模型](./mixed-effects.md) — 处理层次数据结构中的亚组差异

