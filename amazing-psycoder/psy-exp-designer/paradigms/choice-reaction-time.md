# Choice Reaction Time Task

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/choice_reaction_time) · PsychoJS

## When to Use

User mentions: Choice reaction time, CRT, choice RT, Hick's law, 选择反应时. Measures the speed of decision-making when participants must discriminate among multiple stimuli and select the corresponding response — unlike simple RT (one stimulus, one response), choice RT requires both stimulus discrimination and response selection.

## Core Logic

Participants respond to visual targets that appear at one of several possible screen positions. The target can be one of multiple stimulus types (e.g., cross, square, plus), each mapped to a different response. The task requires both stimulus identification (which shape?) and response selection (which key/position?), making it a measure of decision complexity beyond simple detection.

**This implementation** uses 3 target shapes (cross, square, plus) that appear at 4 possible positions arranged around the screen. Each shape is associated with a specific keyboard response: C, V, or B keys. Additionally, mouse clicks on the target position are accepted as a valid response. This dual-modality design allows measuring both stimulus-identity-driven (keyboard) and location-driven (mouse) response selection.

**Position cueing**: Before the target appears, outline placeholder tiles are shown at all 4 possible positions for 500 ms, cuing the participant to the possible target locations. The target then appears at one position for a brief 200 ms display window, requiring rapid encoding.

**Variable onset timing**: The target onset time (`onsetTime`) varies per trial as specified in the condition file, introducing temporal uncertainty and preventing anticipatory responses. Reaction time is calculated relative to this onset (`RT = keyResp.rt - onsetTime`).

**Two-block design**: Practice block (1 repetition of conditions) with detailed feedback showing RT, response type, and accuracy after each trial, followed by the experimental block (2 repetitions) with the same feedback. The practice and main blocks share the same trial structure and condition logic.

**Multi-alternative choice design**: 3 possible stimulus shapes, each mapped to a specific key. This is the key difference from simple RT (one stimulus, one key) -- the participant must recognize which shape appeared and select the correct response from multiple options. Hick's Law predicts that RT increases logarithmically with the number of response alternatives.

## Must Confirm

- **Stimulus shapes**: How many shapes, and which ones? (cross, square, plus -- or custom)
- **Stimulus positions**: How many locations on screen, and where?
- **Response modality**: Keyboard only, mouse only, or both? Which keys map to which shapes?
- **Target duration**: Brief flash (200 ms) or response-terminated display?
- **Onset timing**: Fixed SOA, variable from condition file, or immediate?
- **Position cueing**: Show position tiles before target (500 ms), or no pre-cue?
- **Trial count**: How many practice repetitions? How many experimental repetitions?
- **Feedback content**: RT, accuracy, response type -- or accuracy only?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Position Cues            │    │ Target Display           │    │ Feedback                 │
│ Content: 4 outline tiles │    │ Content: shape (cross/   │    │ Content: RT, response    │
│ at target positions      │    │ square/plus) at one      │    │ type, accuracy           │
│ Duration: 500 ms         │    │ position                  │    │ Duration: ~1 s            │
│ Response: none           │    │ Duration: 200 ms         │    │ Response: none           │
│ Data: none               │    │ Response: key (C/V/B) or │    │ Data: none               │
│                          │    │ mouse click on position  │    │                           │
│                          │    │ Data: rt (from onsetTime)│    │                           │
│                          │    │ key, acc, response_type  │    │                           │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

## Data Analysis

