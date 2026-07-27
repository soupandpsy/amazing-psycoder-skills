# Example: Unified Workflow in Action

This file demonstrates the complete 5-phase workflow with a realistic Stroop experiment. Use this as a reference for how each phase should unfold.

> **Note**: This is a condensed example for quick reference. The full Stroop specification is also embedded in [../paradigms/stroop.md](../paradigms/stroop.md) under `## Example`. The paradigm file is authoritative for paradigm-specific logic; this file demonstrates the workflow mechanics.

**User input:**
> "我想做一个Stroop实验，被试看到颜色词（红、绿、蓝），字本身也有颜色，判断字的颜色，按f/j键反应。先指导语，然后20个练习trial，然后2个正式block各60个trial"

## Phase 1: Assess

Config skeleton from what was stated. Load [paradigms/stroop.md](../paradigms/stroop.md).

```yaml
name: "Stroop Color-Word Task"
paradigm: stroop
platform: [MISSING]
```

Detected from input: 3 words (红/绿/蓝), 3 ink colors, f/j keys (only 2 keys for 3 colors → conflict flagged), practice 20 trials, 2 formal loop sequences × 60.

**Questions:**
1. "使用什么平台？PsychoPy？"
2. "只有f/j两个键，三种颜色（红/绿/蓝），蓝色对应哪个键？还是只用两种颜色？"

### User: "PsychoPy，蓝色按k键"

---

## Phase 2: Define Windows & Rules

Build the trial window timeline, then immediately finalize key mapping and accuracy rules:

```text
序列: 练习
  execution: loop (每个试次一次，重复 20 次)

  ┌─ 注视点 ────┐  ┌─ 刺激 ──────┐  ┌─ 反应 ────────┐  ┌─ 反馈 ─────────┐  ┌─ ITI ──────┐
  │ "+"        │  │ "色词文字"   │  │ "色词文字"    │  │ "正确/错误"    │  │ ""         │
  │ [MISSING]  │→ │ until_key   │→ │ until_key     │→ │ 500ms           │→ │ [MISSING]  │
  │ 无响应     │  │ 无响应      │  │ [f, j, k]     │  │ 无响应          │  │ 无响应     │
  └────────────┘  └─────────────┘  └───────────────┘  └─────────────────┘  └────────────┘
                                            RT: self
                                            数据: rt, key, acc

序列: 正式实验
  execution: loop (每个试次一次，重复 60 次)

  ┌─ 注视点 ────┐  ┌─ 刺激 ──────┐  ┌─ 反应 ────────┐  ┌─ ITI ──────┐
  │ "+"        │  │ "色词文字"   │  │ "色词文字"    │  │ ""         │
  │ [MISSING]  │→ │ until_key   │→ │ until_key     │→ │ [MISSING]  │
  │ 无响应     │  │ 无响应      │  │ [f, j, k]     │  │ 无响应     │
  └────────────┘  └─────────────┘  └───────────────┘  └────────────┘
                                           RT: self
                                           数据: rt, key, acc

序列: 指导语    → execution: once   → [MISSING]
序列: 结束      → execution: once   → [MISSING]
```

| 窗口 | 内容 | Duration | 响应 | 条件绑定 | 数据 |
|--------|---------|----------|----------|-----------|------|
| 注视点 | + | [MISSING] | 无 | 无 | onset |
| 刺激 | 色词文字 | until_key | [f, j, k] | {word}, {ink_color} | onset, rt, key, acc |
| 反馈 | 正确/错误 | 500ms | 无 | {correct_response} | 无 |
| ITI | (blank) | [MISSING] | 无 | 无 | onset |

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
    response_event: key_down
    rt_onset: self
    rt_rationale: "RT starts at the verified display onset of the scored color word"
    rt_contract_status: confirmed
    data: [rt, key, acc]
  - name: Feedback
    content: correct_incorrect
    duration: 500
    response: none
    show_in: [practice]
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
  filename_pattern: "sub-{subject_id}_stroop_{run_id}.csv"
```

---

## Phase 3: Build Conditions

No existing xlsx files → generate from design:
- 3 words × 3 ink colors = 9 conditions
- 50:50 congruent:incongruent
- Condition xlsx columns: `{word}`, `{ink_color}`, `{correct_response}` (all referenced by windows)

**Questions:**
1. "刺激是文字直接生成（TextStim），还是需要图片文件？如果是图片，放在哪个文件夹？"

### User: "直接生成文字就行"

Conditions structured. Stimulus: text-based, no image folder needed.

---

## Phase 4: Set Sequence Structure

Now that the trial is defined (4 windows) and conditions are known (9 types, 50:50), determine sequence ordering and execution. Known from user's initial description: Practice loop × 20, 2 formal loops × 60.

Each sequence runs top-to-bottom. Window order within each sequence is left-to-right.

**Questions:**
1. "反馈只在练习阶段显示，还是正式实验也有？"
2. "序列顺序固定还是被试间平衡？"

### User: "反馈只在练习。顺序固定。"

Sequences complete:

```yaml
sequences:
  - name: 指导语
    order: 1
    window_ids: [Welcome]
    execution:
      mode: once

  - name: 练习
    order: 2
    window_ids: [Fixation, Stroop, Feedback, ITI]
    execution:
      mode: loop
      repetitions: 20
    show_in: [practice]

  - name: 正式实验_1
    order: 3
    window_ids: [Fixation, Stroop, ITI]
    execution:
      mode: loop
      repetitions: 60

  - name: 正式实验_2
    order: 4
    window_ids: [Fixation, Stroop, ITI]
    execution:
      mode: loop
      repetitions: 60

  - name: 结束
    order: 5
    window_ids: [ThankYou]
    execution:
      mode: once
```

---

## Phase 5: Validate & Route

All `[MISSING]` resolved. 13 validation checks pass. Route to psy-exp-coder for code generation.
