# Reviewer — R 平台独立审计清单

## Quality Gate（审计入口）

本清单是 reviewer 审计 R 分析脚本的**独立入口**。无需依赖 coder。

| # | 检查项 | grep 命令 | 失败级别 |
|---|--------|----------|---------|
| 1 | seed 已设 | `grep -q "set\.seed" script.R` | Critical |
| 2 | 排除日志存在 | `grep -q "Exclusion\|排除" script.R` | Critical |
| 3 | 正态性检验 | `grep -q "shapiro\.test\|qqnorm\|geom_qq" script.R` | Major |
| 4 | 方差齐性检验 | `grep -q "leveneTest\|bartlett\.test" script.R` | Major |
| 5 | 效应量 | `grep -q "cohens_d\|eta_squared\|r2(\|effectsize" script.R` | Critical |
| 6 | 多重比较校正 | `grep -q "p\.adjust\|emmeans.*adjust\|bonferroni\|fdr" script.R` | Critical |
| 7 | sessionInfo | `grep -q "sessionInfo()" script.R` | Major |
| 8 | 无绝对路径 | `! grep -q "/Users/\|/home/\|C:\\\\" script.R` | Major |
| 9 | 列名校验 | `grep -q "setdiff.*names\|stopifnot.*%in%" script.R` | Critical |
| 10 | 图表保存 | `grep -q "ggsave" script.R` | Minor |
| 11 | 包版本输出 | `grep -q "packageVersion\|sessionInfo" script.R` | Major |
| 12 | 敏感性分析 | `grep -q "Sensitivity\|敏感\|Method A.*Method B" script.R` | Minor |

## 统计反模式 Grep 模式

| # | 反模式 | grep（命中=FAIL） | 严重性 |
|---|--------|------------------|--------|
| 1 | `attach()` | `grep -q "attach(" script.R` | Critical |
| 2 | `setwd()` | `grep -q "setwd(" script.R` | Major |
| 3 | `save.image()` | `grep -q "save\.image" script.R` | Major |
| 4 | `rm(list=ls())` | `grep -q "rm(list.*ls" script.R` | Major |
| 5 | `aov()` 被试内 | `grep -q "aov(" script.R` + design=within | Critical |
| 6 | 错误的 R² | `grep -q "summary.*lmer.*r\.sq" script.R` | Critical |
| 7 | `stringsAsFactors=T` | `grep -q "stringsAsFactors\s*=\s*TRUE" script.R` | Minor |
| 8 | `t.test()` 未配对 | `grep -q "t\.test" script.R` 但 design=within 且无 `paired=TRUE` | Critical |
| 9 | 硬编码数字阈值 | 清洗阈值不在 config/params 中声明 | Major |

## 模型适配检查

| 设计类型 | 预期模型 | grep 验证 |
|---------|---------|----------|
| 被试内 2 组 | `t.test(..., paired=TRUE)` 或 `lmer(...\|subject)` | `grep -q "paired.*TRUE\|lmer.*\|" script.R` |
| 被试间 2 组 | `t.test(...)` 或 `wilcox.test` | `grep -q "t\.test\|wilcox" script.R` |
| 被试内 3+ 组 | `lmer` 或 `aov_ez` | `grep -q "lmer\|aov_ez" script.R` |
| 混合设计 | `lmer` + 交叉随机效应 | `grep -q "lmer.*\|.*\|" script.R` |
| 二分类 DV | `glmer(..., family=binomial)` | `grep -q "glmer.*binomial\|family.*binomial" script.R` |

## 效应量类型检查

| 检验方法 | 预期效应量函数 | grep |
|---------|-------------|------|
| t 检验 | `cohens_d()` | `grep -q "cohens_d" script.R` |
| ANOVA | `eta_squared()` | `grep -q "eta_squared" script.R` |
| 混合模型 | `r2()` | `grep -q "performance::r2\|r2(" script.R` |
| 逻辑模型 | `exp(fixef())` → OR | `grep -q "exp.*fixef\|exp.*coef" script.R` |
| 非参数检验 | rank-biserial 或 Cliff's delta | `grep -q "rank_biserial\|cliff" script.R` |
