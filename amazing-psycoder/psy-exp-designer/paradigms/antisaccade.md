# Antisaccade Task

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/antisaccade) · PsychoJS

## When to Use

User mentions: Antisaccade, anti-saccade, inhibitory control, oculomotor inhibition, 反眼跳任务. Measures the ability to inhibit a reflexive prosaccade toward a peripheral cue and instead generate a voluntary saccade to the opposite location.

## Core Logic

On each trial, a central fixation cross is presented, followed by a brief peripheral cue flash on one side of the screen. After the cue disappears, a target stimulus (often a letter or arrow) appears on the opposite side. The participant must rapidly identify the target by pressing the correct key. The critical manipulation is that the target appears in the opposite hemifield from the cue, requiring inhibition of the prepotent reflexive saccade toward the sudden-onset cue.

Trials are driven by a condition file (`conditions.xlsx`) specifying cue position, target identity, and correct answer for each trial. Trials are randomly shuffled. The cue-target asynchrony and stimulus durations are precisely controlled using frame-accurate timing.

**Response modes**: The participant selects their input method at experiment start — keyboard (left/right arrow keys or letter keys), mouse click (click on target location), or hover (move cursor to target location). This multi-modal input design accommodates different hardware setups and populations.

**Trial structure**: fixation (variable duration, typically 1000–2000 ms) → peripheral cue (brief flash, typically 200 ms) → target at opposite location (brief, typically 100–150 ms, often masked) → response window. Accuracy is determined by comparing the participant's key response to the `corr_ans` column from the condition file. Response time is measured from target onset.

**Conditions**: Typically a mix of prosaccade trials (target same side as cue) and antisaccade trials (target opposite side as cue). The antisaccade error rate (incorrect saccades toward the cue on antisaccade trials) and the latency difference between correct antisaccades and prosaccades (antisaccade cost) are the central dependent measures.

## Must Confirm

- **Response mode**: Keyboard, mouse click, or hover? Which specific keys for keyboard mode?
- **Stimulus identity**: Are targets letters (requiring letter identification), arrows (directional judgment), or simple dots (detection only)?
- **Trial mix**: What proportion of prosaccade vs. antisaccade trials? 50:50 or different ratio?
- **Timing parameters**: Fixation duration, cue duration, target duration, and response deadline?
- **Masking**: Is the target masked (e.g., by a visual pattern) after offset, or does it simply disappear?
- **Eye-tracking integration**: Is this a manual-response-only version, or does it require eye-tracking for saccade measurement?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Peripheral Cue           │    │ Target                   │    │ ITI / Response Window     │
│ Content: + at center     │    │ Content: dot/square      │    │ Content: letter/arrow    │    │ Content: blank           │
│ Duration: 1000-2000 ms   │    │ Duration: ~200 ms        │    │ Duration: 100-150 ms     │    │ Duration: until response │
│ Response: none           │    │ Response: none           │    │ Response: key/click/hover│    │ Response: none           │
│ Condition: none          │    │ Condition: cue_position  │    │ Condition: target_id     │    │ Condition: none          │
│ Data: none               │    │ Data: none               │    │ Data: rt, key, acc       │    │ Data: none               │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

## Data Analysis

Key measures: antisaccade error rate (proportion of trials where response was toward the cue side), antisaccade latency vs. prosaccade latency (antisaccade cost), and accuracy of target identification. Analyze condition differences (prosaccade vs. antisaccade) via paired t-tests or repeated-measures ANOVA. Higher error rates and longer latencies on antisaccade trials index poorer inhibitory control. Typical findings show patients with frontal lobe damage, schizophrenia, or ADHD have elevated antisaccade error rates.

## References

Hallett, P. E. (1978). Primary and secondary saccades to goals defined by instructions. *Vision Research, 18*(10), 1279–1296. https://doi.org/10.1016/0042-6989(78)90218-3

Munoz, D. P., & Everling, S. (2004). Look away: The anti-saccade task and the voluntary control of eye movement. *Nature Reviews Neuroscience, 5*(3), 218–228. https://doi.org/10.1038/nrn1345

## Do Not Assume

