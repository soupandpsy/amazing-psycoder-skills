# Visual Search Paradigm

> **Structure ref**: [spec-template.md](../references/spec-template.md)
> **Standards**: [timing](../references/timing.md) · [data recording](../references/data-recording.md) · [randomization](../references/randomization.md) · [missing info](../references/missing-information.md) · [condition file](../references/condition-file.md)

## When to Use

User mentions: Visual search, 视觉搜索, attention, pop-out, conjunction search, feature search, set size.

## Core Logic

Participants search for a target among distractors. Measures attentional selection efficiency. Response time as a function of set size reveals search type: flat slope = parallel/pop-out search; positive slope = serial/conjunction search.

Key conditions:
- **Target present vs absent**: Absent trials require exhaustive search
- **Set size**: Number of items in display (typically 4, 8, 12, 16)
- **Search type**: Feature (pop-out) vs conjunction (serial)
- **Target-distractor similarity**: High similarity = harder search

Typical: Fixation (500 ms) → Search display (until response, deadline 3000-5000 ms) → Feedback (500 ms) → ITI (500-1000 ms).

## Must Confirm

Before generating visual search code, confirm ALL of these:

1. **Target**: What is the target? Single feature or conjunction?
2. **Distractors**: What are the distractors? How distinct from target?
3. **Search type**: Feature search (pop-out, e.g., red among green) or conjunction search (e.g., red-X among red-O and green-X)?
4. **Set sizes**: Which set sizes? (typically 4, 8, 12 or similar)
5. **Target presence**: What percent target-present? (typically 50%)
6. **Response mapping**: Two keys (present/absent) or go/no-go (respond only to present)?
7. **Display layout**: Random positions on imaginary grid/circle, or fixed positions?
8. **Stimulus dimensions**: Color, shape, orientation, size — which vary, which are task-relevant?
9. **Display area**: 搜索区域大小（视觉角度）和刺激大小？
10. **ITI duration**: 试次间隔时间和变化范围？
11. **OS & font**: 在什么操作系统运行？如使用中文，确认字体
12. **Instruction text**: 指导语内容？

## Do Not Assume

- Do not assume feature search — if target is defined by a conjunction, this is a fundamentally different task
- Do not assume set sizes — confirm the exact values
- Do not assume 50% target-present ratio — some designs use different proportions
- Do not assume go/no-go response — present/absent two-key response is more common
- Do not assume random positions — some designs constrain to an imaginary circle or grid
- Do not assume on-screen response — some use vocal response for RT measurement

## Condition File Columns

Columns in the xlsx/csv file that drives each trial:

| Column | Type | Description |
|--------|------|-------------|
| set_size | int | Number of items in display |
| target_present | int | 1 if target present, 0 if absent |
| search_type | str | `"feature"` or `"conjunction"` |
| target_stimulus | str | Target identity |
| distractor_type | str | Distractor type used |

## Data Output Columns

| Column | Type | Description |
|--------|------|-------------|
| set_size | int | Number of items in display |
| target_present | int | 1 if target present, 0 if absent |
| search_type | str | `"feature"` or `"conjunction"` |
| target_stimulus | str | Target identity |
| distractor_stimuli | str | Distractor type(s) used |
| search_slope | float | RT slope per item (calculated offline) |

## Randomization Checks

- Target present/absent ratio verified per set size
- Target position randomized (not disproportionately in one quadrant)
- Distractor positions randomized, no overlap
- No more than 3 consecutive same-response trials
- Each set size appears equally often

## Common Failure Modes

