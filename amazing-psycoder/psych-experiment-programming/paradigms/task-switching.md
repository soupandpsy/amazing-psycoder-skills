# Task Switching Paradigm

> **Structure ref**: [spec-template.md](../references/spec-template.md)
> **Standards**: [timing](../references/timing.md) · [data recording](../references/data-recording.md) · [randomization](../references/randomization.md) · [missing info](../references/missing-information.md) · [condition file](../references/condition-file.md)

## When to Use

User mentions: Task switching, 任务转换, switch cost, cognitive flexibility, set shifting, alternating tasks, cued task switching.

## Core Logic

Participants alternate between two or more tasks. Some trials repeat the previous task (repeat trials), others switch (switch trials). The RT difference (switch cost = RT_switch - RT_repeat) measures cognitive flexibility and executive control.

Key parameters:
- **Cue-stimulus interval (CSI)**: Time between task cue and target onset. Longer CSI = more preparation time = smaller switch cost.
- **Response-cue interval (RCI)**: Time between response and next cue. Longer RCI = less task-set inertia.
- **Switch probability**: Typically 50% switch trials within a mixed block.

Typical tasks: number parity (odd/even) + magnitude (</> 5), or letter vowel/consonant + uppercase/lowercase, or color + shape judgment.

## Must Confirm

Before generating task-switching code, confirm ALL of these:

1. **Tasks**: What are the two (or more) tasks? What is the decision rule for each?
2. **Stimuli**: What stimuli? Bivalent (both tasks applicable) or univalent (only one task applicable)?
3. **Cue type**: Verbal (words), symbolic (shapes/colors), or spatial (position)?
4. **Cue-stimulus interval (CSI)**: Fixed or varied? What value/range? (typically 100-1000 ms)
5. **Response-cue interval (RCI)**: Fixed or varied? What value?
6. **Switch ratio**: What proportion of switch vs repeat trials? (typically 50%)
7. **Response mapping**: Keys for each task? Overlapping or non-overlapping response sets?
8. **Single-task blocks**: Are there pure blocks (one task only) for baseline comparison?
9. **Trial count**: How many per block? Per condition (switch/repeat × task)?
10. **Block order**: 单任务block在前还是混合block在前？是否需要平衡？
11. **ITI duration**: 试次间隔时间和变化范围？
12. **OS & font**: 在什么操作系统运行？如使用中文，确认字体
13. **Display**: 全屏还是窗口？刺激大小和屏幕位置？
14. **Instruction text**: 指导语内容？如何向被试说明任务切换规则？

## Do Not Assume

