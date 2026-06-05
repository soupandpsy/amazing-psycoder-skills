---
name: psych-experiment-code-reviewer
description: Use for reviewing psychological experiment code quality at any stage — from early design idea through completed code. Supports five modes: code-audit (full platform-aware code review with smoke test protocol), config-audit (pre-code design review), implementation-plan-review (architecture review), triage-only (missing-information checklist from natural-language idea), and blocked (insufficient input). Does NOT generate or fix code. Trigger for 检查实验代码、code review、实验程序审查、能不能正式采集、代码有没有问题、check experiment code、实验设计有没有问题、帮我看看这个实验方案.
version: 1.2
status: stable
---

# Psychological Experiment Code Reviewer

## Version

v1.2 — smoke test protocol, data integrity verification, paradigm-specific checks, 2026-06-06.

## Purpose

Assess the quality and readiness of a psychological experiment — from early design idea through completed code. The reviewer adapts its mode to the input available. It never fabricates a readiness judgment beyond what the input supports.

This is the **final mandatory gate** in the experiment development chain. The full chain is **Programming → Coder → Reviewer** — no experiment code should proceed to data collection without passing reviewer audit with `ready_for_collection` or `ready_after_minor_fixes`. It does NOT generate or fix code — it reports issues and recommends next steps.

### What "Production-Ready" Means

Code that passes reviewer audit must meet five conditions:

1. **Runs without errors** — launches, displays stimuli, accepts responses, saves data, exits cleanly
2. **Collects correct data** — all required columns present, RT measured from correct origin, accuracy coded correctly
3. **Does not crash mid-experiment** — try/finally protects data, Escape works in every loop
4. **Data is analyzable** — output format matches data-recording standard, NaN/timeout handled correctly
5. **Experiment logic is correct** — trial sequence matches paradigm, response mapping unambiguous, condition ratios verified

## Integration with Coder Skill

The reviewer cross-references the [psych-experiment-coder](../psych-experiment-coder/SKILL.md) skill's artifacts:

| Coder artifact | Reviewer use |
|---------------|-------------|
| Platform spec Canonical Skeleton | Reference for correct API patterns — compare generated code against skeleton |
| Platform spec anti-pattern table | Checklist of forbidden patterns to scan for |
| Coder Quality Gate (9 items) | Minimum bar — if any gate fails, automatic `not_ready_for_collection` |
| Platform mapping README | Verify config→code mapping correctness |
| Paradigm reference files | Verify experiment logic (window sequence, accuracy rules) matches paradigm |

The reviewer also cross-references the [psych-experiment-programming](../psych-experiment-programming/SKILL.md) skill's artifacts:

| Programming artifact | Reviewer use |
|---------------------|-------------|
| Paradigm `## Common Failure Modes` | Paradigm-specific checks — verify known pitfalls are addressed |
| `references/data-recording.md` | Data output column validation — all 10 base columns present |
| `references/config-schema.md` | Config validation rules — all 9 checks pass before code generation |

## Review Modes

Before reviewing, classify the request into one mode.

| Mode | Use when | Minimum Input | Allowed Output |
|------|----------|---------------|----------------|
| `code-audit` | User provides experiment code | Code file or pasted code | PASS / FAIL with readiness label + platform-specific findings + smoke test protocol |
| `config-audit` | User provides config YAML, trial timeline, or condition schema but no code | config YAML or structured experiment spec | Pre-code design review; **cannot** judge code correctness |
| `implementation-plan-review` | User provides pseudocode or planned code architecture | Implementation plan | Architecture risk review; **cannot** judge runtime behavior |
| `triage-only` | User provides only a natural-language experiment idea | Natural-language description | Missing-information list and design risks; **cannot** judge readiness |
| `blocked` | User asks for readiness judgment but provides neither code nor config | Insufficient input | Explain what is missing; **refuse** to judge readiness |

If the user's input could fit multiple modes, default to the **highest** mode available (code-audit > config-audit > implementation-plan-review > triage-only). If input is insufficient for any productive review, use `blocked`.

## Readiness Labels

