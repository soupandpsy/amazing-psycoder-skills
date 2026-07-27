---
name: psy-exp-designer
description: >-
  Design or revise a psychological experiment before implementation. Use when
  the user has an idea, partial protocol, trial/block structure, timing,
  randomization, response mapping, condition table, PsychoPy/jsPsych/
  Psychtoolbox target, or a paradigm such as Stroop, IAT, N-back, priming,
  dot-probe, visual search, task switching, Go/No-go, or stop-signal, and needs
  a confirmed experiment config YAML. Do not use to implement/debug existing
  code or to audit readiness; use psy-exp-coder or psy-exp-reviewer instead.
---

# Psychological Experiment Designer

## Version

v1.4.0 — unified evidence-gated contract, 2026-07-23. Sub-skill of [amazing-psycoder](../SKILL.md).

## Purpose

Convert psychological experiment ideas into a complete experiment specification (config YAML) through progressive refinement, then route the validated config to `psy-exp-coder`. Do not generate implementation code in this skill.

## Design Philosophy

Let the user own design decisions while the system enforces explicit semantics, progressive confirmation, traceable assumptions, and a complete config before code generation. Paradigm references suggest questions; they do not own the design.

## Paradigm References Are Non-Authoritative

`paradigm` and `paradigm_family` classify a design and may select an optional
knowledge reference. They never select executable logic. Templates initialize
editable fields only. After import, the user's confirmed windows, condition
model, correctness rules, randomization constraints, feedback, and data schema
are authoritative.

Do not collapse variants into a family implementation. Classic color-word,
semantic, emotional, bilingual, and numerical Stroop may require different
stimulus schemas, factors, derived variables, correctness rules, and analysis
interpretations. If no exact reference exists, continue as a custom design and
derive every semantic rule from the user-confirmed config.

## When Not to Use

Route implementation/debugging to `psy-exp-coder`, readiness audits to `psy-exp-reviewer`, and answer quick platform API questions directly.

## Core Model

Model every experiment as `Experiment → Sequence → Window → Data`. Require one trial-summary row per trial; add a linked event-level table when a trial has repeated responses, trajectories, adaptive steps, drag events, or other one-to-many observations. Never force repeated events into a single lossy cell.

## Red Lines

Hard prohibitions. These must never be violated — no exceptions, no "just this once."

| # | Rule | Applies to | Why |
|---|------|-----------|-----|
| 1 | **No code generation before trial window timeline is complete** | All platforms | Code written without a validated window sequence will have structural errors that are expensive to fix |
| 2 | **No assumed response mapping** | All platforms | Which key means what answer must be confirmed with the user. Guessing invalidates accuracy data |
| 3 | **No blocking sleep in timing-critical or interactive windows** | PsychoPy, jsPsych | Blocking waits make timing and abort handling unreliable. Use frame/timeline scheduling; never use a setup wait as an RT source |
| 4 | **No `event.getKeys(maxWait=...)`** | PsychoPy | Blocks the event loop. Use `keyboard.Keyboard` with `win.callOnFlip(kb.clock.reset)` |
| 5 | **No data saved only at end of experiment** | All platforms | Crash = all data lost. Save incrementally per trial or per sequence with `try/finally` |
| 6 | **No silent filling of `[MISSING]` values** | All platforms | Every `[MISSING]` must be resolved by asking the user or offering an explicitly-flagged default |
| 7 | **Font-sensitive/CJK text needs an explicit font strategy** | All platforms | Record a suitable family/path/fallback for the target runtime and verify glyphs and layout visually; browser fallback stacks are acceptable when tested |
| 8 | **No skipping relevant design decisions** | All platforms | Exact paradigm references may suggest questions, but only the actual experiment specification determines what must be confirmed |
| 9 | **No `rt_onset` omitted on response windows** | All platforms | Incorrect or missing RT onset invalidates all reaction time data. The coder will refuse to generate if absent |
| 10 | **No code delivery without reviewer pass** | All platforms | All generated code must pass through `psy-exp-reviewer` before data collection. Programming → Coder → Reviewer is a mandatory chain |

## Config as Single Source of Truth

The [experiment config YAML](references/config-schema.md) is the central artifact. Every design decision lives in one file:

