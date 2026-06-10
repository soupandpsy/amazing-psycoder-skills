---
name: psy-exp-designer
description: Use for designing and specifying psychological experiments. Guides through a unified 5-phase workflow to produce a complete config YAML, then routes to psy-exp-coder for code generation. Does NOT generate code itself — the orchestration and specification layer. Supports PsychoPy, jsPsych, and Psychtoolbox with 38 paradigm references. Trigger for 中文/English requests about 心理学实验程序、实验代码、PsychoPy、trial/block结构、刺激呈现、随机化、反应时、条件表、Go/No-go、Navon、Stroop、priming、IAT、N-back、dot-probe、visual search、task switching、rating、stop-signal / 心理学実験、実験デザイン、サイコパイ / psychologisches Experiment, Experimentdesign / experience psychologique, protocole experimental, PsychoPy.
version: 1.3
status: stable
---

# Psychological Experiment Designer

## Version

v1.3 — stable, 2026-06-10. Sub-skill of [amazing-psycoder](../SKILL.md).

## Purpose

Convert psychological experiment ideas into a complete experiment specification (config YAML) through a single, unified workflow. Every design decision accumulates in the **config YAML** — the single source of truth. When the config is complete, this skill routes to `psy-exp-coder` for code generation.

This is the **orchestration and specification layer**. It does NOT generate code — it guides the user through progressive refinement of the experiment design, produces a validated config YAML, then routes to the platform coder for implementation.

## Design Philosophy

**用户的实验，系统的规范。** The user owns the experimental design — every decision is confirmed with them. The system provides the guardrails: paradigm-specific Must-Confirm lists, timing conventions, accuracy rules, and code quality standards. The Design Decision Registry ensures every detail is tracked, every assumption is flagged, and nothing reaches code generation without explicit user approval.