| Label | Allowed in mode | Meaning |
|-------|----------------|---------|
| `ready_for_collection` | `code-audit` only | Zero critical or major issues; code matches platform spec skeleton; smoke test passed |
| `ready_after_minor_fixes` | `code-audit` only | Only minor issues remain; smoke-testable but fix before analysis |
| `not_ready_for_collection` | `code-audit`, `config-audit` | Critical or major issues exist; do NOT collect data |
| `pre_code_ready` | `config-audit` only | Config/spec complete and ready for code generation |
| `needs_experiment_info` | `triage-only`, `config-audit` | Key design information is missing |
| `blocked` | `blocked` | Cannot review; input is insufficient |

**Hard rule**: `ready_for_collection` and `ready_after_minor_fixes` require actual code review. If no code was provided, the highest possible label is `pre_code_ready`.

## Scope Limitation Rule

At the start of every review output, state what was and was not reviewed. If no code was provided:

> **Scope**: No experiment code was provided. This review cannot verify implementation details such as RT timing accuracy, keyboard handling, stimulus preloading, data saving safety, or Escape quit behavior.

## Platform Detection (code-audit only)

When code is provided, first detect the platform:

| Signature | Platform |
|-----------|----------|
| `from psychopy import` / `visual.Window` / `keyboard.Keyboard` | PsychoPy |
| `initJsPsych` / `jsPsych.run` / `jsPsychHtmlKeyboardResponse` | jsPsych |
| `PsychImaging` / `Screen('Flip'` / `KbQueueCreate` / `sca` | Psychtoolbox |

Once detected, load the corresponding coder spec for authoritative API patterns:
- PsychoPy → `../psych-experiment-coder/psychopy/spec/README.md`
- jsPsych → `../psych-experiment-coder/jspsych/spec/README.md`
- Psychtoolbox → `../psych-experiment-coder/psychtoolbox/spec/README.md`

Also load the paradigm file from the programming layer for failure mode cross-reference:
- `../psych-experiment-programming/paradigms/{paradigm_name}.md`

If the platform cannot be detected, flag this as a critical issue.

---

## Review Checklist — code-audit

### Gate 0: Coder Quality Gate (minimum bar)

Run the 9-item Quality Gate from the coder SKILL.md first. Any failure = automatic critical issue.

| # | Check | Pass condition | How to verify |
|---|-------|---------------|---------------|
| 1 | Skeleton match | Code structure matches platform Canonical Skeleton | Compare section-by-section: imports → params → display → preload → trial loop → data save → cleanup. Order and structure must match |
| 2 | No anti-patterns | Zero occurrences of any pattern in platform spec anti-pattern table | `grep` for each forbidden pattern. See §Platform Anti-Pattern Grep Patterns below |
| 3 | Spec API patterns used | API patterns in code come from platform spec canonical skeleton, not paradigms/demo files | Check RT source, keyboard API, timing loop, data save pattern against spec skeleton — not against paradigm .md examples |
| 4 | Parameters at top | All editable values in parameter block; no magic numbers | Scan for hardcoded numbers in trial loop: durations, colors, key names, file paths. Every number in trial logic must reference a variable from the params block |
| 5 | Escape in every loop | Every while loop that contains Flip/flip/frame-draw includes an escape/abort check | Count `while` loops in the trial section. Count escape checks. Must be equal |
| 6 | RT source | Platform-correct RT source (see §Platform-Specific Timing & RT) | Find where `rt` is assigned. Verify it comes from the correct source for the detected platform |
| 7 | Incremental save | Per-trial data flush; try/finally or try/catch/sca | Find the data save call. Is it inside the trial loop? Is it wrapped in try/finally? |
| 8 | Preload outside loop | No stimulus construction inside trial loop | Scan trial loop for `imread`, `ImageStim(`, `MakeTexture`, `Sound(` |
| 9 | FONT_CONFIG | CJK text → FONT_CONFIG toggle present | If text contains Chinese/Japanese/Korean characters, verify FONT_CONFIG block with OS auto-detect exists in params section |

### Platform Anti-Pattern Grep Patterns

When auditing code, scan for these exact patterns per platform:

