# Psychophysics Staircase (Adaptive Threshold Estimation)

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/staircase_demo) · PsychoJS

## When to Use

User mentions: Staircase, psychophysics, adaptive threshold, orientation discrimination, just noticeable difference, 心理物理阶梯法, 自适应阈值. An adaptive psychophysical procedure that efficiently estimates sensory thresholds by adjusting stimulus intensity based on the participant's recent performance.

## Core Logic

The staircase procedure adaptively changes the difficulty of a perceptual discrimination task to converge on a participant's threshold. This implementation is a custom staircase (no built-in `MultiStairHandler`) that measures the minimal orientation difference at which a participant can distinguish between two tilted gratings.

**Task**: On each trial, two grating images are presented — one on the left and one on the right. One grating is tilted slightly clockwise, the other counterclockwise. The participant must indicate which side has the clockwise-tilted grating by pressing the left or right arrow key (2AFC — two-alternative forced choice).

**Staircase parameters** (all configurable in code):
- **Starting value**: 70 degrees (large initial orientation difference, easy to discriminate)
- **Step sizes**: [10, 5, 2, 1, 0.5] degrees — progressively finer steps across successive reversals for precise threshold estimation
- **Up/Down rule**: 1-up 1-down (converges to 50% threshold). Each correct response decreases the difference (makes it harder); each incorrect response increases the difference (makes it easier).
- **Number of reversals**: 5 — the staircase stops after 5 direction changes
- **Bounds**: min 0 degrees, max 90 degrees
- **Direction tracking**: Starts in "down" direction (decreasing orientation difference after correct responses)

**Reversals and threshold**: A "reversal" occurs when the staircase changes direction (from decreasing to increasing, or vice versa). The threshold is calculated as the average of the stimulus levels (orientation differences) at all reversal points. The first few reversals are sometimes excluded to allow the staircase to settle.

**Common staircase rules**:
- 1-up 1-down → converges to 50% threshold
- 2-up 1-down → converges to ~70.7% threshold (most common for detection tasks)
- 3-up 1-down → converges to ~79.4% threshold

**Safety limits**: A maximum number of trials (e.g., 100) serves as a safety net if the required number of reversals is not met.

## Must Confirm

- **Perceptual dimension**: Orientation discrimination (grating tilt), contrast detection, motion coherence, auditory frequency, or other?
- **Up/Down rule**: 1-up 1-down (50% threshold), 2-up 1-down (~70.7%), or 3-up 1-down (~79.4%)?
- **Starting value**: Large initial difference (easy) or near-threshold (faster convergence)?
- **Step sizes**: What step size sequence? Single fixed step or decreasing sequence?
- **Number of reversals**: How many reversals before stopping? (5-8 typical)
- **Maximum trials**: Safety limit on total trials?
- **Threshold calculation**: Average of all reversal values, or exclude first N reversals?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Grating Pair             │    │ Feedback (optional)      │    │ ITI                      │
│ Content: + at center     │    │ Content: 2 tilted        │    │ Content: correct/incorrect│   │ Content: blank           │
│ Duration: 500 ms         │    │   gratings (L and R)     │    │ Duration: 300 ms         │    │ Duration: 500 ms         │
│ Response: none           │    │ Duration: until key      │    │ Response: none           │    │ Response: none           │
│ Condition: none          │    │ Response: left/right key │    │ Condition: none          │    │ Condition: none          │
│ Data: none               │    │ Condition: {level}       │    │ Data: none               │    │ Data: none               │
└──────────────────────────┘    │   (orientation difference)│    └──────────────────────────┘    └──────────────────────────┘
                                │ Data: rt, key, acc,      │
                                │   level, direction       │
                                └──────────────────────────┘
