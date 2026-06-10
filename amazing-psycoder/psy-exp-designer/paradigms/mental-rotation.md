# Mental Rotation Task

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/mental_rotation) · PsychoJS

## When to Use

User mentions: Mental rotation, spatial cognition, visuospatial processing, 心理旋转, 空间认知. Measures the ability to mentally rotate two-dimensional or three-dimensional objects, a classic paradigm in spatial cognition research.

## Core Logic

Participants view two stimuli presented side by side and must judge whether they are the same (identical) or different (mirror images). One stimulus is rotated relative to the other by varying angular disparities (e.g., 0, 45, 90, 135, 180 degrees). The key finding is that reaction time increases approximately linearly with the angle of rotation, suggesting analog mental transformation.

**This implementation** uses letter-like shapes (e.g., 'F') presented at various orientations — a simplified version of Shepard & Metzler's (1971) classic 3D block-figure paradigm. The left stimulus shows the original letter; the right stimulus shows either the same letter (rotated) or its mirror-reversed version (also rotated). Participants press 's' for same (identical) and 'd' for different (mirror image).

**Condition file** (`MentalRot.csv`): Specifies rotation angle, which image file to display for the left and right positions (`F.png` and `FR.png` for mirror image), and the correct answer. The `TrialHandler` iterates over this file with random or sequential order.

**Trial structure**: Two instruction screens → fixation → stimulus pair (left + right images, until response) → optional feedback → ITI.

**Rotation angle manipulation**: The condition file systematically varies angular disparity. The classic finding is a linear RT increase from 0 to 180 degrees, with a symmetrical decrease from 180 to 360 degrees, producing a peak at 180 degrees.

## Must Confirm

- **Stimulus type**: Letter-like shapes (F, R, G), 3D block figures (Shepard-Metzler style), or abstract polygons?
- **Response mapping**: 's'/'d' for same/different, or arrow keys for left/right judgment, or different mapping?
- **Rotation angles**: Which angular disparities? (typically 0, 45, 90, 135, 180 degrees, in both clockwise and counterclockwise directions)
- **Mirror stimuli**: Is the "different" condition always a mirror image, or can it be a different letter entirely?
- **Trial count**: How many trials per angle? How many repetitions?
- **Practice**: Practice block with feedback before formal trials?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Stimulus Pair            │    │ Feedback (optional)      │    │ ITI                      │
│ Content: + at center     │    │ Content: F (left)        │    │ Content: correct/incorrect│   │ Content: blank           │
│ Duration: 500 ms         │    │   rotated F/R (right)    │    │ Duration: 500 ms         │    │ Duration: 500-1000 ms    │
│ Response: none           │    │ Duration: until key      │    │ Response: none           │    │ Response: none           │
│ Condition: none          │    │ Response: s=same, d=diff │    │ Condition: none          │    │ Condition: none          │
│ Data: none               │    │ Condition: {angle, pair} │    │ Data: none               │    │ Data: none               │
└──────────────────────────┘    │ Data: rt, key, acc       │    └──────────────────────────┘    └──────────────────────────┘
                                └──────────────────────────┘
```

## Data Analysis

Plot mean RT as a function of rotation angle (expect a peak-shaped function, linear increase peaking at 180 degrees, then decreasing back toward 0/360). Compute the mental rotation slope (ms/degree) via linear regression on same-pair trials. Compare slopes and intercepts between groups (e.g., sex differences — males typically show faster rotation speed). Also analyze accuracy, which tends to decrease at larger angular disparities.

## References

Shepard, R. N., & Metzler, J. (1971). Mental rotation of three-dimensional objects. *Science, 171*(3972), 701–703. https://doi.org/10.1126/science.171.3972.701

Gray, J. R., & Pasmanter, N. R. (2013). Mental rotation demo. Michigan State University.

## Do Not Assume

- Do not assume the "different" condition always uses mirror-reversed images — in some designs, "different" means a completely different character (e.g., F vs G), not a mirror image of the same letter
- Do not assume rotation angles are symmetric (0-360 in both directions) — some experiments only use 0-180 degrees in one direction, or a subset of angles (e.g., only 0, 60, 120, 180)
- Do not assume same/different response mapping ('s'/'d') — some variants use left/right arrow keys, or ask participants to judge whether the rotated stimulus matches a standard orientation target
- Do not assume the stimuli are 2D letter shapes — the Shepard-Metzler classical paradigm uses 3D block figures rendered at various depth rotations, which differ substantially in visual complexity and cognitive processing
- Do not assume feedback is always shown — in formal blocks, feedback is often omitted to avoid learning effects or speed-accuracy trade-off confounds
- Do not assume identical trial counts across angles — some designs oversample larger angular disparities where errors are more frequent, to ensure sufficient data for psychometric fitting

## Condition File Columns

Columns in the xlsx/csv file that drives each trial:

| Column | Type | Description |
|--------|------|-------------|
| angle | int | 旋转角度（度数），如 0, 45, 90, 135, 180 |
| left_stim | str | 左侧刺激图片文件名，如 `F.png` |
| right_stim | str | 右侧刺激图片文件名，如 `F.png`（相同）或 `FR.png`（镜像） |
| correct_resp | str | 正确反应键，`'s'` 表示相同，`'d'` 表示不同 |
| condition | str | 条件类型：`"same"` 或 `"different"`（或 `"mirror"`） |

## Variants

- **Shepard-Metzler 经典 3D 版**：使用由多个立方体组成的三维图形，刺激对在三维空间中旋转。参与者判断两个图形是否可以通过旋转重合（相同物体）或互为镜像（不同物体）。这是认知心理学中最经典的心理旋转范式，视觉复杂度高，对空间想象能力要求更强。如需实现此版本，需准备 3D 渲染后的多角度图像集。
- **字母/字符旋转版（2D 符号）**：使用字母（F、G、R）或抽象符号，一侧为原始或旋转后的图形，另一侧为旋转后的图形或镜像版本。刺激简单、便于标准化，广泛用于在线实验和临床评估。本文件主要覆盖此版本。
- **手部/身体旋转版**：呈现人手（或脚部）的图片，参与者需判断图片中是左手还是右手（或左脚/右脚）。此类任务激活运动想象与身体图式脑区，涉及具身认知过程，与经典物体心理旋转的认知机制存在差异。如需参考反应时分析逻辑，参见 [go-nogo.md](go-nogo.md) 的数据分析部分。

## Example

### User Request

> "我要做一个心理旋转实验。屏幕中央左右两侧同时呈现两个字母'F'的图片。左侧始终是正常朝向的F，右侧是经过旋转的F（可能是原始图形或镜像图形）。参与者需要判断两个图形是否完全相同（忽略旋转）。相同按's'键，不同（镜像）按'd'键。旋转角度包括0, 45, 90, 135, 180度（顺时针和逆时针各一套）。共6个block，每block 48个试次。试次开始前呈现注视点500ms，刺激呈现最长3000ms或直到按键。ITI随机600-1000ms。实验开始前有10个练习试次（含反馈）。用PsychoPy。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Stimulus Pair            │    │ Feedback (练习仅)        │    │ ITI                      │
│ Content: +               │    │ Content: F (左)          │    │ Content: 正确/错误       │    │ Content: 空白            │
│ Duration: 500 ms         │    │   rotated F/FR (右)      │    │ Duration: 800 ms         │    │ Duration: 600-1000 ms    │
│ Response: none           │    │ Duration: max 3000 ms    │    │ Response: none           │    │ Response: none           │
│ Condition: none          │    │ Response: s=same, d=diff │    │ Condition: none          │    │ Condition: none          │
│ Data: none               │    │ Condition: {angle, cond.}│    │ Data: none               │    │ Data: none               │
└──────────────────────────┘    │ Data: rt, key, acc       │    └──────────────────────────┘    └──────────────────────────┘
                               └──────────────────────────┘
```

