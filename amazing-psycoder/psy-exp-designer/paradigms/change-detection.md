# Change Detection Task

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/change-detection) · PsychoJS

## When to Use

User mentions: Change detection, visual working memory, VWM, change blindness, 变化检测, 视觉工作记忆. Measures the capacity and precision of visual working memory by testing whether observers can detect changes between a study array and a test probe.

## Core Logic

Participants view a brief study array containing multiple colored circles at fixed angular positions around a central fixation point. After a short retention interval, a test array is presented that is either identical to the study array (no-change trial) or has one item whose color changed (change trial). Participants respond whether they detected a change (same/different judgment).

**Two-phase design**:

1. **Change Detection Phase**: Participants judge whether any circle changed color. This phase measures basic VWM capacity — can they detect the presence of a change?
2. **Localisation Phase**: Participants identify which specific circle changed. This provides a more sensitive assay of VWM precision — do they know which item changed, not just that something changed?

Each phase has its own instructions, trial loop, and condition files. The set size (number of circles, typically 2–8) varies across trials to parametrically manipulate memory load.

**Stimuli**: Colored circles rendered programmatically at calculated angular positions around fixation (evenly spaced). Colors are specified by RGB values from CSV condition files. Circle positions stay consistent; colors change per trial.

**Trial structure**: fixation (500 ms) → memory array (100–500 ms) → blank retention interval (900–1000 ms) → test array/probe (until response, typically 2000 ms deadline). A progress counter is shown to track trial position within the session.

**Capacity estimation**: VWM capacity (k) is estimated using the formula k = N * (H – FA) / (1 – FA), where N is set size, H is hit rate (correct change detection), and FA is false alarm rate (incorrectly reporting a change on no-change trials).

## Must Confirm

- **Phases**: Both change-detection and localisation phases, or just one?
- **Set sizes**: Which set sizes to include? (typically 2, 4, 6, 8)
- **Stimulus type**: Colored circles, oriented bars, complex shapes, or other?
- **Change type**: Color change only, or also position/orientation changes?
- **Trial count per set size**: How many change and no-change trials per set size?
- **Array duration**: How long is the memory array displayed? Brief (100 ms) to prevent verbal encoding, or longer?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Memory Array             │    │ Retention Interval       │    │ Test Array / Response    │
│ Content: + at center     │    │ Content: N colored circles│   │ Content: blank           │    │ Content: N circles       │
│ Duration: 500 ms         │    │ Duration: 100-500 ms     │    │ Duration: 900-1000 ms    │    │ Duration: until key      │
│ Response: none           │    │ Response: none           │    │ Response: none           │    │ (deadline ~2000 ms)      │
│ Condition: none          │    │ Condition: {set_size}    │    │ Condition: none          │    │ Response: same/diff key  │
│ Data: none               │    │ Data: none               │    │ Data: none               │    │ Condition: {change_type} │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    │ Data: rt, key, acc       │
                                                                                                └──────────────────────────┘
```

## Data Analysis

Primary measure is working memory capacity (k) estimated from hit and false alarm rates at each set size. Also analyze overall accuracy and response time as a function of set size. Individual differences in k correlate with fluid intelligence, academic performance, and attentional control. For the localisation phase, analyze which-position accuracy as a function of set size.

## References

Luck, S. J., & Vogel, E. K. (1997). The capacity of visual working memory for features and conjunctions. *Nature, 390*(6657), 279–281. https://doi.org/10.1038/36846

Pashler, H. (1988). Familiarity and visual change detection. *Perception & Psychophysics, 44*(4), 369–378. https://doi.org/10.3758/BF03210419

## Do Not Assume

- Do not assume both detection and localisation phases are required — many experiments use only the change-detection phase without asking which item changed
- Do not assume standard set sizes (2, 4, 6, 8) — confirm which set sizes the user wants; some designs use fewer levels or non-standard values
- Do not assume only color changes — changes can involve orientation, shape, spatial position, or feature conjunctions
- Do not assume a 50:50 change/no-change ratio — confirm the ratio explicitly; some designs use 60:40 or other proportions
- Do not assume unlimited response deadline — typical deadline is 2000 ms, but confirm
- Do not assume the memory array duration is fixed at one value — brief durations (100–200 ms) prevent verbal encoding, while longer durations (500 ms+) are sometimes used

## Condition File Columns

Columns in the xlsx/csv file that drives each trial:

| Column | Type | Description |
|--------|------|-------------|
| set_size | int | 记忆阵列中圆点/项目的数量 (如 2, 4, 6, 8) |
| change_present | int | 1 = 变化试次，0 = 无变化试次 |
| change_position | int | 发生变化的目标位置 (1-indexed)，无变化试次为 -1 或 NA |
| target_color | str | 变化后的目标颜色 (RGB 或颜色名)，无变化试次为 NA |

## Variants

- **单探针变化检测 (Single-probe)**: 记忆阵列消失后呈现单个探测刺激（通常用圆圈标记位置），被试判断该位置项目的颜色/特征是否与记忆阵列一致。这是测量视觉工作记忆容量最常用的变式。参见 [visual-search.md](visual-search.md)（视觉搜索，共享注意负荷操作）。
- **整体显示变化检测 (Whole-display)**: 测试阶段重新呈现完整阵列，被试判断是否有任何项目发生变化。常与变化盲视（change blindness）范式结合，通过闪烁或空白间隔操纵检测难度。
- **线索化变化检测 (Cued)**: 记忆阵列消失后呈现空间线索（如箭头或方框），指向可能发生变化的位置。线索减少了记忆负荷，用于测量注意分配和视觉工作记忆精度。参见 [posner-cuing.md](posner-cuing.md)（空间线索范式）。

---

## Example

### User Request

> "我想做一个变化检测实验。屏幕中央先呈现注视点500 ms，然后呈现记忆阵列（4个或6个彩色圆点，均匀分布在以中央注视点为中心的虚拟圆上）250 ms，接着空白屏保持900 ms，最后呈现测试阵列直到被试按键反应（最长2000 ms，超时记为错误）。一半试次有一个圆点的颜色改变，一半试次不变。被试按F键表示检测到变化，按J键表示无变化。总共240个正式试次（每种set_size各120个试次），先进行24个练习试次。用PsychoPy。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ 注视点                    │    │ 记忆阵列                  │    │ 保持间隔                  │    │ 测试阵列 / 反应           │
│ Content: + at center     │    │ Content: N 个彩色圆点     │    │ Content: blank           │    │ Content: N 个彩色圆点     │
│ Duration: 500 ms         │    │ Duration: 250 ms         │    │ Duration: 900 ms         │    │ Duration: until key      │
│ Response: none           │    │ Response: none           │    │ Response: none           │    │ (deadline 2000 ms)       │
│ Condition: none          │    │ Condition: {set_size}    │    │ Condition: none          │    │ Response: f=变化, j=无变化 │
│ Data: none               │    │ Data: none               │    │ Data: none               │    │ Condition: {change_present}│
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    │ Data: rt, key, acc       │
                                                                                                └──────────────────────────┘
```