**PsychoPy (14 patterns to scan):**
```
event.getKeys(           ← blocks event loop
event.waitKeys(          ← blocks event loop
kb.waitKeys(             ← blocks event loop in trial
time.sleep(              ← blocks event loop
core.wait(               ← blocks event loop (>5ms)
imread(                  ← inside trial loop = frame drop
ImageStim(               ← inside trial loop = jitter
time.time()              ← wrong RT source
clock.getTime()          ← wrong RT source (use key.rt)
waitRelease=True         ← adds release delay to RT
Keyboard()               ← missing backend='ptb'
.exec(                   ← Pavlovia incompatible
preBuffer=-1             ← missing on Sound()
addLoop(                 ← called before loop runs (not right before)
```

**Psychtoolbox (15 patterns to scan):**
```
WaitSecs(                ← blocks execution (except for ITI pre-trial)
KbWait                   ← blocking, no RT timestamp
KbCheck                  ← inside response loop (use KbQueueCheck)
GetSecs - stimOnset      ← manual RT calculation
input(                   ← invisible in fullscreen
imread(                  ← inside trial loop
MakeTexture(             ← inside trial loop
KbQueueCreate(           ← inside trial loop (should be before)
KbQueueStart(            ← inside trial loop (should be before)
KbQueueFlush             ← MISSING at trial start
SkipSyncTests, 1         ← sync tests skipped
Sound(                   ← high latency audio
DrawText(..., '+'        ← text-based fixation cross
Screen('Flip', w)        ← missing 'when' parameter
Screen('Flip', w, 0)     ← zero when parameter
```

**jsPsych (12 patterns to scan):**
```
jsPsych.init(            ← v7 removed
'html-keyboard-response' ← string plugin type (should be class)
jsPsych.NO_KEYS          ← v7 removed (use "NO_KEYS")
jsPsych.ALL_KEYS         ← v7 removed (use "ALL_KEYS")
timelineVariable('x')    ← missing second argument (should be true)
Date.now()               ← manual RT timing
setTimeout(              ← breaks event loop
setInterval(             ← breaks event loop
XMLHttpRequest           ← in-trial network call
fetch(                   ← in-trial network call
keyCode:                 ← hardcoded keyCode number
.select('col')           ← v7 removed method
```

### 1. Experiment Logic

- [ ] Trial window sequence matches the stated paradigm (compare against paradigm file `## Trial Window Timeline`)
- [ ] Each window has defined content, duration, response rule — no window is ambiguous
- [ ] Correctness rule is unambiguous for every trial type (including no-go/catch/timeout)
- [ ] Condition table covers all factorial combinations
- [ ] Block transitions handled (rest screens, instructions between blocks)
- [ ] Feedback only in practice blocks (unless explicitly designed otherwise)
- [ ] **NEW** Instruction text includes all key mapping information (which key = which answer)
- [ ] **NEW** Debrief/thank-you screen exists and provides clean exit path

### 2. Platform-Specific Timing & RT

**PsychoPy:**
- [ ] `keyboard.Keyboard(backend='ptb')` — not default backend (50-70ms RT error if missing)
- [ ] `win.callOnFlip(kb.clock.reset)` — clock reset at stimulus onset, not before flip
- [ ] `kb.getKeys(waitRelease=False)` — not default True (adds 100-200ms)
- [ ] `key.rt` used for RT — not `kb.clock.getTime()`, not `time.time()`
- [ ] `CountdownTimer` loop for response deadline — not `core.wait()`
- [ ] `win.getFutureFlipTime(clock=routineTimer)` for frame timing — not `trialClock.getTime()`
- [ ] **NEW** `kb.clearEvents()` BEFORE stimulus flip — prevents pre-stimulus key contamination
- [ ] **NEW** `sound.Sound(preBuffer=-1)` if audio used — PTB backend for low latency
- [ ] **NEW** `win.callOnFlip(port.setData, code)` if EEG trigger — trigger AFTER flip, not before
- [ ] **NEW** `thisExp.addLoop(trials)` called right before the loop runs, not at experiment start

