# R 分析平台 — Reviewer 检查清单

## Quality Gate（交付前必查）

| # | 检查项 | grep 命令 |
|---|--------|----------|
| 1 | seed 已设 | `grep -q "set\.seed" script.R` |
| 2 | 排除日志存在 | `grep -q "Exclusion\|排除" script.R` |
| 3 | Shapiro-Wilk | `grep -q "shapiro\.test" script.R` |
| 4 | 效应量 | `grep -q "cohens_d\|eta_squared\|r2(" script.R` |
| 5 | 多重比较校正 | `grep -q "p\.adjust\|emmeans.*adjust" script.R` |
| 6 | sessionInfo | `grep -q "sessionInfo()" script.R` |
| 7 | 无绝对路径 | `! grep -q "/Users/\|/home/\|C:\\\\" script.R` |
| 8 | 图表保存 | `grep -q "ggsave" script.R` |
| 9 | 列名校验 | `grep -q "setdiff.*names" script.R` |
| 10 | 包版本 | `grep -q "packageVersion" script.R` |

## 反模式检查

| # | 反模式 | grep 命令（不得出现） |
|---|--------|---------------------|
| 1 | attach() | `! grep -q "attach(" script.R` |
| 2 | setwd() | `! grep -q "setwd(" script.R` |
| 3 | save.image() | `! grep -q "save\.image" script.R` |
| 4 | rm(list=ls()) | `! grep -q "rm(list.*ls" script.R` |
| 5 | aov() 用于被试内 | 如 design=within，`! grep -q "aov(" script.R` |

## 统计正确性检查

| # | 检查项 | 验证方式 |
|---|--------|---------|
| 1 | 模型与设计匹配 | within→paired t/lmer, between→ind t/aov |
| 2 | 随机效应合理 | lmer 至少含 `(1\|subject)` |
| 3 | 分类变量为 factor | `grep -q "as\.factor\|factor(" script.R` |
| 4 | 效应量类型正确 | t-test→d, ANOVA→η², lmer→R² |
| 5 | 敏感度分析 | `grep -q "Sensitivity\|敏感\|agree" script.R` |
| 6 | 排除标准已声明 | cat() 输出每步排除原因 |
| 7 | 多重比较已说明 | 注释或 cat() 说明校正方法 |