```

## Data Analysis

The primary output is the threshold estimate (mean of reversal values). Plot the staircase trajectory (stimulus level vs. trial number) to visualize convergence. The threshold represents the just-noticeable difference (JND) for the perceptual dimension tested. Compare thresholds between conditions or groups. Check that the staircase converged (stable oscillation around threshold by final reversals) and that the number of trials was sufficient.

## References

Cornsweet, T. N. (1962). The staircase-method in psychophysics. *The American Journal of Psychology, 75*(3), 485–491. https://doi.org/10.2307/1419876

Levitt, H. (1971). Transformed up-down methods in psychoacoustics. *The Journal of the Acoustical Society of America, 49*(2B), 467–477. https://doi.org/10.1121/1.1912375

---

## Do Not Assume

- Do not assume 阶梯法使用 1-up 1-down 规则。虽然这是自定义阶梯法的默认实现，但不同的上下规则收敛于不同的阈限水平。1-up 1-down 收敛于 50% 正确率阈限，2-up 1-down 收敛于约 70.7%，3-up 1-down 收敛于约 79.4%。生成代码前必须确认具体规则，否则阈限估计的系统偏差将无法控制。
- Do not assume 起始值总是很大（容易辨别）。本实现从 70 度起始（方向辨别差异很大），但起始值应根据具体知觉维度和被试群体调整。起始值过大导致阶梯收敛缓慢（需要更多试次才能接近阈限），起始值过小导致早期试次全是错误反应、被试受挫。需确认起始值对应的任务难度。
- Do not assume 步长序列固定不变。本实现使用 [10, 5, 2, 1, 0.5] 度的递减步长序列，但步长的选择取决于刺激维度（对比度、空间频率、运动一致性等）和阈限期望精度。固定步长（如始终 2 dB）和递减序列各有优劣，需确认步长策略。
- Do not assume 阈限计算使用所有 reversal 的平均值。有些阶梯实现会排除前 1-3 个 reversal（允许阶梯先收敛到阈限附近再开始正式记录），仅用后几个 reversal 计算阈限。需确认是否排除初始 reversal，以及阈限的计算方式（均值还是中位数）。
- Do not assume 阶梯法不需要条件文件。虽然传统阶梯法的刺激水平完全由被试前几个试次的表现决定（自适应），但许多现代实现仍需要条件文件来指定：多个交叉阶梯的起始值、每种条件下的 staircase ID、或 block 级别的参数设置。尤其在交错阶梯设计中，条件文件是必需的。
- Do not assume 知觉维度总是朝向辨别（grating tilt）。本参考实现使用光栅倾斜辨别（orientation discrimination），但阶梯法广泛应用于对比度检测（contrast detection）、运动一致性辨别（motion coherence）、听觉频率辨别（auditory frequency discrimination）、触觉阈值等各类心理物理任务。刺激创建和 staircase 更新逻辑随知觉维度不同而有本质差异。

## Condition File Columns

| Column | Type | Description |
|--------|------|-------------|
| staircase_id | int | 阶梯编号，用于交错阶梯设计中区分不同的 staircase（如不同起始值或不同刺激条件）。单阶梯设计可省略 |
| start_level | float | 该 staircase 的起始刺激水平值（如起始方向差异度数、起始对比度值等），用于初始化 staircase 的当前水平 |
| condition_label | str | 该 staircase 对应的实验条件标签（如 `"high_contrast_adapt"` 或 `"low_contrast_adapt"`），用于分组分析和数据筛选 |

## Variants

- **变换上下法（Transformed Up-Down Staircase）**：改变上下规则以收敛于不同的心理测量函数点。常见变体包括 2-up 1-down（收敛于 ~70.7% 阈限）、3-up 1-down（收敛于 ~79.4% 阈限）以及加权上下法（如 1-up 2-down 收敛于 ~29.3%）。适用于需要估计特定正确率阈限（而非 50% 点）的检测和辨别任务。参考：Levitt (1971)。
- **交错阶梯法（Interleaved Staircase）**：同时运行 2-4 个独立的 staircase，每个 staircase 的试次随机交错呈现。不同 staircase 可以对应不同的刺激条件（如不同空间频率、不同适应状态）或不同的起始值。交错设计使被试无法预测当前试次属于哪个 staircase，从而减少期望偏差和反应策略的干扰。适用于需要同时测量多个阈限的条件对比实验。相关范式：[dual-task](./dual-task.md)（共享交错试次设计的逻辑）。
- **贝叶斯自适应阶梯法（Bayesian Adaptive Staircase, e.g., QUEST / Psi）**：使用贝叶斯推断在每次试次后更新整个心理测量函数的后验分布，并根据信息增益最大的原则选择下一个试次的刺激水平。相比于传统阶梯法仅在阈限附近采样，QUEST 和 Psi 方法能更高效地同时估计阈限和斜率参数，通常只需 20-40 个试次即可达到传统阶梯法 60-100 个试次的精度。适用于试次数有限或需要同时估计多个参数的场景。

---

## Example

### User Request

> "我想做一个对比度检测的心理物理阶梯实验。屏幕中央先呈现注视点 500 ms，然后在屏幕中央呈现一个 Gabor 光栅（正弦光栅，空间频率 2 cpd，高斯包络 sigma=2°），持续 200 ms。被试的任务是判断是否看到了光栅——看到按 'z' 键（是），没看到按 '/' 键（否）。采用 2-up 1-down 阶梯法，起始对比度 50%（Michelson 对比度），初始步长 0.1 log 单位，第二个 reversal 后步长缩小为 0.05 log 单位。总共 8 个 reversal 后停止，最多 120 个试次。阈限取最后 6 个 reversal 的平均值。用 PsychoPy 实现。"

### Trial Window Timeline

```text
┌──────────────────────────────┐    ┌──────────────────────────────┐    ┌──────────────────────────────┐    ┌──────────────────────────────┐
│ Window 1                     │ →  │ Window 2                     │ →  │ Window 3                     │ →  │ Window 4                     │
│ 注视点                       │    │ 刺激呈现                     │    │ 反应窗口                     │    │ ITI                          │
│ Content: + 在屏幕中央        │    │ Content: Gabor 光栅          │    │ Content: 空白屏幕            │    │ Content: 空白               │
│ Duration: 500 ms             │    │   (target contrast, 2 cpd)  │    │ Duration: 直到按键或3000ms  │    │ Duration: 400-800 ms       │
│ Response: 无                 │    │ Duration: 200 ms             │    │ Response: z（看到）/        │    │ Response: 无               │
│ Condition: 无                │    │ Response: 无                 │    │   /（没看到）               │    │ Condition: 无               │
│ Data: 无                     │    │ Condition: {contrast_level}  │    │ Condition: {correct_resp}   │    │ Data: 无                     │
│                               │    │ Data: stimulus_onset_time   │    │ Data: rt, key, acc,         │    │                               │
│                               │    │                              │    │   contrast_level,           │    │                               │
│                               │    │                              │    │   reversal_count            │    │                               │
└──────────────────────────────┘    └──────────────────────────────┘    └──────────────────────────────┘    └──────────────────────────────┘
```

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| 实验名称 | 对比度检测阶梯实验 |
| 平台 | PsychoPy |
| 任务类型 | 心理物理阶梯法（Contrast Detection, 2AFC Yes/No） |
| 知觉维度 | 对比度检测（Contrast Detection） |
| 刺激类型 | Gabor 光栅（正弦光栅，空间频率 2 cpd，高斯包络 sigma=2°） |
| 上下规则 | 2-up 1-down（收敛于 ~70.7% 阈限） |
| 起始对比度 | 50% Michelson 对比度 |
| 步长序列 | 初始 0.1 log 单位，第 2 个 reversal 后缩小为 0.05 log 单位 |
| 停止条件 | 8 个 reversal / 最多 120 试次（安全上限） |
| 阈限计算 | 最后 6 个 reversal 的平均值（排除前 2 个 reversal） |
| 刺激持续时间 | 200 ms |
| 注视点持续时间 | 500 ms |
| 反应截止时间 | 3000 ms |
| 反应按键 | z（看到/是）, /（没看到/否） |

### Missing Information

1. ITI 持续时间未明确说明 → 假设 400–800 ms 随机均匀分布，需向用户确认具体范围
2. 是否需要在实验开始时呈现空白试次（catch trial，对比度=0）以估计虚报率 → 用户未提及，需确认。若包含 catch trial，其比例和 staircase 如何响应虚报反应需要定义
3. 是否需要试次级反馈 → 心理物理实验中通常不提供反馈以避免反应偏差，但有些设计在练习阶段或整个实验中使用反馈。需确认反馈策略

### Critical Assumptions

- 对比度以 log10 单位进行步长变化，阶梯在当前对比度水平上加减步长。对比度下界为 0.001（0.1%），上界为 1.0（100%）。当计算出的对比度超出边界时，钳制在边界值
- 注视点持续时间固定为 500 ms（非随机），ITI 随机范围为 400–800 ms，在条件生成时预先采样以确保可复现性
- 2-up 1-down 规则的实现逻辑：连续 2 个正确反应后对比度降低（难度增加），1 个错误反应后对比度升高（难度降低）。Reversal 定义为阶梯方向改变的点（从下降到上升或反之）。阈限计算排除前 2 个 reversal

### Code Architecture

```
staircase_contrast.py
├── 参数设置
│   ├── 阶梯参数：起始对比度（0.5）、步长序列（[0.1, 0.05]）、
│   │   上下规则（2-up 1-down）、最大 reversal（8）、最大试次（120）
│   ├── 时间参数：注视点（500 ms）、刺激（200 ms）、反应截止（3000 ms）、ITI（400-800 ms）
│   └── 刺激参数：空间频率（2 cpd）、高斯 sigma（2°）、Gabor 尺寸和相位
├── 窗口初始化（全屏或窗口，背景设为灰色以匹配平均亮度）
├── 刺激预加载
│   ├── TextStim：注视点 "+"
│   ├── GratingStim：Gabor 光栅（正弦光栅 + 高斯包络，对比度在试次中动态更新）
│   └── TextStim：指导语（"看到按z，没看到按/"）
├── 阶梯状态初始化
│   ├── current_level ← start_level（0.5）
│   ├── step_index ← 0（使用第一个步长 0.1）
│   ├── reversal_count ← 0
│   ├── direction ← "down"（初始方向为下降，连续正确后降低对比度）
│   ├── consecutive_correct ← 0（跟踪连续正确次数，用于 2-up 规则）
│   └── reversal_values ← []（记录每个 reversal 点的对比度值）
├── 试次循环：
│   ├── 注视点窗口（500 ms）
│   ├── 刺激窗口（200 ms，Gabor 光栅以 current_level 对比度呈现）
│   │   └── GratingStim.contrast ← current_level
│   ├── 反应窗口（deadline 3000 ms，监听 z 和 / 键）
│   │   ├── 记录 rt、key_resp
│   │   ├── 正确判断：刺激对比度 > 0 且按键 z → acc = 1
│   │   │   或刺激对比度 == 0（catch trial）且按键 / → acc = 1
│   │   └── 更新 staircase 状态（见下方 staircase 更新逻辑）
│   ├── ITI（400–800 ms 随机）
│   └── 检查停止条件（reversal_count >= 8 或 trial_count >= 120）
├── 阶梯更新逻辑（每个试次后）：
│   ├── 如果 acc == 1：
│   │   ├── consecutive_correct += 1
│   │   └── 如果 consecutive_correct >= 2（2-up 条件满足）：
│   │       ├── 如果 direction == "up" → reversal 发生，记录 reversal_values
│   │       ├── direction ← "down"
│   │       ├── current_level -= step_sizes[step_index]（降低对比度，变难）
│   │       └── consecutive_correct ← 0
│   ├── 如果 acc == 0：
│   │   ├── 如果 direction == "down" → reversal 发生，记录 reversal_values
│   │   ├── direction ← "up"
│   │   ├── current_level += step_sizes[step_index]（升高对比度，变容易）
│   │   ├── consecutive_correct ← 0
│   │   └── 如果 reversal_count >= 2 → step_index ← 1（切换到更小步长 0.05）
│   └── 钳制 current_level 到 [0.001, 1.0] 范围内
├── 阈限计算：取 reversal_values 中最后 6 个值的均值
├── 数据保存：CSV 格式，每条试次一行，包含 staircase 状态快照
└── 结果摘要：显示估计阈限值、总试次数、staircase 轨迹图
```

### Expected Data Columns

| Column | Type | Description |
|--------|------|-------------|
| trial_index | int | 试次序号（从 0 开始） |
| contrast_level | float | 当前试次的对比度水平（线性单位，0.001–1.0） |
| log10_contrast | float | 当前试次的对比度（log10 单位），便于与步长对接 |
| stimulus_onset | float | 刺激开始呈现时间（相对于试次开始，s） |
| rt | float | 反应时间（ms，从刺激 onset 算起） |
| key_resp | str | 被试实际按键（`"z"`、`"/"` 或 `None` 表示超时） |
| acc | int | 正确率（1 = 正确，0 = 错误或超时） |
| reversal_count | int | 截止当前试次已发生的 reversal 次数 |
| direction | str | 当前阶梯方向（`"up"` 或 `"down"`） |
| consecutive_correct | int | 当前连续正确反应次数（用于 2-up 规则判断） |
| step_size | float | 当前使用的步长（log 单位） |
| timeout | int | 是否超时（1 = 超时，0 = 在截止时间内做出反应） |