**jsPsych:**
- [ ] `initJsPsych()` + `jsPsych.run()` — not `jsPsych.init()`
- [ ] Plugin types are class references — not strings
- [ ] `data.rt` used for RT — no manual `Date.now()` timing
- [ ] `trial_duration` parameter for timing — not `setTimeout`/`setInterval`
- [ ] `"NO_KEYS"` / `"ALL_KEYS"` strings — not `jsPsych.NO_KEYS`
- [ ] **NEW** `preload` plugin as FIRST timeline node — not after stimuli
- [ ] **NEW** `'escape'` in `choices` array for every response trial, or escape check in `on_finish`
- [ ] **NEW** `jsPsych.data.get().localSave('csv', filename)` in `on_finish` — not in trial callbacks
- [ ] **NEW** `timeline_variables` pre-computed at script load — not generated at runtime
- [ ] **NEW** `jsPsych.pluginAPI.compareKeys()` for accuracy — not manual `==` comparison

**Psychtoolbox:**
- [ ] `KbQueueCreate` + `KbQueueCheck` — not `KbCheck` for RT
- [ ] `VBLTimestamp` from `Screen('Flip')` as RT origin — not `GetSecs`
- [ ] `firstPress - stimOnset` for RT calculation (ms precision)
- [ ] `vbl + (waitframes - 0.5) * ifi` for frame timing — not `WaitSecs()`
- [ ] `KbQueueFlush([], 2)` at start of each trial
- [ ] `try/catch/sca/Priority(0)/ShowCursor` — not bare `sca`
- [ ] **NEW** KbQueue lifecycle: `Create` + `Start` before trial loop, `Stop` + `Release` after loop — never inside
- [ ] **NEW** `Screen('Flip', window, vbl + (wf-0.5)*ifi)` — every Flip has `when` parameter
- [ ] **NEW** `Screen('DrawingFinished')` before Flip if heavy drawing — prevents frame overrun
- [ ] **NEW** `InitializePsychSound(1)` + `PsychPortAudio('Open',...,2,...)` if audio — low-latency mode
- [ ] **NEW** `SkipSyncTests, 0` — production must not skip sync tests
- [ ] **NEW** `HideCursor` + `Priority(MaxPriority(window))` — called after window open, before trial loop

### 3. Response Collection

- [ ] Response keys validated against allowed set (not arbitrary keys)
- [ ] Anticipatory responses (RT < 100ms) recorded but flagged (not discarded silently)
- [ ] Multiple keypresses within one trial handled correctly (first press wins for RT)
- [ ] Timeout responses correctly coded (response = None/timeout, rt = NaN/empty)
- [ ] No-go trials: no-response = correct rejection (accuracy=1)
- [ ] Go trials with no response = miss (accuracy=0)
- [ ] Escape checked during every response window
- [ ] **NEW** Response window has a hard deadline (not infinite wait)
- [ ] **NEW** Key-release events do NOT count as responses (waitRelease=False / KbQueue firstPress only)
- [ ] **NEW** Pre-existing keyboard buffer cleared before each trial (Flush/clearEvents)

### 4. Randomization & Conditions

- [ ] Trial order randomized within each block
- [ ] Randomization seed set for reproducibility
- [ ] Condition ratios match stated design (e.g., go:no-go, congruent:incongruent)
- [ ] Counterbalancing implemented if required by paradigm (check paradigm `## Must Confirm`)
- [ ] No consecutive same-condition constraint checked if needed (paradigm-specific)
- [ ] **NEW** Condition file validated: all column names referenced in code exist in file
- [ ] **NEW** Condition file validated: row count matches `block.trials` (or explicitly auto-generated)
- [ ] **NEW** Stimulus file existence: all files referenced in condition columns exist on disk

### 5. Stimulus Validation

