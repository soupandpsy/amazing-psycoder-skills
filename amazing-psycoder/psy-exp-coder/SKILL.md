---
name: psy-exp-coder
description: >-
  Generate, modify, or debug runnable psychological experiment code when a
  completed experiment config YAML or concrete existing code is available.
  Use for PsychoPy/Python, jsPsych/JavaScript, or Psychtoolbox/MATLAB timing,
  stimuli, condition files, trial loops, data saving, hardware integration,
  CJK text, runtime errors, and targeted code changes. Do not invent unresolved
  experimental design choices or issue readiness verdicts; route those to
  psy-exp-designer or psy-exp-reviewer.
---

# Experiment Coder

## Version

v1.4.0 — unified evidence-gated contract, 2026-07-23. Sub-skill of [amazing-psycoder](../SKILL.md).

## Purpose

Generate a runnable delivery candidate from a confirmed config, or modify/debug concrete existing code without silently redesigning the experiment. See [Platform Support Status](#platform-support-status) for the evidence boundary of each target.

## Intake Modes

| Mode | Minimum input | Design gate |
|------|---------------|-------------|
| `generate` | Saved validated config + conditions + confirmed Decision Registry | Designer Gate 5 required |
| `modify` | Existing code + requested behavioral change | Gate 5 not replayed; require config/clarification only when the change alters design semantics |
| `debug` | Existing code + observed error/log/reproduction context | Gate 5 not replayed; preserve behavior unless the root cause is a design defect |

State the selected mode. Never reject a targeted bug fix merely because the original project lacks a PsyCoder config, and never use `modify/debug` to bypass unresolved design choices for a new experiment.

## Design Philosophy

**输出即交付候选。** Generated code must be runnable as-is — not pseudocode — but it is not collection-ready until Reviewer audit and target-machine smoke tests pass. In standalone mode, keep confirmed user-editable values in one named config/parameter section and require revalidation after edits. In Studio mode, the compiler-owned immutable `ExecutionPlan@2.0` is the only experiment-parameter source; generated runtime code must not create a second editable copy of its semantics.

Core principles:
- **用户的实验，系统的规范** — the user owns the design; the system enforces explicit code-quality checks and reports remaining uncertainty
- **骨架先行** — new generated scripts use the platform Canonical Code Skeleton as the validated API baseline. A structural deviation is allowed only when the config requires it, the reason is documented, equivalent safety/timing/data contracts are preserved, and the deviation is specifically tested; `modify`/`debug` need not rewrite unrelated existing architecture.
- **规格提供逻辑，适配器提供 API** — only the confirmed config/ExperimentSpec defines window sequence, stimuli, conditions, correctness, timing, randomization, and data behavior. Paradigm files are optional references, never executable templates. If a reference conflicts with the config, the config wins; if the config is incomplete, stop and return to Designer.
- **反模式零容忍** — block `time.sleep()`, `event.getKeys(maxWait=)`, `KbCheck` for RT, and stimulus/media I/O inside timed windows. Persist trial data immediately after each trial, outside timing-critical windows.
- **代码生成优先级** — confirmed ExperimentSpec/ExecutionPlan > current platform spec and anti-patterns > config→code mapping > optional exact-design reference. A family reference never supplies executable semantics.
- **生成后必经审计** — code generation is not the final step. After delivery, the user MUST run the code through `psy-exp-reviewer` before collecting data. The reviewer is the mandatory quality gate between code generation and data collection.
- **语言与实验内容一致** — user-facing instructions, feedback, UI prose, comments, and README follow the user's language unless the confirmed config says otherwise. Stimuli preserve the confirmed experimental language/content. API tokens, response keys, identifiers, filenames, and data schema are never translated merely to match the conversation language.

> **下一步**: 代码候选生成完成。由 `psy-exp-reviewer` 做静态审计，再在目标机器执行 smoke test；两类证据都通过后才可能标记 `ready_for_collection`。

## Routing

After code generation completes → route to psy-exp-reviewer for mandatory audit. No experiment code proceeds to data collection without passing reviewer audit.

## Language Consistency (Red Line)

User-facing prose must use the language confirmed during the design workflow. Paradigm reference files and config schemas may contain example text in a specific language — these are placeholders showing the concept, not literal text to copy. Scientific stimulus language/content remains a design variable and must be preserved exactly from the confirmed config.

| Content type | Language rule |
|---|---|
| Instruction text, rest prompts, debrief screens | **User's language** |
| Stimulus words/images/audio | **Confirmed stimulus set and language; never auto-translate** |
| Feedback text ("Correct!", "Too slow!"), button labels, UI prose | **User's language unless config declares another participant language** |
| Condition codes, category identifiers, response keys, API constants | **Exact config/runtime values; never translate** |
| Code comments, README | **User's language** |
| Variable names, function names | English (universal) |
| Data column names | Stable schema values (English recommended); do not localize between runs |

Language determination is automatic from the design workflow conversation:

- **中文用户** → 中文指导语/反馈/注释/README；刺激按 confirmed config
- **English user** → English instructions/feedback/comments/README; stimuli follow the confirmed config
- 其他语言同理；如果参与者语言与开发者会话语言不同，以确认后的参与者语言和刺激材料为准

**Critical:** Never copy instructions or feedback from a paradigm reference without adapting them to the confirmed participant language. Never translate scientific stimuli, key tokens, condition codes, or data fields unless that transformation is an explicit design decision.

## Platform Support Status

All three platforms share the same Generation Pipeline (`ExperimentSpec → ExecutionPlan → Platform Adapter → Code`). Experimental semantics are fixed before the adapter boundary; only platform implementation, packaging, and runtime validation differ. Each platform README documents its implementation details.

| Platform | Status | What to do |
|----------|--------|------------|
| **PsychoPy** | Static reference + validator coverage | Generate a candidate, then verify installed version, display/keyboard timing, data recovery, and full run on target hardware. See [psychopy/](psychopy/) |
| **jsPsych 8.x (exact version pinned in config)** | Static reference + Node syntax coverage | Generate a candidate, then verify core/plugin compatibility, browser/server checkpoint recovery, and full timeline behavior. See [jspsych/](jspsych/) |
| **Psychtoolbox** | Static reference coverage; MATLAB/PTB runtime not guaranteed locally | Generate a candidate, then run MATLAB `checkcode`, sync tests, keyboard/audio checks, and full target-machine smoke test. See [psychtoolbox/](psychtoolbox/) |

All three platforms use the same artifact flow, but evidence levels differ. Describe concrete limitations; “four layers present” is not proof of runtime support.

## Platform Reference

Platform-specific implementation details live in subdirectories. Open the relevant platform README when generating or debugging code:

```
psychopy/          ← 统一生成流水线，4层全满
  README.md        → 平台入口（生成流程 + 强制 API + 范式差异速查）
  spec/            → L1: Canonical Skeleton + API 规范 + 反模式
  mapping/         → L2: Config→代码映射 + 三种窗口模式 + 三版本对照
  paradigms/        → L3: 28 个范式（索引见 paradigms/README.md）
  demo/_raw/       → L4: 45 个 .py

jspsych/           ← 统一生成流水线，4层全满
  README.md        → 平台入口（生成流程 + 强制 API + 平台特性）
  spec/            → L1: Canonical Skeleton + API 规范 + 反模式
  mapping/         → L2: Config→timeline 映射 + legacy→8.x 迁移表
  paradigms/        → L3: 26 个 reference-only legacy 来源（代码块隔离）
  demo/_raw/       → L4: 23 个 .js

psychtoolbox/      ← 统一生成流水线，4层全满
  README.md        → 平台入口（生成流程 + 强制 API + 范式差异速查）
  spec/            → L1: Canonical Skeleton + API 规范 + 反模式 + 入门示例
  mapping/         → L2: Config→MATLAB 映射 + 三种帧循环模式
  paradigms/        → L3: 5 个范式（索引见 paradigms/README.md）
  demo/_raw/       → L4: 100 个 .md（按功能分类）
```

Platform paradigm files may contain candidate design patterns and historical **Code Examples**. Use them only to raise questions and identify risks; the confirmed config supplies all executable semantics. Legacy/mismatched code is neither a runnable template nor correctness evidence.

### 4-Layer Code Generation Architecture (Platform-Independent)

The confirmed config and Decision Registry are the design source of truth. Beneath them, every platform uses the same implementation-reference stack:

```
Layer 1: spec/README.md     ← 当前平台 API/安全/数据契约基线
Layer 2: Config → Code Mapping       ← 结构映射：config YAML 字段 → 平台代码
Layer 3: Paradigm reference files    ← 可选领域提示；不提供或继承可执行语义
Layer 4: Raw demo code               ← 隔离来源：不进入正常生成上下文
```

Config controls experiment semantics. A deterministic ExecutionPlan preserves
those semantics. L1 controls supported implementation contracts; L2 may map but
not change either. L3 may supply questions, risks, and literature context only.
It must not fill missing fields or override the config. L4 and legacy L3 code
never override or supply APIs.

Treat `demo/_raw/` and every L3 code block for a mismatched/legacy runtime as quarantined evidence. Extract only paradigm semantics, discard imports/API calls, and re-implement against the pinned L1-L2 target. Never copy quarantined code into generated output.

**Fill status per platform:**

| Layer | PsychoPy | jsPsych | Psychtoolbox |
|-------|----------|---------|-------------|
| L1 `spec/` | ✅ [psychopy/spec/README.md](psychopy/spec/README.md) | ✅ [jspsych/spec/README.md](jspsych/spec/README.md) | ✅ [psychtoolbox/spec/README.md](psychtoolbox/spec/README.md) |
| L2 `mapping/` | ✅ [psychopy/mapping/README.md](psychopy/mapping/README.md) | ✅ [jspsych/mapping/README.md](jspsych/mapping/README.md) | ✅ [psychtoolbox/mapping/README.md](psychtoolbox/mapping/README.md) |
| L3 `paradigms/` | ✅ 28个 (`psychopy/paradigms/`) | ✅ 26个 (`jspsych/paradigms/`) | ✅ 5个 (`psychtoolbox/paradigms/`) |
| L4 `demo/_raw/` | ✅ 45个 `.py` (`psychopy/demo/_raw/`) | ✅ 23个 `.js` (`jspsych/demo/_raw/`) | ✅ 100个 `.md` (`psychtoolbox/demo/_raw/` by category) |

**All three platforms have reference material for all 4 layers.** The generation flow is identical across platforms. Apply the same priority rule regardless of platform: confirmed semantics > platform adapter contract > optional exact-design evidence > demos.


## Code Template

Every generated experiment script follows this structure, regardless of platform (PsychoPy, jsPsych, Psychtoolbox):

```
1. Imports / dependencies
2. Experiment parameters
   - Standalone: one centralized section mirroring the confirmed config; edits require revalidation
   - Studio: read the compiler-owned immutable plan; do not duplicate editable experimental semantics
   - Include a target-runtime font family/path/fallback strategy when text is font-sensitive (especially CJK), then require visual verification
3. Display setup (window / canvas / screen)
4. Stimulus preloading (outside trial loop)
5. Condition file loading / generation
6. Helper functions
7. Instruction routine when declared
8. Practice routine when declared
9. Main experimental loop generated from `windows[]`/`sequences[]` (primary) or `windows[]`/`blocks[]` (legacy), without inserting undeclared fixation, feedback, rest, or debrief stages
   a. Sequence-level setup (execution mode: once/loop)
   b. Per-sequence: window order + repetition count
   c. Per-trial within loop-mode sequence: windows in order, then feedback/ITI
10. Data saving (incremental, try/finally)
11. Cleanup / quit (always with escape / abort handler)
12. Package as platform file + generate README
```

### Generated Runtime Documentation Contract (MANDATORY)

Every generated executable runtime file (`main.py`, `experiment.js`, or
`main.m`) must contain the exact marker `PSYCODER-COMMENT-CONTRACT: v1` and
these six exact section markers:

1. `SECTION 1: IMMUTABLE DESIGN CONTRACT`
2. `SECTION 2: RUNTIME AND INPUT NORMALIZATION`
3. `SECTION 3: STIMULUS AND TIMING`
4. `SECTION 4: INCREMENTAL DATA CHECKPOINT`
5. `SECTION 5: SEQUENCE AND TRIAL EXECUTION`
6. `SECTION 6: CLEANUP AND ABORT SAFETY`

Each section contains substantive comments that explain **why** the code
preserves the confirmed design, validates/normalizes external inputs, anchors
stimulus onset and RT, checkpoints each completed trial, follows the declared
window/sequence order, and guarantees cleanup plus abort handling. Comments
and docstrings follow the confirmed user/project language. Do not translate
stimuli, identifiers, keys, filenames, or data fields merely for comments.

The contract is documentation-only: it cannot introduce, reinterpret, or
duplicate experiment semantics. Avoid line-by-line narration and generic empty
headings. Repair mode preserves/restores the contract, and Reviewer treats a
missing marker or non-substantive section as a quality-gate failure.

The same file must expose an auditable Canvas projection with the exact marker
`PSYCODER-CANVAS-MAP: v1`, one `CANVAS-SEQUENCE: <stable id>` entry for every
sequence in declared order, and one `CANVAS-WINDOW: <stable id>` entry for each
window in its owning sequence's order. Summaries include the saved name,
execution mode/repetitions, stimulus binding or static content, timing, and
responses. The runtime still consumes the immutable plan; the map is not a
second execution source. Never infer roles such as practice, formal, rest, or
debrief from display labels when the confirmed execution fields say otherwise.

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
- Stable parameter names and the named parameters section (line numbers may be included only after verifying the final file and are not the primary locator)
- Known limitations or assumptions

**Language consistency**: See [Language Consistency (Red Line)](#language-consistency-red-line) above. README/comments and participant-facing prose follow the confirmed language; scientific stimuli and machine-readable tokens follow the config exactly.

## Config-Driven Code Generation

When the user provides a `config.yaml` + condition xlsx files, translate the config directly to platform code using the structure defined in the Code Template above. The user decides the platform — this structure is platform-independent.

### Config → Code Mapping

| Config section | Code generated |
|---------------|----------------|
| `name` | Script docstring |
| `paradigm`, `paradigm_family`, `variant` | Optional metadata and reference lookup only; never select correctness or condition logic |
| `runtime` | Pin framework/core/plugin versions and emit a dependency manifest or lock strategy for the confirmed target environment |
| `stimulus_folder` | Global path prepended to image-file `{column}` references |
| `windows[]` | Trial event loop: each window = one screen update / flip |
| `windows[].content: "{col}"` | Text stimulus or image stimulus from condition row column |
| `windows[].duration: N` | Fixed-duration timer (N ms) |
| `windows[].duration: [min, max]` | Random duration in [min, max] ms |
| `windows[].response: [keys]` | Response collection with timed loop (platform-specific: see implementation guide) |
| `windows[].rt_onset` | Which window's display onset starts the RT clock. `"self"` = this window. A window name = clock reset at that window's display |
| `sequences[]` | Sequence loop (primary format): `execution.mode` = once/loop, `execution.repetitions` for loop, `window_ids` determine per-sequence window order |
| `sequences[].show_in` | Context filter: restrict sequence to practice/formal/rest/debrief |
| `blocks[]` | Block loop + condition file loading **(legacy — use sequences for new designs)** |
| `blocks[].condition_file` | Load condition data from xlsx/csv **(legacy)** |
| `randomization` | Resolve method + `seed_scope`/seed before constructing order; save the resolved seed or realized-order reference with every trial/session |
| `response_rules.correct` | Accuracy evaluation in trial loop |
| `paradigm_config` | Explicit user-confirmed custom logic (SSD staircase, n-back target detection, etc.); compile exactly as specified |
| `display` | Display / window creation parameters |
| `font` | Font specification (family, size, file path); auto-detect CJK font by OS if Chinese text used |
| `audio` | Sound preloading + playback; platform-specific backend selection (PTB for low latency) |
| `participant_info` | Subject ID dialog / form; fields (age, gender, handedness), dropdown lists, session number |
| `output` | Platform-specific durable checkpoint after each trial + final export |

### Validation Before Code Generation

In `generate` mode, run every config rule from [config-schema.md](../psy-exp-designer/references/config-schema.md#validation-rules), then execute `python3 <amazing-psycoder-root>/scripts/validate_experiment.py <config.yaml>`. Do not generate code while it reports an error. In `modify/debug`, validate any available config but do not fabricate one; run code/static checks on the changed artifact and escalate only design-semantic gaps.

Then run these code-generation-specific checks:

1. **Semantic completeness**: Every stimulus binding, condition or derived field, correctness rule, timing rule, randomization constraint, and data field is explicit in the confirmed config. A paradigm reference cannot satisfy this check
2. **Platform compatibility**: The config's `platform` is exactly `psychopy`, `jspsych`, or `psychtoolbox`; load that platform's L1-L2 resources plus an exact optional paradigm reference when available, and state only concrete artifact/runtime limitations
3. **rt_onset resolvable**: Every response window's `rt_onset` maps to a real window name. If `rt_onset` is missing, ask before generating — this is a blocking check
4. **Escape handler**: Every timed loop includes an escape key check. Verify the code template pattern is applied
5. **Incremental save**: `try/finally` block wraps the main experiment loop, with per-trial flush

### Post-Generation Quality Gate (MANDATORY)

Load and run all 10 checks in [references/quality-gate.md](references/quality-gate.md), the single authoritative gate shared with `psy-exp-reviewer`. Fix every failure before delivery and include the results in the handoff.

Also run `python3 <amazing-psycoder-root>/scripts/validate_experiment.py <config.yaml> --code <generated-file>`. A pass means only that deterministic static checks succeeded; never convert it into `ready_for_collection`.

## Output Format

Before `generate` mode, confirm Designer **Gate 5** and saved artifact paths. Do not dump YAML by default, but never hide it: report the config path and show it on request.

When generating code, output:

1. **Trial Window Timeline** — box diagram showing the window sequence with response rules (user-facing)
2. **Condition tables** — xlsx file summary (rows, columns, condition ratios)
3. **Platform experiment file** — runnable code saved with the correct extension (`.py` / `.js` / `.m`); standalone parameters are centralized, while Studio code consumes the immutable plan without a second semantic copy; use a platform-appropriate explicit font strategy when participant-visible CJK text is used, with code comments in the user's language
4. **README file** — companion document describing exact pinned prerequisites, tested target environment, experiment logic, data contract, how to run, parameter locations, and known limitations. Language matches the user's language (中文 or English)
5. **Data output columns** — column names and descriptions per trial
6. **How to Run & Test** — actionable steps embedded in the README:
   - **Install**: platform-specific installation instructions
   - **File structure**: Exact directory layout — where to put the script, condition files, stimulus files, and where data will be saved.
   - **Run**: the exact command to launch the experiment
   - **Test**: Run a full session with a non-production test identity and a unique session/run ID. Check that stimuli appear correctly, keys respond, the centralized abort path cleans up, and a new non-overwriting data file appears in `data/`.
   - **Quick check**: Verify the data CSV has the expected columns and at least one row per trial.
7. **Pre-collection checklist** — things to verify before running subjects:
   - Dependencies (platform version, packages)
   - File structure (where stimuli, data, and scripts live)
   - Parameter locations (stable parameter names/section; optional verified final line numbers)
   - Font configuration appropriate to the platform (for example PsychoPy `FONT_AUTO_DETECT`/`MANUAL_FONT_PATH`, bundled web fonts/CSS, or PTB `Screen('TextFont')`)
   - Known limitations (any assumptions or simplifications)

The config YAML is a persisted handoff artifact. Report its path; display it when requested.

## Debugging & Iteration Loop

When the user reports that generated code has an error or unexpected behavior:

1. **Read the error**: Ask the user to paste the full error message and traceback.
2. **Classify the error**:
   - **ImportError / ModuleNotFoundError** → Missing or mismatched dependency. Add the exact compatible version to the declared dependency file/lock, rebuild the isolated environment, and re-run validation; do not prescribe an unpinned ad-hoc install as the durable fix.
   - **FileNotFoundError** → Missing stimulus file or condition xlsx. Check file paths and `stimulus_folder`.
   - **SyntaxError / NameError** → Bug in generated code. Fix the code and regenerate.
   - **RuntimeError (PsychoPy)** → Usually timing or stimulus issue. Check font paths, image dimensions, units.
   - **No data saved / empty CSV** → `try/finally` block issue. Verify flush logic, check if experiment crashed before finally block.
3. **Fix within the authorized layer**: In `modify`, `debug`, or Studio repair mode, patch the concrete model-owned runtime candidate when that is the requested scope. Never alter the confirmed design or compiler-owned files to make a test pass. If the same defect originates in a reusable adapter or generation rule, record and fix that source separately so later candidates do not repeat it.
4. **Re-test checklist**: After fixing, run static validation and then a new target-machine test with a unique session/run ID; confirm that the prior output was not overwritten.
5. **Update patterns**: If the fix reveals a gap in a maintained implementation guide, adapter, or exact-design reference, update the authoritative source only when it is in scope and validate it separately from the candidate repair.