- Do not assume the target always appears on the opposite side. 在标准反眼跳任务中，朝向眼跳试次（目标与线索同侧）通常与反眼跳试次随机混合呈现。必须明确确认试次混合比例，以及两种试次类型在条件文件中如何编码（如 `trial_type` 列标记为 `"pro"` 或 `"anti"`）。
- Do not assume keyboard response is the only input mode. 反眼跳任务支持键盘、鼠标点击和悬停（hover）三种输入方式。需在实验开始前让被试选择输入模式，并确认对应的按键映射或响应区域定义。若不确认，生成的代码可能只实现键盘模式，导致无法在触摸屏或无键盘设备上运行。
- Do not assume the target is always a letter requiring identification. 目标刺激可能是字母（需字母识别，如判断字母是 A 还是 E）、箭头（方向判断，如左箭头按左键）、或简单探测点（检测是否出现）。目标身份影响正确反应的定义方式和条件文件中 `corr_ans` 列的取值。
- Do not assume there is no response deadline. 目标呈现时间通常很短（100–150 ms），但反应窗口可能设有截止时间（如 2000 ms）。需确认是否设置最大反应时间、超时后如何编码（`acc = -1` 或 `acc = 0` 且 `timeout = 1`）。
- Do not assume eye-tracking data is always required. 许多反眼跳实验仅使用手动反应（按键或点击）来测量行为抑制指标（错误率、反应时），而无需眼动仪。需明确是否需要集成眼动追踪硬件，若不需要，则无需在代码中包含 EyeLink 或 Tobii 的通信逻辑。
- Do not assume the cue-target interval is always zero. 线索消失到目标出现之间的间隔（cue-target asynchrony, CTA）可能为 0 ms（无间隔）、200 ms（gap条件），或在实验中系统变化。CTA 影响反眼跳潜伏期和错误率，需在生成代码前确认具体参数。

## Condition File Columns

| Column | Type | Description |
|--------|------|-------------|
| cue_pos | str | 外周线索出现的位置，`"left"` 或 `"right"` |
| target_id | str | 目标刺激的标识（如字母 `"A"`/`"E"`、箭头方向 `"left"`/`"right"`、或点探测 `"dot"`） |
| trial_type | str | 试次类型，`"pro"`（朝向眼跳，目标与线索同侧）或 `"anti"`（反眼跳，目标与线索对侧） |
| corr_ans | str | 正确反应按键，如 `"left"`、`"right"`、`"a"`、`"e"`，由目标身份决定 |
| target_pos | str | 目标出现的位置，`"left"` 或 `"right"`。在反眼跳试次中与 `cue_pos` 相反，可用于推导 `trial_type` |

## Variants

- **Gap/Overlap Antisaccade Task（间隙/重叠反眼跳任务）**：在固定点消失（gap条件，固定点在线索出现前消失200 ms）或不消失（overlap条件，固定点持续显示）后呈现外周线索。Gap条件降低了反眼跳潜伏期，用于研究注意脱离（attentional disengagement）和眼动准备机制。相关范式：[gap-overlap](./gap-overlap.md)
- **Memory-Guided Antisaccade Task（记忆引导反眼跳任务）**：目标仅在极短时间内闪现（如 50–100 ms），被试需在延迟期（数秒）后向目标镜像位置执行眼跳。增加了工作记忆负荷，用于分离抑制控制与空间工作记忆成分，常见于精神分裂症和额叶损伤研究。
- **Mixed Pro/Anti Blocked Design（混合/分块设计反眼跳任务）**：将朝向眼跳和反眼跳试次按 block 分离（而非随机混合），每个 block 内试次类型相同。Block 起始有明确的线索提示当前 block 类型。用于研究任务切换成本（switch cost）和自上而下的抑制准备效应。

---

## Example

### User Request

> "我想做一个反眼跳实验。屏幕中央先呈现注视点1000到2000 ms随机，然后在左侧或右侧快速闪现一个白色方块作为线索，持续200 ms。线索消失后，在相反方向呈现一个箭头（←或→），持续150 ms。被试需要用左右箭头键尽快判断箭头方向。线索位置和目标方向是独立随机的。总共200个试次，反眼跳和朝向眼跳各占一半。先做20个练习试次。用PsychoPy实现。"

### Trial Window Timeline

```text
┌──────────────────────────────┐    ┌──────────────────────────────┐    ┌──────────────────────────────┐    ┌──────────────────────────────┐
│ Window 1                     │ →  │ Window 2                     │ →  │ Window 3                     │ →  │ Window 4                     │
│ 注视点                       │    │ 外周线索                     │    │ 目标箭头                     │    │ ITI                          │
│ Content: + 在屏幕中央        │    │ Content: 白色方块            │    │ Content: ← 或 →              │    │ Content: 空白               │
│ Duration: 1000-2000 ms 随机  │    │ Duration: 200 ms             │    │ Duration: 150 ms             │    │ Duration: 500-1000 ms       │
│ Response: 无                 │    │ Response: 无                 │    │ Response: left/right 箭头键  │    │ Response: 无               │
│ Condition: 无                │    │ Condition: {cue_pos}         │    │ Condition: {target_id}       │    │ Condition: 无               │
│ Data: 无                     │    │ Data: 无                     │    │ Data: rt, key, acc           │    │ Data: 无                     │
└──────────────────────────────┘    └──────────────────────────────┘    └──────────────────────────────┘    └──────────────────────────────┘
```

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| 实验名称 | 箭头反眼跳任务 |
| 平台 | PsychoPy |
| 任务类型 | 反眼跳任务（Antisaccade） |
| 线索刺激 | 白色方块（外周闪现） |
| 目标刺激 | 箭头（← 或 →） |
| 反应方式 | 左右箭头键判断目标箭头方向 |
| 注视点持续时间 | 1000–2000 ms 随机（均匀分布） |
| 线索持续时间 | 200 ms |
| 目标持续时间 | 150 ms |
| 试次混合比例 | 50% 朝向眼跳 / 50% 反眼跳 |
| 总试次数 | 200 正式试次 + 20 练习试次 |
| 反应模式 | 键盘（左右箭头键） |

