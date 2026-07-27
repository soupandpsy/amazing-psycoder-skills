---
name: psy-ana-designer
description: >-
  Design a behavioral-psychology data analysis plan and produce a confirmed
  analysis config YAML. Use for scientific-question formulation, data-structure
  intake, statistical-method selection, analysis plans, cleaning/exclusion
  rules, effect sizes, assumption checks, sensitivity analyses, and figure
  choices, including “数据该怎么分析/用什么统计方法”. Compare viable methods
  before the user chooses. Do not generate or audit R/Python code; use
  psy-ana-coder or psy-ana-reviewer for those stages.
---

# Analysis Designer

## Version

v1.4.0 — unified evidence-gated contract, 2026-07-23. Sub-skill of [amazing-psycoder](../SKILL.md).

## Purpose

Transform experimental data and scientific questions into a complete analysis plan. Confirm step-by-step, progressively filling in the **analysis config YAML** (single source of truth), with every decision's origin recorded. Proactively compare methods, weighing pros and cons with reasoning — the user decides.

Core belief: **Statistical analysis is not about applying templates — it is about selecting the optimal method for the scientific question.**

## When Not to Use

- Generating code: `psy-ana-coder`
- Auditing code: `psy-ana-reviewer`
- Designing experiments: `psy-exp-designer`

## Design Philosophy

- **Scientific question driven** — Understand the question first, then choose the tool
- **Data determines method** — Design type, variables, and distribution characteristics determine the analysis approach
- **Progressive confirmation** — Fill specific config sections at each phase; Gates cannot be skipped; default items marked `[ASSUMED]`, reviewed at Gate 5
- **Traceable decisions** — Every item annotated with its source: `用户确认` / `范式惯例` / `通用默认` / `自动推断`
- **Proportionate alternatives assessment** — Compare genuinely viable methods on the dimensions that can change the decision; use the full 12-dimension matrix for high-impact or closely competing choices
- **Ask before selecting** — Confirm fundamental data characteristics before recommending methods

## Red Lines

| # | Rule |
|---|------|
| 1 | Do not recommend analysis methods until the scientific question is understood |
| 2 | Do not finalize method selection until fundamental data characteristics are confirmed |
| 3 | Every method selection must state the estimand, data hierarchy, viable alternatives considered, and why the selected method answers the question; do not manufacture a false A-vs-B choice |
| 4 | All data exclusion rules must be confirmed by the user |
| 5 | Offer user choice only among scientifically viable options; do not implement an unsuitable method merely because the user prefers it |

## Analysis Config as Single Source of Truth

Use [references/config-schema.md](references/config-schema.md) as the canonical schema. Fill `analysis_mode`, `experiment`, `design`, `questions`, `cleaning`, `model`, and `output` progressively. Save the YAML at final handoff and report its path; do not dump it by default, but show it on request.

## Question Protocol

Each phase follows:

1. **Show current state** — List confirmed and unconfirmed items (decision checklist format, do not display YAML)
2. **At most 3 questions per round** — Prioritize questions that unlock the most downstream decisions. Complex phases (Phase 3/4) may be split into multiple rounds; keep each round focused
3. **Write answers into config** — Update immediately, show changes
4. **Output phase decision checklist** — Table format, each item annotated with source
5. **Advance after user confirmation** — "以上确认无误，进入下一阶段？"
6. **Mark default items** — Inferred and default values marked ⚠️, uniformly reviewed at Gate 5
7. **Gates cannot be skipped** — If a preference conflicts with the estimand or data hierarchy, explain the consequence and offer viable alternatives; do not force a ceremonial 12-row comparison when it adds no decision value

---

## Phase 1: Understand Experiment and Scientific Questions

**Fill config**: `analysis_mode` · `design` · `experiment.config_path`

**Goal**: Understand what the experiment did, whether the work is confirmatory or exploratory, and what quantity each question aims to estimate.

Confirm `analysis_mode: confirmatory | exploratory | mixed`. For confirmatory questions, distinguish primary, secondary, and manipulation-check outcomes before inspecting condition effects; record alpha and any preregistration reference. For exploratory questions, label them as such rather than presenting post-data choices as preregistered.

### 1.1 Obtain Experiment Config

First confirm the location of the experiment config YAML:
> "请提供实验的 config YAML 文件路径。这个文件通常是 psy-exp-designer 生成的。如果没有，也可以直接描述你的实验设计。"

