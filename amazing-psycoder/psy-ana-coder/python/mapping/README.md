# Python 分析平台 — Config → 代码映射

## 字段映射

| Config 路径 | Python 代码位置 | 映射规则 |
|------------|---------------|---------|
| `experiment.data_path` | `pd.read_csv("{value}")` | 直接替换 |
| `design.ivs[].name` | `groupby("{name}")` | 作为分组列 |
| `design.dvs[].name` | `agg({name}=('dv','mean'))` | DV列名 |
| `design.dvs[].type` | 模型选择 | continuous→MixedLM/lmer, binary→Logit |
| `design.design_type` | 模型结构 | within→ttest_rel/MixedLM, between→ttest_ind |
| `cleaning.rt_lower` | `df = df[df['rt'] > {value}]` | 数值替换 |
| `cleaning.rt_upper` | `df = df[df['rt'] < {value}]` | 数值替换 |
| `cleaning.accuracy_min` | `subj_acc >= {value}` | 数值替换 |
| `cleaning.trial_exclusion` | `abs(rt-mean) > {value}*std` | SD倍数 |
| `cleaning.missing_policy` | listwise→`dropna()`, mice→`IterativeImputer` | 分支 |
| `model.seed` | `np.random.seed({value})` | 直接替换 |
| `model.contrast` | `"contrast_coding": "{value}"` → patsy | treatment/sum/helmert |
| `model.correction` | `multipletests(pvals, method='{value}')` | bonferroni/fdr_bh |
| `output.save_path` | `plt.savefig("{value}/fig1.png")` | 路径拼接 |
| `output.report_format` | Jupyter notebook 或 Quarto | ipynb/qmd |
| `output.figures` | 条件分支 | raincloud/boxplot/interaction/scatter |
| `output.effect_sizes` | 条件分支 | cohens_d/eta_squared/r2 |

## 公式构建规则

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
| `read_csv()` | `pd.read_csv()` |
| `filter()` | `df[df['col'] > x]` |
| `group_by() %>% summarise()` | `df.groupby().agg()` |
| `mutate()` | `df['new'] = ...` |
| `t.test(paired=TRUE)` | `scipy.stats.ttest_rel()` |
| `t.test(var.equal=FALSE)` | `scipy.stats.ttest_ind()` |
| `aov_ez()` | `pingouin.rm_anova()` |
| `lmer()` | `statsmodels.MixedLM()` |
| `glmer(binomial)` | `statsmodels.Logit()` + manual RE |
| `shapiro.test()` | `scipy.stats.shapiro()` |
| `leveneTest()` | `scipy.stats.levene()` |
| `cohens_d()` | `pingouin.compute_effsize(eftype='cohen')` |
| `eta_squared()` | `pingouin.anova(detailed=True)` |
| `emmeans()` | `statsmodels.stats.multicomp.pairwise_tukeyhsd()` |
| `ggplot2` | `seaborn` + `matplotlib` |
| `ggsave()` | `plt.savefig()` |
| `sessionInfo()` | `sys.version` + `!pip freeze` |

## 模型选择决策树

同 R 平台，见 `r/mapping/README.md`。
