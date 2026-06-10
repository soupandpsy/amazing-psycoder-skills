# Sternberg Memory Scanning Task

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/sternberg) · reference

## When to Use

User mentions: Sternberg task, memory scanning, short-term memory search, set size effect, 斯滕伯格任务, 记忆扫描. Measures the speed and nature of short-term memory retrieval by varying the number of items held in a memory set and measuring the time to determine whether a probe was present.

## Core Logic

On each trial, participants are shown a memory set of items (typically digits, e.g., "3 7 1") to memorize. After a brief retention interval, a single probe item is presented. Participants respond whether the probe was present in the memory set (yes/no judgment). The critical manipulation is the set size — the number of items in the memory set — which varies from trial to trial (e.g., 1 to 6 items).

Sternberg's (1969) classic finding is that RT increases linearly with set size at approximately 30-40 ms per additional item, and the slope is roughly equal for both positive (probe present) and negative (probe absent) responses. This parallel slope pattern supports a serial, exhaustive search model: the entire memory set is scanned on every trial, even when the probe is found early (self-terminating search would predict shallower slopes for positive trials). The intercept of the RT function estimates encoding + response time, while the slope estimates scanning rate per item.

This implementation uses a precisely timed trial sequence with all items of the memory set shown simultaneously: fixation cross for 1.0 s, memory set display for 1.5 s (digits as a space-separated string, e.g., "3 7 1"), a 2.0 s blank retention interval, then the probe digit appears. The keyboard begins listening at probe onset for frame-accurate RT. Response reminders ("LEFT if it was NOT" / "RIGHT if it WAS") appear after the probe has been on screen briefly. 

Design includes a practice block (with 1.0 s feedback showing "Correct! RT=Nms" or "Oops! That was wrong") followed by the main block (no feedback). Separate condition files (`pracTrials.xlsx`, `mainTrials.xlsx`) each have columns: `numberSet` (memory set string), `target` (probe digit string), and `corrAns` ('left' or 'right').

## Must Confirm

- **Set sizes**: Which memory set sizes to include? (typically 1-6 items)
- **Stimulus type**: Digits, letters, words, or other?
- **Memory set presentation**: Simultaneous (all items at once) or sequential (one at a time)?
- **Timing**: Fixation duration, memory set display duration, retention interval length?
- **Response mapping**: Which keys for "yes/in set" and "no/not in set"?
- **Practice**: Include a practice block with RT feedback before the main task?
- **Trial count**: How many trials per set size per response type (positive/negative)?

## Trial Window Timeline

```text
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│ Window 1             │→ │ Window 2             │→ │ Window 3             │→ │ Window 4             │→ │ Window 5             │
│ Fixation             │  │ Memory Set           │  │ Retention Interval   │  │ Probe                │  │ Feedback (practice   │
│ Content: +           │  │ Content: digits      │  │ Content: blank       │  │ Content: digit       │  │ only)                │
│ Duration: 1.0 s      │  │ (e.g., "3 7 1")      │  │ Duration: 2.0 s      │  │ Duration: ≤2.0 s     │  │ Content: correct/    │
│ Response: none       │  │ starts at t=1.2 s    │  │ Response: none       │  │ starts at t=4.7 s    │  │ incorrect + RT       │
│ Data: none           │  │ Duration: 1.5 s      │  │ Data: none           │  │ Response: left/right │  │ Duration: 1.0 s      │
│                      │  │ Response: none       │  │                      │  │ Data: rt, key, acc   │  │ Response: none       │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘
```

## Data Analysis

Plot mean RT as a function of set size, separately for positive and negative trials. Fit linear regression to estimate slope (ms/item) and intercept. Compare slopes between positive and negative responses (serial exhaustive vs. self-terminating). Test whether different populations (e.g., older adults, schizophrenia patients) show steeper slopes (slower scanning) or higher intercepts (slower encoding/response). Also analyze accuracy to ensure ceiling-level performance.

## References

Sternberg, S. (1969). Memory-scanning: Mental processes revealed by reaction-time experiments. *American Scientist, 57*(4), 421–457.

## Do Not Assume

- Do not assume 记忆集以同时呈现方式显示。Sternberg任务也可以是序列呈现（逐项呈现），这两种方式的编码过程和扫描策略可能不同，需与用户确认。
- Do not assume 探测刺激出现在屏幕中央位置。有的实现将探测项显示在固定位置之外的位置（如随机位置），以叠加空间成分，需确认探测项的位置和大小。
- Do not assume 刺激材料一定是数字。字母、单词、图片或其他符号也常用于该范式，需确认刺激类型及是否需要字体支持。
- Do not assume 正负试次的比率为1:1。虽然标准设计中两种试次数量相等，但用户可能有意调整比例（如2:1），需明确确认。
- Do not assume 记忆集大小范围固定为1–6。根据被试群体和实验目的，范围可能是1–4、2–6或其他，需确认记忆集大小的取值。
- Do not assume 练习block中必须包含反馈。反馈可能仅在练习中、仅在正式中、两者都有或都没有，需向用户确认反馈策略。

## Condition File Columns

| Column | Type | Description |
|--------|------|-------------|
| numberSet | str | 记忆集字符串，各项以空格分隔，如 `"3 7 1"` |
| target | str | 探测刺激，如 `"7"`（存在于记忆集中）或 `"5"`（不存在） |
| corrAns | str | 正确按键，`"left"`（不在记忆中）或 `"right"`（在记忆中） |
| setSize | int | 记忆集中的项目数量（可从numberSet推导，但显式记录更方便分析） |