- [ ] All stimulus files validated at startup (not mid-experiment) — fail-fast on missing files
- [ ] Images/sounds preloaded outside trial loop
- [ ] CJK text rendered with explicit font (FONT_CONFIG block or equivalent)
- [ ] Stimulus sizes appropriate for viewing distance (if visual angle specified)
- [ ] Fixation cross drawn with lines/shapes — not text "+"
- [ ] **NEW** Audio files preloaded: `Sound()` + `CreateBuffer` before trial loop, not `FillBuffer` per trial
- [ ] **NEW** Gabor/texture stimuli created once with `CreateProceduralGabor` / `MakeTexture` — not per trial
- [ ] **NEW** Text stimuli: `TextStyle` / `TextFont` set once before loop, only content changes per trial

### 6. Data Integrity Verification

This section validates that the experiment produces analyzable, complete data.

#### 6.1 Output Column Compliance

Cross-reference against [data-recording.md](../psych-experiment-programming/references/data-recording.md). All 10 base columns must be present:

| # | Required Column | Check |
|---|----------------|-------|
| 1 | `subject_id` | Present in output, not hardcoded |
| 2 | `block` | 1-indexed, increments correctly across blocks |
| 3 | `trial` | 1-indexed, resets or continues correctly per block |
| 4 | `condition` | Human-readable label (not just numeric code) |
| 5 | `stimulus` | Filename or stimulus ID — traceable to condition |
| 6 | `correct_response` | Expected key name or `None` for no-go |
| 7 | `response` | Actual key pressed or `None`/empty for timeout |
| 8 | `rt` | Float in ms, empty string `''` for timeout (not `'None'` or `'NaN'`) |
| 9 | `accuracy` | 1=correct, 0=incorrect, -1=timeout |
| 10 | `timestamp` | ISO 8601 of trial onset |

#### 6.2 Accuracy Coding Correctness

| Trial type | Correct behavior | accuracy value |
|-----------|-----------------|----------------|
| Go trial, correct key | response == correct_response | 1 |
| Go trial, wrong key | response != correct_response | 0 |
| Go trial, timeout | no response within deadline | -1 |
| No-go trial, withheld | no response | 1 |
| No-go trial, responded | any key pressed | 0 |
| Stop-signal, stop success | no response after stop signal | 1 |
| Stop-signal, stop fail | responded despite stop signal | 0 |

**How to verify**: Read the accuracy evaluation code. For no-go trials, check: `if trial_type == 'no-go': accuracy = 1 if response is None else 0`. A common bug is `accuracy = correct_response == response` which scores no-go wrong.

#### 6.3 Crash Recovery Test

- [ ] try/finally (PsychoPy) or try/catch/sca (PTB) wraps the entire experiment loop
- [ ] Data file is flushed/closed in the finally/catch block — not only at normal exit
- [ ] Simulated crash: if the experiment is force-quit mid-session, all trials up to the crash point are saved
- [ ] **Test**: Run experiment, force-quit after trial 10, check CSV has 10 rows with complete data

#### 6.4 NaN/Timeout Handling

- [ ] Timeout RT stored as empty string `''` in CSV — not `'None'`, `'NaN'`, `-999`, or `0`
- [ ] Timeout response stored as empty string `''` or `'timeout'` — consistent across all trials
- [ ] Analysis scripts can distinguish "no response" (empty) from "response with RT=0" (impossible)
- [ ] **Anti-pattern**: `rt = NaN` or `rt = -1` in CSV — these break analysis imports

### 7. Emergency Quit

- [ ] Escape saves partial data before exit
- [ ] Escape checked during response windows AND between trials/ITIs
- [ ] Cleanup block restores cursor, priority, closes window
- [ ] In jsPsych: `'escape'` in `choices` arrays or checked in `on_finish`
- [ ] **NEW** Escape during instruction/practice also exits cleanly (not stuck on instruction screen)
- [ ] **NEW** Two consecutive Escape presses = forced quit (safety for stuck loops)
- [ ] **NEW** Window close button (X) also triggers cleanup (where platform supports it)

### 8. Pre-collection Readiness

- [ ] Non-programmer can edit parameters without reading logic code
- [ ] All parameter line numbers documented in accompanying README
- [ ] No debug/test code remaining (no `print()`, `console.log()`, `disp()` without guard)
- [ ] Hardware triggers validated (if EEG/parallel port used)
- [ ] Monitor gamma/calibration verified (if luminance-critical stimuli)
- [ ] **NEW** Experiment runs full-length without memory leaks or slowdown
- [ ] **NEW** Output filename includes subject ID — prevents overwriting previous subject data
- [ ] **NEW** Data directory auto-created if missing (`mkdir`/`exist` check)

