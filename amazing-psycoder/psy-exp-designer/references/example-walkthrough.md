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

Detected from input: 3 words (红/绿/蓝), 3 ink colors, f/j keys (only 2 keys for 3 colors → conflict flagged), practice 20 trials, 2 formal blocks × 60.

**Questions:**
1. "使用什么平台？PsychoPy？"
2. "只有f/j两个键，三种颜色（红/绿/蓝），蓝色对应哪个键？还是只用两种颜色？"

### User: "PsychoPy，蓝色按k键"

---

## Phase 2: Define Windows & Rules

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

## Phase 4: Set Block Structure

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

## Phase 5: Validate & Route

All `[MISSING]` resolved. 9 validation checks pass. Route to psy-exp-coder for code generation.