- Do not assume verbal cues — spatial and symbolic cues are common
- Do not assume fixed CSI — variable CSI designs tease apart preparation from passive decay
- Do not assume 50% switch probability — some designs use 33% or unpredictable ratios
- Do not assume two tasks only — some designs use 3+ tasks
- Do not assume overlapping key mapping — separate keys per task simplify but confound
- Do not assume single-task blocks are included — they provide important baseline RTs
- Do not assume the first trial of each block is a switch or repeat (it's neither; exclude from analysis)

## Condition File Columns

Columns in the xlsx/csv file that drives each trial:

| Column | Type | Description |
|--------|------|-------------|
| task | str | Current task identity |
| previous_task | str | Previous trial's task |
| trial_type | str | `"switch"`, `"repeat"`, or `"first"` |
| cue | str | Cue stimulus identity |
| csi | int | Cue-stimulus interval (ms) |
| block_type | str | `"single_task"` or `"mixed"` |

## Data Output Columns

| Column | Type | Description |
|--------|------|-------------|
| task | str | Current task identity |
| previous_task | str | Previous trial's task identity |
| trial_type | str | `"switch"` or `"repeat"` (or `"first"` for block-initial) |
| cue | str | Cue stimulus identity |
| csi | float | Cue-stimulus interval (ms) |
| rci | float | Response-cue interval (ms) |
| switch_cost | float | RT_switch - RT_repeat (calculated per condition) |

## Randomization Checks

- Switch/repeat ratio verified per block (typically 50%)
- No more than 4 consecutive switch or repeat trials
- Each task appears equally often
- Cue-task mapping counterbalanced if cue is symbolic
- First trial of each block excluded from switch/repeat labeling

## Common Failure Modes

- Labeling the first trial of a block as switch or repeat (there's no previous trial; must code as `None`/excluded)
- Not separating cue and target presentation timing (CSI requires two distinct onsets)
- Using overlapping response mappings without tracking which task was intended
- Not including single-task baseline blocks (can't compute mixing cost without them)
- CSI too short for LCD refresh (need minimum ~100 ms for cue to be visible)
- Not recording previous-trial task identity (required for switch/repeat labeling)

## References

Allport, A., Styles, E. A., & Hsieh, S. (1994). Shifting intentional set: Exploring the dynamic control of tasks. In C. Umilta & M. Moscovitch (Eds.), *Attention and performance XV* (pp. 421–452). MIT Press.

Monsell, S. (2003). Task switching. *Trends in Cognitive Sciences*, *7*(3), 134–140. https://doi.org/10.1016/S1364-6613(03)00028-7

Rogers, R. D., & Monsell, S. (1995). Costs of a predictable switch between simple cognitive tasks. *Journal of Experimental Psychology: General*, *124*(2), 207–231. https://doi.org/10.1037/0096-3445.124.2.207

Kiesel, A., Steinhauser, M., Wendt, M., Falkenstein, M., Jost, K., Philipp, A. M., & Koch, I. (2010). Control and interference in task switching — A review. *Psychological Bulletin*, *136*(5), 849–874. https://doi.org/10.1037/a0019842

---

## Example

### User Request

> "我想做一个任务转换实验。被试对数字做两个任务：奇偶判断（奇数/偶数）和大小判断（大于5/小于5）。用颜色边框提示任务：红色边框=奇偶判断，蓝色边框=大小判断。线索呈现300 ms后出现数字。50%重复，50%转换。数字为1-9（排除5）。先40个练习，然后4个正式block各48个trial。CSI=300 ms，RCI=1000 ms。用PsychoPy。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │ →  │ Window 5                 │
│ Cue                      │    │ Target                   │    │ Response                 │    │ Feedback                 │    │ ITI (RCI)                │
│ Content: 红/蓝色边框      │    │ Content: {digit}         │    │ Content: {digit}         │    │ Content: 正确/错误        │    │ Content: empty           │
│ Duration: 300 ms         │    │ Duration: until key      │    │ Duration: until key      │    │ Duration: 500 ms         │    │ Duration: 1000 ms        │
│ Response: none           │    │ Response: none           │    │ Response: f/j            │    │ Response: none           │    │ Response: none           │
│ File: none               │    │ File: none (text)        │    │ File: none               │    │ File: none               │    │ File: none               │
│ Condition: {task_cue}    │    │ Condition: {digit}       │    │ Condition: {correct_resp}│    │ Condition: {correct_resp}│    │ Condition: none          │
│ Data: none               │    │ Data: none               │    │ Data: rt, key, acc       │    │ Data: none               │    │ Data: none               │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | File/Folder | Condition | Data |
|--------|---------|----------|----------|-------------|-----------|------|
| Cue | 红/蓝色边框 | 300 ms | none | none (generated) | {task_cue} | none |
| Target | {digit} | until key (deadline 3000 ms) | none (target onset) | none (text) | {digit} | none |
| Response | {digit} (after cue+target) | merged with target | f/j (task-dependent) | none | {correct_response} | rt, key, acc |
| Feedback | 正确/错误 | 500 ms | none | none | {correct_response} | none |
| ITI (RCI) | empty | 1000 ms | none | none | none | none |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| Experiment name | Cued Task Switching |
| Platform | PsychoPy |
| Task type | Task switching (cued, two tasks) |
| Tasks | Parity (odd/even) + Magnitude (</> 5) |
| Cue type | Color border (red=parity, blue=magnitude) |
| CSI | 300 ms |
| RCI | 1000 ms |
| Stimuli | Digits 1-9 (excluding 5) |
| Switch ratio | 50% switch, 50% repeat |
| Response mapping | f/j, overlapping (both tasks use same keys) |
| Phases | Instruction → Practice(40) → Block1-4(48 each) |

### Missing Information

1. Response mapping details → will ask: odd=left, even=right? How for magnitude?
2. Fixation before cue? → assumed no (cue serves as trial onset)
3. Feedback in formal blocks? → will ask

### Assumptions

- Overlapping response keys: both tasks use F/J with remapped meanings
- First trial of each block excluded from switch/repeat analysis
- Block structure: single-task practice blocks + mixed formal blocks
- Cue remains visible during target presentation (border persists)
- Red=parity (odd→F, even→J), Blue=magnitude (<5→F, >5→J) — will confirm

### Expected Code Architecture

```
task_switching.py
├── Parameters (tasks, cues, CSI, RCI, keys, digits)
├── Window setup
├── Generate condition table per block:
│   ├── 48 trials: 50% switch, 50% repeat
│   ├── Each task appears equally (24 parity + 24 magnitude)
│   ├── First trial flagged as "first" (excluded from analysis)
│   └── Record previous_trial task for switch/repeat labeling
├── Trial loop:
│   ├── Cue (colored border, 300 ms)
│   ├── Target digit appears (border remains)
│   ├── Response (until key, deadline 3000 ms)
│   ├── Feedback (practice only, 500 ms)
│   └── ITI/RCI (1000 ms)
├── Data: try/finally CSV with incremental writes
```

### Expected Data Columns

Base columns + task, previous_task, trial_type, cue, csi, rci
