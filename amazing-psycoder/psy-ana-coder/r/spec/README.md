# R 分析平台 — API 规范

## Canonical Code Skeleton

所有生成的 R 脚本必须遵循此 12 步骨架：

```
1. 标题注释     ← 实验名、模型、日期、seed
2. 环境设置     ← library 加载、set.seed、全局选项
3. 数据导入     ← read_csv + 列名校验（缺列→stop）
4. 数据清洗     ← RT过滤→正确试次→被试排除→SD排除→缺失处理
5. 排除日志     ← cat() 每步排除量+比例
6. 描述统计     ← group_by+summarise: n, mean, sd, se, ci95
7. 假设检验     ← Shapiro-Wilk + QQ图 + Levene/Mauchly（按需）
8. 统计建模     ← t.test/lmer/glmer/aov（按config选择）
9. 效应量       ← cohens_d/eta_squared/r2/exp(fixef)
10. 事后比较    ← emmeans + pairs(adjust=)
11. 图表生成    ← ggplot + ggsave
12. 环境信息    ← sessionInfo() + 包版本
```

步骤顺序不可改变。每一步输出 `cat("\n========== Step N: Name ==========\n")`。

---

## API 速查

| 操作 | 函数 | 包 |
|------|------|-----|
| 数据导入 | `read_csv(path, show_col_types=FALSE)` | readr |
| 过滤 | `filter(condition)` | dplyr |
| 分组汇总 | `group_by(col) %>% summarise(...)` | dplyr |
| 创建/修改变量 | `mutate(new = expr)` | dplyr |
| 管道 | `%>%` | dplyr |
| 数据重塑 | `pivot_longer/pivot_wider` | tidyr |
| 配对t检验 | `t.test(y ~ x, data, paired=TRUE)` | stats |
| 独立t检验 | `t.test(y ~ x, data, var.equal=FALSE)` | stats |
| 被试内ANOVA | `aov_ez(id, dv, data, within)` | afex |
| 被试间ANOVA | `oneway.test(y ~ x, data)` | stats |
| 线性混合模型 | `lmer(y ~ x + (1+x\|subj), data)` | lme4/lmerTest |
| 逻辑混合模型 | `glmer(y ~ x + (1+x\|subj), data, family=binomial)` | lme4 |
| 正态性 | `shapiro.test(x)` | stats |
| 方差齐性 | `leveneTest(y ~ x, data)` | car |
| Cohen's d (被试内) | `repeated_measures_d(y ~ x \| subject, data)` | effectsize |
| Cohen's d (被试间) | `cohens_d(y ~ x, data)` | effectsize |
| η² | `eta_squared(model)` | effectsize |
| R²(混合) | `r2(model)` | performance |
| 边际均值 | `emmeans(model, ~ condition)` | emmeans |
| 两两比较 | `pairs(emm, adjust="bonferroni")` | emmeans |
| 雨云图 | `geom_rain()` | ggrain |
| 保存图 | `ggsave(path, plot, width, height, dpi)` | ggplot2 |
| 随机种子 | `set.seed(n)` | base |
| 环境信息 | `sessionInfo()` | utils |

---

## 反模式 (15 项)

以下模式在生成代码中绝不出现：

| # | 反模式 | 为什么 | 替代 |
|---|--------|--------|------|
| 1 | `attach(df)` | 命名空间污染 | `with()` 或 `dplyr::` |
| 2 | `setwd()` | 可重复性 | 相对路径或 `here::here()` |
| 3 | `save.image()` | 不可复现 | `saveRDS(obj, file)` |
| 4 | `rm(list=ls())` | 破坏可重复性 | 不在脚本开头加 |
| 5 | `options(stringsAsFactors=TRUE)` | 过时默认 | R ≥4.0 默认 FALSE |
| 6 | `1:ncol(data)` 循环无预分配 | 性能 | `vector("list", n)` 或 `purrr::map()` |
| 7 | `summary(lmer)$r.squared` | 不存在 | `performance::r2(model)` |
| 8 | `aov()` 用于不平衡设计 | 错误结果 | `car::Anova(type="III")` |
| 9 | 绝对路径硬编码 | 不可移植 | config 读取 + 相对路径 |
| 10 | 排除标准未显式声明 | 不可重复 | cat() 打印排除日志 |
| 11 | `t.test()` 未检查正态性 | 假设不验证 | 步骤7 先做 Shapiro |
| 12 | 多重比较未校正 | 假阳性膨胀 | `pairs(emm, adjust=)` |
| 13 | 无效应量报告 | APA 不合规 | 步骤9 必须输出 |
| 14 | 无 `sessionInfo()` | 不可重复 | 步骤12 必须输出 |
| 15 | 接近天花板用 ANOVA 做准确率 | 假阳性严重膨胀 | 必须用 `glmer(binomial)` |

