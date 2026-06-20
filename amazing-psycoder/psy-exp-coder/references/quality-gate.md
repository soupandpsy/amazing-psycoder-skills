# Post-Generation Quality Gate

**Authoritative source.** This file is the single source of truth for the code generation quality gate. Both `psy-exp-coder` and `psy-exp-reviewer` reference this file — the coder applies it before delivery, and the reviewer verifies it during audit. Any update here applies to both skills.

## Purpose

After generating experiment code, run this checklist against the output file before presenting it to the user. **Any failure = fix before delivery.**

## The 9 Checks

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
| 9 | **FONT_CONFIG toggle** | If experiment uses Chinese/CJK text, `FONT_AUTO_DETECT`/`MANUAL_FONT_PATH` block is present in the parameters section. |

## Reviewer Integration

When used by `psy-exp-reviewer` during code-audit, these 9 checks form **Gate 0** — the minimum bar. Any failure is automatically classified as a **Critical** issue with severity `not_ready_for_collection`.

### How to verify each check (reviewer supplement)

| # | Pass condition | Verification method |
|---|---------------|-------------------|
| 1 | Code structure matches platform Canonical Skeleton | Compare section-by-section: imports → params → display → preload → trial loop → data save → cleanup. Order and structure must match |
| 2 | Zero occurrences of any pattern in platform spec anti-pattern table | `grep` for each forbidden pattern. See platform-specific anti-pattern lists in reviewer SKILL.md §Platform Anti-Pattern Grep Patterns |
| 3 | API patterns in code come from platform spec canonical skeleton, not paradigms/demo files | Check RT source, keyboard API, timing loop, data save pattern against spec skeleton — not against paradigm .md examples |
| 4 | All editable values in parameter block; no magic numbers | Scan for hardcoded numbers in trial loop: durations, colors, key names, file paths. Every number in trial logic must reference a variable from the params block |
| 5 | Every while loop with Flip/flip/frame-draw includes escape/abort | Count `while` loops in trial section. Count escape checks. Must be equal |
| 6 | Platform-correct RT source | Find where `rt` is assigned. Verify it comes from the correct source for the detected platform |
| 7 | Per-trial data flush; try/finally or try/catch/sca | Find data save call. Is it inside trial loop? Is it wrapped in try/finally? |
| 8 | No stimulus construction inside trial loop | Scan trial loop for `imread`, `ImageStim(`, `MakeTexture`, `Sound(` |
| 9 | CJK text → FONT_CONFIG toggle present | If text contains Chinese/Japanese/Korean, verify FONT_CONFIG block with OS auto-detect exists in params |
