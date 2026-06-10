# R 分析平台 — Config → 代码映射

## 字段映射

分析 config YAML 的每个字段直接映射到 R 代码：

| Config 路径 | R 代码位置 | 映射规则 |
|------------|-----------|---------|
| `experiment.data_path` | 步骤3: `read_csv("{value}")` | 直接替换 |
| `design.ivs[].name` | 步骤6: `group_by({name})` | 作为分组列 |
| `design.ivs[].levels` | 步骤6: 描述统计分组数 | 验证列的唯一值数 |
| `design.dvs[].name` | 步骤6: `summarise(mean_{name}=mean({name}))` | DV列名 |
| `design.dvs[].type` | 步骤8: 模型选择 | continuous→lmer, binary→glmer |
| `design.design_type` | 步骤8: 随机效应结构 | within→(1+cond\|subj), between→(1\|subj), mixed→(1+cond\|subj)+(1\|item) |
| `questions[].model_formula` | 步骤8: 公式字符串 | 直接替换到 lmer/glmer |
| `cleaning.rt_lower` | 步骤4: `filter(rt > {value})` | 数值直接替换 |
| `cleaning.rt_upper` | 步骤4: `filter(rt < {value})` | 数值直接替换 |
| `cleaning.accuracy_min` | 步骤4: `filter(mean_acc >= {value})` | 数值直接替换 |
| `cleaning.trial_exclusion` | 步骤4: `abs(rt-mean) > {value}*sd` | SD倍数 |
| `cleaning.missing_policy` | 步骤4: 分支逻辑 | listwise→na.omit, mice→mice::mice() |
| `model.seed` | 步骤2: `set.seed({value})` | 直接替换 |
| `model.contrast` | 步骤2: `options(contrasts=c("{value}", "contr.poly"))` | treatment/sum/helmert |
| `model.correction` | 步骤10: `pairs(emm, adjust="{value}")` | bonferroni/fdr/tukey/none |
| `output.save_path` | 步骤11: `ggsave("{value}/fig1.png")` | 路径拼接 |
| `output.report_format` | 步骤12: YAML output字段 | RMarkdown/Quarto |
| `output.figures` | 步骤11: 条件分支 | raincloud/boxplot/interaction/scatter |
| `output.effect_sizes` | 步骤9: 条件分支 | cohens_d/eta_squared/r2 |

## 模型选择决策树

```
design.dvs[].type 是什么？
  ├── continuous (RT/分数)
  │     ├── design.design_type = within
  │     │     ├── questions 中指定 → 用指定模型
  │     │     └── 未指定 → 默认 lmer
  │     └── design.design_type = between
  │           └── 默认 Welch t-test / oneway.test
  │
  └── binary (准确率)
        ├── 任何条件准确率 > 90% 或 < 10%
        │     └── 强制 glmer(binomial) — 禁用 ANOVA
        └── 准确率在 10-90% 之间
              └── 推荐 glmer，可接受 ANOVA（标注局限性）
```

## 数据聚合规则

| 分析 | 聚合级别 | 代码 |
|------|---------|------|
| 配对 t 检验 | 被试×条件均值 | `group_by(subj, cond) %>% summarise(m=mean(dv))` |
| lmer | 试次级（不聚合） | 直接传入 data_rt |
| 描述统计 | 条件 | `group_by(cond) %>% summarise(...)` |
| 被试排除 | 被试 | `group_by(subj) %>% summarise(acc=mean(acc))` |

## 公式构建规则

| 设计 | 固定效应 | 随机效应 |
|------|---------|---------|
| 单因素被试内 | `dv ~ condition` | `(1 + condition \| subject)` |
| 单因素被试间 | `dv ~ condition` | — |
| 两因素被试内 | `dv ~ A * B` | `(1 + A*B \| subject)` |
| 混合设计 | `dv ~ A * B` | `(1 + A \| subject)` (A被试内, B被试间) |
| 含协变量 | `dv ~ condition + covariate` | `(1 + condition \| subject)` |

## 图表映射

| Config `output.figures` 值 | R 代码 |
|---------------------------|--------|
| `raincloud` | `ggrain::geom_rain()` |
| `individual` | `geom_line(aes(group=subj))` + `stat_summary()` |
| `boxplot` | `geom_boxplot()` + `geom_jitter()` |
| `interaction` | `stat_summary(geom="line")` + `stat_summary(geom="errorbar")` |