---

## 必装包

```r
install.packages(c(
  "tidyverse", "lme4", "lmerTest", "effectsize",
  "ggplot2", "ggrain", "patchwork", "emmeans",
  "performance", "afex", "car", "BayesFactor"
))
```

---

## Canonical Code Skeleton（完整 12 步模板）

以下模板可直接填入 config 字段生成完整 R 脚本。所有 `{placeholder}` 从 analysis config YAML 读取。

### 步骤 1-2: 环境设置 + 数据导入

```r
library(tidyverse); library(lme4); library(lmerTest)
library(effectsize); library(ggplot2); library(ggrain)
library(patchwork); library(emmeans); library(performance)
set.seed({seed})
options(dplyr.summarise.inform = FALSE)

data <- read_csv("{data_path}", show_col_types = FALSE)
expected_cols <- c("{subject_col}", "{condition_col}", "{rt_col}", "{acc_col}")
missing_cols <- setdiff(expected_cols, names(data))
if (length(missing_cols) > 0) stop("Missing columns: ", paste(missing_cols, collapse = ", "))
cat(sprintf("Loaded %d rows, %d cols\n", nrow(data), ncol(data)))
```

### 步骤 3: 数据清洗

```r
n_before <- nrow(data)
data <- data %>% filter({rt_col} > {rt_lower} & {rt_col} < {rt_upper})
n_rt <- n_before - nrow(data)
cat(sprintf("RT outliers: %d (%.1f%%)\n", n_rt, 100*n_rt/n_before))

n_with_acc <- nrow(data)
data_rt <- data %>% filter({acc_col} == 1)
cat(sprintf("Incorrect: %d (%.1f%%)\n", n_with_acc-nrow(data_rt), 100*(n_with_acc-nrow(data_rt))/n_with_acc))

subj_acc <- data %>% group_by({subject_col}) %>% summarise(mean_acc = mean({acc_col}, na.rm=TRUE), .groups="drop")
excluded_subj <- subj_acc %>% filter(mean_acc < {accuracy_min})
if (nrow(excluded_subj) > 0) {
  data_rt <- data_rt %>% filter(!{subject_col} %in% excluded_subj${subject_col})
  cat(sprintf("Subjects <%.0f%% acc: %d\n", {accuracy_min}*100, nrow(excluded_subj)))
}

data_rt <- data_rt %>% group_by({subject_col}, {condition_col}) %>%
  mutate(mean_rt=mean({rt_col},na.rm=TRUE), sd_rt=sd({rt_col},na.rm=TRUE),
         is_outlier=abs({rt_col}-mean_rt)>{sd_multiplier}*sd_rt) %>% ungroup()
cat(sprintf("SD exclusion: %d (%.1f%%)\n", sum(data_rt$is_outlier), 100*sum(data_rt$is_outlier)/nrow(data_rt)))
data_rt <- data_rt %>% filter(!is_outlier)
```

### 步骤 4: 描述统计

```r
desc <- data_rt %>% group_by({condition_col}) %>%
  summarise(n=n(), n_subj=n_distinct({subject_col}), mean_rt=mean({rt_col},na.rm=TRUE),
            sd_rt=sd({rt_col},na.rm=TRUE), se_rt=sd_rt/sqrt(n_subj),
            ci95_lo=mean_rt-qt(0.975,n_subj-1)*se_rt, ci95_hi=mean_rt+qt(0.975,n_subj-1)*se_rt,
            median_rt=median({rt_col},na.rm=TRUE), .groups="drop")
print(desc, width=120)
```

### 步骤 5: 假设检验

```r
data_rt %>% group_by({condition_col}) %>%
  summarise(W=shapiro.test({rt_col})$statistic, p=shapiro.test({rt_col})$p.value, .groups="drop") %>%
  mutate(verdict=ifelse(p>0.05,"PASS","FAIL")) %>% print()

ggplot(data_rt, aes(sample={rt_col})) + geom_qq()+geom_qq_line(color="red") +
  facet_wrap(~{condition_col}) + labs(title="Q-Q Plots") + theme_minimal()

library(car); leveneTest({rt_col} ~ {condition_col}, data=data_rt)
```