```yaml
name:        # experiment name
paradigm:    # which paradigm
paradigm_family: # optional research lineage; metadata only
variant:     # optional exact variant; metadata only
platform:    # psychopy / psychtoolbox / jsPsych
stimulus_folder:  # global path for image file references
windows:     # trial event sequence
sequences:   # sequence structure + execution modes (once/loop)
blocks:      # LEGACY — block structure (use sequences for new designs)
response_rules:  # keys, deadline, accuracy logic
randomization:   # method, seed, sequence/counterbalance constraints
paradigm_config: # paradigm-specific settings
output:      # data directory, filename pattern
```

The conversation has one goal: **fill every `[MISSING]` field in this config**. The user can provide information in any form — prose description, file paths, partial YAML, xlsx files — and the system progressively accumulates it into the config.

## Unified Workflow

Every new experiment follows the same 5 phases. The order reflects how experimenters naturally design: **trial first (with rules), then sequence structure**. The config YAML is filled progressively.

```
Phase 1: Assess    → 收集已有信息
Phase 2: Windows & Rules → 定义 Trial + 反应规则（最关键）
Phase 3: Conditions→ 定义 trial 序列（xlsx + 刺激文件）
Phase 4: Sequences → 定义序列结构和执行模式
Phase 5: Validate  → 验证并移交代码生成
```

### Blocking Gates

Hard checkpoints. The workflow does not advance past a gate until its condition is met. If a gate fails, return to the relevant phase; do not proceed.

| Gate | After | Condition | Fail → Return to |
|------|-------|-----------|------------------|
| **Gate 1** | Phase 2 | Trial window timeline has no `[MISSING]`. Every window has `name`, `content`, `duration`, `response`. Response windows have `rt_onset`. Response keys, mapping, accuracy rules, and output format are confirmed. Phase 2 decision checklist presented and user confirmed | Phase 2 |
| **Gate 2** | Phase 3 | Every `{column_name}` in `windows[]` exists in condition xlsx. Condition file is on disk OR has been generated by Phase 3. Stimulus folder (if used) resolves. Phase 3 decision checklist presented and user confirmed | Phase 2 or 3 |
| **Gate 3** | Phase 4 | Config has zero `[MISSING]` markers. All sections (`windows`, `sequences`, `response_rules`, `paradigm_config`, `randomization`, `output`) are complete. Phase 4 decision checklist presented and user confirmed | Phase 2/3/4 (whichever section has `[MISSING]`) |
| **Gate 4** | Phase 5 | All rules in config-schema.md pass and `scripts/validate_experiment.py` reports zero errors. No missing columns/files, ambiguous accuracy coding, unseeded randomization, or unsafe output contract remains | Phase 1/2/3/4 (based on error type, per Phase 5 routing table) |
| **Gate 5** | Phase 5 (before coder) | **Final Design Review**: Full Design Decision Registry presented. User explicitly confirms ALL decisions (including `[ASSUMED]` items) before code generation. No decision left un-reviewed | Phase 1/2/3/4 (user can correct any decision) |

### Phase 1: Assess Input

Determine what the user already has, what paradigm, and what platform.