- Not varying set size (can't compute search slope without at least 3 set sizes)
- Target position bias (target appearing disproportionately in easy-to-find locations)
- Not pre-generating item positions (on-the-fly layout causes timing jitter)
- Insufficient trials per set-size × presence condition
- Distractors too similar to target (ceiling effects) or too different (floor effects)
- Using `visual.ElementArrayStim` without precomputing positions

## References

Treisman, A. M., & Gelade, G. (1980). A feature-integration theory of attention. *Cognitive Psychology*, *12*(1), 97–136. https://doi.org/10.1016/0010-0285(80)90005-5

Wolfe, J. M. (1998). What can 1 million trials tell us about visual search? *Psychological Science*, *9*(1), 33–39. https://doi.org/10.1111/1467-9280.00006

Wolfe, J. M. (2007). Guided Search 4.0: Current progress with a model of visual search. In W. D. Gray (Ed.), *Integrated models of cognitive systems* (pp. 99–119). Oxford University Press.

Duncan, J., & Humphreys, G. W. (1989). Visual search and stimulus similarity. *Psychological Review*, *96*(3), 433–458. https://doi.org/10.1037/0033-295X.96.3.433

---

## Example

### User Request

> "我想做一个视觉搜索实验。目标是一个红色X，干扰子为红色O和绿色X。set size有4、8、12三种。目标出现在50%的试次中。被试判断目标是否存在，存在按F，不存在按J。刺激随机排列在假想圆形上。先30个练习，然后4个正式block各60个trial。刺激呈现直到按键，截止4000 ms。ITI随机600-900 ms。用PsychoPy。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Search Display           │    │ Feedback                 │    │ ITI                      │
│ Content: +               │    │ Content: 多个色字        │    │ Content: 正确/错误        │    │ Content: empty           │
│ Duration: 500 ms         │    │ Duration: until key      │    │ Duration: 500 ms         │    │ Duration: 600-900 ms      │
│ Response: none           │    │ Response: f/j            │    │ Response: none           │    │ Response: none           │
│ File: none               │    │ File: none (generated)   │    │ File: none               │    │ File: none               │
│ Condition: none          │    │ Condition: {set_size}    │    │ Condition: {correct_resp}│    │ Condition: none          │
│ Data: none               │    │ Data: rt, key, acc       │    │ Data: none               │    │ Data: none               │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | File/Folder | Condition | Data |
|--------|---------|----------|----------|-------------|-----------|------|
| Fixation | + | 500 ms | none | none | none | none |
| Search Display | 红色X + 干扰子 | until key (deadline 4000 ms) | f=存在, j=不存在 | none (generated) | {set_size}, {target_present} | rt, key, acc |
| Feedback | 正确/错误/太慢 | 500 ms | none | none | {correct_response} | none |
| ITI | empty | 600-900 ms random | none | none | none | none |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| Experiment name | Conjunction Visual Search Task |
| Platform | PsychoPy |
| Task type | Visual search (conjunction) |
| Target | Red X |
| Distractors | Red O, Green X |
| Search type | Conjunction (color + shape) |
| Set sizes | 4, 8, 12 |
| Target presence | 50% present, 50% absent |
| Response mapping | F=present, J=absent |
| Display layout | Imaginary circle, random positions |
| Phases | Instruction → Practice(30) → Block1-4(60 each) |

### Missing Information

1. Fixation not stated → assumed 500 ms
2. Feedback in formal blocks? → will ask
3. Item positions: exact radius and item size? → will ask

### Assumptions

- Items placed on imaginary circle, random angular positions
- Pre-generated position arrays per trial (no on-the-fly computation)
- Each set size equally frequent (20 trials per set size per block)
- Target position randomized across all possible locations
- Key items: TextStim for X and O, with color set per condition

### Expected Code Architecture

```
visual_search_conjunction.py
├── Parameters (set_sizes, colors, shapes, timing)
├── Window setup (units='deg')
├── Precompute position arrays for each set size
├── Generate condition table:
│   ├── 4 blocks × 60 trials = 240 total
│   ├── 50% target present, 50% absent
│   └── Equal set size distribution
├── Trial loop:
│   ├── Fixation (500 ms)
│   ├── Search display (until response, deadline 4000 ms)
│   │   ├── For each position: randomly assign Red-X, Red-O, or Green-X
│   │   ├── Target present: one item = Red-X (target)
│   │   └── Target absent: no Red-X, only Red-O and Green-X
│   ├── Feedback (practice only, 500 ms)
│   └── ITI (600-900 ms random)
├── Data: try/finally CSV with incremental writes
```

### Expected Data Columns

Base columns + set_size, target_present, search_type, target_stimulus, distractor_stimuli
