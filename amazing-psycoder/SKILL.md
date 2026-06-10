---
name: amazing-psycoder
description: Entry point for the Amazing PsyCoder system. Routes user requests through two mandatory three-skill chains — Experiment: Designer(5-phase design)→Coder→Reviewer, and Analysis: Designer(5-phase progressive)→Coder→Reviewer. Supports PsychoPy, jsPsych, Psychtoolbox (38 paradigms) for experiments; R and Python for data analysis (60 methods + 48 charts). Trigger for 心理学实验、实验代码、PsychoPy实验、编写实验、数据分析、统计分析、analysis plan、生成分析代码、审计实验代码、审计分析代码.
version: 1.3
status: stable
compatibility: Claude Code, Codex, Hermes, OpenClaw (agentskills.io standard)
---

# Amazing PsyCoder — System Orchestrator

## Version

v1.3 — stable, 2026-06-10. Adds analysis pipeline (psy-ana-designer → psy-ana-coder → psy-ana-reviewer).

## Purpose

This is the single entry point for the Amazing PsyCoder system. It orchestrates two **mandatory sequential chains** that convert psychological experiments from idea to audited code, and experimental data from raw files to publication-ready analysis:

- **Experiment Pipeline**: psy-exp-designer (5-phase design) → psy-exp-coder (code generation) → psy-exp-reviewer (audit)
- **Analysis Pipeline**: psy-ana-designer (5-phase progressive) → psy-ana-coder (R/Python code) → psy-ana-reviewer (audit)

**This skill does NOT generate code itself.** It routes the user through the correct sequence and enforces that no step may be skipped.