### 步骤 6: 统计模型

```r
# 根据 config model.type 选择:
# lmer: model <- lmer({rt_col} ~ {fixed_effects} + (1+{condition_col}|{subject_col}), data=data_rt, control=lmerControl(optimizer="bobyqa"))
# t-test: tt <- t.test(mean_rt ~ {condition_col}, data=data_agg, paired=TRUE)
# glmer: model <- glmer({acc_col} ~ {fixed_effects} + (1+{condition_col}|{subject_col}), data=data, family=binomial, control=glmerControl(optimizer="bobyqa"))
# Gamma: model <- glmer({rt_col} ~ {fixed_effects} + (1+{condition_col}|{subject_col}), data=data_rt, family=Gamma(link="log"))
# ANOVA: aov_result <- aov_ez(id="{subject_col}", dv="{rt_col}", data=data_rt, within="{condition_col}")
```

### 步骤 7: 效应量

```r
# t-test (被试内): effectsize::repeated_measures_d(mean_rt ~ condition | subject, data=data_agg)
# t-test (被试间): effectsize::cohens_d(mean_rt ~ condition, data=data_agg)
# ANOVA: effectsize::eta_squared(aov_result)
# lmer: performance::r2(model)
# glmer: exp(fixef(model))  # OR
```

### 步骤 8: 事后比较

```r
emm <- emmeans(model, ~ {condition_col})
pairs(emm, adjust = "{correction}")  # bonferroni / fdr / tukey
```

### 步骤 9: 敏感性分析

```r
data_agg <- data_rt %>% group_by({subject_col}, {condition_col}) %>% summarise(mean_rt=mean({rt_col}), .groups="drop")
tt <- t.test(mean_rt ~ {condition_col}, data=data_agg, paired=TRUE)
cat(sprintf("A (t-test): t=%.2f, p=%.4f, d=%.2f\n", tt$statistic, tt$p.value,
    effectsize::repeated_measures_d(mean_rt~{condition_col}|{subject_col},data=data_agg)$Cohens_d))
cat(sprintf("B (lmer): p=%.4f\n", summary(model)$coefficients[2,5]))
cat(sprintf("Agree: %s\n", ifelse((tt$p.value<.05)==(summary(model)$coefficients[2,5]<.05),"YES ✓","NO ✗")))
```

### 步骤 10: 图表

```r
# 雨云图
ggplot(data_rt, aes(x={condition_col}, y={rt_col}, fill={condition_col}, color={condition_col})) +
  ggrain::geom_rain(alpha=0.5, point.size=1) + scale_fill_brewer(palette="Set2") +
  scale_color_brewer(palette="Set2") + labs(title="{experiment_name}") + theme_minimal(12) +
  theme(legend.position="none")
ggsave("{save_path}/fig1_raincloud.png", width=6, height=5, dpi=300)

# 个体连线
data_agg %>% ggplot(aes(x={condition_col}, y=mean_rt, group={subject_col})) +
  geom_line(alpha=0.3, linewidth=0.5) + geom_point(alpha=0.3, size=1) +
  stat_summary(aes(group=1), fun=mean, geom="line", linewidth=1.5, color="red") +
  stat_summary(fun=mean, geom="point", size=3, color="red") +
  labs(title="Individual Changes") + theme_minimal(12)
ggsave("{save_path}/fig2_individual.png", width=6, height=5, dpi=300)
```

### 步骤 11: 环境信息

```r
cat(sprintf("Generated: %s\nR: %s\n", Sys.time(), R.version.string))
for (pkg in c("tidyverse","lme4","lmerTest","effectsize","ggplot2","ggrain","emmeans","performance"))
  cat(sprintf("  %s: %s\n", pkg, as.character(packageVersion(pkg))))
sessionInfo()
```

### 步骤 12: RMarkdown 报告

```yaml
---
title: "{experiment_name} — Analysis Report"
author: "psy-ana-coder"
date: "`r Sys.Date()`"
output: html_document: {toc: true, toc_float: true, theme: flatly}
---

## Exclusion Summary
| Step | Trials | % |
|------|--------|----|
| RT cutoffs | `r n_rt` | `r round(100*n_rt/n_before,1)`% |
| **Final** | `r nrow(data_rt)` | ... |

## Descriptive Statistics
`r knitr::kable(desc, digits=1)`

## Model Results
`r summary(model)`

## Figures
![]({save_path}/fig1_raincloud.png)
![]({save_path}/fig2_individual.png)

## Environment
- R `r R.version.string`
```
