# 混合 ANOVA (Split-plot)

## 概述

混合 ANOVA 同时包含被试内因素和被试间因素。

**典型场景**: 2(组别: ADHD/对照组, 被试间) × 2(条件: 一致/不一致, 被试内) 的交互效应。

## 何时使用

| 条件 | 要求 |
|------|------|
| 设计 | 至少1个被试内IV + 1个被试间IV |
| DV | 连续 |
| 关键 | 组×条件的交互效应 |

## 关键输出

- **组间主效应**: 被试间因素的整体差异
- **被试内主效应**: 条件的主效应
- **交互作用**: 组×条件——这是混合设计的核心。组间差异是否在不同条件下有所不同?

## 效应量

η²p。交互效应的η²p通常比主效应更受关注。

## R 代码

```r
# 加载所需包
library(afex)
library(emmeans)

# 模拟数据
set.seed(123)
n_per_group <- 30
data <- data.frame(
  subject  = factor(1:(n_per_group * 2)),
  group    = factor(rep(c("ADHD", "Control"), each = n_per_group)),
  congruent   = c(rnorm(n_per_group, 500, 80), rnorm(n_per_group, 450, 70)),
  incongruent = c(rnorm(n_per_group, 600, 90), rnorm(n_per_group, 500, 75))
)

# 转换为长格式
data_long <- reshape(
  data,
  direction = "long",
  varying   = c("congruent", "incongruent"),
  v.names   = "rt",
  timevar   = "condition",
  times     = c("congruent", "incongruent"),
  idvar     = "subject"
)
data_long$condition <- factor(data_long$condition)

# 混合 ANOVA（afex，默认 GG 校正 + 偏 η²）
model <- aov_ez(
  id          = "subject",
  dv          = "rt",
  between     = "group",
  within      = "condition",
  data        = data_long,
  anova_table = list(correction = "GG", es = "pes")
)

# 输出 ANOVA 表
print(model)

# 交互效应显著时的简单效应分析
em <- emmeans(model, ~ condition | group)
print(pairs(em))
```

## 报告格式

> A 2(Group)×2(Condition) mixed ANOVA revealed a significant Group×Condition interaction, F(1,58)=6.45, p=.014, η²p=.10. The ADHD group showed a larger congruency effect (M_diff=85ms) than controls (M_diff=45ms).

## 备选方法

- **lmer**: `dv ~ group*condition + (1+condition|subject)`