## Variants

- **序列呈现变式 (Sequential Presentation)**：记忆集中的项目逐个依次呈现（如每项500 ms），而非同时显示。这种变式用于研究编码策略和时间压力下的扫描过程。相关参考：[n-back](../paradigms/n-back.md)。
- **视觉搜索对照变式 (Visual Search Comparison)**：完成一项Sternberg任务后，被试再完成对应的视觉搜索任务（刺激同时呈现但无需记忆），通过对比记忆扫描斜率与视觉搜索斜率揭示工作记忆扫描与知觉搜索的差异。
- **双重任务变式 (Dual-task)**：在进行记忆扫描的同时执行第二任务（如发音抑制、按键分心等），用于考察中央执行器在工作记忆扫描过程中的作用。相关参考：complex-span（复杂广度任务，可用于工作记忆容量个体差异测量）。

---

## Example

### 用户请求

> "我想做一个Sternberg记忆扫描实验。屏幕中央先出现注视点500 ms，然后同时显示2到5个随机数字作为记忆集，呈现1.5秒让被试记住。空屏保持2秒后，出现一个探测数字。如果探测数字在记忆集中，按右箭头键；如果不在，按左箭头键。探测数字最多呈现2秒。先做12个练习trial带反馈，再做4个正式block各24个trial。ITI随机800-1200 ms。用jsPsych实现。"

### 试次窗口时间线

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │ →  │ Window 5                 │
│ 注视点                   │    │ 记忆集                   │    │ 保持间隔                 │    │ 探测项                   │    │ 反馈（仅练习）           │
│ Content: +               │    │ Content: "3 7 1 9"       │    │ Content: blank           │    │ Content: "7"             │    │ Content: "正确! RT=452ms"│
│ Duration: 500 ms         │    │ Duration: 1500 ms        │    │ Duration: 2000 ms        │    │ Duration: ≤2000 ms       │    │ Duration: 1000 ms        │
│ Response: none           │    │ Response: none           │    │ Response: none           │    │ Response: left/right     │    │ Response: none           │
│ Data: none               │    │ Data: none               │    │ Data: none               │    │ Data: rt, key, acc       │    │ Data: none               │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

### 解析后的实验规格

| 字段 | 值 |
|------|-----|
| 实验名称 | 数字Sternberg记忆扫描任务 |
| 平台 | jsPsych |
| 任务类型 | Sternberg记忆扫描 |
| 刺激材料 | 数字 (0-9) |
| 记忆集大小 | 2, 3, 4, 5 |
| 记忆集呈现方式 | 同时呈现 |
| 记忆集呈现时长 | 1500 ms |
| 注视点时长 | 500 ms |
| 保持间隔 | 2000 ms |
| 探测项最大呈现时长 | 2000 ms |
| 反应映射 | 右箭头=在记忆中，左箭头=不在记忆中 |
| 阶段 | 指导语 → 练习(12 trial) → Block1-4(各24 trial) |
| ITI | 800-1200 ms 随机 |

### 缺失信息

1. **字体和中文支持**：用户使用数字作为刺激，不需要中文字体。但如果需要呈现中文指导语，需确认字体加载路径。
2. **反馈方式**：用户仅提到练习有反馈，未说明反馈的具体格式（仅文字还是包含声音/颜色），需确认。
3. **block间休息**：用户未提及block之间的休息时间，需确认是否需要休息页面及休息时长。

### 关键假设

- 正负试次比率默认为1:1（探测项有一半概率在记忆集中）
- 练习阶段反馈显示"正确/错误"并附带RT（标准Sternberg练习设置）
- 记忆集中的数字在同一试次内不重复（无放回抽样）
- 预期RT阈值：200 ms（低于此视为提前反应）
- 全屏运行，默认白色背景黑色文字

### 代码架构

```
sternberg.html (或 sternberg.js)
├── 参数配置 (setSizes, timing, key mapping)
├── 试次条件生成（交叉setSize与正负类型）
├── jsPsych初始化 + 插件加载
├── 时间线构建:
│   ├── 指导语页面
│   ├── 练习block（12试次 + 反馈）
│   ├── 过渡页面
│   └── 正式实验（4 blocks × 24试次）:
│       ├── block开始提示
│       ├── 试次循环:
│       │   ├── 注视点 (500 ms)
│       │   ├── 记忆集 (1500 ms)
│       │   ├── 保持间隔 (2000 ms)
│       │   ├── 探测项 (≤2000 ms，左/右箭头反应)
│       │   └── ITI (800-1200 ms 随机)
│       └── block结束（如需要休息）
└── 数据保存（jsPsych数据 + CSV导出）
```

### 预期数据列

| Column | Type | Description |
|--------|------|-------------|
| numberSet | str | 该试次的记忆集字符串 |
| target | str | 探测数字 |
| corrAns | str | 正确按键 (`"left"` 或 `"right"`) |
| setSize | int | 记忆集大小 |
| probeInSet | int | 探测项是否在记忆中 (1=在, 0=不在) |
| rt | float | 反应时 (ms) |
| acc | int | 正确性 (1=正确, 0=错误) |
| keyPressed | str | 实际按下的键 |
| block | int | block编号 (0=练习, 1-4=正式) |
| trialType | str | `"positive"` 或 `"negative"` |