**When a config file exists**: Auto-extract after reading — do not ask:
- IVs (name, type, number of levels)
- DVs (name, type: rt/acc/score, unit)
- Design type (within/between/mixed)
- Paradigm name

**When no config file**: Collect core information via 3 questions:
> 1. "你的实验有几个自变量（IV）？每个叫什么名字、几个水平？"
> 2. "你的因变量（DV）是什么？测量什么？（RT/准确率/分数）"
> 3. "实验设计是被试内（同一批人做所有条件）还是被试间（不同组做不同条件）？"

After collection, fill the `design` section, annotating source as `用户确认`.

```yaml
# Auto-filled
design:
  ivs: [{name: condition, type: categorical, levels: [congruent, incongruent]}]
  dvs: [{name: rt, type: continuous, unit: ms}, {name: acc, type: binary}]
  design_type: within
```

### 1.2 Follow up on Scientific Questions

> "你的核心研究问题是什么？不是'我要用什么方法'，是'我要回答什么科学问题'。"

If the user says "I want to do ANOVA," follow up: "ANOVA 是方法。你具体想检验什么？"

Guiding example: "Stroop 一致 vs 不一致条件 RT 是否有显著差异？"

If the experiment config has multiple recorded variables, identify which are analyzed outcomes. Do not force an inferential question for logging/quality-control variables.

### 1.3 DV → Question Mapping

| Outcome | Scientific question | Estimand / role |
|---------|---------------------|------------------|
| rt | 一致 vs 不一致 RT 差异？ | Population mean/median contrast; primary |
| accuracy | 条件间反应正确概率是否不同？ | Odds/probability contrast; secondary |

**Gate 1**: Every analyzed outcome has a clear question, estimand, role, and analysis mode. Questions are recorded in `questions[]`; non-analyzed recorded fields need no hypothesis.

**Phase 1 Decision Checklist** (example):

| # | Decision Item | Value | Source |
|---|---------------|-------|--------|
| 1 | Experiment paradigm | Stroop | 自动推断 |
| 2 | Design type | Within-subject | 自动推断 |
| 3 | DV: rt | Continuous, ms | 自动推断 |
| 4 | DV: acc | Binary | 自动推断 |
| 5 | Scientific question Q1 | 一致 vs 不一致 RT 差异 | 用户确认 |
| 6 | Scientific question Q2 | 条件间准确率差异 | 用户确认 |

---

## Phase 2: Understand Data Structure

**Fill config**: `experiment.data_path` · `design` (confirmation)

**Goal**: Confirm what the data looks like — do not assume. **This is the critical foundation for code generation** — data structure determines all downstream data import and cleaning logic.

### 2.1 Data File Organization (Must Confirm First)

> "你的实验数据是怎么存储的？"

Confirm the following step by step — **order cannot be skipped**:

#### 2.1.1 File Hierarchy

> "有多少个被试？每个被试一个数据文件，还是所有被试在一个文件里？"

| Common Scenario | Example | Subsequent Handling |
|----------------|---------|---------------------|
| One file per subject | `sub-001.csv`, `sub-002.csv` … | Batch read + merge, or process per file |
| All subjects in one file | `all_data.csv` | Group by `subject_id` column |
| One file per subject per condition | `sub-001_congruent.csv`, `sub-001_incongruent.csv` | Need to understand filename encoding rules |

#### 2.1.2 File Naming Rules

If one file per subject, **must confirm naming rules** to enable batch reading:

> "数据文件是怎么命名的？例如 `sub-001_stroop.csv`？被试编号在文件名什么位置？"

Example confirmations:
- Naming pattern: `sub-{subject_id}_{task}.csv` or `P{number}_session{1/2}.txt`?
- Subject ID length: fixed width (e.g. 001-099) or variable?
- Any group prefix: `control/sub-001.csv` vs `experimental/sub-001.csv`?

Record in config:
```yaml
experiment:
  data_path: "data/"               # Data directory
  file_pattern: "sub-{subject_id}_stroop.csv"  # File naming pattern
  file_format: "csv"               # csv / tsv / txt / xlsx
  multi_file: true                 # Whether multi-file
```

#### 2.1.3 File Format and Reading Method

> "数据文件是什么格式？"