| Window | Content | Duration | Response | Condition | Data |
|--------|---------|----------|----------|-----------|------|
| Fixation | + | 500 ms | none | none | none |
| Stimulus Pair | F（左）+ 旋转F/FR（右） | max 3000 ms（直到按键） | s（相同）/ d（不同） | {angle, left_stim, right_stim, correct_resp, condition} | rt, key, acc |
| Feedback | 正确/错误（仅练习） | 800 ms | none | none | none |
| ITI | 空白 | 600-1000 ms 随机 | none | none | none |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| 实验名称 | 字母心理旋转任务 |
| 平台 | PsychoPy |
| 任务类型 | Mental Rotation（心理旋转） |
| 刺激类型 | 字母 F（正常朝向与镜像版本） |
| 旋转角度 | 0, 45, 90, 135, 180 度（顺/逆时针） |
| 反应映射 | s = 相同，d = 不同 |
| 刺激呈现时长 | 最长 3000 ms（按键终止） |
| 试次结构 | 注视点(500ms) → 刺激对(≤3000ms) → 反馈(仅练习) → ITI(600-1000ms) |
| 试次数 | 6 blocks × 48 trials = 288 正式试次 + 10 练习 |
| 反馈 | 仅练习阶段 |

### Missing Information

1. Block间休息未说明 — 假设每个 block 结束后呈现休息界面，用户自行按键继续
2. 指导语未提供 — 需确认指导语内容和呈现方式（文字 + 示意图提示？）
3. 刺激图片未提供 — 需确认角度图片文件已准备（F 的 0°/45°/90°/135°/180° 版本及其镜像对应版本共 20 张图片）

### Critical Assumptions

- 左侧刺激始终为正常朝向的 F（0°），右侧为旋转后的 F 或镜像 F。若左侧也需要旋转，则需额外确认角度配置
- 顺/逆时针各一套角度意味着每个角度有两个方向的试次（如 45° 顺时针和 45° 逆时针），条件排列需在条件文件中预先指定朝向标记
- 反应时超过 3000ms 视为超时（无反应），记为缺失值（accuracy=0, rt=NaN）

### Code Architecture

```
mental_rotation.py
├── 参数配置（angles, response_keys, timing, n_blocks）
├── 窗口与显示器设置（全屏/窗口）
├── 刺激预加载（ImageStim 对象，按角度和类型载入）
├── 条件文件读取（MentalRot.csv，含 angle, left_stim, right_stim, correct_resp, condition）
├── 试次循环：
│   ├── 注视点（500 ms — TextStim "+"）
│   ├── 刺激对呈现（max 3000 ms — 左侧 + 右侧 ImageStim）
│   ├── 反应收集（Keyboard，keys=["s", "d", "escape"]）
│   ├── 反馈（仅练习 — 800 ms 文字反馈）
│   └── ITI（600-1000 ms 随机 — 空白屏幕）
├── Block间休息（用户按键继续）
├── 数据保存：try/finally 逐行写入 CSV
```

### Expected Data Columns

| Column | Type | Description |
|--------|------|-------------|
| angle | int | 旋转角度（度数） |
| condition | str | `"same"` 或 `"different"` |
| left_stim | str | 左侧刺激文件名 |
| right_stim | str | 右侧刺激文件名 |
| correct_resp | str | 正确反应键 |
| rt | float | 反应时（秒） |
| key_resp | str | 实际按键 |
| acc | int | 正确性（1=正确，0=错误） |
| block | int | Block 编号 |
| trial | int | Block内试次编号 |
