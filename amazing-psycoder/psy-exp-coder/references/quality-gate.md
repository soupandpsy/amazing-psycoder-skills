# Post-Generation Quality Gate

**Authoritative source.** This file is the single source of truth for the code generation quality gate. Both `psy-exp-coder` and `psy-exp-reviewer` reference this file — the coder applies it before delivery, and the reviewer verifies it during audit. Any update here applies to both skills.

The quality gate operates at two levels: **structural compliance** (17-rule template) and **semantic correctness** (10 checks). Structural failures block delivery before semantic review begins.

## Purpose

After generating experiment code, run both checklists against the output file before presenting it to the user. **Any failure = fix before delivery.**

## Structural Gate: 17-Rule Template Compliance

These checks verify the code follows the structural skeleton defined in the platform spec. All 17 rules must pass before semantic review.

| # | Rule | Check |
|---|------|-------|
| S1 | 分段式骨架 | Code sections appear in documented order. PsychoPy/jsPsych: 9 sections. PTB: 8 sections (collapses text constants into parameters). Section count is platform-specific; order invariants are platform-independent |
| S2 | 文件头三要素 | First 20 lines contain: filename, flow diagram (stage1 → stage2 → stage3), data output paths, key modification log |
| S3 | 配置在前 1/3 | All tunable parameters (timing, keys, paths, constraints) defined before screen initialization |
| S4 | 变量命名三段式 | Config variables use `<STAGE>_<CATEGORY>_<MEANING>` pattern; no bare names like `iti` or `timeout` |
| S5 | 文本常量集中 | All instruction/feedback/prompt text defined as constants in section 3; no inline strings in trial function |
| S6 | 伪随机可配置 | Each constraint = one named constant; `max_tries` prevents infinite loop; failure = exit, never silent fallback |
| S7 | 退出安全网 | `aborted_by_user` flag + `exit_without_saving()` + `cleanup_outputs()` present and called at all exit points |
| S8 | try-except-finally | Main flow has `try` → `except SystemExit` → `except Exception` → `finally` with independent cleanup per operation |
| S9 | 条件表先校验 | Before any trial: column existence, row count, value validity, file existence all checked; failure = exit |
| S10 | 逐 trial 写入 | `nextEntry()` (ExperimentHandler) or `fprintf`+`fclose` (manual) called at end of every trial |
| S11 | 阶段完成即保存 | `saveAsWideText` + `saveAsPickle` called after each experiment stage; not deferred to end |
| S12 | Trial 五步法则 | Trial function body follows: ① present → ② collect → ③ feedback → ④ ITI → ⑤ write data, in order |
| S13 | 过程无硬编码 | Zero bare numbers in trial function body; all values reference named config constants |
| S14 | RT 整数毫秒 | RT stored as `int(timing_source * 1000)`; no floating-point RT in output |
| S15 | 布尔值转 0/1 | All categorical/boolean output columns stored as integers; no `"true"/"false"` strings |
| S16 | 运行时值保存 | All dynamically-generated values (random durations, actual ITI, onset timestamps) written to data |
| S17 | 注释仅解释意图 | No comments that restate what the code does; only design intent, deletion reasons, and non-obvious choices |

## Semantic Gate: The 10 Checks