### 9. Paradigm-Specific Failure Mode Checks

Cross-reference the paradigm file from the programming layer for known failure modes.
Load `../psych-experiment-programming/paradigms/{paradigm_name}.md` and check each item in `## Common Failure Modes`.

**Go/No-go:**
- [ ] No-go accuracy: witholding = accuracy 1 (correct rejection), responding = accuracy 0 (commission error)
- [ ] Not using `event.getKeys(maxWait=...)` / `KbWait` — must use non-blocking keyboard API
- [ ] Escape check present within response window loop

**IAT:**
- [ ] Block order counterbalanced (compatible-first vs incompatible-first) across subjects
- [ ] Stimulus identity recorded per trial (which exemplar appeared)
- [ ] Error penalty implemented: error trial RT replaced with `block_mean_correct_RT + 600ms`
- [ ] D-score uses improved algorithm (Greenwald et al., 2003), not original 1998
- [ ] RT > 10,000ms trials deleted; subjects with >10% RT < 300ms flagged
- [ ] Minimum 4 exemplars per category (ideally 6+)

**Stop-signal:**
- [ ] SSD staircase: SSD decreases after failed stop, increases after successful stop
- [ ] Stop-signal delay independent of go RT distribution (tracking algorithm)
- [ ] SSRT estimable: ~50% stop success rate maintained by staircase

**N-back:**
- [ ] Match detection: buffer comparison uses correct n-back distance
- [ ] Lure trials (stimulus appeared n±1 back) correctly counted as non-targets
- [ ] d-prime calculation: hits/(targets) vs false-alarms/(non-targets)

**Dot-probe:**
- [ ] Congruency coding: congruent = target replaces cue, incongruent = target replaces opposite
- [ ] Cue-target SOA appropriate for the attentional process (100ms vs 500ms)
- [ ] Bias score: `meanRT_incongruent - meanRT_congruent` (or per standard convention)

**Stroop:**
- [ ] Congruency ratio: congruent and incongruent trials balanced (typically 50:50)
- [ ] Response mapping: 2-choice (exclude neutral) or 3-choice (include neutral) — explicitly defined
- [ ] Color rendering: RGB values verified to be perceptually distinct on target display

**For paradigms without a `## Common Failure Modes` section**: Run the generic checks:
- [ ] Trial window sequence matches the paradigm's canonical window structure
- [ ] Response mapping unambiguous for every condition
- [ ] Condition ratios match paradigm conventions
- [ ] RT onset correctly set (merged stimulus+response vs split)

### 10. Smoke Test Protocol (NEW — code-audit only)

After automated checks pass, provide the user with a concrete, step-by-step smoke test.
This is a **5-minute manual test** that verifies the code actually works before real data collection.

```
## Smoke Test Protocol

Run this test with subject ID "test" before collecting real data.

### Test 1: Launch & Display (30 seconds)
1. Run the experiment: [exact command]
2. Verify: Window opens in fullscreen at correct resolution
3. Verify: No error messages in console
4. Press Escape → verify experiment exits cleanly (screen restored, cursor visible)

### Test 2: Full Run-through (2 minutes)
1. Run with subject ID "smoke_test_1"
2. Complete instruction screens → verify all text readable, key mappings correct
3. Complete practice trials → verify feedback displays correctly
4. Complete all formal blocks → verify block transitions work
5. Reach "thank you" screen → verify clean exit path

### Test 3: Data Output (1 minute)
1. Locate the output CSV in data/
2. Open in Excel / text editor
3. Verify: One row per trial (check row count against expected)
4. Verify: All columns present (check column headers)
5. Verify: rt column has numeric values (not empty for responded trials)
6. Verify: accuracy column has 1/0/-1 values (no unexpected codes)

### Test 4: Crash Recovery (1 minute)
1. Run with subject ID "crash_test"
2. After trial ~10, force-quit: [how to force quit on this OS]
3. Reopen the data file → verify trials 1-10 are saved with complete data
4. Verify: No corrupted/partial rows

### Test 5: Edge Cases (30 seconds)
1. Press keys NOT in the allowed set during response → verify ignored
2. Press key before stimulus onset → verify not counted as response
3. Let a trial timeout (don't press anything) → verify timeout coded correctly
4. Press Escape mid-trial → verify exits cleanly
```