| Format | Confirmation Items | R Read | Python Read |
|--------|--------------------|--------|-------------|
| CSV | Delimiter (`,` `;` `\t`)? Has header? | `readr::read_csv()` | `pd.read_csv()` |
| TSV/TXT | Delimiter (`\t` space)? Encoding? | `readr::read_tsv()` | `pd.read_csv(sep='\t')` |
| Excel | Which sheet? Which row does data start? | `readxl::read_excel()` | `pd.read_excel()` |
| Special format | e.g. Psychopy csv + log mixed | Need to confirm skip rows / extraction rules | Same as above |

If raw data files are available, ask the user to show the first few rows or `str()` output of **at least two subjects'** files to verify structural consistency.

### 2.2 Single-File Data Structure

Confirm the internal data structure of individual files:

#### 2.2.1 Column Names and Variable Mapping

Confirm column names one by one — do not ask irrelevant questions:

> "确认以下列名：被试 ID 列名？条件列名？几个水平？RT 列名？单位 ms/s？正确性列？编码方式？"

For column names inferable from the experiment config, present them directly and only ask about what is uncertain.

> "除了这些核心列，数据文件里还有其他列吗？（如 trial 序号、block 编号、stimulus 文件名等）有的话也告诉我——后续分析可能需要用到。"

#### 2.2.2 Data Structure Verification

Ask the user to show the first few rows of at least 1-2 subjects' files:
> "方便展示一下某个被试数据文件的前几行吗？我确认一下结构。"
> or "在 R 里跑一下 `str(read_csv('sub-001.csv'))` 给我看。"

Verify:
- Whether column names match the user's description
- Whether data types are correct (RT is numeric, not string; condition column is categorical)
- Whether the number of trials per subject per condition matches expectations
- Whether there are extra marker columns (e.g. practice=1 for practice trials)

### 2.3 Design Matrix

Confirm (infer from config as much as possible; only ask what cannot be inferred):
- Within/between? → Read from config
- Trials per condition? Trials per subject?
- Any missing data or dropouts?

**Gate 2**: Data file organization confirmed (file hierarchy + naming rules + format); variable mapping table confirmed; design type confirmed. If multi-file naming rules are not confirmed, do not proceed to Phase 3.

**Phase 2 Decision Checklist** (example):

| # | Decision Item | Value | Source |
|---|---------------|-------|--------|
| 1 | Data file organization | One file per subject, 30 subjects | 用户确认 |
| 2 | File naming pattern | sub-{subject_id}_stroop.csv | 用户确认 |
| 3 | File format | CSV, comma-delimited, with header | 用户确认 |
| 4 | subject_id column name | subject_id | 用户确认 |
| 5 | Condition column + levels | condition, 2 levels (congruent/incongruent) | 用户确认 |
| 6 | RT column + unit | rt, ms | 用户确认 |
| 7 | Accuracy column + coding | acc, 1=correct/0=incorrect | 用户确认 |
| 8 | Trials per subject per condition | ~60 | 用户确认 |
| 9 | Design type | Within-subject | 自动推断 |
| 10 | Additional columns | trial_id, block | 用户确认 |

---

## Phase 3: Confirm Data Characteristics + Match Methods

**Fill config**: `questions[].selected_method` · `questions[].alternatives_considered` · `questions[].rationale` · `questions[].model_formula` · `questions[].dependence_structure` · `model.diagnostics` · conditional `model.seed`

**Goal**: Confirm fundamental data characteristics first, then match analysis methods. This is the core phase.

### 3.1 Data Characteristics and Decision Timing

> "在确定方法之前，先确认几个关于数据的问题："
>
> 1. "RT 分布大概什么样？严重右偏还是大致对称？各条件准确率有没有接近 100% 或 0%？"
> 2. "不同被试之间波动大吗？有没有表现特别异常的（准确率很低/RT 特别快或慢）？"
> 3. "有缺失试次吗？大概比例是多少？"

**If data are available**: inspect schema and prespecified diagnostics directly; do not rely only on subjective descriptions. For confirmatory work, avoid selecting the primary model by peeking at the focal condition effect. Predefine diagnostics and fallback/sensitivity rules, or use blinded/pilot data.

**If data are unavailable**: specify decision rules to execute later instead of guessing the distribution.

**Adjust subsequent method selection based on responses**:

| Evidence | Design implication |
|----------|--------------------|
| RT distribution is incompatible with the prespecified Gaussian-scale estimand/model | Use a prespecified transform/distributional model or label a data-driven change exploratory; compare estimands, not just fit |
| Binary trial accuracy | Use a binomial model that represents repeated observations; ceiling/floor informs diagnostics, not whether the outcome is binary |
| Subject/item/session variation | Represent the sampling/dependence structure with a justified random/correlation/aggregation strategy |
| Missing observations | Identify level, reason, and plausible mechanism; choose handling/sensitivity from evidence, not a universal percentage cutoff |