| Window | Content | Duration | Response | Condition | Data |
|--------|---------|----------|----------|-----------|------|
| 注视点 | + | 500 ms | none | none | none |
| 记忆阵列 | N 个彩色圆点 (N=4或6) | 250 ms | none | {set_size} | none |
| 保持间隔 | blank | 900 ms | none | none | none |
| 测试阵列 | N 个彩色圆点 | until key (deadline 2000 ms) | f=变化, j=无变化 | {change_present} | rt, key, acc |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| 实验名称 | 视觉变化检测任务 |
| 平台 | PsychoPy |
| 任务类型 | Change Detection (视觉工作记忆) |
| Set sizes | 4, 6 |
| 刺激类型 | 彩色圆点（均匀分布于虚拟圆） |
| 变化类型 | 颜色变化（单个圆点） |
| 变化/无变化比例 | 50:50 |
| 记忆阵列呈现时间 | 250 ms |
| 保持间隔 | 900 ms |
| 反应窗口 | 最长 2000 ms |
| 阶段 | 指导语 → 练习(24试次) → 正式实验(240试次，含中场休息) |

### Missing Information

1. 颜色集合未指定（使用哪些颜色？颜色之间的可区分性如何控制？）→ 需确认标准颜色集或自定义 RGB 值
2. 是否包含位置判断阶段未说明 → 需确认是否仅做变化检测，还是也需要位置判断
3. 正式实验是否需要中场休息、休息间隔和次数未说明 → 需确认 block 划分

### Assumptions

- 仅包含变化检测阶段（不包含位置判断/定位阶段）
- 颜色从预定义的标准颜色集中随机选取（如红、蓝、绿、黄、紫、橙、青等 7–9 种易区分颜色），试次间不重复使用同一颜色组合
- 圆点位置均匀分布（set_size=4 时角度间隔 90°，set_size=6 时角度间隔 60°），起始角度随机
- 无试次间反馈（仅练习阶段可能提供反馈）
- 无 ITI（保持间隔结束后下一个试次的注视点即作为试次间隔）

### Expected Code Architecture

```
change_detection.py
├── Parameters (set_sizes, colors, n_trials, timing, keys)
├── Window setup (fullscreen or windowed)
├── Stimulus preloading:
│   ├── Fixation cross (TextStim: "+")
│   ├── Circle template (ShapeStim, reused with color/position updates)
├── Generate condition dataframe:
│   ├── 240 trials: 120 per set_size, balanced change/no-change
│   ├── Columns: set_size, change_present, change_position, target_color
│   └── Shuffle with constraint (no more than 3 consecutive same type)
├── Trial loop:
│   ├── 注视点 (500 ms)
│   ├── 记忆阵列 (250 ms — N circles at computed positions)
│   ├── 保持间隔 (900 ms blank)
│   ├── 测试阵列 (until response, deadline 2000 ms)
│   │   ├── If change_present=1: one circle color replaced with target_color
│   │   └── If change_present=0: identical to memory array
│   ├── Response recording (f/j keys, rt, acc)
│   └── Block break every 60 trials
├── Data saving: try/finally with incremental CSV writes
├── Escape key check at every window for early exit
```

### Expected Data Columns

Base columns + set_size, change_present, change_position, target_color