**Platforms**: Claude Code / Codex / Hermes / OpenClaw — follows the [agentskills.io](https://agentskills.io) open standard. See [PLATFORMS.md](PLATFORMS.md) for platform-specific installation and tool mapping.

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
               │ config YAML (internal artifact, not shown to user)
               ▼
┌──────────────────────────────────────┐
│ ② psy-exp-coder            │  Code generation layer
│   Input: config YAML + conditions    │  12-step code template
│   Output: runnable code + README     │  4-layer priority architecture
│   Gate: 9-item post-generation check │  Canonical Code Skeleton
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
│   Output: analysis config YAML        │  12-dimension method comparison
│   Gates: Gate 1→2→3→4→5             │  60 methods + 48 charts refs
└──────────────┬───────────────────────┘
               │ analysis config YAML
               ▼
┌──────────────────────────────────────┐
│ ⑤ psy-ana-coder              │  Analysis code generation
│   Input: analysis config YAML        │  12-step script structure
│   Output: analysis.R/.py + report    │  R (tidyverse/lme4/ggplot2)
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

> **All steps in both pipelines are mandatory — none can be skipped.** Experiment: Designer → Coder → Reviewer. Analysis: Designer → Coder → Reviewer. No experiment code is complete without passing reviewer audit. No analysis script is publishable without reproducibility audit.

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
       ├─ "有哪些分析方法" → 60 methods + 48 charts summary
       └─ "这个系统怎么用" → System overview + both pipelines
```

### Mandatory Execution Order

**Experiment Pipeline:**
1. **First**: Invoke `psy-exp-designer` — guide user through 5-phase design. Output: experiment config YAML
2. **Second**: Invoke `psy-exp-coder` — generate platform code from config. Output: `.py`/`.js`/`.m` + README
3. **Third**: Invoke `psy-exp-reviewer` — audit the generated code. Output: audit report + readiness label

**Analysis Pipeline:**
1. **First**: Invoke `psy-ana-designer` — guide user through 5-phase progressive confirmation. Output: analysis config YAML
2. **Second**: Invoke `psy-ana-coder` — generate R or Python analysis script. Output: `analysis.R`/`.py` + report
3. **Third**: Invoke `psy-ana-reviewer` — audit the analysis script. Output: audit report + readiness label

**Never skip a step. Never generate experiment code before the trial window timeline is confirmed. Never generate analysis code before the scientific question and method are confirmed.**

---

## Design Principles (System-Wide)

| # | Principle | Description | Applies to |
|---|-----------|-------------|------------|
| 1 | **Output is deliverable** | Every phase produces complete, usable artifacts | All |
| 2 | **Progressive confirmation** | Design decisions confirmed phase by phase; defaults flagged ⚠️ | Both Designers |
| 3 | **Decision traceability** | Decision Registry records source of every decision | Both Designers |
| 4 | **Skeleton-first generation** | All code generation MUST start from platform spec Canonical Code Skeleton | Both Coders |
| 5 | **Spec provides API, reference provides logic** | Paradigms/methods define logic; API patterns from spec | Both Coders |
| 6 | **Anti-pattern zero-tolerance** | Blocking APIs, wrong RT sources, missing random effects — blocked | Both Coders & Reviewers |
| 7 | **Your experiment/analysis, our standards** | User owns the design; system guarantees code quality | All |
| 8 | **Design before code** | No code generation before design is confirmed | Both pipelines |
| 9 | **Post-generation audit mandatory** | All generated code must pass through Reviewer before use | Both Coders & Reviewers |
| 10 | **Input bounds output** | Reviewer's conclusions cannot exceed what the input supports | Both Reviewers |
| 11 | **Scientific question drives method** | Analysis methods chosen by scientific question, not habit | psy-ana-designer |
| 12 | **12-dimension comparison** | Every method choice backed by structured A vs B comparison | psy-ana-designer |
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
| R7 | **No Chinese/CJK text without explicit font** | psy-exp-coder | PsychoPy default font lacks CJK glyphs; text renders as tofu (□□□) |
| R8 | **No skipping paradigm Must-Confirm items** | psy-exp-designer | Unconfirmed items produce broken experiments |
| R9 | **No `rt_onset` omitted on response windows** | psy-exp-coder | Missing/incorrect RT onset invalidates all reaction time data |
| R10 | **No code delivery without Reviewer pass** | All | All code must pass reviewer audit before data collection |
| R11 | **No analysis method recommendation without 12-dimension comparison** | psy-ana-designer | Unexamined method choice risks statistical validity |
| R12 | **No analysis code without seed + exclusion log + effect size** | psy-ana-coder | Missing elements break reproducibility |
| R13 | **No analysis script delivery without session info output** | psy-ana-coder | Non-reproducible without environment capture |

---

## Code Generation Architecture (4-Layer Priority)

All platforms use the same 4-layer priority stack. When layers conflict, higher always wins:

```
Layer 1: spec/          ← Highest: API spec, anti-patterns, Canonical Code Skeleton
Layer 2: mapping/       ← Structural: config YAML fields → platform code structures
Layer 3: paradigms/      ← Paradigm logic: window sequence, accuracy rules, condition structure
Layer 4: demo/          ← Lowest: raw demo code, logic reference only, never API reference
```

**Code generation priority**: spec canonical skeleton > spec anti-patterns > config→code mapping > paradigm logic > demos

### Platform Layer Fill Status

| Layer | PsychoPy | jsPsych | Psychtoolbox |
|-------|----------|---------|-------------|
| L1 `spec/` | ✅ | ✅ | ✅ |
| L2 `mapping/` | ✅ | ✅ | ✅ |
| L3 `paradigms/` | ✅ 27 paradigms | ✅ 25 paradigms | ✅ 5 paradigms |
| L4 `demo/_raw/` | ✅ 45 `.py` | ✅ 23 `.js` | ✅ 100 `.md` |

---

## Code Template (Overview)

All generated code follows a 12-step structure: imports → parameters → display setup → stimulus preloading → condition loading → helpers → instructions → practice → main loop (blocks → randomization → per-trial windows) → incremental data save → cleanup → package with README. The full template with detailed per-step requirements is in the [coder SKILL.md](psy-exp-coder/SKILL.md#code-template).

---

## Post-Generation Quality Gate (Overview)

Before delivery, all generated code must pass the 9-item Quality Gate defined in the [coder SKILL.md](psy-exp-coder/SKILL.md#post-generation-quality-gate-mandatory). Covers: spec skeleton compliance, anti-pattern scan, API patterns, parameter placement, escape handling, RT source, incremental save, preloading, and CJK font config. **Any failure = fix before delivery.**

---

## Review Modes and Readiness Labels

### Experiment Review Modes (psy-exp-reviewer)

| Mode | Input | Maximum label |
|------|-------|--------------|
| `code-audit` | Complete experiment code | `ready_for_collection` |
| `config-audit` | Config YAML / trial timeline | `pre_code_ready` |
| `implementation-plan-review` | Pseudocode / architecture plan | `pre_code_ready` |
| `triage-only` | Natural-language description | None (missing-info list only) |
| `blocked` | Insufficient input | None (state what's needed) |

### Analysis Review Modes (psy-ana-reviewer)

| Mode | Input | Maximum label |
|------|-------|--------------|
| `analysis-audit` | Complete analysis script + data | `ready_for_publication` |
| `plan-review` | Analysis config YAML | `analysis_plan_ready` |
| `triage-only` | Research question | None (missing-info list only) |
| `blocked` | Insufficient input | None |

### Readiness Labels

| Label | Pipeline | Meaning |
|-------|---------|---------|
| `ready_for_collection` | Experiment | Zero Critical + zero Major — can collect data |
| `ready_for_publication` | Analysis | Zero Critical + zero Major — reproducible and complete |
| `ready_after_minor_fixes` | Both | Only Minor issues remain |
| `not_ready_for_collection` | Experiment | Critical or Major issues exist — do NOT collect |
| `not_ready` | Analysis | Critical or Major issues exist |
| `pre_code_ready` | Experiment | Design complete, ready for code generation |
| `analysis_plan_ready` | Analysis | Analysis design complete, ready for code generation |
| `blocked` | Both | Input insufficient for any review |

---

## Severity Classification

| Severity | Definition | Can proceed? |
|----------|-----------|-------------|
| **Critical** | Invalidates all data; must fix before any collection | No — fix before any data collection or publication |
| **Major** | Degrades data quality; fix before formal collection | No — fix before formal data collection (exp) or publication (ana) |
| **Minor** | Does not affect data quality; fix when convenient | Yes — fix when convenient |

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
| Coder psychopy/paradigms/ | 27 | PsychoPy code references with platform-specific generation logic |
| Coder jspsych/paradigms/ | 25 | jsPsych code references with timeline plugins |
| Coder psychtoolbox/paradigms/ | 5 | PTB code references; most paradigms use 12-step template for manual adaptation |

---

## Cross-Platform Mandatory API Quick Reference

| Dimension | PsychoPy | jsPsych (7.x) | Psychtoolbox |
|-----------|----------|---------------|-------------|
| Keyboard | `keyboard.Keyboard(backend='ptb')` | Plugin class references | `KbQueueCreate` + `KbQueueCheck` |
| RT source | `key.rt` (USB HID async) | `data.rt` (automatic) | `firstPress - VBLTimestamp` |
| RT origin | `win.callOnFlip(kb.clock.reset)` | Stimulus onset (automatic) | `VBLTimestamp` = `Screen('Flip')` return |
| Timing loop | `CountdownTimer` | `trial_duration` parameter | `vbl + (waitframes-0.5)*ifi` |
| Data save | `try/finally` + per-trial flush | `on_finish` callback | `try/catch` + `fopen`/`fprintf`/`fclose` |
| Quit | Escape check in every loop | `'escape'` in choices | `KbCheck(KbName('ESCAPE'))` |
| Cleanup | `win.close()` + `core.quit()` | `jsPsych.endCurrentTimeline()` | `sca` + `Priority(0)` + `ShowCursor` |
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
| GLMM (binomial) | `lme4::glmer(family=binomial)` | `statsmodels.Logit()` / `pymer4` |
| Effect size | `effectsize::cohens_d()` / `repeated_measures_d()` | `pingouin.compute_effsize()` |
| Post-hoc | `emmeans::emmeans()` + `pairs()` | `statsmodels.stats.multicomp` |
| Visualization | `ggplot2` + `ggrain` | `matplotlib` + `seaborn` |
| Reproducibility | `set.seed()` + `sessionInfo()` | `np.random.seed()` + `sys.version` |

---

## Inter-Skill Communication Protocol

### Experiment Pipeline

**psy-exp-designer → psy-exp-coder:**
- **Artifact**: Complete `config.yaml` (internal, never shown to user)
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
| Experiment config YAML | psy-exp-designer | psy-exp-coder | `.yaml` (internal) |
| Condition files | psy-exp-designer | psy-exp-coder | `.xlsx` / `.csv` |
| Experiment code | psy-exp-coder | psy-exp-reviewer | `.py` / `.js` / `.m` |
| Experiment README | psy-exp-coder | psy-exp-reviewer | `.md` |
| Analysis config YAML | psy-ana-designer | psy-ana-coder | `.yaml` (saved to disk) |
| Analysis script | psy-ana-coder | psy-ana-reviewer | `.R` / `.py` |
| Analysis report | psy-ana-coder | psy-ana-reviewer | `.Rmd` / `.ipynb` |
| Audit report | Both Reviewers | User | Markdown (graded + readiness label) |

---

## Code Output Specification

### Experiment Deliverables

| File | Format | Content |
|------|--------|--------|
| Platform experiment file | `.py` / `.js` / `.m` | Runnable code, all parameters at top, `FONT_CONFIG` toggle if CJK used |
| Experiment README | `.md` | Window sequence diagram, condition/block structure, response rules, data columns, how to run, parameter line numbers, known limitations |

### Analysis Deliverables

| File | Format | Content |
|------|--------|--------|
| Analysis script | `.R` / `.py` | Config-driven, 12-step structure, seed + exclusion log + effect sizes + session info |
| Analysis report | `.Rmd` / `.ipynb` | Exclusion summary, descriptive stats, model results, figures, environment info |

### Language Consistency

Code comments and README language MUST match the user's language:
- 中文用户 → 中文 README + 中文代码注释
- English user → English README + English code comments

---

## File Structure

```
amazing-psycoder-skills/
├── amazing-psycoder/                       ← Entry orchestrator (this skill)
│   ├── SKILL.md
│   ├── PLATFORMS.md                        ← Platform adapter reference
│   ├── install.sh                          ← Cross-platform installer
│   │
│   │   # === Experiment Pipeline ===
│   ├── psy-exp-designer/        ← ① Experiment design
│   │   ├── SKILL.md                         ← 5-phase workflow + red lines
│   │   ├── README.md
│   │   ├── paradigms/                       ← 38 paradigm reference files
│   │   └── references/                      ← config-schema, timing, data-recording
│   ├── psy-exp-coder/              ← ② Experiment code generation
│   │   ├── SKILL.md                         ← 4-layer arch + 9-item gate
│   │   ├── README.md
│   │   ├── psychopy/                        ← PsychoPy (full auto)
│   │   ├── jspsych/                         ← jsPsych
│   │   └── psychtoolbox/                    ← PTB
│   ├── psy-exp-reviewer/      ← ③ Experiment audit
│   │   ├── SKILL.md                         ← 5 review modes + platform-aware audit
│   │   └── README.md
│   │
│   │   # === Analysis Pipeline ===
│   ├── psy-ana-designer/        ← ④ Analysis design
│   │   ├── SKILL.md                         ← 5-phase progressive + 12-dimension comparison
│   │   ├── README.md
│   │   ├── methods/                         ← 60 analysis method references
│   │   └── plots/                           ← 48 chart type references
│   ├── psy-ana-coder/               ← ⑤ Analysis code generation
│   │   ├── SKILL.md                         ← 12-step script + R↔Python mapping
│   │   ├── README.md
│   │   ├── r/                               ← R platform (spec/mapping/checklist/demo)
│   │   └── python/                          ← Python platform (spec/mapping/checklist/demo)
│   └── psy-ana-reviewer/       ← ⑥ Analysis audit
│       ├── SKILL.md                         ← 4 review modes + reproducibility scoring
│       ├── README.md
│       ├── r/checklist/                     ← R audit checklist
│       └── python/checklist/                ← Python audit checklist
├── docs/                                    ← Multi-language READMEs
│   ├── README_EN.md
│   ├── README_ZH-HANT.md
│   ├── README_JA.md
│   ├── README_DE.md
│   └── README_FR.md
└── README.md                                ← Main README (简体中文)
```

---

## When NOT to Use This Skill

- **Quick PsychoPy/jsPsych/PTB API questions**: Answer directly; don't invoke the full workflow
- **Quick R/Python stats questions**: Answer directly; don't invoke the full analysis pipeline
- **General Python/JavaScript/MATLAB/R questions**: Answer directly
- **Non-experiment programming tasks**: Not in scope
- **Data analysis without experiment context**: The analysis pipeline CAN handle standalone data — psy-ana-designer will manually collect experiment information if no config YAML exists
