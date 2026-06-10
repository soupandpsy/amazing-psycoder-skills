# Posner Cuing Task

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/posner) · reference

## When to Use

User mentions: Posner cuing, spatial cuing, covert attention, endogenous/exogenous attention, 波斯纳线索任务, 空间注意. Measures the ability to orient covert spatial attention in response to predictive or non-predictive cues, dissociating voluntary (endogenous) and reflexive (exogenous) orienting.

## Core Logic

Participants fixate on a central point and respond as quickly as possible to a target that appears in one of two (or more) peripheral locations. Before target onset, a cue directs attention to a location. On valid trials (typically ~80% of cued trials), the target appears at the cued location. On invalid trials (~20%), the target appears at the uncued location. Neutral trials (no directional cue) provide a baseline.

The cuing effect (invalid RT – valid RT) measures the cost-plus-benefit of spatial attention. Two cue types are typically used: peripheral cues (a brief flash at the target location, e.g., 50 ms) that elicit reflexive, exogenous attention shifting, and central symbolic cues (an arrow at fixation) that require voluntary, endogenous attention shifting. Peripheral cues produce rapid (peak ~100-150 ms) but transient facilitation followed by inhibition of return (IOR) at longer cue-target intervals (>300 ms). Central cues produce slower but sustained facilitation.

Key temporal parameter: stimulus onset asynchrony (SOA) between cue and target is varied (e.g., 100, 300, 500, 800 ms) to map the time course of attentional effects. Short SOAs with peripheral cues show facilitation; long SOAs show IOR (slower responses to cued vs. uncued locations).

## Data Analysis

Compute mean RT for valid, invalid, and neutral conditions. Test cuing effect (invalid – valid RT) and its subscores: benefit (neutral – valid), cost (invalid – neutral). Analyze cuing effect as a function of SOA and cue type. IOR is indexed by valid > invalid RT at long SOAs. Compare cuing effects between populations (e.g., reduced cuing effects in neglect, schizophrenia; altered IOR in ADHD).

## Must Confirm

- **Target type**: Gabor patch, simple shape, or letter? What visual properties (spatial frequency, contrast, size)?
- **Cue type**: Peripheral box cue (reflexive exogenous), central arrow (voluntary endogenous), or both?
- **Cue validity ratio**: What proportion valid vs invalid? (typically 80% valid / 20% invalid)
- **SOA values**: What cue-target onset asynchronies to use? (e.g., 100, 300, 500, 800 ms)
- **Trial counts**: How many trials per condition × SOA combination?
- **Response mapping**: Left/right arrow keys for left/right target? Or detection key (one key for any target)?

## Trial Window Timeline

From the psychtoolbox reference implementation (Gabor target, peripheral box cue):