After the user completes the smoke test, they report back. If all 5 tests pass, the code is `ready_for_collection`.

---

## Review Checklist — config-audit

Only design-level checks. Do not check implementation details.

- [ ] Trial window timeline is complete (every window has content, duration, response)
- [ ] Every response window has `rt_onset` defined
- [ ] Every `{column_name}` in `windows[]` exists in the condition file
- [ ] Every trial type has a resolvable correct response (including no-go/stop/catch/timeout)
- [ ] Block structure is complete (practice, formal, rest with valid types)
- [ ] Feedback windows only appear in practice blocks (or as explicitly designed)
- [ ] Condition ratios match the stated design
- [ ] Counterbalancing rule is specified (if paradigm requires it)
- [ ] Data output columns are sufficient for planned analysis
- [ ] Response mapping is unambiguous (which key = which answer)
- [ ] Audio config (if present) specifies backend and preloading strategy
- [ ] Participant info fields are appropriate for the experiment

## Review Checklist — implementation-plan-review

- [ ] Trial loop structure is clear and matches a known platform pattern
- [ ] Timing and response collection approaches are named (even if not implemented)
- [ ] Known platform anti-patterns are absent from the plan
- [ ] Data saving strategy is described (incremental, format, filename convention)
- [ ] Escape/quit strategy is described
- [ ] Plan specifies which code skeleton it will build from

## Review Checklist — triage-only

- [ ] What paradigm is described? (if unclear, flag)
- [ ] What trial windows are implied? (list; mark missing ones)
- [ ] What is the response rule? (keys? mapping? deadline?)
- [ ] What varies trial-to-trial? (conditions)
- [ ] What is the block structure? (practice? formal? trial counts?)
- [ ] What data is collected? (rt? key? acc? additional measures?)
- [ ] Is the platform stated? (default to PsychoPy if unstated)

---

## Severity Classification

| Severity | Definition | Concrete examples |
|----------|-----------|-------------------|
| **Critical** | Invalidates all data; must fix before any collection | Wrong RT measurement source (`KbCheck` for RT, `time.time()` for RT), no data save or save-only-at-end, no Escape handling, accuracy coding inverted (no-go scored as miss), KbQueue Create/Start inside trial loop, missing `backend='ptb'`, `jsPsych.init()` in v7, `WaitSecs()` for trial timing |
| **Major** | Degrades data quality; fix before formal collection | Missing Escape in ITI between trials, no randomization seed, CJK font missing (tofu characters), feedback shown in formal blocks, no `KbQueueFlush` before trial, `waitRelease=True` on RT keyboard, `SkipSyncTests` enabled, no `preBuffer=-1` on audio, stimulus loaded inside trial loop |
| **Minor** | Does not affect data quality; fix when convenient | Extra debug print left in code, variable naming convention, missing code comment, parameter ordering, redundant import, hardcoded path that works but should be configurable |

---

## Output Format

Every review output follows this structure:

