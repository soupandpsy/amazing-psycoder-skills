# Python 分析平台 — Config → 代码映射

## 字段映射

| Config 路径 | Python 代码位置 | 映射规则 |
|------------|---------------|---------|
| `experiment.data_path` + `file_format` + `loader_options` + `multi_file` | format-dispatch loader | 用项目内路径；单/多文件按契约加载并保留 source file/row provenance，不固定为 CSV |
| `runtime.language_version` + `dependency_file` | 启动门禁 + environment manifest | 精确核对 Python patch 版本；依赖文件必须存在且与实际 imports 对应 |
| `design.ivs[].name` | `groupby("{name}")` | 作为分组列 |
| `design.dvs[].name` | `agg({name}=('dv','mean'))` | DV列名 |
| `design.dvs[].type` | 结果分布核验 | continuous/binary/ordinal/count 必须与所选模型 family 一致 |
| `design.observation_level` + `design.clustering` | 依赖结构 | 按 subject/item/session/site 层级实现，不机械映射 design_type |
| `questions[].selected_method` | 估计器 | 直接实现；缺失或 Python 无可靠实现时阻断并返回 Designer |
| `cleaning.rt_lower` / `rt_upper` | reason-coded mask + exclusion log | 按 config 的含义/边界运算符执行，保留 raw row；不静默删除 |
| `cleaning.accuracy_min` | subject-level QC table + reason-coded exclusion | 仅在确认的层级/分母/规则下计算 |
| `cleaning.trial_exclusion` | config-specific rule function | 不把任意值机械解释为 SD trimming |
| `cleaning.missing_policy` | policy-specific implementation + diagnostics/sensitivity | 删除、插补、似然或权重方法需与缺失机制、层级和 estimand 相容；`IterativeImputer` 不是 MICE 的通用替代 |
| `model.stochastic` + `model.seed` | 环境设置 | 仅随机步骤设置 seed，并记录采样/并行配置 |
| `model.contrast` | `"contrast_coding": "{value}"` → patsy | treatment/sum/helmert |
| `model.correction` | claim-family-aware contrast/inference layer | planned/hierarchical/Tukey/Holm/Bonferroni/FDR/none 等按 config 和 estimator 支持实现 |
| `output.save_path` | project-bound output directory | 校验不越出项目根目录后创建；所有结果写入该目录 |
| `output.report_format` | Jupyter notebook 或 Quarto | ipynb/qmd |
| `output.figures` | 条件分支 | raincloud/boxplot/interaction/scatter |
| `output.effect_sizes` | 估计与不确定性分支 | 输出 config 声明的 raw/standardized/probability/OR 等 claim-compatible 估计；不统一映射成 d/η²/R² |

## 公式核验示例（不是自动默认）

| 设计 | 固定效应 | 随机效应 |
|------|---------|---------|
| 单因素被试内 | `dv ~ condition` | `groups="subject_id", re_formula="~condition"` |
| 单因素被试间 | `dv ~ condition` | — |
| 两因素被试内 | `dv ~ A * B` | `groups="subject_id", re_formula="~A*B"` |
| 混合设计 | `dv ~ A * B` | `groups="subject_id"` (A被试内, B被试间) |
| 含协变量 | `dv ~ condition + covariate` | `groups="subject_id", re_formula="~condition"` |

## 图表映射

| Config `output.figures` 值 | Python 代码 |
|---------------------------|-----------|
| `raincloud` | `ptitprince.RainCloud()` 或 violin+stripplot组合 |
| `individual` | `sns.lineplot()` + 个体线 |
| `boxplot` | `sns.boxplot()` + `sns.stripplot()` |
| `interaction` | `sns.pointplot()` + 误差棒 |

## R ↔ Python 对照

| R 函数 | Python 等效 |
|--------|-----------|
| format-dispatch loader | pandas matching reader (`read_csv`/`read_excel`/`read_parquet`/`read_json`) |
| `filter()` | `df[df['col'] > x]` |
| `group_by() %>% summarise()` | `df.groupby().agg()` |
| `mutate()` | `df['new'] = ...` |
| `t.test(paired=TRUE)` | `scipy.stats.ttest_rel()` |
| `t.test(var.equal=FALSE)` | `scipy.stats.ttest_ind(..., equal_var=False)` |
| `aov_ez()` | 无通用等价；仅在设计/缺失/协方差/校正契约相容时考虑 `pingouin.rm_anova()` |
| `lmer()` | `statsmodels.MixedLM()` 仅在其 grouping/variance-component 能表达已确认结构时；否则使用已验证实现或阻断 |
| `glmer(binomial)` | Bambi Bernoulli multilevel model；或在限制明确时用 `BinomialBayesMixedGLM`。普通 `Logit()` 没有随机效应 |
| 模型诊断 | estimator-specific residual/convergence/dispersion/posterior-predictive checks |
| `leveneTest()` | `scipy.stats.levene()` |
| `cohens_d()` | `pingouin.compute_effsize(eftype='cohen')` |
| `eta_squared()` | `pingouin.anova(detailed=True)` |
| `emmeans()` | 无通用等价；使用所选模型的预测/设计矩阵与协方差构造声明的 marginal contrast。`pairwise_tukeyhsd()` 只适用于其简单独立组场景 |
| `ggplot2` | `seaborn` + `matplotlib` |
| `ggsave()` | `plt.savefig()` |
| `sessionInfo()` | exact `platform.python_version()` check + platform + actual imported-distribution snapshot + declared dependency artifact |

## 模型实现门禁

与 R 平台使用同一 estimand/层级契约，但不假设 API 等价。若 Python 生态没有经过验证的实现，报告依赖限制并返回 Designer 选择经确认的替代方案；禁止用普通 `Logit()` 冒充 GLMM。
