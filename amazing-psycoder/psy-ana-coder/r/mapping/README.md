# R 分析平台 — Config → 代码映射

## 字段映射

分析 config YAML 的每个字段直接映射到 R 代码：

| Config 路径 | R 代码位置 | 映射规则 |
|------------|-----------|---------|
| `experiment.data_path` + `file_format` + `loader_options` + `multi_file` | 步骤3: format-dispatch loader | 项目内路径；单/多文件按契约加载并保留 source file/row provenance，不固定为 CSV |
| `runtime.language_version` + `dependency_file` | 步骤2: 启动门禁 + environment manifest | 精确核对 R patch 版本；`renv.lock` 必须存在并与实际加载包一致 |
| `design.ivs[].name` | 步骤6: `group_by({name})` | 作为分组列 |
| `design.ivs[].levels` | 步骤6: 描述统计分组数 | 验证列的唯一值数 |
| `design.dvs[].name` | 步骤6: `summarise(mean_{name}=mean({name}))` | DV列名 |
| `design.dvs[].type` | 步骤8: outcome-family compatibility check | 只用于核验已确认方法/分布/链接；不能仅凭类型自动选模型 |
| `design.observation_level` + `design.clustering` | 步骤8: 依赖结构 | 按已确认的 subject/item/session/site 层级实现，不从 within/between 标签机械推断 |
| `questions[].selected_method` | 步骤8: 估计器 | 必须直接实现；缺失或不兼容时停止并返回 Designer |
| `questions[].model_formula` | 步骤8: 公式字符串 | 直接替换到 lmer/glmer |
| `cleaning.rt_lower` / `rt_upper` | 步骤4: reason-coded mask + exclusion log | 按 config 声明的层级、边界和依据执行；保留原始行，不静默删除 |
| `cleaning.accuracy_min` | 步骤4: subject-level QC table + reason-coded exclusion | 仅按已确认的分母、层级和规则计算 |
| `cleaning.trial_exclusion` | 步骤4: config-specific rule function | 不把任意值机械解释成 SD trimming |
| `cleaning.missing_policy` | 步骤4: policy-specific implementation + diagnostics/sensitivity | 删除、插补、似然或权重方法必须匹配缺失机制、层级和 estimand；不自动 `na.omit()` 或 `mice()` |
| `model.stochastic` + `model.seed` | 步骤2 | 仅随机步骤需要 `set.seed()`；同时记录并行/采样设置 |
| `model.contrast` | 步骤2: `options(contrasts=c("{value}", "contr.poly"))` | treatment/sum/helmert |
| `model.correction` | 步骤10: claim-family-aware inference | planned/hierarchical/Tukey/Holm/Bonferroni/FDR/none 等按声明的 claim family 与 estimator 支持实现 |
| `output.save_path` | 步骤11: project-bound output directory | 校验不越出项目根目录后创建；所有结果写入该目录 |
| `output.report_format` | 步骤12: YAML output字段 | RMarkdown/Quarto |
| `output.figures` | 步骤11: 条件分支 | raincloud/boxplot/interaction/scatter |
| `output.effect_sizes` | 步骤9: 估计与不确定性分支 | 输出 config 声明的 raw/standardized/probability/OR 等 claim-compatible 估计；不统一映射成 d/η²/R² |

## 模型实现门禁

```
selected_method + estimand + outcome family + observation hierarchy
  ├── 兼容且 R API 已验证 → 按 config 实现
  ├── 公式缺少已声明的 subject/item/session 依赖 → 阻断
  └── 方法未确认/不兼容 → 返回 psy-ana-designer，不静默换模型
```

## 数据聚合规则

| 分析 | 聚合级别 | 代码 |
|------|---------|------|
| 配对 t 检验 | 仅当 estimand 是被试×条件摘要且 item 依赖已处理/论证时聚合 | `group_by(subj, cond) %>% summarise(m=mean(dv))`，并记录分母/缺失规则 |
| lmer | 试次级（不聚合） | 直接传入 data_rt |
| 描述统计 | 条件 | `group_by(cond) %>% summarise(...)` |
| 被试排除 | 被试 | `group_by(subj) %>% summarise(acc=mean(acc))` |

## 公式核验示例（不是自动默认）

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

## 环境与依赖门禁

- 生成并保存 config 声明的 `renv.lock`，只锁定实际加载和执行所需依赖。
- 启动时精确比对 R patch 版本；clean run 保存 `sessionInfo()`，Reviewer 核对其与 lockfile 是否一致。
- 选择的方法在目标 R 版本或锁定包版本中不可用时必须阻断并返回 Designer，不静默替换 API 或模型。
