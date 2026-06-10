# Continuous Performance Test (CPT)

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/continuous_performance_test) · PsychoJS

## When to Use

User mentions: CPT, continuous performance test, sustained attention, vigilance, 持续注意测试, 连续表现测试. Measures sustained attention and vigilance over an extended period by requiring participants to respond to frequent go stimuli while withholding responses to infrequent no-go targets.

## Core Logic

This implementation is a go/no-go CPT variant. Participants view a rapid stream of letter stimuli presented one at a time. They must press the spacebar for every letter **except** the target letter 'X'. This inverts the typical CPT structure (where the target is rare and requires a response) — here the target 'X' requires response **inhibition**, making it a measure of both sustained attention and inhibitory control.

**Trial structure**: fixation cross (1000 ms) → letter stimulus (1000 ms) → next trial. The keyboard is monitored during the letter presentation window. Each trial's condition comes from `conditions.xlsx` with columns specifying the letter to display and the correct answer (`corrAns`: 'space' for go trials, 'none' for no-go/X trials).

**Accuracy logic**: Two-path accuracy check. When a key is pressed, the response is compared against `corrAns`. When no key is pressed, the code checks whether `corrAns` is 'none' (correct withholding on X trials). A `correct_counter` accumulates correct trials and is displayed as the final score.

**Trial count and target frequency**: The condition file defines the sequence. The target 'X' typically appears on 20–30% of trials. A trial counter (e.g., "Trial 12 / 120") is shown throughout the experiment to provide participant pacing.

**Key dependent variables**:
- **Omission errors**: Failing to press spacebar on non-X trials (indexes inattention)
- **Commission errors**: Pressing spacebar on X trials (indexes impulsivity / inhibitory failure)
- **Reaction time**: For correct go responses; RT variability over time indexes attentional fluctuation
- **d-prime**: Signal detection measure combining hits and false alarms

## Must Confirm

- **CPT variant**: Go/no-go (this version: respond to all except X), X-CPT (respond only to X), AX-CPT (respond to X only when preceded by A), or Identical Pairs?
- **Stimulus type**: Letters (single uppercase), digits, or shapes?
- **Trial count**: Total number of trials? (needs to be substantial, 100–300+, to tax sustained attention)
- **Stimulus and fixation durations**: 1000 ms each, or custom?
- **Response key**: Spacebar for all go responses, or specific keys?
- **No-go target**: Single letter 'X', or multiple no-go stimuli?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │
│ Fixation                 │    │ Letter Stimulus          │
│ Content: + at center     │    │ Content: letter (A-Z)    │
│ Duration: 1000 ms        │    │ Duration: 1000 ms        │
│ Response: none           │    │ Response: spacebar       │
│ Condition: none          │    │ (withhold on X)          │
│ Data: none               │    │ Condition: {letter}      │
└──────────────────────────┘    │ Data: rt, key, acc,      │
                                │   omission/commission     │
                                └──────────────────────────┘
