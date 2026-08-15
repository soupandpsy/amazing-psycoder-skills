---
name: amazing-psycoder
description: >-
  Route Amazing PsyCoder requests to the correct psychological experiment or
  behavioral-data analysis stage: Designer, Coder, or Reviewer. Use for
  end-to-end or multi-stage work, ambiguous requests such as “帮我做 Stroop”,
  cross-pipeline work, system-capability questions, or explicit invocations of
  Amazing PsyCoder. Supports PsychoPy, jsPsych, Psychtoolbox, R, and Python.
  For a clearly scoped single-stage request, route directly to the matching
  psy-exp-* or psy-ana-* skill.
---

# Amazing PsyCoder — System Orchestrator

## Version

v1.4.0 — unified standalone and PsyCoder Studio contract, 2026-07-23; direct ExperimentModel@4 and Generation Envelope 4.0 amendment, 2026-08-15. Supports scoped model transactions, bounded AI runtime repair, independent review, and evidence-derived readiness without conflating deployment capability boundaries.

## Purpose

This is the entry point for the Amazing PsyCoder system. It routes work into two sequential pipelines that convert psychological experiments from idea to audited code candidates, and experimental data from raw files to audited analysis artifacts whose readiness is limited by the evidence actually reviewed:

- **Experiment Pipeline**: psy-exp-designer (5-phase design) → psy-exp-coder (code generation) → psy-exp-reviewer (audit)
- **Analysis Pipeline**: psy-ana-designer (5-phase progressive) → psy-ana-coder (R/Python code) → psy-ana-reviewer (audit)

**This skill does NOT generate code itself.** For end-to-end generation, it enforces design → code → review. For an existing artifact, it starts at the highest stage supported by the input: a complete config may go to Coder, and existing code may go directly to Reviewer.