### 3.2 Method Matching

Auto-match candidates from experiment config design type + data characteristics from Phase 3.1. Before opening any individual card under [methods/](methods/), read [methods/USAGE.md](methods/USAGE.md); cards are provisional references and never override the estimand/hierarchy contract.

**Method Selection Decision Tree**:

```
Start with the estimand and observation hierarchy:
  ├── Continuous RT/score
  │     ├── Subject-level planned contrast → paired/Welch test or repeated-measures model
  │     └── Trial-level repeated observations → LMM or suitable distributional model;
  │           include subject and item/session effects when the sampling design requires them
  ├── Binary trial outcome → binomial GLMM, GEE, or prespecified Bayesian hierarchical model
  ├── Aggregated successes / attempts → binomial or beta-binomial model with denominators
  ├── Continuous proportion strictly inside (0,1), not binomial counts → beta-family model
  ├── Ordinal response → ordinal model preserving order
  ├── Count → Poisson/NB family after dispersion/zero diagnostics
  ├── Correlation with repeated measures → repeated-measures correlation or multilevel model
  ├── Genuine event/censoring time → survival model
  └── Stop-signal SSRT → consensus SSRT estimation (typically integration method) plus
        trigger-failure/assumption diagnostics; this is not ordinary survival analysis
```

| Estimand/data pattern | Viable families to assess (not automatic substitutes) |
|-----------------------|------------------------------------------------------|
| Subject-level planned contrast | Paired/Welch/robust or randomization procedure matched to assignment and target contrast |
| Trial-level continuous repeated outcome | LMM, distributional/robust mixed model, GEE, or justified aggregation; include sampled dependence units |
| Repeated binary outcome | Binomial GLMM, GEE, Bayesian hierarchical model, or justified binomial aggregation; population-average and cluster-specific effects differ |
| Ordinal/count/proportion | Compatible ordinal, count, binomial/beta-binomial, or beta-family model according to support and denominator |
| Genuine event/censoring time | Survival model with estimand and censoring assumptions; never use this row to route SSRT |

### 3.3 Comparative Recommendation

When two or more methods remain genuinely viable, compare them on the dimensions that can change the decision. Use the full 12-dimension matrix for high-impact or closely balanced choices; otherwise document excluded alternatives concisely. Never invent an inferior Candidate A just to satisfy a template.

| Dimension | What to Examine |
|-----------|----------------|
| Statistical power | Which detects effects more easily? Sample size requirements? |
| False positive control | False positive inflation when assumptions violated? |
| Data utilization | Aggregate to means or use all trials? |
| Outlier sensitivity | Do extreme values distort results? |
| Assumption robustness | When normality/homoscedasticity/sphericity violated? |
| Interpretability | Can reviewers understand it? |
| Field acceptance | Recognition level in the field? |
| Effect size comparability | Standardized? Meta-analyzable? |
| Replicability | Method standardized? |
| Extensibility | Easy to add covariates / change design? |
| Sample size constraints | Minimum N? Reliable with small samples? |
| Computational feasibility | Can the user run it? Learning cost? |

Format: decision-relevant comparison + recommendation. The user confirms among viable methods; if a requested method cannot answer the estimand or represent dependence, explain and keep it out of the viable set.

Record decision in config:

```yaml
questions:
  - id: Q1
    question: "一致 vs 不一致条件 RT 差异"
    dv: rt
    role: primary
    estimand: "population mean RT contrast: incongruent - congruent"
    selected_method: lmer
    alternatives_considered: [paired_t_test]
    rationale: "目标是 trial-level population contrast；模型表示被试和刺激抽样，并预先声明残差/收敛诊断"
    model_formula: "rt ~ condition + (1 + condition | subject_id)"
    dependence_structure: "subject random intercept/slope; add item effect when items are sampled/repeated"
```

### 3.4 Multiple Comparisons

When multiple claims may form an inferential family, define that family and confirm a compatible strategy: planned contrasts or hierarchical testing, Tukey for a declared all-pairs family, Holm/Bonferroni for family-wise control, FDR for a declared discovery family, or no adjustment when no multiplicity family is induced and the rationale is explicit.

### 3.5 Random Seed