```

## Data Analysis

Key measures: omission errors (misses), commission errors (false alarms), mean RT (and RT variability/SD), signal detection measures (d', criterion). Performance decline across blocks indexes the vigilance decrement. Examine commission errors as a behavioral index of impulsivity/inhibitory control, and omissions/RT variability as indices of inattention. The CPT is widely used in ADHD assessment; elevated commission errors and RT variability are characteristic.

## References

Rosvold, H. E., Mirsky, A. F., Sarason, I., Bransome, E. D., Jr., & Beck, L. H. (1956). A continuous performance test of brain damage. *Journal of Consulting Psychology, 20*(5), 343–350. https://doi.org/10.1037/h0043220

Cohen, J. D., Barch, D. M., Carter, C., & Servan-Schreiber, D. (1999). Context-processing deficits in schizophrenia: Converging evidence from three theoretically motivated cognitive tasks. *Journal of Abnormal Psychology, 108*(1), 120–133. https://doi.org/10.1037/0021-843X.108.1.120

## Do Not Assume

- Do not assume CPT 的响应规则是"对目标按、对非目标不按"。标准 X-CPT 要求对稀有目标 X 按键，但 go/no-go CPT 变式要求对所有字母按键唯独对 X 抑制。两种规则完全相反，必须在生成代码前确认使用哪种。
- Do not assume no-go 试次上 RT=NaN 是错误。在 X 试次上被试应当抑制反应，因此 RT 缺失是正确表现的预期结果，不应在数据清洗中将其标记为异常。
- Do not assume 条件文件总是由代码随机生成。部分实验设计需要预先生成的伪随机序列以保证目标出现间隔和频率符合要求，应确认是由代码生成还是从外部文件读取。
- Do not assume 刺激类型仅限于单个大写字母。CPT 也可使用数字、形状或图片刺激，不同刺激类型的视觉特征会影响辨别难度和持续注意负荷。
- Do not assume 注视点和刺激呈现时间相同。虽然常见默认均为 1000 ms，但注视点可以更短（如 500 ms）以加快试次节奏，刺激窗口可以更长（如 1500 ms）以容纳反应时间要求。
- Do not assume 反馈必然存在。部分 CPT 设计刻意省略试次间反馈以避免干扰持续注意过程，尤其是正式实验阶段通常不提供反馈。

## Condition File Columns

| Column | Type | Description |
|--------|------|-------------|
| letter | str | 当前试次呈现的字母（如 `"A"`, `"X"`） |
| corrAns | str | 正确反应：`"space"`（go 试次需按键）或 `"none"`（no-go 试次需抑制） |

## Variants

- **X-CPT（标准 CPT）**：对稀有目标字母 X 按键反应，对其他字母不反应。这是最经典的 Rosvold 等人（1956）版本，目标试次占比约 20–30%，主要测量持续注意和警觉。
- **Go/No-Go CPT**：对所有字母按键反应，唯独对 X 抑制反应。该变式将任务从"对稀有目标反应"反转为"对频繁 go 刺激反应、对罕见 no-go 刺激抑制"，因此同时测量持续注意和反应抑制能力。本文件描述的即是此变式。相关范式见 [go-nogo.md](go-nogo.md)。
- **AX-CPT**：仅在字母 X 紧随字母 A 出现时按键反应，其他所有情况（包括单独出现 X 或 A 后接非 X）均不反应。该变式增加了上下文加工负荷，广泛用于精神分裂症的认知缺陷研究。相关范式见上下文加工任务。

## Example

#### 用户请求

> "我要做一个CPT实验。屏幕中央逐个呈现大写字母，看到任何字母都按空格键，唯独看到字母X时不要按。总共150个试次，其中X占20%。每个试次先呈现注视点+ 500ms，再呈现字母800ms，反应窗口从字母出现开始持续1000ms。ITI随机600-1000ms。先做10个练习试次（有反馈），再做正式实验（无反馈）。用jsPsych。"

#### 试次窗口时间线

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ 注视点                    │    │ 刺激呈现                  │    │ 反应窗口                  │    │ ITI                      │
│ 内容: +                  │    │ 内容: A-Z (非X/X)         │    │ 内容: A-Z (非X/X)         │    │ 内容: 空白                │
│ 时长: 500 ms             │    │ 时长: 800 ms             │    │ 时长: 1000 ms             │    │ 时长: 600-1000 ms 随机     │
│ 反应: 无                  │    │ 反应: 无                  │    │ 反应: space (X时不按)      │    │ 反应: 无                  │
│ 条件: 无                  │    │ 条件: {letter}            │    │ 条件: {corrAns}           │    │ 条件: 无                  │
│ 数据: 无                  │    │ 数据: 无                  │    │ 数据: rt, key, acc       │    │ 数据: 无                  │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

#### 解析后的实验规格

| 字段 | 值 |
|------|-----|
| 实验名称 | Letter Go/No-Go CPT |
| 平台 | jsPsych |
| 任务类型 | Go/No-Go CPT（对所有非X按空格，对X抑制） |
| 刺激类型 | 大写字母 (A-Z) |
| No-go 目标 | X |
| No-go 比例 | 20% (30 / 150 试次) |
| 总试次数 | 150（不含练习） |
| 注视点时长 | 500 ms |
| 刺激呈现时长 | 800 ms |
| 反应窗口 | 1000 ms（从刺激出现起算） |
| ITI | 600-1000 ms 随机 |
| 练习试次 | 10 个，有反馈 |
| 正式实验 | 150 个试次，无反馈 |

#### 缺失信息

1. 是否允许连续出现两个及以上 X 试次？最大连续次数限制是多少？（通常不允许超过 2 个连续 no-go）
2. 练习阶段的 X 比例是否与正式阶段一致？（通常一致，但需确认）
3. 指导语的具体措辞？是否需要休息间隔？（150 试次约需 6-8 分钟，可能不需要中间休息）

#### 关键假设

- 注视点时长 500 ms 为用户明确指定；字母呈现 800 ms + 反应窗口 1000 ms 为用户明确指定
- 无反馈在正式阶段（用户明确说明"正式实验无反馈"），练习阶段有反馈
- 条件序列由代码随机生成，go/no-go 比例 80:20，限制连续 no-go 不超过 2 个
- 反应键为空格键，提前反应（< 100 ms）标记为无效

#### 代码架构

```
cpt.html (jsPsych 插件式结构)
├── 参数定义 (go_key, no_go_target, ratio, timing)
├── 条件序列生成 (150 试次, 80:20 go:nogo, 限制连续nogo≤2)
├── 时间线构建:
│   ├── 指导语 (html-keyboard-response)
│   ├── 练习阶段 (10 试次):
│   │   └── 试次循环:
│   │       ├── 注视点 (500 ms, html-keyboard-response 禁用按键)
│   │       ├── 刺激 (800 ms, html-keyboard-response, stimulus_duration: 800, trial_duration: 1800)
│   │       └── 反馈 (html-keyboard-response, 正确/错误/超时提示)
│   ├── 正式阶段提示 (html-keyboard-response)
│   └── 正式阶段 (150 试次):
│       └── 试次循环:
│           ├── 注视点 (500 ms)
│           ├── 刺激+反应 (html-keyboard-response, stimulus_duration: 800, trial_duration: 1800)
│           └── ITI (600-1000 ms 随机)
├── 数据保存 (jsPsych data → CSV)
└── 结束页面
```

#### 预期数据列

| Column | Type | Description |
|--------|------|-------------|
| trial_index | int | 试次序号（含练习） |
| phase | str | `"practice"` 或 `"test"` |
| stimulus | str | 当前呈现的字母 |
| corrAns | str | 正确反应 (`"space"` 或 `"none"`) |
| response | str | 被试实际按键 (`"space"` 或 `null`) |
| rt | float | 反应时 (ms)，no-go 正确抑制时为 null |
| acc | int | 正确性 (1=正确, 0=错误) |
| commission_error | int | 误报错误 (对X按键=1, 否则0) |
| omission_error | int | 遗漏错误 (对非X未按键=1, 否则0) |