```
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │ →  │ Window 5                 │
│ Fixation                 │    │ Cue                      │    │ CTI (Gap)                │    │ Target                   │    │ Response + ITI           │
│ Content: fixation dot    │    │ Content: box cue (L/R)   │    │ Content: fixation dot    │    │ Content: Gabor target    │    │ Content: blank grey      │
│ Duration: 500 ms         │    │ + fixation dot           │    │ Duration: 300 ms (CTI)   │    │ Duration: 150 ms         │    │ Duration: until keypress │
│ Response: none           │    │ Duration: 150 ms         │    │ Response: none           │    │ Response: none           │    │ Response: LeftArrow/     │
│ Condition: none          │    │ Response: none           │    │ Condition: {cue_pos}     │    │ Condition: {target_pos}  │    │   RightArrow             │
│ Data: none               │    │ Condition: {cue_pos}     │    │ Data: none               │    │ Data: none               │    │ Data: rt, correctness    │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

2×2 factorial design: cue position (left/right) × target position (left/right). Contingent = same location; Non-contingent = different location. Key parameter: Cue-Target Interval (CTI) — 300ms in reference implementation, varied in full paradigm.

## Condition File Structure

| Column | Values | Description |
|--------|--------|-------------|
| cue_pos | 0=left, 1=right | Position of the box cue |
| target_pos | 0=left, 1=right | Position of the Gabor target |
| correct_response | left/right | Expected key response |
| contingency | contingent/non-contingent | Whether cue and target share location |

Base matrix `[0 0 1 1; 0 1 0 1]` (4 combinations) repeated `numReps` times, then shuffled. `cue_pos == target_pos` → contingent; `cue_pos != target_pos` → non-contingent.

## References

Posner, M. I. (1980). Orienting of attention. *Quarterly Journal of Experimental Psychology, 32*(1), 3–25. https://doi.org/10.1080/00335558008248231

Posner, M. I., Snyder, C. R. R., & Davidson, B. J. (1980). Attention and the detection of signals. *Journal of Experimental Psychology: General, 109*(2), 160–174. https://doi.org/10.1037/0096-3445.109.2.160

Scarfe, P. (n.d.). Posner cuing experiment (Psychtoolbox demo). https://peterscarfe.com/poserCuingExperiment.html

## Do Not Assume

- Do not assume 线索有效性比例为 80%/20%，须显式确认。虽然经典设计使用 80% 有效试次，但有些实验使用 50%/50% 或包含中性试次，须直接询问用户。
- Do not assume 外周线索总是出现在目标位置。外周线索通常为方框闪烁或亮度变化，确认线索的视觉属性（方框、圆点、亮度增减）及其与目标位置的空间关系。
- Do not assume 中央线索一定是箭头符号。中央线索可为箭头、文字（"左"/"右"）、数字或注视线索（gaze cue），确认线索的具体呈现形式。
- Do not assume 仅使用单一 SOA 值。Posner 范式的核心在于绘制注意的时间进程曲线，通常需要多个 SOA（如 100、300、500、800 ms），须确认 SOA 集合。
- Do not assume 目标刺激类型默认为简单方块。确认目标的视觉属性：Gabor 光栅、字母、形状、大小、对比度等。
- Do not assume 被试反应方式为左右按键。可能为探测反应（单键检测目标出现）或辨别反应（区分目标属性），确认反应映射规则。

## Condition File Columns

| Column | Type | Description |
|--------|------|-------------|
| cue_pos | int | 线索位置：0=左侧，1=右侧 |
| target_pos | int | 目标位置：0=左侧，1=右侧 |
| soa | float | 线索-目标呈现异步（SOA），单位 ms |
| validity | str | `"valid"`（线索与目标同侧）、`"invalid"`（异侧）或 `"neutral"`（无线索） |
| cue_type | str | `"peripheral"`（外周线索）或 `"central"`（中央线索） |

## Variants

- **外周线索变式（外源性注意）**：在目标可能出现的周边位置短暂呈现方框闪烁或亮度变化（典型 50-150 ms），引发自下而上的反射性注意定向。短 SOA 下产生易化效应，长 SOA（>300 ms）下出现返回抑制（IOR）。这是 Posner 经典实验的原始形式。
- **中央线索变式（内源性注意）**：在中央注视点呈现箭头、文字或符号线索（如 "←" 或 "→"），引发自上而下的意志性注意定向。需要更长的 SOA（通常 >300 ms）才能产生易化效应，且不易出现返回抑制。可关联范式：[stroop](../paradigms/stroop.md)（涉及中央符号加工）。
- **注视线索变式（社会性注意）**：中央呈现面孔图片，其眼睛注视方向作为线索，引发社会性注意定向。即使告知被试线索无预测性，仍会产生注意转移效应。可关联范式：[dot-probe](../paradigms/dot-probe.md)（涉及面孔与注意偏向）。

## Example

### 用户请求

> "做一个波斯纳线索任务。屏幕左右两侧各有一个方框，中央是注视点。试次开始时，左侧或右侧的方框会短暂闪烁（50ms）作为外周线索。80% 的试次目标出现在线索一侧（有效），20% 出现在另一侧（无效）。闪烁后间隔 200ms 出现目标（字母 E），要求被试看到目标后尽快按空格键。目标呈现 200ms，反应窗口 1500ms。共 200 个试次，分 4 个 block。用 PsychoPy。"

### 试次窗口时间线

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │ →  │ Window 5                 │
│ 注视点                   │    │ 线索                     │    │ SOA 间隔                 │    │ 目标                     │    │ 反应 + ITI               │
│ Content: 中央+ 左右方框   │    │ Content: 单侧方框闪烁     │    │ Content: 中央+ 左右方框   │    │ Content: 字母 E         │    │ Content: 空屏            │
│ Duration: 500 ms         │    │ Duration: 50 ms          │    │ Duration: 150 ms         │    │ Duration: 200 ms         │    │ Duration: 至按键         │
│ Response: 无             │    │ Response: 无             │    │ Response: 无             │    │ Response: 无             │    │   (deadline 1500 ms)     │
│ Condition: 无            │    │ Condition: {cue_pos}     │    │ Condition: {cue_pos}     │    │ Condition: {target_pos}  │    │ Response: 空格键         │
│ Data: 无                 │    │ Data: 无                 │    │ Data: 无                 │    │ Data: 无                 │    │ Data: rt, acc            │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | Condition | Data |
|--------|---------|----------|----------|-----------|------|
| 注视点 | 中央+ 左右方框 | 500 ms | 无 | 无 | 无 |
| 线索 | 单侧方框闪烁 | 50 ms | 无 | {cue_pos} | 无 |
| SOA 间隔 | 中央+ 左右方框 | 150 ms | 无 | {cue_pos} | 无 |
| 目标 | 字母 E | 200 ms | 无 | {target_pos} | 无 |
| 反应+ITI | 空屏 | 至按键（deadline 1500 ms） | 空格键 | 无 | rt, acc |

### 解析的实验规格

| Field | Value |
|-------|-------|
| 实验名称 | Posner 外周线索任务 |
| 平台 | PsychoPy |
| 任务类型 | Posner cuing（外源性空间注意） |
| 线索类型 | 外周方框闪烁（外源性） |
| 线索持续时间 | 50 ms |
| 目标刺激 | 字母 E |
| 目标持续时间 | 200 ms |
| SOA | 200 ms（50 ms 线索 + 150 ms 间隔） |
| 线索有效性 | 80% 有效 / 20% 无效 |
| 反应方式 | 单键探测（空格键） |
| 试次数量 | 200 试次（4 blocks × 50） |

### 缺失信息

1. 注视点持续时间未明确说明 → 假定为 500 ms（设计假设，需标注）
2. ITI 持续时间未提及 → 将询问用户（固定/随机范围）
3. 练习试次未提及 → 将询问是否需要练习阶段及试次数量
4. 是否告知被试线索的预测性（80% 有效）→ 将确认指导语内容

### 关键假设

- 外周线索为方框亮度变化（加粗或高亮），非其他视觉属性变化
- 无中性试次（仅包含有效和无效两种条件）
- 试次间无反馈（正式阶段不呈现反馈）
- 预期 RT 阈值：100 ms（低于此值标记为预期反应）
- 线索-目标 SOA 固定为 200 ms（用户未要求多个 SOA）

### 代码架构

```
posner_cuing.py
├── 参数定义（线索时长、SOA、目标时长、反应截止时间、试次数量）
├── 窗口设置（全屏/窗口模式）
├── 刺激预加载（注视点、方框、目标字母 E）
├── 条件表生成（cue_pos × target_pos 矩阵，80/20 比例）
├── 指导语呈现
├── 试次循环：
│   ├── 注视点 (500 ms)
│   ├── 线索呈现 (50 ms — 闪烁方框)
│   ├── SOA 间隔 (150 ms)
│   ├── 目标呈现 (200 ms — 字母 E)
│   ├── 反应窗口 (deadline 1500 ms)
│   ├── ITI
│   └── 数据记录 (rt, acc, cue_pos, target_pos, validity)
├── 数据保存：try/finally CSV 增量写入
```

### 预期数据列

| Column | Type | Description |
|--------|------|-------------|
| cue_pos | int | 线索位置（0=左，1=右） |
| target_pos | int | 目标位置（0=左，1=右） |
| validity | str | 线索有效性：`"valid"` 或 `"invalid"` |
| soa | float | 线索-目标 SOA（ms） |
| rt | float | 反应时间（ms） |
| acc | int | 正确反应=1，错误=0 |
| trial_index | int | 试次序号（0-based） |
| block | int | Block 编号 |
