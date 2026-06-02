---
name: amazing-psycoder
description: Entry point for the Amazing PsyCoder system. Routes user requests through the mandatory three-skill chain: Programming (5-phase design) → Coder (code generation) → Reviewer (audit). Supports PsychoPy, jsPsych, and Psychtoolbox with 38 paradigm references. Trigger for 心理学实验、实验代码、实验程序、PsychoPy实验、jsPsych实验、psychtoolbox实验、编写实验、生成实验代码、审计实验代码.
version: 1.0
status: stable
---

# Amazing PsyCoder — System Orchestrator

## Version

v1.0 — stable, 2026-05-30.

## Purpose

This is the single entry point for the Amazing PsyCoder experimental skill system. It orchestrates a **mandatory sequential chain** of three sub-skills that convert psychological experiment ideas into audited, production-quality code.

**This skill does NOT generate code itself.** It routes the user through the correct sequence and enforces the chain: Programming → Coder → Reviewer. No step may be skipped.

## System Architecture

```
User describes experiment (English / 中文)
       │
       ▼
┌──────────────────────────────────────┐
│ ① psych-experiment-programming      │  Orchestration layer
│   Input: natural language description│  5-phase design workflow
│   Output: config YAML + conditions   │  Design Decision Registry
│   Gates: Gate 1→2→3→4→5             │  Progressive confirmation
└──────────────┬───────────────────────┘
               │ config YAML (internal artifact, not shown to user)
               ▼
┌──────────────────────────────────────┐
│ ② psych-experiment-coder            │  Code generation layer
│   Input: config YAML + conditions    │  12-step code template
│   Output: runnable code + README     │  4-layer priority architecture
│   Gate: 9-item post-generation check │  Canonical Code Skeleton
└──────────────┬───────────────────────┘
               │ Runnable experiment code
               ▼
┌──────────────────────────────────────┐
│ ③ psych-experiment-code-reviewer    │  Audit layer (final mandatory gate)
│   Input: code / config / plan        │  5 review modes
│   Output: audit report + readiness   │  Platform-aware checks
│   Gate: 0 Critical + 0 Major         │  Severity grading
└──────────────────────────────────────┘
```

> **All three steps are mandatory — none can be skipped.** Programming → Coder → Reviewer. No experiment code is considered complete without passing reviewer audit with `ready_for_collection` or `ready_after_minor_fixes`.

## How to Use This Skill

When a user invokes this skill, determine where they are in the pipeline and route accordingly:

### Routing Decision Tree

```
User request
  │
  ├─ "I want to build an experiment" / "我要做一个…实验"
  │    → Invoke psych-experiment-programming (start Phase 1)
  │
  ├─ "Generate code for this config" / "生成代码"
  │    → Check: has Programming Gate 5 passed?
  │       Yes → Invoke psych-experiment-coder
  │       No  → Route back to psych-experiment-programming first
  │
  ├─ "Review this experiment code" / "审计这个实验"
  │    → Invoke psych-experiment-code-reviewer
  │
  ├─ "I got an error" / "代码报错"
  │    → Check the error type:
  │       Design error → psych-experiment-programming
  │       Code error   → psych-experiment-coder (see Debugging & Iteration Loop)
  │
  ├─ "Review found issues" / "审计不通过" / "代码有问题需要修"
  │    → Check the severity:
  │       Critical/Major issues → Fix in psych-experiment-coder, re-audit after
  │       Minor only → User can collect data; fix when convenient
  │
  ├─ "What paradigms are available?" / "有哪些范式"
  │    → Show [Paradigm Coverage Matrix](#paradigm-coverage-matrix)
  │
  └─ "How does this system work?" / "这个系统怎么用"
       → Show system overview + three-step chain
```

### Mandatory Execution Order

1. **First**: Invoke `psych-experiment-programming` — guide user through 5-phase design. Output: complete config YAML (internal, not shown to user)
2. **Second**: Invoke `psych-experiment-coder` — generate platform code from config. Output: `.py`/`.js`/`.m` + README
3. **Third**: Invoke `psych-experiment-code-reviewer` — audit the generated code. Output: audit report + readiness label

**Never skip a step. Never generate code before the trial window timeline is confirmed.**

---

## Design Principles (System-Wide)