Core principles:
- **输出即交付** — the output (config YAML) is complete and ready for code generation, not a draft
- **渐进确认** — each design detail is confirmed before advancing; defaults are flagged as `[ASSUMED]` and reviewed at Gate 5
- **决策可追溯** — every decision's source is recorded (用户确认 / 范式惯例 / 自动推断)
- **先窗口后代码** — no code is generated before the trial window timeline is complete (Red Line #1)

## When Not to Use

- **Generating or modifying experiment code directly**: That's `psy-exp-coder`'s job. Route there instead.
- **Code review or production audit**: That's `psy-exp-reviewer`'s job. Route there instead.
- **Quick PsychoPy API questions**: If the user asks a general PsychoPy question unrelated to experiment design, answer directly without invoking the full workflow.

## Core Model

Every experiment follows this structure:

```
Experiment → Block → Trial → Window → Data
```

- **Block**: A group of trials sharing the same randomization or condition set. Block types: `practice`, `formal`, `rest`, `debrief`.
- **Window**: A single screen within a trial (fixation, stimulus, mask, feedback)
- **Trial**: One complete unit of stimulus → response → feedback
- **Data**: One row per trial, one column per measured variable

## Red Lines

Hard prohibitions. These must never be violated — no exceptions, no "just this once."

| # | Rule | Applies to | Why |
|---|------|-----------|-----|
| 1 | **No code generation before trial window timeline is complete** | All platforms | Code written without a validated window sequence will have structural errors that are expensive to fix |
| 2 | **No assumed response mapping** | All platforms | Which key means what answer must be confirmed with the user. Guessing invalidates accuracy data |
| 3 | **No `time.sleep()` / `core.wait()` in experiment code** | PsychoPy, jsPsych | Blocks the event loop; Escape becomes unresponsive. Use `CountdownTimer` loops instead |
| 4 | **No `event.getKeys(maxWait=...)`** | PsychoPy | Blocks the event loop. Use `keyboard.Keyboard` with `win.callOnFlip(kb.clock.reset)` |
| 5 | **No data saved only at end of experiment** | All platforms | Crash = all data lost. Save incrementally per trial or per block with `try/finally` |
| 6 | **No silent filling of `[MISSING]` values** | All platforms | Every `[MISSING]` must be resolved by asking the user or offering an explicitly-flagged default |
| 7 | **No Chinese/CJK text without an explicit font** | PsychoPy, Psychtoolbox | Platform default font lacks CJK glyphs; text will render as tofu (□□□). jsPsych relies on browser/OS fonts — verify but no explicit path needed |
| 8 | **No skipping paradigm Must-Confirm items** | All platforms | Each paradigm file lists critical design decisions. Unconfirmed items produce broken experiments |
| 9 | **No `rt_onset` omitted on response windows** | All platforms | Incorrect or missing RT onset invalidates all reaction time data. The coder will refuse to generate if absent |
| 10 | **No code delivery without reviewer pass** | All platforms | All generated code must pass through `psy-exp-reviewer` before data collection. Programming → Coder → Reviewer is a mandatory chain |

## Config as Single Source of Truth

The [experiment config YAML](references/config-schema.md) is the central artifact. Every design decision lives in one file:

```yaml
name:        # experiment name
paradigm:    # which paradigm
platform:    # psychopy / psychtoolbox / jsPsych
stimulus_folder:  # global path for image file references
windows:     # trial event sequence (box timeline → YAML)
blocks:      # block structure + condition file paths
response_rules:  # keys, deadline, accuracy logic
paradigm_config: # paradigm-specific settings
output:      # data directory, filename pattern
```

The conversation has one goal: **fill every `[MISSING]` field in this config**. The user can provide information in any form — prose description, file paths, partial YAML, xlsx files — and the system progressively accumulates it into the config.

## Trial Window Timeline Rule

When clarifying, summarizing, or designing trial logic, **always represent the trial as a sequence of window boxes before writing code**. Do not describe trial events in prose alone — visual timeline first, text second.

Each trial window box must include:

1. Window name (e.g., Fixation, Prime, Target, ITI)
2. Visual content shown on screen
3. Duration (ms, or `until response`)
4. Response rule (none / allowed keys / deadline)
5. **File/Folder** — stimulus file or folder used in this window (if applicable)
6. **Condition source** — which xlsx column drives this window (if applicable)
7. Data recorded at this step, if any

Use this format:

```text
   Window 1: Fixation            Window 2: Stimulus            Window 3: Response   
┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
│                      │      │                      │      │                      │
│          +           │  →   │      {stimulus}      │  →   │      {stimulus}      │
│                      │      │                      │      │                      │
└──────────────────────┘      └──────────────────────┘      └──────────────────────┘
    Duration: 500 ms              Duration: 500 ms            Duration: until key   
     Response: none                Response: none               Response: f / j     
       File: none             File: stimuli/images/*.png      Condition: conditions.xlsx
                                 Data: rt, key, acc                                 
```                                                               

**Max 3 windows per row** — if the trial has more than 3 windows, wrap to the next row.

After the box timeline, also provide a structured table:

| Window | Content | Duration | Response | File/Folder | Condition | Data |
|--------|---------|----------|----------|-------------|-----------|------|
| Fixation | + | 500 ms | none | none | none | none |
| Stimulus | {stimulus} | 500 ms | none | stimuli/images/*.png | {stimulus} col | none |
| Response | {stimulus} | until key | f/j | none | {correct_response} col | rt, key, acc |

If any part of the trial logic is unclear, mark it directly as `[MISSING]` inside the box and in the table. Do not silently fill in missing values.

**Do not generate experiment code until the trial window sequence is clear.**

## Unified Workflow

Every new experiment follows the same 5 phases. The order reflects how experimenters naturally design: **trial first (with rules), then blocks**. The config YAML is filled progressively.

```
Phase 1: Assess    → 收集已有信息
Phase 2: Windows   → 定义 Trial + 反应规则（最关键）
Phase 3: Conditions→ 定义 trial 序列（xlsx + 刺激文件）
Phase 4: Blocks    → 定义 block 结构和循环
Phase 5: Validate  → 验证并移交代码生成
```

### Blocking Gates

Hard checkpoints. The workflow does not advance past a gate until its condition is met. If a gate fails, return to the relevant phase; do not proceed.

| Gate | After | Condition | Fail → Return to |
|------|-------|-----------|------------------|
| **Gate 1** | Phase 2 | Trial window timeline has no `[MISSING]`. Every window has `name`, `content`, `duration`, `response`. Response windows have `rt_onset`. Response keys, mapping, accuracy rules, and output format are confirmed. Phase 2 decision checklist presented and user confirmed | Phase 2 |
| **Gate 2** | Phase 3 | Every `{column_name}` in `windows[]` exists in condition xlsx. Condition file is on disk OR has been generated by Phase 3. Stimulus folder (if used) resolves. Phase 3 decision checklist presented and user confirmed | Phase 2 or 3 |
| **Gate 3** | Phase 4 | Config has zero `[MISSING]` markers. All sections (`windows`, `blocks`, `response_rules`, `output`) are complete. Phase 4 decision checklist presented and user confirmed | Phase 2/3/4 (whichever section has `[MISSING]`) |
| **Gate 4** | Phase 5 | All validation rules pass. Validation rules 1-6 (blocking, from config-schema.md) must pass before code generation; rules 7-9 are design-level verification. No missing columns, no broken file paths, no ambiguous accuracy coding | Phase 1/2/3/4 (based on error type, per Phase 5 routing table) |
| **Gate 5** | Phase 5 (before coder) | **Final Design Review**: Full Design Decision Registry presented. User explicitly confirms ALL decisions (including `[ASSUMED]` items) before code generation. No decision left un-reviewed | Phase 1/2/3/4 (user can correct any decision) |

### Phase 1: Assess Input

Determine what the user already has, what paradigm, and what platform.

| User provides | Action |
|--------------|--------|
| Natural-language description ("我想做一个Stroop实验...") | Parse into skeleton config; flag all unknowns as `[MISSING]` |
| Partial config YAML | Load it; identify which sections are filled vs missing |
| config.yaml + conditions/*.xlsx | Load everything; validate; skip to Phase 5 if complete |
| Existing experiment code to modify | Identify the platform; read the code; apply changes; skip to Phase 5 |
| "帮我检查这段代码" | Route to `psy-exp-reviewer` directly |

Also resolve in Phase 1 if the user hasn't stated it:
- Paradigm (match to [paradigm file](paradigms/); ask if unclear)
- Platform (PsychoPy / Psychtoolbox / jsPsych)
- **Operating system + font (blocking)**: Every experiment using text stimuli must confirm the target OS and font before advancing past Phase 1. Ask: "实验在什么操作系统上运行？（macOS / Windows / Linux）" — this determines font paths. If the user doesn't know, the coder will generate auto-detection with a manual override switch. This is not optional — CJK text without proper font = □□□ tofu.

**After loading the paradigm file**: Cross-reference its `## Must Confirm` list against what the user already stated. For each unconfirmed item, assign it to the phase where it will be asked:

| Must Confirm item type | Target phase |
|------------------------|--------------|
| Stimulus identity, content, modality | Phase 2 |
| Key assignment, response mapping | Phase 2 |
| Timing values (durations, deadlines, SOA) | Phase 2 |
| Accuracy rules, error coding, catch trials | Phase 2 |
| Output format (data directory, filename) | Phase 2 |
| Trial counts, condition ratios | Phase 3 |
| Stimulus file source (image vs generated) | Phase 3 |
| Block count, trials per block, feedback presence | Phase 4 |
| Counterbalancing, block order | Phase 4 |

If a Must Confirm item doesn't fit any later phase (e.g., paradigm-specific correctness logic), ask it now in Phase 1. Do not leave Must Confirm items unassigned.

**Output**: Config with `name`, `paradigm`, `platform`, OS filled. Phase 1 Decision Checklist presented for user confirmation before advancing to Phase 2.

### Phase 2: Define Windows & Rules (Trial)

Build the trial window timeline — the most critical phase. Every screen event in a single trial becomes a window. Also finalize all response rules here: key mapping, accuracy logic, and output format. These belong together because the response keys defined in the window timeline directly determine the mapping and accuracy rules.

**What to determine** for each window:
- Window name and order (e.g., Fixation → Stimulus → Response → Feedback → ITI)
- Content (literal text, `{column_reference}`, or image file path)
- Duration (fixed ms, `[min, max]`, `until_key`, or `self_paced`)
- Response rule (none / allowed keys / deadline)
- File/folder reference (which stimulus files?)
- Condition source (which xlsx column drives this window?)

**How to present**: Window name centered above the box, content centered inside, other fields centered below. Box columns 24 chars wide with 6-space gaps. Arrow (→) between boxes.

```text
   Window 1: Fixation            Window 2: Stimulus            Window 3: Response   
┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
│                      │      │                      │      │                      │
│          +           │  →   │       [MISSING]      │  →   │       [MISSING]      │
│                      │      │                      │      │                      │
└──────────────────────┘      └──────────────────────┘      └──────────────────────┘
     Duration: [MISSING]           Duration: [MISSING]          Duration: until key   
      Response: none                Response: none               Response: [MISSING]  
        File: none                  File: [MISSING]             Condition: [MISSING]  
                                 Data: rt, key, acc                                 

Format rules:
- Window name/sequence number centered above the box (column width = 24 chars, box + borders)
- Content centered inside the box (box interior = 22 characters)
- Duration, Response, File, Condition, Data centered below the box within each column
- Arrow (→) between windows in the same row: `  →   ` (6 chars, matches gap)
- Box gap = 6 spaces between all columns, all rows aligned
- **Max 3 windows per row** — windows 4+ wrap to the next row automatically
- [MISSING] marks unresolved items that must be confirmed before Gate 1
```

**Questions (max 3)**:
1. "每个窗口的持续时间是多少？反应窗口的截止时间？"
2. "被试按哪些键反应？哪个键对应哪个条件？"
3. "刺激呈现什么内容？文字、图片还是图形？"

Also ask any paradigm Must-Confirm items assigned to Phase 2 (stimulus identity, timing values, key assignment, accuracy rules). Phase 2 typically carries the most Must-Confirm items — if paradigm questions + generic questions exceed the 3-question limit, apply the [Must-Confirm overflow rule](#must-confirm-overflow-rule) (batch compatible questions, default low-risk items with ⚠️ flag, defer to later phases where logical).

**How many windows?** The paradigm determines the window count — it is NOT fixed at 5. Standard RT tasks may have 4 (Fixation → Stimulus → Response → ITI). Masked priming may need 6+ (Forward Mask → Prime → Backward Mask → Target → Response → ITI). The paradigm file's `## Example` section shows the canonical window sequence.

**Stimulus + Response: merge or split?** Two patterns are valid:
- **Split**: Stimulus window (fixed duration, no response) → Response window (stimulus stays + keys accepted). Use when the stimulus must be visible for a fixed time before responses are allowed. RT is measured from Response window onset, excluding stimulus encoding time.
- **Merged**: A single window with `duration: until_key` and `response: [keys]`. Use when the participant responds immediately to the stimulus (e.g., Stroop, Flanker). RT is measured from stimulus onset.

**rt_onset — auto-inferred, not asked.** Do NOT ask the user to choose between split/merged or to specify rt_onset directly. Instead, infer it from the window structure and inform the user:

| Window structure | Inferred rt_onset | Example paradigms |
|------------------|-------------------|-------------------|
| One window has both `content: "{stimulus}"` AND `response: [keys]` | `rt_onset: self` (merged) | Stroop, Flanker, Simon, IAT, EAST |
| Separate Stimulus window (no response) → Response window (keys accepted) | `rt_onset: self` on response window (Go/No-go, Stop-signal) OR `rt_onset: <stimulus_window_name>` (Dot-probe, Priming). **Default**: for tasks where RT is measured from response-window onset use `self`; for tasks where RT is measured from initial stimulus onset, use the stimulus window name | Go/No-go (self), Stop-signal (self), Dot-probe (probe window name), Priming (target window name) |

**How to present to the user**: Instead of asking "split or merged?", state the inference and confirm:
> "根据你的 trial 结构，反应时将从 **[窗口名]** 开始计时（[合并/分离]模式）。这符合 **[范式名]** 的标准做法。如有特殊需求可调整。"

This transforms a technical decision the user can't make into an informed confirmation. The coder's code-generation-specific check #3 (rt_onset resolvable) remains as the safety net.

### Response Rules (also Phase 2)

Once windows are defined, immediately finalize the response rules — don't defer to a later phase. The response keys named in the window timeline directly determine these rules.

**What to determine**:
- **Response mapping**: Which key = which answer (e.g., f=red, j=green, k=blue). Ask this alongside the key list in the windows phase — it's unnatural to separate them
- **Accuracy logic**: What makes a response correct for each condition. For simple designs, this is just `key == correct_response`. For paradigms like Go/No-go: no-go + no key = correct; go + no key = miss
- **No-go / stop / catch trial handling**: How to score trials where the correct response is to NOT respond
- **Deadline**: Maximum response time per trial (default: 2000ms; adjust based on paradigm conventions)

**Questions (ask alongside window questions above — don't create a separate question round)**:
- "哪个键对应哪个条件？" (if mapping not obvious from key list)
- "No-go试次不按键=正确，按键=错误，确认吗？" (paradigm-specific, from Must-Confirm)

**Output format** — also finalized here, but offer defaults; only ask if customization needed:
- Data directory: `data/` (default)
- Filename pattern: `sub-{subject_id}_{task_name}_{date}.csv` (default)
- Question (only if user needs changes): "数据用默认设置保存，需要修改吗？" (counts toward the 3-question limit only if asked)

**Output**: Config `windows[]`, `response_rules`, `paradigm_config`, and `output` sections complete. Phase 2 Decision Checklist presented for user confirmation. Gate 1 check: windows have no `[MISSING]`, response keys and mapping confirmed, accuracy rules defined, rt_onset auto-inferred.

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

**Output**: Condition xlsx files (validated or generated). Config `windows[].stimulus_folder` filled. Phase 3 Decision Checklist presented for user confirmation.

### Phase 4: Set Block Structure

With the trial defined (Phase 2) and conditions built (Phase 3), determine how trials are grouped into blocks and how blocks loop.

**What to determine**:
- Block types: practice (with feedback, repeatable), formal (no feedback), rest (pause), debrief (results display)
- Trials per block — now informed by condition counts from Phase 3
- Block order and iteration logic
- Between-block instructions or rest screens
- Feedback presence per block (practice only? formal too?)
- **Counterbalancing**: Is block order fixed or counterbalanced across subjects? If counterbalanced, by what rule (subject ID parity, Latin square)? Required by most paradigms — check the paradigm file's `## Must Confirm` and `## Randomization Checks`.

**Before finalizing blocks**, run this consistency check:
- If any block has `feedback: true` but no Feedback window exists in `windows[]`, insert one after the Response window and before ITI: `{name: Feedback, content: correct_incorrect, duration: 500, response: none}`.
- **How `feedback` and `show_in` interact**: A Feedback window appears in a block when the block's `feedback` is `true`. The `show_in` field restricts further — e.g., `show_in: [practice]` means the Feedback window only appears in practice blocks, even if a formal block also sets `feedback: true`. If `show_in` is absent, the window respects only the block's `feedback` flag. If a block has `feedback: false`, the Feedback window is skipped regardless of `show_in`.

**Questions (max 3)**:
1. "实验分为几个 block？练习几个 trial，正式每个 block 几个 trial？"
2. "反馈在哪些 block 显示？只在练习还是正式实验也有？"
3. "block 呈现顺序是固定的还是在被试间平衡？"

For Rest blocks, also ask: "休息时屏幕显示什么文字？" (default: "休息一下，按空格键继续").

Also ask any paradigm Must-Confirm items assigned to Phase 4 (block order, counterbalancing).

**Output**: Config `blocks[]` section complete. Each block has `name`, `condition_file`, `type`, `feedback`, `trials`. Phase 4 Decision Checklist presented for user confirmation.

### Phase 5: Validate & Route

Cross-check everything, **present the final design to the user for confirmation**, then route to the coder for code generation.

**Step 1: Technical validation** — Run all 9 rules from [config-schema.md § Validation Rules](references/config-schema.md). These are the authoritative checks.

**If validation fails**: Report specific errors. Return to the relevant phase based on error type:
- Missing config metadata (`name`, `paradigm`, `platform`) → Phase 1
- Missing or incomplete window definitions (`content`, `duration`, `response`, `rt_onset`), missing response rules, ambiguous accuracy coding → Phase 2
- Missing condition file, invalid columns, row count mismatch, or missing stimulus files → Phase 3
- Missing block fields or invalid block types → Phase 4

**Step 2: Final Design Review (Gate 5, blocking)** — Present the final design for user confirmation. This is mandatory before routing to code generation.

**CRITICAL: Do NOT display the full config YAML.** The YAML is an internal machine-readable artifact — most users cannot read it. Displaying raw YAML during confirmation confuses users and undermines trust. Instead, present only these two user-facing outputs:

1. **Trial Window Timeline** — the box diagram with response rules (same format as Phase 2 output)
2. **Complete Design Decision Registry** — all decisions from all phases in table form

Format:

```
## 最终设计确认

### Trial 窗口与反应规则

   Window 1: Fixation            Window 2: Stroop              Window 3: Feedback   
┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
│                      │      │                      │      │                      │
│          +           │  →   │       色词文字       │  →   │      正确/错误      │
│                      │      │                      │      │                      │
└──────────────────────┘      └──────────────────────┘      └──────────────────────┘
         500ms                       until key                        500ms          
         none                       f / j / k                        none           
                                  ← RT onset                                       

   Window 4: ITI     
┌──────────────────────┐
│                      │
│                      │
│                      │
└──────────────────────┘
      600-900ms       
         none          

| Window | Content | Duration | Response | Condition | Data |
|--------|---------|----------|----------|-----------|------|
| Fixation | + | 500 ms | none | none | none |
| Stroop | 色词文字 | until key | f/j/k | {word}, {ink_color} | rt, key, acc |
| Feedback | 正确/错误 | 500 ms | none | {correct_response} | none |
| ITI | (blank) | 600-900 ms | none | none | none |

### 完整决策注册表

| # | 阶段 | 决策项 | 确认值 | 来源 |
|---|------|--------|--------|------|
| 1 | Phase 1 | 实验范式 | Stroop | 用户描述 |
| 2 | Phase 1 | 平台 | PsychoPy | 用户确认 |
| 3 | Phase 1 | 操作系统 | macOS | 用户确认 |
| 4 | Phase 2 | 窗口序列 | Fixation→Stroop→Feedback→ITI | 用户确认 |
| 5 | Phase 2 | 注视点持续时间 | 500ms | 默认（范式惯例） ⚠️ |
| 6 | Phase 2 | 反应按键 | f/j/k | 用户确认 |
| 7 | Phase 2 | 按键映射 | f=红, j=绿, k=蓝 | 用户确认 |
| ... | ... | ... | ... | ... |

⚠️ = 默认/推断项，请在生成代码前特别确认
```

- Items marked ⚠️ are defaults/assumptions — the user MUST be prompted to review them
- Ask: "以上所有设计决策确认无误，可以生成代码？如需修改请指定编号和新值。"
- Do NOT route to the coder until the user explicitly confirms the full registry
- If the user wants to change any item, return to the relevant phase, update the config, and re-run validation
- **The config YAML is never shown to the user.** It is the internal artifact passed silently to the coder in Step 3

**Parameter Quick-Reference Table**: In addition to the Design Decision Registry, present a compact parameter table so users can find and edit key values in the generated code without reading YAML:

```
### 参数速查表 (Parameter Quick Reference)

| 参数 | 值 | 代码位置 |
|------|-----|---------|
| 注视点持续时间 | 500 ms | Line ~85: FIXATION_DUR |
| 刺激呈现时间 | 500 ms | Line ~86: STIM_DUR |
| 反应截止时间 | 2000 ms | Line ~87: RESP_DEADLINE |
| ITI 范围 | 600-900 ms | Line ~88: ITI_MIN, ITI_MAX |
| 反应按键 | f, j, k | Line ~91: VALID_KEYS |
| 按键映射 | f=红, j=绿, k=蓝 | Line ~94: KEY_MAP |
| 练习 trial 数 | 20 | Line ~97: N_PRACTICE |
| 正式 block 数 | 2 × 60 | Line ~100: N_BLOCKS, TRIALS_PER_BLOCK |
| 数据保存路径 | data/ | Line ~103: DATA_DIR |
| 字体配置 | FONT_AUTO_DETECT | Line ~50: FONT_CONFIG |
```

The parameter table is a **compact supplement** to the Design Decision Registry — it focuses on editable values and their code locations. The full registry remains the canonical record of all design decisions with sources.

**Step 3: Code generation** — Only after Gate 5 passes (full registry confirmed), route to `psy-exp-coder` with the completed config. After code is generated, route to `psy-exp-reviewer` for audit. No experiment code is considered complete until it passes reviewer audit with `ready_for_collection` or `ready_after_minor_fixes`.

> **下一步**: 实验设计完成。输入 `/psy-exp-coder` 并提供 config 开始生成实验代码。生成后输入 `/psy-exp-reviewer` 审计代码。

## Question Protocol

At every phase, follow this protocol:

1. **Show current design state** — display what's known and what's still `[MISSING]` using the phase decision checklist format (not raw YAML). The user must see what's confirmed and what's unknown before answering more questions. Raw YAML is an internal format — users read decision tables, not YAML.
2. **Check paradigm Must-Confirm items** — before asking generic phase questions, check if any paradigm Must-Confirm items are assigned to this phase. Paradigm-specific questions take priority over generic ones.
3. **Ask 2-3 highest-priority questions** — the ones that unblock the most decisions. Skip questions whose answers are already in the config (de-duplicate).
4. **Fill answers into config** — update the YAML immediately after each answer. Show the diff so the user sees what changed.
5. **Output phase decision summary** — at the end of every phase, output a **Design Decision Checklist** listing every decision confirmed in that phase. Format:

```
## Phase N 设计决策确认清单

| # | 决策项 | 确认值 | 来源 |
|---|--------|--------|------|
| 1 | 注视点持续时间 | 500ms | 用户确认 |
| 2 | 反应按键 | f/j/k | 用户确认 |
| 3 | 反应截止时间 | 2000ms | 默认（范式惯例） |
| 4 | 按键映射 | f=红, j=绿, k=蓝 | 用户确认 |
| ... | ... | ... | ... |
```

Each decision's **来源** must be one of: `用户确认` / `默认（范式惯例）` / `默认（通用）` / `自动推断`. Defaulted decisions must be flagged so the user can correct them before advancing.

6. **Get phase-level confirmation** — after showing the checklist, ask: "以上设计决策确认无误，进入下一阶段？" or equivalent. Do NOT advance until the user confirms.

7. **Advance phase** — when the current phase's section is complete (no `[MISSING]` in that section) AND the user has confirmed the decision checklist.

### Design Decision Registry (Universal)

Every decision — whether confirmed, defaulted, or inferred — must be tracked in a **Design Decision Registry** that spans all phases. This is NOT optional and is NOT limited to overflow scenarios.

The registry lives alongside the config YAML and persists throughout the conversation:

```
## 实验设计决策注册表

### Phase 1: Assess
| # | 决策项 | 值 | 来源 |
|---|--------|-----|------|
| 1 | 实验范式 | Stroop | 用户描述 |
| 2 | 平台 | PsychoPy | 用户确认 |
| 3 | 操作系统 | macOS | 用户确认 |

### Phase 2: Windows & Rules
| # | 决策项 | 值 | 来源 |
|---|--------|-----|------|
| ... | ... | ... | ... |
```

Rules:
- **Every** non-trivial design choice (durations, key assignments, stimulus content, condition ratios, block counts, feedback presence, output format, etc.) must appear in the registry
- Source must be explicit: `用户确认` / `默认（范式惯例）` / `默认（通用）` / `自动推断`
- Defaulted items (`默认...` / `自动推断`) must be visually distinct (e.g., marked with ⚠️ or `[ASSUMED]`)
- The registry is cumulative — each phase appends to it
- Before code generation (Gate 5), present the FULL registry and require explicit user confirmation

### Priority order for questions (from trial-inward to experiment-outward):

```
Trial level (Phase 2):   window sequence → content → duration → response keys → key mapping → accuracy rules → output format
Trial level (Phase 3):   condition columns → trial counts → stimulus file paths
Block level  (Phase 4):  block types → trials per block → feedback per block → counterbalancing → looping
```

Never ask more than 3 questions in one response. Never skip a phase with `[MISSING]` fields. If all generic and paradigm questions for a phase are resolved with fewer than 3 questions, advance early — don't pad.

**<a id="must-confirm-overflow-rule"></a>Must-Confirm overflow rule**: When a phase has more Must-Confirm items + generic questions than the 3-question limit, handle overflow as follows:

1. **Batch compatible questions**: Combine related items into one question (e.g., "注视点 500ms，ITI 500-800ms 随机，反馈显示 500ms，这些时间参数可以吗？").
2. **Default low-risk items with flag**: For items with strong paradigm conventions, apply the default immediately, enter it in the registry with source `默认（范式惯例）`, and flag it in the phase decision checklist. Do not consume a question slot.
3. **Defer to next phase if logical**: Items that could be asked in a later phase without blocking current progress (e.g., feedback presence can be deferred to Phase 4 even if the paradigm file assigns it to Phase 2).
4. **If overflow is unavoidable**: State which items were defaulted and why, and invite the user to correct any: "以下 2 项按惯例默认设置，如需修改请告知：[列表]。"
5. **Registry review**: All defaulted/assumed items in the registry are reviewed at Gate 5 (Final Design Review) before code generation.

The goal: every Must-Confirm item is either explicitly confirmed by the user, or explicitly flagged as an assumption the user can correct — and all assumptions are reviewed before code is generated.

**When the user doesn't know an answer**: Offer a reasonable default based on paradigm conventions (from the paradigm file) or common practice. Enter it in the registry with source `默认（通用）` and flag it. Tell the user: "通常用500ms，我先按这个设定，后续可以改。"

## Supplementary Patterns

These patterns extend the core 5-phase workflow. They are optional but recommended for production-quality experiments.

### Questionnaire / Scale Integration

When the experiment includes surveys, scales, or demographic collection, insert a **Questionnaire Phase** between Phase 4 (Blocks) and Phase 5 (Validate). This phase follows the same window-condition-block pattern but with survey-specific concerns:

**Demographics** — Single-item windows with button response or form input:
- Sex (buttons), Age (number input with range validation), Education (dropdown)
- Each item = one window block with `response: [keys]` or `response: [mouse]`
- Validation: age range, required fields

**Likert Scales** — Multi-item scales with stimulus content from condition variables:
- Each item = one trial, stimulus text from a condition column
- Response: numbered buttons (1-4, 1-7, etc.)
- Data: tag each item with scale name + item index for later scoring
- **Reverse scoring**: Mark reverse-coded items. Score computation happens in debrief.

**Scale Scoring** — Computed in the debrief stage (not during trials):
- Filter data by scale name, compute per-item means respecting reverse coding
- Formula: `if item_i in reverse_items: score = likert_min + likert_max - response`
- Display: `MEAN('RSES', rev=[3,5,8,9,10], likert=[1,4])`

### Debrief / Results Feedback

After the main experiment and before the final "thank you" screen, insert a **Debrief Phase** that computes and displays results:

1. **Scale scores**: Means with reverse-scoring applied, displayed to participant
2. **Task performance**: Accuracy, mean RT, number of commission/omission errors
3. **Paradigm-specific scores**: IAT D-score, EAST effect, Stroop interference, n-back d'
4. **Validity checks**: Too-fast rate (>10% RT < 300ms = invalid), accuracy floor

This phase is a `Block` type `debrief` — it reads saved experiment data, computes scores, and displays them. No new data is collected.

## Routing

| User request | Action |
|-------------|--------|
| New experiment (any starting format) | Unified Workflow Phase 1-5 |
| "帮我写/改/调试实验代码" | Route to [psy-exp-coder](../psy-exp-coder/SKILL.md) |
| "帮我检查这段实验代码能不能正式采集" | Route to [psy-exp-reviewer](../psy-exp-reviewer/SKILL.md); full audit |
| Code modification / debugging | Route to [psy-exp-coder](../psy-exp-coder/SKILL.md); apply change; show diff |
| Condition table generation | Use [randomization.md](references/randomization.md) + paradigm file |

All three platforms (PsychoPy, jsPsych, Psychtoolbox) share the same Generation Pipeline (Config→Code). The coder applies the same pipeline to any platform, using that platform's L1 skeleton + L2 mapping + L3 paradigm references.

**Platform coverage:**
- **PsychoPy**: 27 paradigm references, 45 demos. Full generation from config YAML.
- **jsPsych**: 25 paradigm references (22 PsychoJS + 1 lab.js + 2 jsPsych 6.1.0). Full generation from config YAML using jsPsych 7.x API.
- **Psychtoolbox**: 5 paradigm references + 100 demos. Full generation from config YAML using KbQueue + VBLTimestamp API.

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
| Questionnaire, 问卷, survey, Likert, 量表 | See [Supplementary Patterns](#supplementary-patterns) |

**Extended paradigms** (reference descriptions; can still be used with the workflow but may lack `## Condition File Columns`, `## Data Output Columns`, and `## Example` — ask paradigm-specific questions manually. All extended paradigms do include `## Must Confirm`):

Antisaccade · ANT · BART · Bilingual Stroop · Change Detection · Children Flanker · Choice RT · Climate Reflection · CPT · Corsi Blocks · Cyberball · Delay Discounting · Drag and Drop · Mental Rotation · Multisensory Nature · Numerical Stroop · Phone a Friend · Posner Cuing · Psychophysics Staircase · Rating to Choice · Sternberg · Ultimatum Game · WCST · Writing Distraction

→ See [paradigms/](paradigms/) for the full list. Each file follows the same naming convention: kebab-case matching the paradigm name.

## Related Files

Open when the task matches:

| File | Open when... |
|------|-------------|
| [config-schema.md](references/config-schema.md) | defining or validating the config YAML — field types, value formats, all 9 validation rules |
| [condition-file.md](references/condition-file.md) | checking condition file format, column name rules, variable substitution `{column}` |
| [condition-file-generation.md](references/condition-file-generation.md) | **generating** condition xlsx files from design parameters — direct write or standalone script |
| [spec-template.md](references/spec-template.md) | need the full specification structure reference (config YAML is the active artifact) |
| [data-recording.md](references/data-recording.md) | defining output columns per trial, accuracy coding rules, incremental save patterns |
| [randomization.md](references/randomization.md) | setting up trial randomization, counterbalancing, consecutive-same constraints, seed |
| [timing.md](references/timing.md) | configuring RT measurement, response deadlines, ITI types, frame-accurate durations |
| [missing-information.md](references/missing-information.md) | unsure what must be confirmed with the user vs what can be defaulted |
| [skill-writing-standard.md](references/skill-writing-standard.md) | creating, modifying, or reviewing any skill file in this system |

## Skill Authoring Rule

When the user asks to create, modify, review, or reorganize a Skill, first read `references/skill-writing-standard.md` and follow it. Do not create or edit Skills without checking the standard.

## Example: Unified Workflow in Action

> **Note**: This is a condensed inline example for quick reference. The full Stroop specification example is embedded in [paradigms/stroop.md](paradigms/stroop.md) under `## Example`. The paradigm file is authoritative for paradigm-specific logic; this inline example demonstrates the workflow mechanics.

**User input:**
> "我想做一个Stroop实验，被试看到颜色词（红、绿、蓝），字本身也有颜色，判断字的颜色，按f/j键反应。先指导语，然后20个练习trial，然后2个正式block各60个trial"

### Phase 1: Assess

Config skeleton from what was stated. Load [paradigms/stroop.md](paradigms/stroop.md).

```yaml
name: "Stroop Color-Word Task"
paradigm: stroop
platform: [MISSING]
```

Detected from input: 3 words (红/绿/蓝), 3 ink colors, f/j keys (only 2 keys for 3 colors → conflict flagged), practice 20 trials, 2 formal blocks × 60.

**Questions:**
1. "使用什么平台？PsychoPy？"
2. "只有f/j两个键，三种颜色（红/绿/蓝），蓝色对应哪个键？还是只用两种颜色？"

### User: "PsychoPy，蓝色按k键"

---

### Phase 2: Define Windows & Rules

Build the trial window timeline, then immediately finalize key mapping and accuracy rules:

```text
   Window 1: Fixation            Window 2: Stroop              Window 3: Feedback   
┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
│                      │      │                      │      │                      │
│          +           │  →   │       色词文字       │  →   │      正确/错误      │
│                      │      │                      │      │                      │
└──────────────────────┘      └──────────────────────┘      └──────────────────────┘
     Duration: [MISSING]           Duration: until key          Duration: 500 ms     
      Response: none                Response: f / j / k          Response: none      
        File: none                Condition: {word}, {ink}      Condition: {correct_resp}
                                 Data: rt, key, acc                                 

   Window 4: ITI     
┌──────────────────────┐
│                      │
│                      │
│                      │
└──────────────────────┘
     Duration: [MISSING]
      Response: none   
     Condition: none   
```

| Window | Content | Duration | Response | File | Condition | Data |
|--------|---------|----------|----------|------|-----------|------|
| Fixation | + | [MISSING] | none | none | none | none |
| Stroop | 色词文字 | until key | f/j/k | none | {word}, {ink_color} | rt, key, acc |
| Feedback | 正确/错误 | 500 ms | none | none | {correct_response} | none |
| ITI | (blank) | [MISSING] | none | none | none | none |

**Questions:**
1. "注视点呈现多久？ITI多久？（通常注视点500ms，ITI随机600-900ms）"
2. "确认按键映射：f=红色，j=绿色，k=蓝色，可以吗？"
3. "数据用默认设置保存（data/文件夹），需要修改吗？"

### User: "注视点500ms，ITI随机600-900ms，按键映射没问题，默认保存"

Windows + rules complete:

```yaml
windows:
  - name: Fixation
    content: "+"
    duration: 500
    response: none
  - name: Stroop
    content: "{word}"
    duration: until_key
    response: [f, j, k]
    rt_onset: self
    data: [rt, key, acc]
  - name: Feedback
    content: correct_incorrect
    duration: 500
    response: none
    show_in: [practice]       # still unknown — asked in Phase 4
  - name: ITI
    content: ""
    duration: [600, 900]
    response: none

response_rules:
  correct: "{correct_response}"
  deadline: 2000
  mapping:
    f: red
    j: green
    k: blue

paradigm_config:
  target_dimension: ink_color
  distractor_dimension: word_meaning
  congruency_ratio: 50:50
  max_consecutive_same_response: 3

output:
  directory: "data/"
  filename_pattern: "sub-{subject_id}_stroop_{date}.csv"
```

---

### Phase 3: Build Conditions

No existing xlsx files → generate from design:
- 3 words × 3 ink colors = 9 conditions
- 50:50 congruent:incongruent
- Condition xlsx columns: `{word}`, `{ink_color}`, `{correct_response}` (all referenced by windows)

**Questions:**
1. "刺激是文字直接生成（TextStim），还是需要图片文件？如果是图片，放在哪个文件夹？"

### User: "直接生成文字就行"

Conditions structured. Stimulus: text-based, no image folder needed.

---

### Phase 4: Set Block Structure

Now that the trial is defined (4 windows) and conditions are known (9 types, 50:50), determine block grouping and looping:

Known from user's initial description: Practice 20 trials, 2 formal blocks × 60 trials.

**Questions:**
1. "反馈只在练习阶段显示，还是正式实验也有？"

### User: "反馈只在练习"

Blocks complete:

```yaml
blocks:
  - name: Practice
    condition_file: "conditions/practice.xlsx"
    type: practice
    trials: 20
    feedback: true
    repeatable: true
  - name: Block_1
    condition_file: "conditions/block_1.xlsx"
    type: formal
    trials: 60
    feedback: false
  - name: Block_2
    condition_file: "conditions/block_2.xlsx"
    type: formal
    trials: 60
    feedback: false
```

---

### Phase 5: Validate & Route

All `[MISSING]` resolved. 9 validation checks pass. Route to psy-exp-coder for code generation.

---

## Code Modification Example

**Input:**
> "这个实验的ITI现在是500 ms，我想改成随机500-800 ms，你帮我改一下代码"

**Output:** Identify the ITI parameter in the existing code, change from fixed to random range, show affected lines only.

## Output Format

For every new experiment, the designer produces:

1. **Trial Window Timeline** — box diagram of the trial sequence with response rules (user-facing)
2. **Complete Design Decision Registry** — all decisions from all phases with sources (user-facing, presented at Gate 5)
3. **Completed config YAML** — the single source of truth (internal artifact, passed to coder; NOT displayed to user)
4. **Condition tables** — generated xlsx files (if not provided by user)

The coder produces the runnable code, README, and pre-collection checklist. The reviewer produces the audit report and readiness label.