```markdown
## Review Mode
[mode]

## Readiness Label
[label]

## Scope
[What was reviewed and what was NOT reviewed]

## Platform
[Detected platform + version assumptions]

## Overall Verdict
[PASS / PASS WITH MINOR ISSUES / FAIL]

## Critical Issues
[Must fix before collecting data — each with file path, line number, fix suggestion]

## Major Issues
[Should fix — may affect data quality — each with file path, line number, fix suggestion]

## Minor Issues
[Nice to fix — unlikely to affect results]

## Quality Gate Results
| # | Check | Result | Detail |
|---|-------|--------|--------|
| 1 | Skeleton match | PASS/FAIL | [specific mismatch if failed] |
| 2 | No anti-patterns | PASS/FAIL | [which patterns found, where] |
| ... | ... | ... | ... |

## Section-by-Section Report
[All applicable checklist sections with findings. For each failed item: what's wrong → why → how to fix]

## Paradigm-Specific Checks
[Results of paradigm failure mode cross-reference]

## Suggested Fixes
[Specific changes with file paths and line numbers. Each fix is self-contained:
 "Line 87: Change `kb = keyboard.Keyboard()` to `kb = keyboard.Keyboard(backend='ptb')`"
 "Line 120: Add `KbQueueFlush([], 2);` before trial loop"
 "Line 156: Change `rt = GetSecs - stimOnset` to `rt = (min(firstPress(keyIdx)) - stimOnset) * 1000`"]

## Smoke Test Protocol
[Only for code-audit with PASS or PASS WITH MINOR ISSUES verdict. The standardized 5-test protocol from §10 above.]
```

---

## Verdict Rules

### code-audit

- **PASS**: Zero critical + zero major issues + smoke test passes. → `ready_for_collection`
- **PASS WITH MINOR ISSUES**: Zero critical + zero major; minor issues only. → `ready_after_minor_fixes`
- **FAIL**: Any critical or major issue. → `not_ready_for_collection`

### config-audit

- Config complete, no design issues → `pre_code_ready`
- Config has gaps or design issues → `needs_experiment_info` or `not_ready_for_collection`

### implementation-plan-review

- Plan clear and complete, no platform issues → `pre_code_ready`
- Plan has gaps or anti-pattern risks → recommend resolving before proceeding

### blocked

No verdict given. State what input is needed to proceed and exit.

---

## Regression Test Guide

When code has been modified after an initial review, re-audit with this focused checklist:

1. **Changed lines**: Read the diff. What was changed?
2. **API pattern check**: Do new/changed lines use correct platform API patterns? (Re-run Gate 0 items 2-3)
3. **Anti-pattern scan**: Do new/changed lines introduce any anti-patterns?
4. **Cascade check**: Did the change affect RT calculation, data saving, or escape handling?
5. **Smoke test re-run**: Run Test 2 (full run-through) and Test 3 (data output) from the Smoke Test Protocol

If the change is trivial (e.g., parameter value only, comment fix), re-audit is optional.
If the change affects trial loop, response collection, or data saving, full re-audit is required.

---

## First-Run Checklist (Pre-First-Subject)

Before the first real participant, the experimenter must verify:

```
□ Smoke test passed (all 5 tests from §10)
□ Monitor at correct resolution and refresh rate
□ Color calibration verified (if luminance-critical stimuli)
□ Audio volume tested at participant position
□ Response device tested (keyboard/button box — all response keys register)
□ Data directory writable (test with subject ID "check_write")
□ Backup plan: where is the data if the computer crashes?
□ Experimenter knows how to force-quit (Escape / Alt+F4 / power button)
□ Participant briefing script ready (explains task, key mapping, duration)
□ Debriefing script ready (explains purpose, answers questions)
```

The reviewer should output this checklist with every `ready_for_collection` verdict.

---

## Related Files

| File | When to load |
|------|-------------|
| [../psych-experiment-coder/psychopy/spec/README.md](../psych-experiment-coder/psychopy/spec/README.md) | PsychoPy code audit — canonical skeleton + 14 anti-patterns |
| [../psych-experiment-coder/jspsych/spec/README.md](../psych-experiment-coder/jspsych/spec/README.md) | jsPsych code audit — canonical skeleton + 12 anti-patterns |
| [../psych-experiment-coder/psychtoolbox/spec/README.md](../psych-experiment-coder/psychtoolbox/spec/README.md) | PTB code audit — canonical skeleton + 15 anti-patterns |
| [../psych-experiment-programming/paradigms/](../psych-experiment-programming/paradigms/) | Paradigm failure mode cross-reference |
| [../psych-experiment-programming/references/data-recording.md](../psych-experiment-programming/references/data-recording.md) | Data output column validation |
| [../psych-experiment-programming/references/config-schema.md](../psych-experiment-programming/references/config-schema.md) | Config validation rules |