| # | Principle | Description | Applies to |
|---|-----------|-------------|------------|
| 1 | **Output is deliverable** | Every phase produces complete, usable artifacts | All |
| 2 | **Progressive confirmation** | Design decisions confirmed phase by phase; defaults flagged `[ASSUMED]` | Programming |
| 3 | **Decision traceability** | Design Decision Registry records source of every decision | Programming |
| 4 | **Skeleton-first generation** | All code generation MUST start from platform spec Canonical Code Skeleton | Coder |
| 5 | **Paradigms provide logic, skeleton provides API** | Paradigm files define experiment logic; API patterns from spec skeleton | Coder |
| 6 | **Anti-pattern zero-tolerance** | `time.sleep()`, `event.getKeys(maxWait=)`, `KbCheck` for RT, `jsPsych.init()`, `WaitSecs` — blocked | Coder, Reviewer |
| 7 | **Your experiment, our standards** | User owns the experimental design; system guarantees code quality | All |
| 8 | **Window timeline before code** | No code generation before trial window timeline is validated | Programming, Coder |
| 9 | **Post-generation audit mandatory** | All generated code must pass through Reviewer before data collection | Coder, Reviewer |
| 10 | **Input bounds output** | Reviewer's conclusions cannot exceed what the input supports | Reviewer |

---

## Red Lines (System-Wide Absolute Prohibitions)

These rules span all three skills. Violation is never acceptable:

| # | Rule | Owned by | Consequence of violation |
|---|------|---------|--------------------------|
| R1 | **No code generation before trial window timeline is complete** | Programming | Structural errors, expensive late-stage fixes |
| R2 | **No assumed response mapping** | Programming | Guessing key mapping invalidates accuracy data |
| R3 | **No `time.sleep()` in experiment code** | Coder | Blocks event loop, Escape unresponsive |
| R4 | **No `event.getKeys(maxWait=...)`** | Coder | Blocks event loop |
| R5 | **No data saved only at experiment end** | Coder | Crash = all data lost |
| R6 | **No silent filling of `[MISSING]` values** | Programming | Every gap must be resolved by asking user or offering flagged default |
| R7 | **No Chinese/CJK text without explicit font** | Coder | PsychoPy default font lacks CJK glyphs; text renders as tofu (□□□) |
| R8 | **No skipping paradigm Must-Confirm items** | Programming | Unconfirmed items produce broken experiments |
| R9 | **No `rt_onset` omitted on response windows** | Coder | Missing/incorrect RT onset invalidates all reaction time data |
| R10 | **No code delivery without Reviewer pass** | All | All code must pass reviewer audit before data collection |

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