| # | Check | How to verify |
|---|-------|---------------|
| 1 | **Spec contract used** | Generated code preserves the canonical skeleton's safety/timing/data invariants. Structural adaptation is allowed for the declared paradigm; cargo-cult section order is not required. |
| 2 | **No context-invalid spec anti-patterns** | Scan against the platform spec. Reject hard-invalid patterns (`time.sleep`, `KbCheck` for scored RT, `event.getKeys(maxWait=)`, legacy `jsPsych.init()`). Context-sensitive blocking calls such as `WaitSecs` require semantic review and fail only where flips, input, triggers, deadlines, or abort handling must continue. |
| 3 | **Spec API patterns used** | Paradigm reference files provide candidate questions and failure modes, not authoritative experiment logic or APIs. Window sequence, accuracy, and conditions must trace to the confirmed spec; APIs must trace to the platform contract. |
| 4 | **Design parameters centralized** | Experiment-defining/editable values (durations, mappings, paths, condition rules, display values) are named in config/parameter sections. Local algorithmic constants may remain near their use with rationale. |
| 5 | **Abort remains reachable** | Every loop or asynchronous phase that can wait, draw, poll, or dispatch hardware has a reachable abort path, either directly or through an audited helper; the abort action cannot be mistaken for a scored response. |
| 6 | **RT source verified** | Confirm RT uses the config-declared event and onset reference: PsychoPy key-down = `key.rt` from the selected backend, PTB key-down = `firstPress - VBLTimestamp`, jsPsych = the selected plugin's documented event field. Wall-clock calls may record metadata but cannot substitute for scored RT event timestamps. |
| 7 | **Durable per-trial checkpoint** | Persist after each trial, outside timing-critical windows. PsychoPy: write + `flush`; PTB: append + close/flush; jsPsych: `on_data_update` to server/IndexedDB/localStorage plus final `localSave`. Crash after trial N must leave N recoverable rows. |
| 8 | **Preload outside loop** | No `imread`/`MakeTexture`/`ImageStim()` constructor inside the trial loop. All stimuli created before the loop. |
| 9 | **Participant-visible CJK font contract** | If participant-visible text is CJK, use a platform-appropriate explicit font strategy (bundled/pinned font, verified OS fallback list, or PsychoPy font config) and record target-machine glyph/layout verification. |
| 10 | **Design fidelity** | Verify every declared ratio, factorial cell, sequence constraint, counterbalance rule, task-relevant correct key, and condition-column reference against config + condition files. Construct constrained sets deterministically before shuffling; never rely on weak post-hoc rebalancing. |

## Review Order

1. **Structural gate first** (S1–S17). Structural failures are cheap to detect and expensive to fix after semantic review.
2. **Semantic gate second** (1–10). Classify by impact: wrong RT source → Critical. Missing durable save → Critical. Design divergence → Critical or Major depending on scope.
3. **Minor findings** (CJK font on ASCII-only stimuli, unused helpers, style nits) do not block packaging.

## Reviewer Integration

When used by `psy-exp-reviewer` during code-audit, these checks form **Gate 0**. Classify wrong RT/correct-response sources, missing durable saving, or data-invalidating design divergence as Critical. Classify other failures by impact on the declared primary outcomes, affected trial scope, recoverability, and testability; do not use arbitrary percentage thresholds. Any unresolved Critical/Major failure sets `not_ready_for_collection`.

### How to verify each check (reviewer supplement)

| # | Pass condition | Verification method |
|---|---------------|-------------------|
| 1 | Code preserves the platform skeleton's invariants | Compare setup, preload, timing/response, durable data, abort, and cleanup contracts; allow justified paradigm-specific structure |
| 2 | Zero hard-invalid patterns; context-sensitive warnings have a documented safe use | Scan the authoritative platform table, then inspect each warning in its control-flow and timing context |
| 3 | API patterns in code come from platform spec canonical skeleton, not paradigms/demo files | Check RT source, keyboard API, timing loop, data save pattern against spec skeleton — not against paradigm .md examples |
| 4 | Experiment-defining values are centralized and traceable | Scan for hardcoded durations, mappings, paths, condition rules, and display values; ignore obvious local indices/algorithmic constants with rationale |
| 5 | Abort action remains reachable in every active phase | Inspect loop/callback control flow and any shared abort helper; simple loop-count equality is not sufficient |
| 6 | Platform-correct RT source | Find where `rt` is assigned. Verify it comes from the correct source for the detected platform |
| 7 | Recoverable checkpoint after every completed trial | Verify the platform-specific persistence path and force-quit recovery; in-memory jsPsych data and end-only `localSave` do not pass |
| 8 | No stimulus construction inside trial loop | Scan trial loop for `imread`, `ImageStim(`, `MakeTexture`, `Sound(` |
| 9 | Participant-visible CJK text → font strategy present | Inspect rendered stimulus/instruction strings rather than comments or docstrings; verify explicit font selection and target-machine glyph/layout evidence |
| 10 | Every config invariant matches condition files and code | Count each declared ratio/factorial cell, scan sequence constraints, verify task-relevant correct-key derivation and exact field names, and compare counterbalance logic with the confirmed registry |