| User provides | Action |
|--------------|--------|
| Natural-language description ("我想做一个Stroop实验...") | Parse into skeleton config; flag all unknowns as `[MISSING]` |
| Partial config YAML | Load it; identify which sections are filled vs missing |
| config.yaml + conditions/*.xlsx | Load everything; validate; skip to Phase 5 if complete |
| Existing experiment code to modify/debug | Route to `psy-exp-coder`; do not modify implementation inside the Designer |
| "帮我检查这段代码" | Route to `psy-exp-reviewer` directly |

Also resolve in Phase 1 if the user hasn't stated it:
- Paradigm/family metadata when useful. Load an exact [paradigm file](paradigms/) only as a reference; an unknown or custom paradigm is valid when its semantics are complete
- Platform (PsychoPy / Psychtoolbox / jsPsych)
- **Runtime contract**: Record an exact framework version, pinned/lockfile dependency strategy, and target environment. Record OS/display details when timing, visual angle, hardware, or font paths depend on them. For CJK or other font-sensitive stimuli, an explicit family plus tested fallback/auto-detection is blocking.

**When an exact paradigm reference exists**: Cross-reference its `## Must Confirm` list against what the user already stated. These are candidate safety questions, not inherited answers. For each relevant unconfirmed item, assign it to the phase where it will be asked:

| Must Confirm item type | Target phase |
|------------------------|--------------|
| Stimulus identity, content, modality | Phase 2 |
| Key assignment, response mapping | Phase 2 |
| Timing values (durations, deadlines, SOA) | Phase 2 |
| Accuracy rules, error coding, catch trials | Phase 2 |
| Output format (data directory, filename) | Phase 2 |
| Trial counts, condition ratios | Phase 3 |
| Stimulus file source (image vs generated) | Phase 3 |
| Sequence count, repetitions per sequence, feedback placement | Phase 4 |
| Counterbalancing, sequence order | Phase 4 |

If a Must Confirm item doesn't fit any later phase (e.g., paradigm-specific correctness logic), ask it now in Phase 1. Do not leave Must Confirm items unassigned.

**Output**: Config with `name`, `paradigm`, `platform`, and `runtime` filled; add detailed OS/display/font fields when required by the design. Present the Phase 1 Decision Checklist before advancing.

### Phase 2: Define Windows & Rules (Trial)

Build the trial window timeline — the most critical phase. Every screen event in a single trial becomes a window. Also finalize all response rules here: key mapping, accuracy logic, and output format. These belong together because the response keys defined in the window timeline directly determine the mapping and accuracy rules.

**What to determine** for each window:
- Window name and order (e.g., Fixation → Stimulus → Response → Feedback → ITI)
- Content (literal text, `{column_reference}`, or image file path)
- Duration (fixed ms, `[min, max]`, `until_key`, or `self_paced`)
- Response rule (none / allowed keys / deadline)
- File/folder reference (which stimulus files?)
- Condition source (which xlsx column drives this window?)

**How to present**: Follow the sequence-row diagram and formatting contract in
[canvas-presentation.md](references/canvas-presentation.md). Each Sequence is
one independent horizontal row. Sequence order is top-to-bottom; window order
is left-to-right. Show every sequence, mark unresolved values as `[MISSING]`,
and annotate the response window with its RT anchor and recorded data.

**Questions (max 3)**:
1. "每个窗口的持续时间是多少？反应窗口的截止时间？"
2. "被试按哪些键反应？哪个键对应哪个条件？"
3. "刺激呈现什么内容？文字、图片还是图形？"

Also ask any paradigm Must-Confirm items assigned to Phase 2 (stimulus identity, timing values, key assignment, accuracy rules). Phase 2 typically carries the most Must-Confirm items — if paradigm questions + generic questions exceed the 3-question limit, apply the [Must-Confirm overflow rule](#must-confirm-overflow-rule) (batch compatible questions, default low-risk items with ⚠️ flag, defer to later phases where logical).

**How many windows?** The confirmed design determines the window count; it is not fixed at 5 and is never inherited solely from a family label. Standard RT tasks may have 4 (Fixation → Stimulus → Response → ITI). Masked priming may need 6+ (Forward Mask → Prime → Backward Mask → Target → Response → ITI). An exact reference may offer a starting example, but the resulting timeline remains fully editable.

**Stimulus + Response: merge or split?** Two patterns are valid:
- **Split**: Stimulus window (fixed duration, no response) → Response window (stimulus stays + keys accepted). Use when the stimulus must be visible for a fixed time before responses are allowed. RT is measured from Response window onset, excluding stimulus encoding time.
- **Merged**: A single window with `duration: until_key` and `response: [keys]`. Use when the participant responds immediately to the stimulus (e.g., Stroop, Flanker). RT is measured from stimulus onset.

**RT measurement contract — proposed, explained, and explicitly confirmed.**
Window structure may suggest an anchor, but a paradigm label or heuristic never defines the dependent variable. Before Gate 1, record `response_event`, `rt_onset`/anchor window, scientific rationale, and `status: confirmed`. For a merged response window, propose its measured display onset; for a stimulus then response sequence, explain that the two possible anchors estimate different quantities and ask which operational definition is intended.

Present the consequence without implementation jargon and request confirmation:
> "我建议把反应时定义为：从 **[可观察事件/窗口]** 的实际呈现时间，到 **[按下/释放/点击]**。这样测量的是 **[研究含义]**；若改从 **[另一事件]** 起算，解释会不同。请确认这一定义。"

Do not confirm the design until the user confirms this definition. Coder
resolvability checks are implementation guards, not scientific validation.

### Response Rules (also Phase 2)

Once windows are defined, immediately finalize the response rules — don't defer to a later phase. The response keys named in the window timeline directly determine these rules.

**What to determine**:
- **Response mapping**: Which key = which answer (e.g., f=red, j=green, k=blue). Ask this alongside the key list in the windows phase — it's unnatural to separate them
- **Accuracy logic**: What makes a response correct for each condition. For simple designs, this is just `key == correct_response`. For paradigms like Go/No-go: no-go + no key = correct; go + no key = miss
- **No-go / stop / catch trial handling**: How to score trials where the correct response is to NOT respond
- **Deadline**: Maximum response time per trial. If unknown, propose a task-appropriate candidate with rationale and keep it unconfirmed; there is no universal paradigm-family default

**Questions (ask alongside window questions above — don't create a separate question round)**:
- "哪个键对应哪个条件？" (if mapping not obvious from key list)
- "No-go试次不按键=正确，按键=错误，确认吗？" (paradigm-specific, from Must-Confirm)

**Output format** — also finalized here, but offer defaults; only ask if customization needed:
- Data directory: `data/` (default)
- Filename pattern: `sub-{subject_id}_{task_name}_{run_id}.csv` (default)
- Question (only if user needs changes): "数据用默认设置保存，需要修改吗？" (counts toward the 3-question limit only if asked)

**Output**: Config `windows[]`, `response_rules`, `paradigm_config`, and `output` sections complete. Phase 2 Decision Checklist presented for user confirmation. Gate 1 check: windows have no `[MISSING]`, response keys and mapping are confirmed, accuracy rules are defined, and the response-event/RT-anchor measurement contract is explicitly confirmed.

### Phase 3: Build Conditions

Define what varies trial-to-trial — the condition table that drives each trial's content and correct answer.

**What to determine**:
- Does the user have existing condition xlsx files?
- If yes: validate file paths, column names, condition ratios
- If no: generate from specification based on the windows defined in Phase 2
- Stimulus file paths (folder location, naming convention)

**How it connects to Phase 2**: Every `{column_name}` in the window `content` and `response` fields must exist as a column in the condition xlsx.

**Condition file generation**: If the user needs condition files created, use [condition-file-generation.md](references/condition-file-generation.md). For simple designs, write the xlsx directly. For complex or reproducible designs, generate a standalone Python script. Always report the generated file's path, row count, columns, and condition distribution.

**Questions (max 3)**:
1. "trial 顺序有现成的 xlsx 文件吗？还是根据条件自动生成？" — if yes, validate the file; skip question 2
2. "每个条件各多少 trial？各条件比例是多少？"
3. "刺激文件放在哪个文件夹？文件命名规则是什么？" — skip if all stimuli are text-based (determined in Phase 2)

Also ask any paradigm Must-Confirm items assigned to Phase 3 (condition ratios, stimulus file source).

**Output**: Condition files (validated or generated). Fill the global `stimulus_folder` when file-backed stimuli are used. Present the Phase 3 Decision Checklist for confirmation.

### Phase 4: Set Sequence Structure

With the trial defined (Phase 2) and conditions built (Phase 3), determine the experiment structure: how sequences are ordered and how each sequence executes.

**Core concept**: A Sequence is one horizontal row of windows that runs from top to bottom. Each sequence has exactly one execution mode:

| Execution Mode | Meaning | Example |
|----------------|---------|---------|
| `once` | Run exactly one time | Welcome screen, rest screen, debrief |
| `loop` | Repeat N times, once per trial | Practice block, formal experiment block |

**What to determine**:
- Sequence order (top to bottom on the canvas)
- Per-sequence execution mode and repetition count
- Feedback placement: does a Feedback window exist in this sequence?
- Sequence visibility: should this sequence only appear in certain contexts? (`show_in`)
- Between-sequence behavior: does the experiment pause, show instructions, or auto-advance?
- **Counterbalancing**: Is sequence order fixed or counterbalanced across subjects? If counterbalanced, by what rule (subject ID parity, Latin square)?

**Sequence naming convention**: Names like Start, Practice, Main, Rest, End are editable labels that help the researcher organize their experiment. They never determine execution behavior — only `execution.mode` and `execution.repetitions` control what happens.

**Block Type Mapping** (for backward compatibility with legacy configs):

| Legacy Block Type | Sequence Equivalent |
|-------------------|---------------------|
| `practice` | `mode: loop` + contains Feedback window |
| `formal` | `mode: loop` + no Feedback window |
| `rest` | `mode: once` + rest text content |
| `debrief` | `mode: once` + results/debrief content |
| instruction | `mode: once` + instruction text |

**Before finalizing sequences**, run this consistency check:
- If any sequence has a Feedback window but no Feedback window exists in `windows[]`, insert one after the Response window: `{name: Feedback, content: correct_incorrect, duration: 500, response: none}`.
- Feedback appears only in sequences that contain a Feedback window. The `show_in` field restricts further — e.g., `show_in: [practice]` means the sequence only appears during practice, even if it shares windows with formal sequences.

**Questions (max 3)**:
1. "实验有几个序列？每个序列重复几次？（如 Start一次、练习20次、正式80次、Rest一次、End一次）"
2. "反馈在哪些序列显示？只在练习还是正式实验也有？"
3. "序列呈现顺序是固定的还是在被试间平衡？"

For Rest sequences, also ask: "休息时屏幕显示什么文字？" (default: "休息一下，按空格键继续").

**Output**: Config `sequences[]` and `randomization` sections complete. Each sequence has `name`, `window_ids`, `execution` (mode + repetitions + optional shuffle), optional `show_in`. Present the Phase 4 Decision Checklist for confirmation.

### Phase 5: Validate & Route

Cross-check everything, **present the final design to the user for confirmation**, then route to the coder for code generation.

**Step 1: Technical validation** — Run every rule in [config-schema.md § Validation Rules](references/config-schema.md), then execute `python3 <amazing-psycoder-root>/scripts/validate_experiment.py <config.yaml>`. Treat every reported error as blocking; the script is a static preflight and never proves runtime readiness.

**If validation fails**: Report specific errors. Return to the relevant phase based on error type:
- Missing config metadata (`name`, `paradigm`, `platform`) → Phase 1
- Missing or incomplete window definitions (`content`, `duration`, `response`, `rt_onset`), missing response rules, ambiguous accuracy coding → Phase 2
- Missing condition file, invalid columns, row count mismatch, or missing stimulus files → Phase 3
- Missing sequence fields or invalid execution modes → Phase 4

**Step 2: Final Design Review (Gate 5, blocking)** — Present the final design for user confirmation. This is mandatory before routing to code generation.

**Do not dump raw YAML by default.** Present the design in readable form, save the YAML as a real artifact, and report its path. Show the YAML whenever the user requests it; it is not secret state. Use these two confirmation views:

1. **Trial Window Timeline** — the box diagram with response rules (same format as Phase 2 output)
2. **Complete Design Decision Registry** — all decisions from all phases in table form

Use the complete final-review example in
[canvas-presentation.md](references/canvas-presentation.md). It must show every
sequence/window, response and RT semantics, plus the cumulative Decision
Registry with all assumed values visibly marked.

- Items marked ⚠️ are defaults/assumptions — the user MUST be prompted to review them
- Ask: "以上所有设计决策确认无误，可以生成代码？如需修改请指定编号和新值。"
- Do NOT route to the coder until the user explicitly confirms the full registry
- If the user wants to change any item, return to the relevant phase, update the config, and re-run validation
- Save the confirmed config and Decision Registry in the project directory before handoff. The Coder documents stable parameter names/sections after code exists; the Designer must never invent future line numbers.

**Step 3: Persist and route** — After Gate 5, save `config.yaml` and the Decision Registry, report both paths, and route `psy-exp-coder` to those artifacts. After generation, route to `psy-exp-reviewer`. Static approval permits packaging for runtime testing; collection still requires observed smoke-test evidence.

> **下一步**: 实验设计完成。将已保存的 config 路径交给 `psy-exp-coder`；生成后由 `psy-exp-reviewer` 审计并核验运行时证据。

## Question Protocol

At every phase, follow this protocol:

1. **Show current design state** — display what's known and what's still `[MISSING]` using the phase decision checklist format (not raw YAML). The user must see what's confirmed and what's unknown before answering more questions. Raw YAML is an internal format — users read decision tables, not YAML.
2. **Check exact-reference candidate questions** — when an exact design reference exists, use its Must-Confirm items to find possible omissions. Keep only questions relevant to the current design; never inherit defaults or logic from a family label.
3. **Ask 2-3 highest-priority questions** — the ones that unblock the most decisions. Skip questions whose answers are already in the config (de-duplicate).
4. **Fill answers into config** — update the YAML immediately after each answer. Show a human-readable decision diff; show raw YAML only when requested.
5. **Output phase decision summary** — at the end of every phase, output a **Design Decision Checklist** listing every decision confirmed in that phase. Format:

```
## Phase N 设计决策确认清单

| # | 决策项 | 确认值 | 来源 |
|---|--------|--------|------|
| 1 | 注视点持续时间 | 500ms | 用户确认 |
| 2 | 反应按键 | f/j/k | 用户确认 |
| 3 | 反应截止时间 | 2000ms | 建议值（待用户确认） |
| 4 | 按键映射 | f=红, j=绿, k=蓝 | 用户确认 |
| ... | ... | ... | ... |
```

Each decision's **来源** must be one of: `用户确认` / `模板建议（待确认）` / `通用建议（待确认）` / `自动推断（待确认）`. A proposed value is never confirmed merely because a template or reference supplied it.

6. **Get phase-level confirmation** — after showing the checklist, ask: "以上设计决策确认无误，进入下一阶段？" or equivalent. Do NOT advance until the user confirms.

7. **Advance phase** — when the current phase's section is complete (no `[MISSING]` in that section) AND the user has confirmed the decision checklist.

### Design Decision Registry (Universal)

Every decision — whether confirmed, defaulted, or inferred — must be tracked in a **Design Decision Registry** that spans all phases. This is NOT optional and is NOT limited to overflow scenarios.

The registry lives alongside the config YAML and persists throughout the
conversation. Use the phase-grouped table format in
[canvas-presentation.md](references/canvas-presentation.md).

Rules:
- **Every** non-trivial design choice (durations, key assignments, stimulus content, condition ratios, sequence repetitions, feedback presence, output format, etc.) must appear in the registry
- Source must be explicit: `用户确认` / `默认（范式惯例）` / `默认（通用）` / `自动推断`
- Defaulted items (`默认...` / `自动推断`) must be visually distinct (e.g., marked with ⚠️ or `[ASSUMED]`)
- The registry is cumulative — each phase appends to it
- Before code generation (Gate 5), present the FULL registry and require explicit user confirmation

### Priority order for questions (from trial-inward to experiment-outward):

```
Trial level (Phase 2):   window sequence → content → duration → response keys → key mapping → accuracy rules → output format
Trial level (Phase 3):   condition columns → trial counts → stimulus file paths
Sequence level (Phase 4): execution modes → repetitions → feedback placement → counterbalancing → looping
```

Never ask more than 3 questions in one response. Never skip a phase with `[MISSING]` fields. If all generic and paradigm questions for a phase are resolved with fewer than 3 questions, advance early — don't pad.

**<a id="must-confirm-overflow-rule"></a>Must-Confirm overflow rule**: When a phase has more Must-Confirm items + generic questions than the 3-question limit, handle overflow as follows:

1. **Batch compatible questions**: Combine related items into one question (e.g., "注视点 500ms，ITI 500-800ms 随机，反馈显示 500ms，这些时间参数可以吗？").
2. **Propose low-risk items with flag**: For items with a strong exact-reference convention, propose a default, enter it in the registry with status `proposed` and source `参考建议`, and flag it in the phase decision checklist. It is not confirmed until the user accepts it.
3. **Defer to next phase if logical**: Items that could be asked in a later phase without blocking current progress (e.g., feedback presence can be deferred to Phase 4 even if the paradigm file assigns it to Phase 2).
4. **If overflow is unavoidable**: State which items were defaulted and why, and invite the user to correct any: "以下 2 项按惯例默认设置，如需修改请告知：[列表]。"
5. **Registry review**: All defaulted/assumed items in the registry are reviewed at Gate 5 (Final Design Review) before code generation.

The goal: every Must-Confirm item is either explicitly confirmed by the user, or explicitly flagged as an assumption the user can correct — and all assumptions are reviewed before code is generated.

**When the user doesn't know an answer**: Offer a reasonable candidate based on an exact reference or common practice. Enter it in the registry as `proposed`, flag it, and explain that generation remains blocked until it is confirmed. Never turn a family convention into executable logic silently.

## Routing

| User request | Action |
|-------------|--------|
| New experiment (any starting format) | Unified Workflow Phase 1-5 |
| "帮我写/改/调试实验代码" | Route to [psy-exp-coder](../psy-exp-coder/SKILL.md) |
| "帮我检查这段实验代码能不能正式采集" | Route to [psy-exp-reviewer](../psy-exp-reviewer/SKILL.md); full audit |
| Code modification / debugging | Route to [psy-exp-coder](../psy-exp-coder/SKILL.md); apply change; show diff |
| Condition table generation | Use the confirmed condition semantics + [randomization.md](references/randomization.md); an exact paradigm reference may suggest checks only |

All three platforms (PsychoPy, jsPsych, Psychtoolbox) share the same Generation Pipeline (`ExperimentSpec → ExecutionPlan → Platform Adapter → Code`). The coder applies platform L1-L2 contracts and may consult an exact L3 reference, but the reference cannot supply missing experiment semantics.

**Platform reference coverage:**
- **PsychoPy**: 28 paradigm references and 45 quarantined demos. Generate only when the complete config maps to an implemented platform adapter.
- **jsPsych**: 26 legacy reference sources (mostly PsychoJS, which is a distinct runtime). Generate only from the pinned jsPsych 8.x adapter; never copy L3 API code.
- **Psychtoolbox**: 5 paradigm references and 100 quarantined demos. Generate only when the complete config maps to an implemented KbQueue/VBLTimestamp adapter.
Reference inventory is not generation coverage. A complete config is necessary but must still pass the host runtime's capability/profile check.

When a user requests any platform, build the config through Phases 1-4, then route to `psy-exp-coder` in Phase 5. The coder applies the unified Generation Pipeline with that platform's specific mappings.

## Paradigm Reference

**Core paradigms** (full spec with `## Must Confirm` and `## Condition File Columns`):

| User mentions | Read this file |
|---------------|---------------|
| Go/No-go, 反应抑制, response inhibition | [paradigms/go-nogo.md](paradigms/go-nogo.md) |
| Navon, 整体局部, global/local, hierarchical letters | [paradigms/navon.md](paradigms/navon.md) |
| Priming, 启动, prime-target, masked prime | [paradigms/priming.md](paradigms/priming.md) |
| Stroop, 斯特鲁普, color-word, 颜色词 | [paradigms/stroop.md](paradigms/stroop.md) |
| Eriksen Flanker, 侧翼冲突, center-surround | [paradigms/eriksen-flanker.md](paradigms/eriksen-flanker.md) |
| Simon, 西蒙任务, spatial compatibility | [paradigms/simon.md](paradigms/simon.md) |
| Rating, 评分, Likert, VAS | [paradigms/rating.md](paradigms/rating.md) |
| Stop-signal, 停止信号, SST, SSRT | [paradigms/stop-signal.md](paradigms/stop-signal.md) |
| IAT, 内隐联想测验, implicit association | [paradigms/iat.md](paradigms/iat.md) |
| N-back, 工作记忆, working memory | [paradigms/n-back.md](paradigms/n-back.md) |
| Dot-probe, 点探测, attentional bias, 注意偏向 | [paradigms/dot-probe.md](paradigms/dot-probe.md) |
| Visual search, 视觉搜索, set size, pop-out, conjunction | [paradigms/visual-search.md](paradigms/visual-search.md) |
| Task switching, 任务转换, switch cost, cognitive flexibility | [paradigms/task-switching.md](paradigms/task-switching.md) |
| EAST, 外在情感性西蒙, implicit attitude, 内隐态度, De Houwer | [paradigms/east.md](paradigms/east.md) |
| Questionnaire, 问卷, survey, Likert, 量表 | Read [references/supplementary-patterns.md](references/supplementary-patterns.md) |

**Extended paradigms**: Use their available sections as design evidence, but verify required headings and missing design details at intake rather than assuming uniform completeness. If a needed condition/data/example section is absent, collect it explicitly and record the gap.

Antisaccade · ANT · BART · Bilingual Stroop · Change Detection · Children Flanker · Choice RT · Climate Reflection · CPT · Corsi Blocks · Cyberball · Delay Discounting · Drag and Drop · Mental Rotation · Multisensory Nature · Numerical Stroop · Phone a Friend · Posner Cuing · Psychophysics Staircase · Rating to Choice · Sternberg · Ultimatum Game · WCST · Writing Distraction

→ See [paradigms/](paradigms/) for the full list. Each file follows the same naming convention: kebab-case matching the paradigm name.

## Related Files

Open when the task matches:

| File | Open when... |
|------|-------------|
| [config-schema.md](references/config-schema.md) | defining or validating the config YAML — field types, value formats, and all blocking validation rules |
| [condition-file.md](references/condition-file.md) | checking condition file format, column name rules, variable substitution `{column}` |
| [condition-file-generation.md](references/condition-file-generation.md) | **generating** condition xlsx files from design parameters — direct write or standalone script |
| [spec-template.md](references/spec-template.md) | need the full specification structure reference (config YAML is the active artifact) |
| [data-recording.md](references/data-recording.md) | defining output columns per trial, accuracy coding rules, incremental save patterns |
| [randomization.md](references/randomization.md) | setting up trial randomization, counterbalancing, consecutive-same constraints, seed |
| [timing.md](references/timing.md) | configuring RT measurement, response deadlines, ITI types, frame-accurate durations |
| [canvas-presentation.md](references/canvas-presentation.md) | presenting sequence rows, phase checklists, the Decision Registry, and Gate 5 review |
| [missing-information.md](references/missing-information.md) | unsure what must be confirmed with the user vs what can be defaulted |
| [supplementary-patterns.md](references/supplementary-patterns.md) | adding questionnaires, scales, debriefs, or participant-facing feedback |
| [example-walkthrough.md](references/example-walkthrough.md) | needing a concrete five-phase Stroop workflow example |
| [skill-writing-standard.md](references/skill-writing-standard.md) | creating, modifying, or reviewing any skill file in this system |

## Output Format

The Designer produces different output formats depending on the execution environment.

### Standalone (Claude Code / Codex terminal)

1. **Sequence Timeline** — sequence-row diagram of the trial structure with response rules (user-facing)
2. **Complete Design Decision Registry** — all decisions from all phases with sources (user-facing, presented at Gate 5)
3. **Completed config YAML** — saved single source of truth; report the path and display content on request
4. **Condition tables** — generated xlsx files (if not provided by user)

The Coder reads the config YAML and condition files to generate runnable code.

### Embedded (PsyCoder Studio Canvas)

When invoked as a plugin inside PsyCoder Studio, the Designer receives a live `CURRENT_SPEC` JSON object (PsyCoderExperimentSpecV2@2.4) and outputs structured data that the Canvas renders directly:

```json
{
  "assistantMessage": "concise explanation of what was designed or proposed",
  "questions": ["0 to 3 clarifying questions"],
  "decisions": [
    {
      "path": "meta.platform",
      "label": "Target Platform",
      "value": "psychopy",
      "source": "user",
      "status": "confirmed"
    }
  ],
  "missingFields": ["semantic paths still unresolved"],
  "commands": [
    {"type": "add_window", "payload": {"sequenceId": "seq-trial", "label": "Fixation", "durationMs": 500, "stimulus": {"staticText": "+"}}}
  ],
  "proposalSummary": "what the commands change on the Canvas",
  "warnings": ["scientific or destructive-change warnings"]
}
```

**Command types available**: create_experiment, update_experiment_meta, add_sequence, update_sequence, remove_sequence, reorder_sequences, add_window, update_window, remove_window, reorder_windows, move_window_to_sequence, update_condition_source, update_response_rule, set_platform, update_data_schema, update_timing_defaults, update_runtime_contract, update_output_contract.

**Canvas safety rules**:
- Return proposed commands only. The user must explicitly apply them.
- Reference only window and sequence IDs provided in CURRENT_SPEC, except new add_sequence may provide a unique stable sequenceId.
- Every add_window command must include sequenceId.
- Windows have no preset role or type. Describe behavior through label, stimulus/displayMode, timing, response, feedback, and data.
- Sequence execution (mode + repetitions) determines scope; never invent practice/formal repetition counts.
- Preserve existing confirmed values unless the user explicitly changes them.
- Removing a non-empty sequence requires removeWindows=true and is destructive; warn explicitly.