All generated code follows a 12-step structure: imports → parameters → display setup → stimulus preloading → condition loading → helpers → instructions → practice → main loop (blocks → randomization → per-trial windows) → incremental data save → cleanup → package with README. The full template with detailed per-step requirements is in the [coder SKILL.md](psych-experiment-coder/SKILL.md#code-template).

---

## Post-Generation Quality Gate (Overview)

Before delivery, all generated code must pass the 9-item Quality Gate defined in the [coder SKILL.md](psych-experiment-coder/SKILL.md#post-generation-quality-gate-mandatory). Covers: spec skeleton compliance, anti-pattern scan, API patterns, parameter placement, escape handling, RT source, incremental save, preloading, and CJK font config. **Any failure = fix before delivery.**

---

## Review Modes and Readiness Labels

### Review Modes (auto-selected by Reviewer)

| Mode | Input | Maximum label |
|------|-------|--------------|
| `code-audit` | Complete experiment code | `ready_for_collection` |
| `config-audit` | Config YAML / trial timeline | `pre_code_ready` |
| `implementation-plan-review` | Pseudocode / architecture plan | `pre_code_ready` |
| `triage-only` | Natural-language description | None (missing-info list only) |
| `blocked` | Insufficient input | None (state what's needed) |

### Readiness Labels

| Label | Meaning |
|-------|---------|
| `ready_for_collection` | Zero Critical + zero Major — can collect data |
| `ready_after_minor_fixes` | Only Minor issues remain |
| `not_ready_for_collection` | Critical or Major issues exist — do NOT collect |
| `pre_code_ready` | Design complete, ready for code generation |
| `needs_experiment_info` | Key design information missing |
| `blocked` | Input insufficient for any review |

---

## Severity Classification

| Severity | Definition | Can collect data? |
|----------|-----------|-------------------|
| **Critical** | Invalidates all data; must fix before any collection | No |
| **Major** | Degrades data quality; fix before formal collection | No |
| **Minor** | Does not affect data quality; fix when convenient | Yes |

---

## Paradigm Coverage Matrix

### Core Paradigms (14) — Full Programming-Layer Spec

All 10 required sections filled (When to Use, Core Logic, Must Confirm, Do Not Assume, Condition File Columns, Trial Window Timeline, Data Output Columns, Randomization Checks, Common Failure Modes, Example):

Go/No-go · Navon · Priming · Stroop · Eriksen Flanker · Simon · Rating · Stop-signal · IAT · N-back · Dot-probe · Visual Search · Task Switching · EAST

### Extended Paradigms (24) — Programming-Layer Reference Descriptions

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

## Inter-Skill Communication Protocol

### Programming → Coder

- **Artifact**: Complete `config.yaml` (internal, never shown to user)
- **Precondition**: Gate 5 passed (user confirmed full Design Decision Registry)
- **Coder's duty**: Load config → select platform → copy skeleton → map code → Quality Gate → deliver

### Coder → Reviewer

- **Artifact**: Generated experiment code (`.py` / `.js` / `.m`) + condition files + README
- **Precondition**: Coder's Post-Generation Quality Gate passed
- **Reviewer's duty**: Detect platform → load corresponding spec → audit each dimension → output graded report + readiness label

### Shared Artifacts

| Artifact | Producer | Consumer | Format |
|----------|---------|---------|--------|
| config YAML | Programming | Coder | `.yaml` (internal, not displayed) |
| Condition files | Programming | Coder | `.xlsx` / `.csv` |
| Experiment code | Coder | Reviewer, User | `.py` / `.js` / `.m` |
| Experiment README | Coder | Reviewer, User | `.md` (alongside code) |
| Audit report | Reviewer | User | Markdown (graded + readiness label) |

---

## Code Output Specification

### Deliverables

Every code generation produces two files:

| File | Format | Content |
|------|--------|---------|
| Platform experiment file | `.py` / `.js` / `.m` | Runnable code, all parameters at top, `FONT_CONFIG` toggle if CJK used |
| Experiment README | `.md` | Window sequence diagram, condition/block structure, response rules, data columns, how to run, parameter line numbers, known limitations |

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
│   ├── psych-experiment-programming/        ← ① Orchestration layer
│   │   ├── SKILL.md                         ← 5-phase workflow + 10 red lines
│   │   ├── README.md
│   │   ├── paradigms/                       ← 38 paradigm reference files
│   │   └── references/                      ← Design references (config-schema, timing, etc.)
│   ├── psych-experiment-coder/              ← ② Code generation layer
│   │   ├── SKILL.md                         ← Generation flow + 4-layer arch + 9-item gate
│   │   ├── README.md
│   │   ├── psychopy/                        ← PsychoPy (full auto)
│   │   │   ├── spec/README.md               ← Canonical Skeleton + anti-patterns
│   │   │   ├── mapping/README.md            ← Config→code mapping
│   │   │   ├── paradigms/                    ← 27 paradigm references
│   │   │   └── demo/_raw/                   ← 45 demo .py files
│   │   ├── jspsych/                         ← jsPsych
│   │   │   ├── spec/README.md               ← Canonical Skeleton + anti-patterns
│   │   │   ├── mapping/README.md            ← Config→timeline + migration table
│   │   │   ├── paradigms/                    ← 25 paradigm references
│   │   │   └── demo/_raw/                   ← 23 demo .js files
│   │   └── psychtoolbox/                    ← PTB
│   │       ├── spec/README.md               ← Canonical Skeleton + anti-patterns
│   │       ├── mapping/README.md            ← Config→MATLAB + frame loops
│   │       ├── paradigms/                    ← 5 paradigm references
│   │       └── demo/_raw/                     ← 100 API demos by category
│   └── psych-experiment-code-reviewer/      ← ③ Audit layer
│       ├── SKILL.md                         ← 5 review modes + platform-aware audit
│       └── README.md
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
- **General Python/JavaScript/MATLAB questions**: Answer directly
- **Non-experiment programming tasks**: Not in scope