**Platforms**: Claude Code / Codex / Hermes / OpenClaw — follows the [agentskills.io](https://agentskills.io) open standard. See [PLATFORMS.md](PLATFORMS.md) for platform-specific installation and tool mapping.

## Execution Profiles

Use **standalone** unless the caller supplies a validated PsyCoder Studio Generation Envelope 4.0 containing a frozen `ExperimentModel@4.0`, canonical `modelHash`, exact asset manifest, and `assetSetHash`.

- **Standalone Agent Skills host**: load [STANDALONE.md](STANDALONE.md). This profile covers Claude Code, Codex, Hermes, OpenClaw, or another compatible host. Persist YAML/config/code/review artifacts in the user's workspace and adapt actions to the host's available tools. Studio service dependencies and Studio capability flags do not apply.
- **PsyCoder Studio**: load [PSYCODER_STUDIO.md](PSYCODER_STUDIO.md) and the
  machine-readable files under `runtime/`. Those files are authoritative for
  website routing, schemas, generation availability, and package shape.

Never infer the profile from the model vendor. Claude and OpenAI models may be
used in either profile; the input envelope and execution environment decide it.

## Authority and Experiment Semantics

Amazing PsyCoder is maintained professional knowledge, not an infallible or
sole scientific authority. If confirmed design or reproducible evidence
contradicts it, preserve the design, report the conflict, fix and validate the
maintained skill source when in scope, then update downstream bundles.

In Studio, the saved `ExperimentModel@4` is the single experiment fact; the
canvas is its visual projection and may honestly omit unsupported advanced
semantics. Direct edits and Psycoder proposals must become the same validated
model transaction. PsychoPy, jsPsych, and Psychtoolbox compile this same frozen
Model directly. AI may propose model patches and bounded runtime-module repairs,
but cannot add unconfirmed semantics, mutate the frozen Model or asset set, or
claim readiness. In standalone use,
the confirmed `ExperimentSpec` is authoritative. Paradigm references may guide
questions but cannot supply missing executable decisions. Related variants stay
independent unless their complete confirmed semantics are identical.

## System Architecture

### Experiment Pipeline

```
User describes experiment (English / 中文)
       │
       ▼
┌──────────────────────────────────────┐
│ ① psy-exp-designer      │  Orchestration layer
│   Input: natural language description│  5-phase design workflow
│   Output: config YAML + conditions   │  Design Decision Registry
│   Gates: Gate 1→2→3→4→5             │  Progressive confirmation
└──────────────┬───────────────────────┘
               │ saved config YAML + reported path
               ▼
┌──────────────────────────────────────┐
│ ② psy-exp-coder            │  Code generation layer
│   Input: config YAML + conditions    │  Standalone config → target code
│   Output: runnable code + README     │  4-layer priority architecture
│   Gate: 10-item post-generation check│  Canonical Code Skeleton
└──────────────┬───────────────────────┘
               │ Runnable experiment code
               ▼
┌──────────────────────────────────────┐
│ ③ psy-exp-reviewer    │  Audit layer (final mandatory gate)
│   Input: code / config / plan        │  5 review modes
│   Output: audit report + readiness   │  Platform-aware checks
│   Gate: 0 Critical + 0 Major         │  Severity grading
└──────────────────────────────────────┘
```

### Analysis Pipeline

```
User has experiment data + scientific questions
       │
       ▼
┌──────────────────────────────────────┐
│ ④ psy-ana-designer      │  Analysis design layer
│   Input: experiment config + questions│  5-phase progressive confirmation
│   Output: analysis config YAML        │  Estimand + hierarchy method selection
│   Gates: Gate 1→2→3→4→5             │  Method/chart reference inventory
└──────────────┬───────────────────────┘
               │ analysis config YAML
               ▼
┌──────────────────────────────────────┐
│ ⑤ psy-ana-coder              │  Analysis code generation
│   Input: analysis config YAML        │  12-step script structure
│   Output: script + report + lock/pins│  R (tidyverse/lme4/ggplot2)
│   Gate: 10-item Quality Gate         │  Python (pandas/statsmodels/seaborn)
└──────────────┬───────────────────────┘
               │ Runnable analysis script
               ▼
┌──────────────────────────────────────┐
│ ⑥ psy-ana-reviewer      │  Analysis audit layer
│   Input: analysis script + data      │  4 review modes
│   Output: audit report + readiness   │  Statistical correctness checks
│   Gate: 0 Critical + 0 Major         │  Reproducibility scoring
└──────────────────────────────────────┘
```

> **Two independent pipelines. Seven skills total (1 orchestrator + 6 sub-skills). Same rigorous standard.** Experiment: Designer→Coder→Reviewer. Analysis: Designer→Coder→Reviewer.

> **End-to-end generation uses every stage.** Direct review of existing code does not replay upstream stages, but no experiment code is ready for collection and no analysis script is ready for publication without the corresponding Reviewer gate.

### Evidence State Model

Do not collapse pipeline progress into a single “passed” state:

| State | Required evidence | What it permits |
|-------|-------------------|-----------------|
| `design_confirmed` | Saved config + confirmed Decision Registry | Code generation |
| `static_review_passed` | Config/code/conditions reviewed; zero unresolved Critical/Major | Packaging for runtime/execution testing |
| `runtime_or_execution_passed` | Complete reviewed per-test target-machine evidence, or successful analysis run with reviewed outputs/environment | Collection/publication readiness evaluation |
| `ready_for_collection` / `ready_for_publication` | Static pass + runtime/execution evidence + final Reviewer verdict | Intended use |

Every handoff must include artifact paths and the evidence state. Never rely on hidden conversational state as the only copy of a config, registry, report, or test result.

## How to Use This Skill

When a user invokes this skill, **analyze their request** to determine which pipeline and stage they need. The user's own words tell you where to route them — no forced stage-selection question unless their intent is genuinely ambiguous.

### Routing Decision Tree

Route directly based on the user's expressed need:

```
Analyze the user's request — what do they actually want?
  │
  ├─ 🧪 EXPERIMENT — they want to build/design/code/review an experiment
  │
  │   ├─ "I want to build an experiment" / "我要做一个…实验" / "设计一个…范式"
  │   │    → psy-exp-designer (start Phase 1)
  │   │
  │   ├─ "Generate experiment code from this config" / "用这个config生成实验代码"
  │   │    → User has config → psy-exp-coder
  │   │
  │   ├─ "Generate experiment code" / "生成实验代码"  (no config visible)
  │   │    → "你有实验 config YAML 吗？如果没有，需要先通过 psy-exp-designer 设计实验。"
  │   │       Has config → psy-exp-coder
  │   │       No config → psy-exp-designer
  │   │
  │   ├─ "Review this experiment code" / "审计这个实验" / "实验代码有没有问题"
  │   │    → psy-exp-reviewer
  │   │
  │   └─ "Experiment code error" / "实验代码报错"
  │        → Design error → psy-exp-designer
  │           Code error   → psy-exp-coder
  │
  ├─ 📊 ANALYSIS — they want to design/code/review a data analysis
  │
  │   ├─ "Design my analysis" / "设计分析方案" / "用什么统计方法" / "怎么分析这个数据"
  │   │    → psy-ana-designer (start Phase 1)
  │   │
  │   ├─ "Analyze my data" / "分析我的数据" / "帮我做统计分析"
  │   │    → psy-ana-designer (design before code — never jump straight to coder)
  │   │
  │   ├─ "Generate analysis code from this config" / "用这个analysis config生成代码"
  │   │    → User has analysis_config.yaml → psy-ana-coder
  │   │
  │   ├─ "Generate analysis code" / "生成分析代码"  (no config visible)
  │   │    → "你有 analysis_config.yaml 吗？如果没有，需要先通过 psy-ana-designer 设计分析方案。"
  │   │       Has config → psy-ana-coder
  │   │       No config → psy-ana-designer
  │   │
  │   ├─ "Review this analysis" / "审计分析代码" / "检查分析脚本"
  │   │    → psy-ana-reviewer
  │   │
  │   └─ "Analysis script error" / "分析代码报错" / "分析结果不对"
  │        → Design error (wrong method) → psy-ana-designer
  │           Code error (API misuse)    → psy-ana-coder
  │
  ├─ 🔀 CROSS-PIPELINE — experiment done, now want analysis
  │
  │   ├─ "Experiment passed review, now analyze the data" / "实验做完了，分析数据"
  │   │    → psy-ana-designer
  │   │    → "如果有实验 config YAML 可以直接复用；没有的话我帮你手动收集实验信息。"
  │   │
  │   └─ "Build experiment AND analyze" / "设计实验并分析数据"
  │        → psy-exp-designer first → after pipeline completes, remind user to return for analysis
  │
  ├─ ❓ AMBIGUOUS — unclear which pipeline
  │
  │   └─ "帮我做 Stroop" / "I want to do a Stroop study"
  │        → "你需要设计实验程序，还是分析已有数据？"
  │           Build experiment → psy-exp-designer
  │           Analyze data      → psy-ana-designer
  │
  └─ ℹ️ GENERAL
       ├─ "有哪些范式" → Paradigm Coverage Matrix
       ├─ "有哪些分析方法" → method/chart reference inventory summary; do not imply verified implementation coverage
       └─ "这个系统怎么用" → System overview + both pipelines
```

### End-to-End Execution Order

**Experiment Pipeline:**
1. **First**: Invoke `psy-exp-designer` — guide user through 5-phase design (assess → windows & rules → conditions → sequences → validate). Output: experiment config YAML
2. **Second**: Invoke `psy-exp-coder` — generate platform code from config. Output: `.py`/`.js`/`.m` + README
3. **Third**: Invoke `psy-exp-reviewer` — audit the generated code. Output: audit report + readiness label

**Analysis Pipeline:**
1. **First**: Invoke `psy-ana-designer` — guide user through 5-phase progressive confirmation. Output: analysis config YAML
2. **Second**: Invoke `psy-ana-coder` — generate R or Python analysis script. Output: `analysis.R`/`.py` + report
3. **Third**: Invoke `psy-ana-reviewer` — audit the analysis script. Output: audit report + readiness label

**For new end-to-end work, do not skip a step.** Never generate experiment code before the trial window timeline is confirmed. Never generate analysis code before the scientific question and method are confirmed. Existing configs and code may enter at the matching downstream stage.

---

## Design Principles (System-Wide)

| # | Principle | Description | Applies to |
|---|-----------|-------------|------------|
| 1 | **Output is deliverable** | Every phase produces complete, usable artifacts | All |
| 2 | **Progressive confirmation** | Design decisions confirmed phase by phase; defaults flagged ⚠️ | Both Designers |
| 3 | **Decision traceability** | Decision Registry records source of every decision | Both Designers |
| 4 | **Skeleton-first generation** | All code generation MUST start from platform spec Canonical Code Skeleton | Both Coders |
| 5 | **Spec provides logic, adapters provide implementation** | Experiment references suggest questions; only confirmed specs define behavior | Experiment pipeline |
| 6 | **Measurement-invalidating anti-patterns are blocked** | Wrong RT origins, unsafe persistence, or ignored dependence structures cannot pass review | Both Coders & Reviewers |
| 7 | **Evidence, not guarantees** | User owns the design; the system enforces checks and states what remains unverified | All |
| 8 | **Design before code** | No code generation before design is confirmed | Both pipelines |
| 9 | **Post-generation audit mandatory** | All generated code must pass through Reviewer before use | Both Coders & Reviewers |
| 10 | **Input bounds output** | Reviewer's conclusions cannot exceed what the input supports | Both Reviewers |
| 11 | **Scientific question drives method** | Analysis methods chosen by scientific question, not habit | psy-ana-designer |
| 12 | **Proportionate alternatives assessment** | Compare viable methods on decision-relevant dimensions; use the full 12-dimension matrix only when alternatives are genuinely competitive or the choice is high-impact | psy-ana-designer |
| 13 | **Method before code** | Analysis method must be confirmed before generating analysis code | psy-ana-designer, psy-ana-coder |
| 14 | **Recovery path always provided** | Audit reports with Critical/Major issues MUST include explicit fix path back to the correct upstream skill | Both Reviewers |

---

## Red Lines (System-Wide Absolute Prohibitions)

These rules span all six pipeline skills. Violation is never acceptable:

| # | Rule | Owned by | Consequence of violation |
|---|------|---------|--------------------------|
| R1 | **No code generation before trial window timeline is complete** | psy-exp-designer | Structural errors, expensive late-stage fixes |
| R2 | **No assumed response mapping** | psy-exp-designer | Guessing key mapping invalidates accuracy data |
| R3 | **No `time.sleep()` in experiment code** | psy-exp-coder | Blocks event loop, Escape unresponsive |
| R4 | **No `event.getKeys(maxWait=...)`** | psy-exp-coder | Blocks event loop |
| R5 | **No data saved only at experiment end** | psy-exp-coder | Crash = all data lost |
| R6 | **No silent filling of `[MISSING]` values** | psy-exp-designer | Every gap must be resolved by asking user or offering flagged default |
| R7 | **No font-sensitive/CJK stimulus without an explicit font strategy and visual verification** | psy-exp-coder | Glyph coverage and layout depend on the target runtime |
| R8 | **No skipping relevant design decisions** | psy-exp-designer | Exact-reference questions are candidates only; every decision required by the actual design must be confirmed |
| R9 | **No `rt_onset` omitted on response windows** | psy-exp-coder | Missing/incorrect RT onset invalidates all reaction time data |
| R10 | **No collection without Reviewer + smoke pass** | All | Static validation or zero findings alone never proves target-machine runtime readiness |
| R11 | **No analysis method recommendation without an estimand, design hierarchy, and documented alternatives assessment** | psy-ana-designer | Method-first selection risks answering the wrong question |
| R12 | **No analysis code without exclusion provenance + claim-appropriate effect estimates; require a seed only for stochastic steps** | psy-ana-coder | Reproducibility requirements must match the actual computation |
| R13 | **No analysis script delivery without session info output** | psy-ana-coder | Non-reproducible without environment capture |
| R14 | **No declared dependency strategy without its concrete pin/lock artifact** | psy-ana-coder | A strategy label alone cannot recreate the environment |

---

## Code Generation Architecture (4-Layer Priority)

All platforms use the same 4-layer priority stack. When layers conflict, higher always wins:

```
Layer 1: spec/          ← Highest: API spec, anti-patterns, Canonical Code Skeleton
Layer 2: mapping/       ← Structural: config YAML fields → platform code structures
Layer 3: paradigms/      ← Optional design evidence only; never fills missing semantics
Layer 4: demo/          ← Lowest: raw demo code, logic reference only, never API reference
```

**Code generation priority**: confirmed standalone config or frozen Studio ExperimentModel@4 > platform spec and anti-patterns > config/Model→code mapping > optional exact-design reference > demos

Treat `demo/_raw/` and any L3 code block targeting a different/legacy runtime as quarantined: extract only design semantics, never copy API calls, and re-implement against the pinned L1-L2 target.

### Platform Layer Fill Status

| Layer | PsychoPy | jsPsych | Psychtoolbox |
|-------|----------|---------|-------------|
| L1 `spec/` | ✅ | ✅ | ✅ |
| L2 `mapping/` | ✅ | ✅ | ✅ |
| L3 `paradigms/` | ✅ 28 paradigms | ✅ 26 paradigms | ✅ 5 paradigms |
| L4 `demo/_raw/` | ✅ 45 `.py` | ✅ 23 `.js` | ✅ 100 `.md` |

---

## Code Template (Overview)

Experiment generation follows config-driven setup → preload → declared windows/blocks → durable data → cleanup → package. Analysis generation follows confirmed estimand/config → schema/provenance checks → modeling/diagnostics → saved results/environment. Run `validate_experiment.py` or `validate_analysis.py` at the relevant handoffs.

---

## Post-Generation Quality Gate (Overview)

Before delivery, run `scripts/validate_experiment.py`, then pass all 10 checks in [quality-gate.md](psy-exp-coder/references/quality-gate.md). Static success is necessary but never sufficient for collection; Reviewer audit and target-machine smoke tests remain mandatory.

## PsyCoder Studio Compatibility

This skill set defines the professional context and integration contract for [PsyCoder Studio](PSYCODER_STUDIO.md)'s AI generation pipeline. A conforming Studio integration uses a Skill Reference Engine to:

- Route required skill documents by stage + platform, plus an optional exact-design reference when present
- Inject skill context into AI prompts at Interpreter, Code Generator, and Reviewer stages
- Enforce Review Gate semantics: unresolved critical/major issues block artifact packaging
- Record skill version and selected documents in pipeline metadata

See [PSYCODER_STUDIO.md](PSYCODER_STUDIO.md) for full pipeline integration contracts. Repository validation proves those contracts are internally consistent; it does not prove a live Studio deployment or target-machine runtime.

---

## Review Modes and Readiness Labels

### Experiment Review Modes (psy-exp-reviewer)

| Mode | Input | Maximum label |
|------|-------|--------------|
| `code-audit` | Complete experiment code + config; target smoke evidence is required for the final label | `ready_for_collection` only when runtime evidence is reviewed; otherwise `not_ready_for_collection` |
| `config-audit` | Config YAML / trial timeline | `pre_code_ready` |
| `implementation-plan-review` | Pseudocode / architecture plan | `not_applicable` (non-readiness architecture review; a validated config is still required) |
| `triage-only` | Natural-language description | None (missing-info list only) |
| `blocked` | Insufficient input | None (state what's needed) |

### Analysis Review Modes (psy-ana-reviewer)

| Mode | Input | Maximum label |
|------|-------|--------------|
| `analysis-audit` | Complete script + config/data schema | `ready_for_execution` unless successful execution outputs are also reviewed |
| `result-audit` | Script + config + dependency artifact + execution log + generated tables/figures | `ready_for_publication` |
| `plan-review` | Analysis config YAML | `analysis_plan_ready` |
| `triage-only` | Research question | None (missing-info list only) |
| `blocked` | Insufficient input | None |

### Readiness Labels

| Label | Pipeline | Meaning |
|-------|---------|---------|
| `ready_for_collection` | Experiment | Zero Critical + zero Major + target-machine smoke tests passed |
| `ready_for_publication` | Analysis | Zero Critical/Major + clean execution evidence + reviewed tables/figures/environment |
| `ready_for_execution` | Analysis | Static audit passed; run and result verification still required |
| `not_ready_for_collection` | Experiment | Critical/Major issues exist, or target-machine smoke evidence is missing/failed — do NOT collect |
| `not_ready` | Analysis | Critical or Major issues exist |
| `pre_code_ready` | Experiment | Design complete, ready for code generation |
| `analysis_plan_ready` | Analysis | Analysis design complete, ready for code generation |
| `blocked` | Both | Input insufficient for any review |

---

## Severity Classification

| Severity | Definition | Can proceed? |
|----------|-----------|-------------|
| **Critical** | Prevents launch/recovery/safe operation, or systematically invalidates the primary measurement/claim | No — intended use is blocked |
| **Major** | Materially compromises design fidelity, estimates/uncertainty, data recoverability, or independent verification | No — fix and re-audit before formal collection/publication |
| **Minor** | Non-material maintainability/reporting issue that does not alter measurement or claims | Only to the maximum evidence-supported label; document/fix as appropriate |

---

## Paradigm Coverage Matrix

### Core Paradigms (14) — Full Programming-Layer Spec

All 10 required sections filled (When to Use, Core Logic, Must Confirm, Do Not Assume, Condition File Columns, Trial Window Timeline, Data Analysis, Variants, References, Example):

Go/No-go · Navon · Priming · Stroop · Eriksen Flanker · Simon · Rating · Stop-signal · IAT · N-back · Dot-probe · Visual Search · Task Switching · EAST

### Extended Paradigms (24) — Full Programming-Layer Spec

Antisaccade · ANT · BART · Bilingual Stroop · Change Detection · Children Flanker · Choice RT · Climate Reflection · CPT · Corsi Blocks · Cyberball · Delay Discounting · Drag and Drop · Mental Rotation · Multisensory Nature · Numerical Stroop · Phone a Friend · Posner Cuing · Psychophysics Staircase · Rating to Choice · Sternberg · Ultimatum Game · WCST · Writing Distraction

### Paradigm Count Explained

| Layer | Count | What they are |
|-------|-------|---------------|
| Programming paradigms/ | 38 (14 core + 24 extended) | **Design references** for the 5-phase workflow. Apply to ALL platforms |
| Coder psychopy/paradigms/ | 28 | PsychoPy code references with platform-specific generation logic |
| Coder jspsych/paradigms/ | 26 | Legacy logic sources (mostly PsychoJS; code blocks quarantined) |
| Coder psychtoolbox/paradigms/ | 5 | PTB code references; most paradigms use 12-step template for manual adaptation |

---

## Cross-Platform Mandatory API Quick Reference

| Dimension | PsychoPy | jsPsych (pinned 8.x target) | Psychtoolbox |
|-----------|----------|---------------|-------------|
| Keyboard | explicit target-supported `Keyboard` backend | Plugin class references | `KbQueueCreate` + `KbQueueCheck` for time-critical keyboard tasks |
| RT source | selected backend's `key.rt` | pinned plugin's documented `data.rt` | `firstPress - VBLTimestamp` |
| RT origin | `win.callOnFlip(kb.clock.reset)` | Stimulus onset (automatic) | `VBLTimestamp` = `Screen('Flip')` return |
| Timing loop | `CountdownTimer` | `trial_duration` parameter | `vbl + (waitframes-0.5)*ifi` |
| Data save | `try/finally` + per-trial flush | durable `on_data_update` checkpoint + final export | `try/catch` + append/flush/close per trial |
| Quit | Escape check in every timed loop | centralized abort path reachable from every interactive node | Escape included in the KbQueue mask and checked between phases |
| Cleanup | `win.close()` + `core.quit()` | durable checkpoint then `jsPsych.abortExperiment()` for aborts | `sca` + `Priority(0)` + `ShowCursor` |
| CJK font | `FONT_CONFIG` toggle + `TextBox2` | CSS `font-family` | `Screen('TextFont')` + `TextStyle` |

---

## Analysis Platform API Quick Reference

| Dimension | R | Python |
|-----------|-----|--------|
| Data import | `readr::read_csv()` | `pandas.read_csv()` |
| Filtering | `dplyr::filter()` | `df[df['col'] > x]` |
| Grouped stats | `group_by() %>% summarise()` | `df.groupby().agg()` |
| Paired t-test | `t.test(paired=TRUE)` | `scipy.stats.ttest_rel()` |
| Mixed model | `lme4::lmer()` | `statsmodels.MixedLM()` |
| GLMM (binomial) | `lme4::glmer(family=binomial)` | `bambi` / `statsmodels.genmod.bayes_mixed_glm` (within supported scope) |
| Effect size | `effectsize::cohens_d()` / `repeated_measures_d()` | `pingouin.compute_effsize()` |
| Post-hoc | `emmeans::emmeans()` + `pairs()` | `statsmodels.stats.multicomp` |
| Visualization | `ggplot2` + `ggrain` | `matplotlib` + `seaborn` |
| Reproducibility | stochastic step: `set.seed()`; always capture `sessionInfo()` | stochastic step: explicit RNG seed; always capture environment/package versions |

---

## Inter-Skill Communication Protocol

### Experiment Pipeline

**psy-exp-designer → psy-exp-coder:**
- **Artifact**: Complete saved `config.yaml` + Decision Registry; report its path to the user (do not dump raw YAML unless requested)
- **Precondition**: Gate 5 passed (user confirmed full Design Decision Registry)
- **Coder's duty**: Load config → select platform → copy skeleton → map code → Quality Gate → deliver

**Coder → Reviewer:**
- **Artifact**: Generated experiment code (`.py` / `.js` / `.m`) + condition files + README
- **Precondition**: Coder's Post-Generation Quality Gate passed
- **Reviewer's duty**: Detect platform → load corresponding spec → audit each dimension → output graded report + readiness label

### Analysis Pipeline

**Designer → Coder:**
- **Artifact**: `analysis_config.yaml` (saved to working directory)
- **Precondition**: Gate 5 passed (user confirmed full Analysis Decision Registry)
- **Coder's duty**: Phase 0 validate config → confirm language (R/Python) → preview plan → generate code → deliver

**Coder → Reviewer:**
- **Artifact**: Generated analysis script (`analysis.R`/`.py`) + report (`.Rmd`/`.ipynb`)
- **Precondition**: Coder's 10-item Quality Gate passed
- **Reviewer's duty**: Intake → detect platform → Gate 0 grep scan → 5-dimension audit → output graded report + readiness label + recovery path

### Shared Artifacts

| Artifact | Producer | Consumer | Format |
|----------|---------|---------|--------|
| Experiment config YAML | psy-exp-designer | psy-exp-coder, User | Saved `.yaml`; path always reported |
| Condition files | psy-exp-designer | psy-exp-coder | `.xlsx` / `.csv` |
| Experiment code | psy-exp-coder | psy-exp-reviewer | `.py` / `.js` / `.m` |
| Experiment README | psy-exp-coder | psy-exp-reviewer | `.md` |
| Analysis config YAML | psy-ana-designer | psy-ana-coder, User | Saved `.yaml`; path always reported |
| Analysis script | psy-ana-coder | psy-ana-reviewer | `.R` / `.py` |
| Analysis report | psy-ana-coder | psy-ana-reviewer | `.Rmd` / `.ipynb` |
| Audit report | Both Reviewers | User | Markdown (graded + readiness label) |

## Code Output Specification

### Experiment Deliverables

| File | Format | Content |
|------|--------|--------|
| Platform experiment file | `.py` / `.js` / `.m` | Runnable code, all parameters at top, platform-appropriate explicit font strategy if participant-visible CJK is used |
| Experiment README | `.md` | Window sequence, condition/block structure, response rules, data columns, how to run, stable parameter names/sections, known limitations |

### Analysis Deliverables

| File | Format | Content |
|------|--------|--------|
| Analysis script | `.R` / `.py` | Config-driven structure, exclusion provenance, estimates + uncertainty, diagnostics, environment capture; seed only for stochastic steps |
| Analysis report | `.Rmd` / `.ipynb` | Exclusion summary, descriptive stats, model results, figures, environment info |

### Language Consistency

Code comments and README language MUST match the user's language:
- 中文用户 → 中文 README + 中文代码注释
- English user → English README + English code comments

## Resource Routing

The orchestrator stays compact; load only the resources required by the selected stage:

| Need | Authoritative resource |
|------|------------------------|
| Platform capabilities | `PLATFORMS.md` |
| Standalone Claude Code/Codex execution | `STANDALONE.md` |
| PsyCoder Studio execution | `PSYCODER_STUDIO.md` + `runtime/` |
| Experiment design / generation / review | `psy-exp-designer/` → `psy-exp-coder/` → `psy-exp-reviewer/` |
| Analysis design / generation / review | `psy-ana-designer/` → `psy-ana-coder/` → `psy-ana-reviewer/` |
| Deterministic preflight checks | `scripts/validate_experiment.py`, `scripts/validate_analysis.py` |
| Installation | `install.sh` |

---

## When NOT to Use This Skill

- **Quick PsychoPy/jsPsych/PTB API questions**: Answer directly; don't invoke the full workflow
- **Quick R/Python stats questions**: Answer directly; don't invoke the full analysis pipeline
- **General Python/JavaScript/MATLAB/R questions**: Answer directly
- **Non-experiment programming tasks**: Not in scope
- **Data analysis without experiment context**: The analysis pipeline CAN handle standalone data — psy-ana-designer will manually collect experiment information if no config YAML exists