> "分析里是否包含插补、Bootstrap、置换、模拟、贝叶斯采样或随机优化？如果有，请确认可记录的 seed 与并行/采样设置；如果没有，标记 `stochastic: false`。"

Record whether any step is stochastic. Require `model.seed` for imputation, bootstrap, permutation, simulation, Bayesian sampling initialization, randomized optimization, or similar steps. A seed alone does not guarantee identical results across package versions, hardware, or parallel backends, so also capture environment and deterministic settings. Deterministic analyses may set `model.stochastic: false` without a seed.

**Gate 3**: A method and estimand-compatible formula are selected for every scientific question, alternatives assessment is documented, multiplicity is confirmed, and stochastic steps have a seed strategy.

**Phase 3 Decision Checklist**: Each question's A vs B choice and rationale, multiple comparison scheme. All annotated with source.

---

## Phase 4: Analysis Details

**Fill config**: `cleaning` · `output` · `model.contrast`

**Goal**: Confirm cleaning standards, missing data handling, effect sizes, and figures.

> **About `model.contrast` (contrast scheme) vs `model.correction` (multiple comparison correction)**:  
> - **contrast** controls how factor levels are coded (treatment = compared to reference level, sum = compared to grand mean, helmert = compared to mean of previous levels), affecting coefficient interpretation in summary() output  
> - **correction** records the declared multiplicity strategy and family of claims; it is not restricted to pairwise p-value adjustment
> - There is no universal inferential default. Factor coding follows the estimand/formula, and multiplicity handling follows the declared claim family; unresolved choices return to Phase 3.

### 4.1 Data Cleaning Standards

| Cleaning Item | Common Default | Why |
|---------------|----------------|-----|
| RT lower bound | Task/device/literature-derived ⚠️ | Flag anticipations without pretending one cutoff fits every task |
| RT upper rule | Response deadline or prespecified distributional rule ⚠️ | Preserve timeouts separately from slow valid responses |
| Correct trials only | Primary correct-RT analysis when justified ⚠️ | Retain error trials for error-rate and sensitivity analyses |
| Subject exclusion | Prespecified quality criteria ⚠️ | Avoid choosing a cutoff from the observed effect |
| Trial exclusion | Prespecified/robust strategy ⚠️ | Prefer transparent rules and sensitivity analysis over automatic ±2.5 SD trimming |

Each comes with rationale. Default values marked ⚠️, uniformly reviewed at Gate 5.

### 4.2 Missing Data Handling

Classify missingness by level and reason (planned no-response, trial loss, subject dropout, item missingness). Listwise deletion, likelihood-based handling, imputation, and sensitivity analysis depend on the estimand and plausible missingness mechanism; no universal 5% cutoff decides the method.

### 4.3 Effect Sizes + Figures

Report claim-appropriate estimates with uncertainty: mean/standardized contrasts for Gaussian outcomes, odds/probability contrasts for binary outcomes, and model-based marginal contrasts where appropriate. Mixed-model R² is model fit, not a substitute for the focal effect estimate.

**Figure Selection Decision Tree**:

```
What do you want to show?
  ├── Distribution
  │     └── Within-subject two groups → Raincloud plot (preferred) / Individual connecting lines
  │         Multi-group comparison → Violin plot / Boxplot+scatter / Ridge plot (3+ groups)
  │         Univariate → Histogram / Density plot
  │         Normality check → QQ plot
  │
  ├── Correlation
  │     └── Two continuous variables → Scatter+regression / Correlation ellipse / Marginal distribution
  │         Multi-variable (4+) → Correlation heatmap / Correlogram (3-8)
  │         Large sample >5000 → Hexbin
  │
  ├── Comparison
  │     └── Between-subject multi-group → Bar chart / Lollipop chart / Cleveland dot plot
  │         Pre-post → Dumbbell chart / Slope chart / Individual connecting lines
  │         Multi-variable profile → Radar chart / Parallel coordinates
  │         Interaction → Interaction plot + significance annotation
  │
  ├── Evolution
  │     └── Time series → Line chart / Time series plot (individual+mean)
  │         Categorical change → Alluvial plot / Stacked area chart
  │
  ├── Composition
  │     └── Proportions → Donut chart / Waffle chart / Treemap
  │         Categorical cross → Mosaic plot / Upset plot
  │
  └── Special
        └── Meta-analysis → Forest plot + Funnel plot
            Diagnostic → ROC curve
            Survival → Kaplan-Meier
            Agreement → Bland-Altman
            Network → Network graph / Chord diagram
            Clustering → Dendrogram
            Dimensionality reduction → Biplot
```