### Missing Information

1. ITI 持续时间未明确说明 → 假设 500–1000 ms 随机，需向用户确认具体范围和分布方式
2. 练习阶段是否需要反馈提示 → 需确认（通常练习阶段提供正确/错误试次级反馈，正式阶段不提供）
3. 目标消失后是否有掩蔽刺激 → 用户未提及掩蔽，假设目标直接消失无掩蔽。需确认是否需要视觉掩蔽以防止后像线索

### Critical Assumptions

- 注视点持续时间在每个试次中独立随机选取（1000–2000 ms 均匀分布），不使用阶梯变化或自适应调整
- 线索位置（左/右）与目标箭头方向（←/→）完全交叉平衡（各 50 试次），确保每个条件组合的试次数均匀
- 反应窗口从目标开始呈现时启动，截止时间为 2000 ms（从目标 onset 算起）。超时标记为错误（`acc = 0`，`timeout = 1`），RT 记录为截止时间值
- 练习阶段提供试次级反馈（正确/错误），正式阶段不提供反馈，block 间显示休息提示

### Code Architecture

```
antisaccade.py
├── 参数设置（注视点持续范围、线索持续、目标持续、ITI范围、反应截止时间）
├── 窗口初始化（全屏或窗口，背景色设置）
├── 刺激预加载
│   ├── TextStim：注视点 "+"
│   ├── Rect：白色线索方块（出现在左/右侧）
│   ├── TextStim：箭头 "←" / "→"（出现在左/右侧）
│   └── TextStim：反馈文字 "正确"/"错误"（仅练习阶段）
├── 条件表生成
│   ├── cue_pos × target_id 完全交叉（左/右 × ←/→ = 4 种组合）
│   ├── trial_type 推导：cue_pos == target_pos → "pro"，否则 → "anti"
│   ├── corr_ans 推导：target_id "left" → corr_ans "left"，target_id "right" → corr_ans "right"
│   └── 按 50:50 比例分配 pro/anti，共 200 试次，随机打乱
├── 试次循环（逐试次执行）：
│   ├── 注视点窗口（1000–2000 ms 随机，从条件表读取固定随机值确保可复现）
│   ├── 线索窗口（200 ms，白色方块在左侧或右侧，位置由 cue_pos 决定）
│   ├── 目标窗口（150 ms，箭头在 target_pos 指定位置呈现）
│   ├── 反应窗口（deadline 2000 ms，监听 left/right 键，记录 rt 和 key）
│   ├── 反馈显示（仅练习阶段，500 ms 正确/错误提示）
│   └── ITI（500–1000 ms 随机，空白屏幕）
├── 数据保存：try/finally 结构，CSV 逐行写入确保数据安全
└── 退出提示（实验结束感谢语）
```

### Expected Data Columns

| Column | Type | Description |
|--------|------|-------------|
| trial_index | int | 试次序号（0–199） |
| cue_pos | str | 线索出现位置（`"left"` 或 `"right"`） |
| target_id | str | 目标箭头方向（`"left"` 或 `"right"`） |
| target_pos | str | 目标出现位置（`"left"` 或 `"right"`） |
| trial_type | str | 试次类型（`"pro"` 或 `"anti"`） |
| corr_ans | str | 正确反应按键（`"left"` 或 `"right"`） |
| fix_dur | float | 注视点实际持续时间（ms） |
| cue_onset | float | 线索开始呈现时间（相对于试次开始，s） |
| target_onset | float | 目标开始呈现时间（相对于试次开始，s） |
| rt | float | 反应时间（ms，从目标 onset 算起） |
| key_resp | str | 被试实际按键（`"left"`、`"right"` 或 `None`） |
| acc | int | 正确率（1 = 正确，0 = 错误或超时） |
| timeout | int | 是否超时（1 = 超时未反应，0 = 在截止时间内做出反应） |
