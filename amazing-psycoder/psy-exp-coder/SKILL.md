---
name: psy-exp-coder
description: Use for generating, modifying, or debugging experiment code across platforms. Receives a completed config YAML and generates platform-specific code using a unified Generation Pipeline. Supports PsychoPy (27 paradigms), jsPsych (25 paradigms), and Psychtoolbox (5 paradigms + 100 demos). Handles timing, stimulus creation (including Chinese text), condition files, trial loops, data saving, and hardware integration. Trigger for 实验代码生成、编写实验、PsychoPy代码、psychopy实验、psychopy报错、psychtoolbox、jspsych / 実験コード生成、サイコパイコード / Experiment-Code generieren, PsychoPy-Code / generer code experience, code PsychoPy.
version: 1.3
status: stable
---

# Experiment Coder

## Version

v1.3 — stable, 2026-06-10. Sub-skill of [amazing-psycoder](../SKILL.md).

## Purpose

Translate a completed experiment config YAML into production-quality platform code. This is the **code generation layer** — it receives a fully specified config (from `psy-exp-designer`) and outputs runnable experiment code for the target platform. See [Platform Support Status](#platform-support-status) for current capabilities.

## Design Philosophy

**输出即交付。** Generated code must be runnable as-is — not a draft, not pseudocode. The user can take the output file and collect data immediately. All editable parameters sit at the top of the script where non-programmers can adjust them without reading logic code. Font configuration uses a `FONT_CONFIG` toggle block so users on any OS can switch between auto-detect and manual path.

Core principles:
- **用户的实验，系统的规范** — the user designed the experiment; the system guarantees code quality
- **骨架先行** — every generated script starts from the platform spec's Canonical Code Skeleton (spec/README.md). The skeleton is the single source of truth for all API patterns. Generated code that diverges structurally from the skeleton is incorrect.
- **范式提供逻辑，骨架提供 API** — paradigm reference files define experiment logic (window sequence, accuracy rules, condition structure). They do NOT define API patterns. If a paradigm file's code example uses `KbCheck` for RT, the spec's `KbQueueCheck` wins.
- **反模式零容忍** — `time.sleep()`, `event.getKeys(maxWait=)`, `KbCheck` for RT, in-loop disk I/O are blocked. The Post-Generation Quality Gate catches violations before delivery.
- **代码生成优先级** — spec canonical skeleton > spec anti-patterns > config→code mapping > paradigm logic > demos (highest to lowest authority)
- **生成后必经审计** — code generation is not the final step. After delivery, the user MUST run the code through `psy-exp-reviewer` before collecting data. The reviewer is the mandatory quality gate between code generation and data collection.
- **语言一致性（最高优先级）** — ALL text in generated code (instructions, stimuli, feedback, UI labels, comments, README) MUST match the user's language from the design workflow. Never copy Chinese/English example text from paradigm references or config schemas into generated output for users of a different language. This rule overrides all paradigm reference examples.

> **下一步**: 代码生成完成。输入 `/psy-exp-reviewer` 并提供生成的实验代码路径进行审计。审计通过 (`ready_for_collection`) 后方可正式采集数据。
> **Next step**: Code generation is complete. Run `/psy-exp-reviewer` with the generated experiment code path for audit. Data collection may only proceed after the audit passes (`ready_for_collection`).

## Routing

After code generation completes → route to psy-exp-reviewer for mandatory audit. No experiment code proceeds to data collection without passing reviewer audit.

## Language Consistency (Red Line)

**This is the highest-priority output rule.** Every string in generated experiment code must use the language the user communicated in during the design workflow (orchestrator Phase 1-5). Paradigm reference files and config schemas may contain example text in a specific language — these are placeholders showing the CONCEPT, not the literal text to generate.

| Content type | Language rule |
|---|---|
| Instruction text, rest prompts, debrief screens | **User's language** |
| Stimulus words, feedback text ("Correct!", "Too slow!") | **User's language** |
| Button labels, category tags, UI elements | **User's language** |
| Code comments, README | **User's language** |
| Variable names, function names | English (universal) |
| Data column names | English (recommended) |

Language determination is automatic from the design workflow conversation:

- **中文用户** → 所有文本用中文（指导语、刺激、反馈、注释、README）
- **English user** → all text in English
- **日本語ユーザー** → all text in Japanese
- **Deutscher Benutzer** → all text in German
- **Utilisateur français** → all text in French

**Critical:** NEVER copy stimulus text, instruction text, or feedback text from paradigm reference files into generated code without translating to the user's language. The paradigm reference's language is accidental — the user's language from the design workflow is authoritative.

## Platform Support Status

All three platforms share the same Generation Pipeline (Config→Code). The flow is identical — only the platform-specific mapping (L2) and code skeleton (L1) differ. Each platform README documents the flow with its platform-specific implementation details.

| Platform | Status | What to do |
|----------|--------|------------|
| **PsychoPy** (2024.x+, Python 3.10+) | 4 layers complete | Generate production-ready code from config YAML. See [psychopy/](psychopy/) |
| **jsPsych** (JavaScript, 7.x) | 4 layers complete | Generate code from config YAML. 25 paradigm files. See [jspsych/](jspsych/) |
| **Psychtoolbox** (MATLAB) | 4 layers complete | Generate code from config YAML. 5 paradigm files + 100 demos. See [psychtoolbox/](psychtoolbox/) |

All three platforms use the unified generation flow documented in their respective README files. Do not treat any platform as "unsupported" — if a platform is requested, apply the same Generation Pipeline using that platform's L1 skeleton and L2 mapping.

## Platform Reference

Platform-specific implementation details live in subdirectories. Open the relevant platform README when generating or debugging code:

```
psychopy/          ← 统一生成流水线，4层全满
  README.md        → 平台入口（生成流程 + 强制 API + 范式差异速查）
  spec/            → L1: Canonical Skeleton + API 规范 + 反模式
  mapping/         → L2: Config→代码映射 + 三种窗口模式 + 三版本对照
  paradigms/        → L3: 27 个范式（索引见 paradigms/README.md）
  demo/_raw/       → L4: 45 个 .py

jspsych/           ← 统一生成流水线，4层全满
  README.md        → 平台入口（生成流程 + 强制 API + 平台特性）
  spec/            → L1: Canonical Skeleton + API 规范 + 反模式
  mapping/         → L2: Config→timeline 映射 + 6.1.0→7.x 迁移表
  paradigms/        → L3: 25 个范式（索引见 paradigms/README.md）
  demo/_raw/       → L4: 23 个 .js

psychtoolbox/      ← 统一生成流水线，4层全满
  README.md        → 平台入口（生成流程 + 强制 API + 范式差异速查）
  spec/            → L1: Canonical Skeleton + API 规范 + 反模式 + 入门示例
  mapping/         → L2: Config→MATLAB 映射 + 三种帧循环模式
  paradigms/        → L3: 5 个范式（索引见 paradigms/README.md）
  demo/_raw/       → L4: 100 个 .md（按功能分类）
```

Each platform paradigm file contains two sections: **Experiment Logic** (window sequence, accuracy rules, condition structure) and **Code Examples** (complete runnable code — but API patterns may be outdated; always defer to the spec's Canonical Skeleton).

### 4-Layer Code Generation Architecture (Platform-Independent)

Every platform uses the same 4-layer priority stack. The layers are identical across platforms — only the **fill status** of each layer varies:

```
Layer 1: spec/README.md     ← 最高优先级：平台 API 规范、反模式表、强制模式
Layer 2: Config → Code Mapping       ← 结构映射：config YAML 字段 → 平台代码
Layer 3: Paradigm reference files    ← 范式逻辑：SSD staircase、match detection、显示布局
Layer 4: Raw demo code               ← 最低优先级：仅参考逻辑，不参考 API 模式
```

When layers conflict, higher layers always take precedence. Lower layers provide logic and algorithms but never override higher-layer API patterns.

**Fill status per platform:**

| Layer | PsychoPy | jsPsych | Psychtoolbox |
|-------|----------|---------|-------------|
| L1 `spec/` | ✅ [psychopy/spec/README.md](psychopy/spec/README.md) | ✅ [jspsych/spec/README.md](jspsych/spec/README.md) | ✅ [psychtoolbox/spec/README.md](psychtoolbox/spec/README.md) |
| L2 `mapping/` | ✅ [psychopy/mapping/README.md](psychopy/mapping/README.md) | ✅ [jspsych/mapping/README.md](jspsych/mapping/README.md) | ✅ [psychtoolbox/mapping/README.md](psychtoolbox/mapping/README.md) |
| L3 `paradigms/` | ✅ 27个 (`psychopy/paradigms/`) | ✅ 25个 (`jspsych/paradigms/`) | ✅ 5个 (`psychtoolbox/paradigms/`) |
| L4 `demo/_raw/` | ✅ 45个 `.py` (`psychopy/demo/_raw/`) | ✅ 23个 `.js` (`jspsych/demo/_raw/`) | ✅ 100个 `.md` (`psychtoolbox/demo/_raw/` by category) |

**All three platforms have all 4 layers filled.** The generation flow is identical across platforms. Apply the same priority rule regardless of platform: spec skeleton > spec anti-patterns > config→code mapping > paradigm logic > demos.


## Code Template

Every generated experiment script follows this structure, regardless of platform (PsychoPy, jsPsych, Psychtoolbox):

```
1. Imports / dependencies
2. Experiment parameters (all editable at top)
   - Include OS detection + font path setup if text stimuli used (esp. CJK)
3. Display setup (window / canvas / screen)
4. Stimulus preloading (outside trial loop)
5. Condition file loading / generation
6. Helper functions
7. Instruction routine
8. Practice routine (with feedback)
9. Main experimental loop
   a. Block-level setup
   b. Trial randomization
   c. Per-trial: fixation → stimulus → response → feedback → ITI
   d. Block-level feedback (if applicable)
10. Data saving (incremental, try/finally)
11. Cleanup / quit (always with escape / abort handler)
12. Package as platform file + generate README
```

### Code Output: Platform File + README

After generating code, always package it into two deliverable files:

**1. Platform experiment file** — the runnable code saved with the correct extension:

| Platform | Extension | Example |
|----------|-----------|---------|
| PsychoPy | `.py` | `stroop_experiment.py` |
| jsPsych | `.js` (or `.html` if standalone) | `stroop_experiment.js` |
| Psychtoolbox | `.m` | `stroop_experiment.m` |

**2. README file** — a human-readable companion document saved alongside the code:

The README describes the experiment logic and how to run it. It must include:
- Experiment name and paradigm
- Trial window sequence (the box diagram)
- Condition structure (factors, levels, ratio)
- Block structure (practice/formal counts, feedback rules)
- Response rules (key mapping, accuracy logic, deadline)
- Data output columns and their meanings
- How to run (install dependencies, file structure, run command)
- Parameter locations (line numbers of editable parameters)
- Known limitations or assumptions

**Language consistency**: See [Language Consistency (Red Line)](#language-consistency-red-line) above. All text — README, comments, instructions, stimuli, feedback, UI labels — must match the user's language. Do not mix languages.

## Config-Driven Code Generation

When the user provides a `config.yaml` + condition xlsx files, translate the config directly to platform code using the structure defined in the Code Template above. The user decides the platform — this structure is platform-independent.

### Config → Code Mapping

| Config section | Code generated |
|---------------|----------------|
| `name` | Script docstring |
| `paradigm` | Load paradigm knowledge, apply paradigm-specific accuracy logic |
| `stimulus_folder` | Global path prepended to image-file `{column}` references |
| `windows[]` | Trial event loop: each window = one screen update / flip |
| `windows[].content: "{col}"` | Text stimulus or image stimulus from condition row column |
| `windows[].duration: N` | Fixed-duration timer (N ms) |
| `windows[].duration: [min, max]` | Random duration in [min, max] ms |
| `windows[].response: [keys]` | Response collection with timed loop (platform-specific: see implementation guide) |
| `windows[].rt_onset` | Which window's display onset starts the RT clock. `"self"` = this window. A window name = clock reset at that window's display |
| `blocks[]` | Block loop + condition file loading |
| `blocks[].condition_file` | Load condition data from xlsx/csv |
| `response_rules.correct` | Accuracy evaluation in trial loop |
| `paradigm_config` | Paradigm-specific logic (SSD staircase, n-back target detection, etc.) |
| `display` | Display / window creation parameters |
| `font` | Font specification (family, size, file path); auto-detect CJK font by OS if Chinese text used |
| `audio` | Sound preloading + playback; platform-specific backend selection (PTB for low latency) |
| `participant_info` | Subject ID dialog / form; fields (age, gender, handedness), dropdown lists, session number |
| `output` | Data save: filename pattern, incremental flush |

### Validation Before Code Generation

First, run the 9 config-level validation rules from [config-schema.md](../psy-exp-designer/references/config-schema.md#validation-rules). These are authoritative for schema correctness.

Then run these code-generation-specific checks:

1. **Paradigm logic loaded**: The relevant paradigm file (from orchestrator's `paradigms/`) has been read for accuracy rules, timing conventions, and edge cases
2. **Platform compatibility**: The config's `platform` field matches a supported platform. If not PsychoPy, state limitations before generating
3. **rt_onset resolvable**: Every response window's `rt_onset` maps to a real window name. If `rt_onset` is missing, ask before generating — this is a blocking check
4. **Escape handler**: Every timed loop includes an escape key check. Verify the code template pattern is applied
5. **Incremental save**: `try/finally` block wraps the main experiment loop, with per-trial flush

### Post-Generation Quality Gate (MANDATORY)

After generating code, run this checklist against the output file before presenting it to the user. **Any failure = fix before delivery**.

| # | Check | How to verify |
|---|-------|---------------|
| 1 | **Spec skeleton used** | Code structure matches the canonical skeleton from the platform spec (spec/README.md §Canonical Code Skeleton). If the skeleton and the generated code diverge structurally, the skeleton is correct — fix the code. |
| 2 | **No spec anti-patterns** | Scan code against the anti-pattern table in the platform spec. Every forbidden pattern (`time.sleep`, `KbCheck` for RT, `event.getKeys(maxWait=)`, `jsPsych.init()`, `WaitSecs`, etc.) = reject. |
| 3 | **Spec API patterns used** | Paradigm reference files provide experiment logic (window sequence, accuracy rules, condition structure) — NOT API patterns. If any API pattern in the generated code came from a paradigms/demo file rather than the spec canonical skeleton, fix it. |
| 4 | **All parameters at top** | Every editable value (subject ID, durations, key mappings, condition file paths, colors) is in the parameters block. No magic numbers in logic code. |
| 5 | **Escape in every loop** | Every `while` loop that contains `Flip`/`flip`/frame-draw includes an escape/abort check. |
| 6 | **RT source verified** | Confirm RT comes from the correct source for the platform: PsychoPy = `key.rt` (USB HID timestamp), PTB = `firstPress - VBLTimestamp`, jsPsych = `data.rt` (automatic). No manual `clock.getTime()` or `GetSecs()` for RT. |
| 7 | **Incremental save** | Per-trial data flush. Crash after trial N → N rows of data survive. |
| 8 | **Preload outside loop** | No `imread`/`MakeTexture`/`ImageStim()` constructor inside the trial loop. All stimuli created before the loop. |
| 9 | **FONT_CONFIG toggle** | If experiment uses Chinese text, `FONT_AUTO_DETECT`/`MANUAL_FONT_PATH` block is present in the parameters section. |

## Output Format

Before generating code, confirm the programming skill's **Gate 5 (Final Design Review)** has passed — the Trial Window Timeline and full Design Decision Registry have been presented to and confirmed by the user. The config YAML is an internal artifact — do NOT display it to the user.

When generating code, output:

1. **Trial Window Timeline** — box diagram showing the window sequence with response rules (user-facing)
2. **Condition tables** — xlsx file summary (rows, columns, condition ratios)
3. **Platform experiment file** — runnable code saved with correct extension (`.py` / `.js` / `.m`), all editable parameters at the top, FONT_CONFIG toggle block if CJK text used, code comments in the user's language
4. **README file** — companion document describing experiment logic (window sequence, conditions, blocks, response rules, data columns, how to run, parameter locations, known limitations). Language matches the user's language (中文 or English)
5. **Data output columns** — column names and descriptions per trial
6. **How to Run & Test** — actionable steps embedded in the README:
   - **Install**: platform-specific installation instructions
   - **File structure**: Exact directory layout — where to put the script, condition files, stimulus files, and where data will be saved.
   - **Run**: the exact command to launch the experiment
   - **Test**: Run a full session as a fake subject (use subject ID "test"). Check that stimuli appear correctly, keys respond, Escape quits, and a CSV file appears in `data/`.
   - **Quick check**: Verify the data CSV has the expected columns and at least one row per trial.
7. **Pre-collection checklist** — things to verify before running subjects:
   - Dependencies (platform version, packages)
   - File structure (where stimuli, data, and scripts live)
   - Parameter locations (every editable parameter with its line number)
   - Font configuration (FONT_AUTO_DETECT / MANUAL_FONT_PATH switch)
   - Known limitations (any assumptions or simplifications)

The config YAML is passed silently from orchestrator to coder — it is never displayed to the user.

## Debugging & Iteration Loop

When the user reports that generated code has an error or unexpected behavior:

1. **Read the error**: Ask the user to paste the full error message and traceback.
2. **Classify the error**:
   - **ImportError / ModuleNotFoundError** → Missing dependency. Tell user to `pip install <package>`.
   - **FileNotFoundError** → Missing stimulus file or condition xlsx. Check file paths and `stimulus_folder`.
   - **SyntaxError / NameError** → Bug in generated code. Fix the code and regenerate.
   - **RuntimeError (PsychoPy)** → Usually timing or stimulus issue. Check font paths, image dimensions, units.
   - **No data saved / empty CSV** → `try/finally` block issue. Verify flush logic, check if experiment crashed before finally block.
3. **Fix the root cause, not the symptom**: If a font path is wrong, fix the auto-detection logic. If a key mapping is backwards, fix the config→code mapping. Don't patch the generated code — fix the generation rules so future experiments don't hit the same bug.
4. **Re-test checklist**: After fixing, ask the user to re-run with subject ID "test2" and confirm the fix.
5. **Update patterns**: If the fix reveals a gap in the implementation guide or a paradigm file, update those files so the fix is permanent.