Before opening an individual card under [plots/](plots/), read [plots/USAGE.md](plots/USAGE.md). Plot cards are provisional visual reminders, not API specifications or publication evidence.

### 4.4 ggplot2 Core Syntax

Load [references/figure-implementation.md](references/figure-implementation.md) only when translating a selected figure into R/ggplot2 or Python/seaborn APIs.

**Gate 4**: Cleaning standards, missing data strategy, effect sizes, figure types confirmed. All default values marked ⚠️.

**Phase 4 Decision Checklist**: Each default value marked ⚠️, confirmed or modified by user.

---

## Phase 5: Final Review

**Goal**: Summarize all decisions; user gives final confirmation. Do not display YAML — only display the decision registry.

### 5.1 Analysis Decision Registry

| # | Phase | Decision Item | Value | Source |
|---|-------|---------------|-------|--------|
| 1 | Phase 1 | Scientific question Q1 | 一致 vs 不一致 RT | 用户确认 |
| 2 | Phase 1 | DV: rt | Continuous, ms | 自动推断 |
| 3 | Phase 2 | RT column name | rt | 用户确认 |
| 4 | Phase 3 | Q1 selected method/formula | LMM with subject/item structure | 用户确认 |
| 5 | Phase 3 | Viable alternatives/exclusions | paired summary contrast; different estimand | 设计推导 |
| 6 | Phase 3 | Multiplicity | one primary contrast; none | 用户确认 |
| 7 | Phase 4 | RT rule | task/device evidence or preregistered rule; otherwise unresolved | 来源标注 |
| 8 | Phase 4 | Missing strategy | mechanism/level-specific plan + sensitivity when needed | 用户确认 |
| ... | ... | ... | ... | ... |

⚠️ = Default item, please confirm with special attention. Each decision annotated with source.

> "以上所有分析决策确认无误？默认项（标 ⚠️）如需修改请指定编号和新值。"

### 5.2 Assumption Checks + Fallbacks

| Assumption | Test | Fallback if Violated |
|------------|------|----------------------|
| Distribution/model fit | Estimand-appropriate residual/predictive diagnostics; QQ or differences diagnostics when relevant | Prespecified transformation, robust/distributional model, or sensitivity analysis |
| Variance/covariance structure | Checks appropriate to the selected independent, repeated, mixed, GEE, or Bayesian model | Prespecified robust covariance, covariance structure, distributional model, or sensitivity analysis |
| Convergence/identifiability | Optimizer/posterior/singularity diagnostics when the model has these failure modes | Simplification or alternative estimator only under a prespecified, estimand-preserving rule |

### 5.3 Sensitivity Analysis

Plan only sensitivities that address a plausible, claim-relevant uncertainty: influential observations, defensible cleaning rules, missingness assumptions, random/correlation structure, distribution/link, or another genuinely viable estimator. If a sensitivity changes the estimand, label it as a different question rather than a robustness check.

### 5.4 Final Confirmation

□ Scientific question → Method mapping (with comparison rationale)
□ Multiple comparison scheme
□ Cleaning standards + Missing data strategy (⚠️ default items reviewed)
□ Effect sizes + Figures
□ Assumption checks + Fallbacks
□ Claim-relevant sensitivity plan, or documented reason none is needed
□ Analysis config complete (can serve as pre-registration analysis plan)

**Gate 5**: User explicitly confirms all decisions, including R/Python, exact language version, the dependency strategy (Python: exact pins or lockfile; R: `renv.lock`), the concrete dependency artifact path, and target environment. Save analysis config YAML, run `python3 <amazing-psycoder-root>/scripts/validate_analysis.py <analysis_config.yaml>`, resolve every error, report the saved path, and route it to `psy-ana-coder`.

> **Next step**: Analysis plan is complete. Enter `/psy-ana-coder` and provide the `analysis_config.yaml` to that skill to start generating analysis code. You may also enter `/psy-ana-reviewer` first and select `plan-review` mode for a pre-audit of the analysis plan.

---

## Routing

```
Analysis config YAML complete
       │
       ▼
psy-ana-coder (R script generation)
       │
       ▼
psy-ana-reviewer (audit)
```

Do not skip steps.

---

## Comparison Examples

Load [references/comparison-examples.md](references/comparison-examples.md) when the user needs a concrete 12-dimension comparison example for RT or accuracy outcomes.