Primary measure is mean RT as a function of number of response alternatives (Hick's Law: RT = a + b * log2(N), where N is the number of choices). Compare RT across different stimulus shapes. Analyze accuracy, which should be high (>90%) for healthy adults. Choice RT is slower than simple RT by approximately 100-150 ms (the time cost of stimulus discrimination and response selection). For the dual-modality version, compare keyboard vs. mouse response RTs to assess modality effects on response selection. Check temporal uncertainty effects by analyzing RT as a function of onset variability. Individual differences in CRT correlate with general cognitive ability and processing speed.

## References

Hick, W. E. (1952). On the rate of gain of information. *Quarterly Journal of Experimental Psychology, 4*(1), 11-26. https://doi.org/10.1080/17470215208416600

## Do Not Assume

- Do not assume 3 shapes with 4 positions — 形状数量和位置数量可任意配置，经典的 Hick 定律实验中常使用 2-8 个选择项
- Do not assume keyboard-only response — 鼠标点击位置也可作为有效反应，双模态设计（键盘+鼠标）是本实现的特色
- Do not assume fixed stimulus onset — onsetTime 按条件文件逐试次变化，引入时间不确定性，需询问变时距范围
- Do not assume response-terminated stimulus display — 本实现中目标仅呈现 200 ms 的短暂闪烁，被试必须在目标消失后继续反应
- Do not assume position cues are always present — 500 ms 的位置预提示（outline tiles）是本实现的默认设置，但部分实验设计可能省略此阶段
- Do not assume RT 从 stimulus onset 计算 — RT 基于条件文件中的 onsetTime 字段计算（`RT = keyResp.rt - onsetTime`），而非简单使用 stimulus 绘制时刻

## Condition File Columns

| Column | Type | Description |
|--------|------|-------------|
| shape | str | 目标形状：`"cross"`, `"square"`, `"plus"` |
| position | str | 目标位置：如 `"left"`, `"right"`, `"top"`, `"bottom"` 或坐标值 |
| correct_key | str | 该形状对应的正确按键：`"c"`, `"v"`, `"b"` |
| onsetTime | float/number | 目标出现时刻（相对于试次开始的秒数），用于变时距控制 |

## Variants

- **简单反应时 (Simple RT)**：仅一个刺激类型、一个反应键，测量纯粹的感觉检测速度。与 CRT 的关键区别在于无需刺激辨别和反应选择，RT 显著更快（约快 100-150 ms）。参见 [simple-reaction-time.md](simple-reaction-time.md)
- **Go/No-go CRT（包含抑制的 CRT）**：在标准 CRT 基础上加入 No-go 试次，要求对特定刺激或特定位置的目标抑制反应。同时测量反应速度和抑制控制能力。参见 [go-nogo.md](go-nogo.md)
- **多维 CRT（Multi-dimensional CRT）**：刺激在多个维度上变化（如形状 + 颜色 + 位置），被试需根据其中一个维度（任务相关维度）做出选择反应，同时忽略其他维度（任务无关维度）。可用于研究选择性注意、冲突加工（如 Stroop 或 Flanker 类似的跨维度干扰）

---

## Example

### User Request

> "我想做一个选择反应时实验。屏幕上有3个位置（左、右、下），会随机出现3种图形（圆形、方形、三角形）。看到圆形按 F 键，方形按 G 键，三角形按 H 键。每个试次先呈现500 ms注视点，然后图形出现。图形一直显示直到被试按键反应，超时3000 ms视为漏报。按键后如果正确直接进入ITI，如果错误屏幕中央显示红色叉号800 ms。练习20个试次，正式实验3个block每个40试次。ITI随机500-1000 ms。用PsychoPy，指导语用中文。"
> 
> （此请求可通过 psy-exp-coder 技能直接生成代码）

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Stimulus                 │    │ Feedback                 │    │ ITI                      │
│ Content: +               │    │ Content: 圆形/方形/三角形 │    │ Content: 红色 X（仅错误）│    │ Content: empty           │
│ Duration: 500 ms         │    │ at 左/右/下 position      │    │ Duration: 800 ms         │    │ Duration: 500-1000 ms     │
│ Response: none           │    │ Duration: until key       │    │ Response: none           │    │ Response: none           │
│ Data: none               │    │ Response: F/G/H 键       │    │ Data: none               │    │ Data: none               │
│                          │    │ Timeout: 3000 ms          │    │                          │    │                           │
│                          │    │ Data: rt, key, acc        │    │                          │    │                           │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | Condition | Data |
|--------|---------|----------|----------|-----------|------|
| Fixation | + | 500 ms | none | none | none |
| Stimulus | 圆形/方形/三角形 at 左/右/下 | until key (deadline 3000 ms) | F/G/H | {shape}, {position}, {correct_key} | rt, key, acc |
| Feedback | 红色X（仅错误试次） | 800 ms | none | none | none |
| ITI | empty | 500-1000 ms random | none | none | none |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| 实验名称 | 三图形选择反应时实验 |
| 平台 | PsychoPy |
| 任务类型 | Choice RT（选择反应时） |
| 刺激形状 | 圆形、方形、三角形 |
| 刺激位置 | 左、右、下（3个） |
| 反应方式 | 键盘按键：F（圆形）、G（方形）、H（三角形） |
| 注视点持续时间 | 500 ms |
| 反应超时 | 3000 ms |
| 错误反馈 | 红色叉号，800 ms |
| 实验阶段 | 指导语 → 练习(20试次) → Block1-3(各40试次) |
| ITI | 500-1000 ms 随机 |

### Missing Information

1. 指导语具体文案未提供 → 将使用标准中文指导语模板，说明每个图形对应的按键
2. 操作系统和字体路径未提供 → 假设中文 Windows/macOS，使用系统默认中文字体（需确认 `Songti SC` 或 `SimHei` 路径）
3. 练习阶段是否给予反馈未明确 → 假设练习有逐试次反馈（含 RT 和正确性），正式 block 仅错误时显示红色叉号

### Critical Assumptions

- 注视点持续时间 500 ms（用户在请求中明确提及）
- 刺激在被试按键后立即消失（response-terminated display），超时 3000 ms 后自动进入 ITI
- 每个 block 内各条件（shape × position）均等呈现，试次顺序随机化
- 正确试次不显示反馈，直接进入 ITI；错误试次显示红色叉号 800 ms 后进入 ITI
- 无位置预提示（position cuing），与 Pavlovia 标准实现不同

### Code Architecture

```
crt.py
├── 参数定义（形状列表、位置列表、按键映射、时间参数）
├── 窗口创建（Window）
├── 刺激预加载（TextStim 注视点、ShapeStim 图形、TextStim 反馈）
├── 条件表生成（shape × position 全因子组合 × 重复次数）
├── 指导语呈现
├── 试次循环：
│   ├── 注视点（500 ms）
│   ├── 目标刺激（按键终止，deadline 3000 ms）
│   ├── 错误反馈（红色叉号 800 ms，仅错误试次）
│   └── ITI（500-1000 ms 随机）
└── 数据保存（try/finally，增量写入 CSV）
```

### Expected Data Columns

| Column | Type | Description |
|--------|------|-------------|
| shape | str | 刺激形状（"圆形"/"方形"/"三角形"） |
| position | str | 刺激位置（"左"/"右"/"下"） |
| correct_key | str | 正确按键（"f"/"g"/"h"） |
| rt | float | 反应时（ms），相对刺激出现时刻 |
| key_resp | str | 被试实际按键 |
| acc | int | 正确性（1=正确，0=错误，-1=超时漏报） |
| timeout | int | 是否超时（1=超时，0=正常反应） |
