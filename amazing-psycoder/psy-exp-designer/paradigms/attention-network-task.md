# Attention Network Task (ANT)

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/attention_network_task) · PsychoJS

## When to Use

User mentions: ANT, attention network test, alerting, orienting, executive control, Fan task, 注意网络任务. A combined cued reaction time and flanker task that measures three independent attentional networks — alerting, orienting, and executive control — within a single 30-minute session.

## Core Logic

Participants respond to the direction (left or right) of a central arrow target flanked by four other arrows. The flankers can be congruent (same direction as target), incongruent (opposite direction), or neutral (lines without directional information). Target onset is preceded by one of four cue conditions:

- **No cue**: No warning signal (baseline)
- **Center cue**: Fixation point changes briefly (provides temporal alerting but no spatial information)
- **Double cue**: Both possible target locations cued simultaneously (measures alerting — temporal warning without spatial information)
- **Spatial cue**: Valid cue at the exact target location (measures orienting — spatial attention benefit)

Each trial: cue (100 ms) → fixation (400 ms) → target + flankers (max 1700 ms or until response). Participants press left or right arrow key based on the central arrow direction, ignoring flankers. Stimuli are pre-rendered as PNG images (`congLeft.png`, `incongRight.png`, etc.) covering all cue-target-flanker combinations. The condition file (`cond.xlsx`) specifies which stimulus image to display and the correct key response per trial.

**Trial count**: Typically 288 trials total (3 blocks of 96). All combinations of cue type (4) and flanker type (3) are presented, balanced across blocks.

**Attentional network scores** are computed by subtracting reaction times between specific conditions:
- **Alerting effect** = RT(no cue) – RT(double cue). Larger positive values indicate stronger alerting.
- **Orienting effect** = RT(center cue) – RT(spatial cue). Larger positive values indicate stronger orienting.
- **Executive control effect** = RT(incongruent) – RT(congruent). Larger values indicate poorer conflict resolution.

## Must Confirm

- **Cue type design**: Full ANT (4 cue types: no cue, center, double, spatial) or simplified version?
- **Flanker types**: 3 levels (congruent, incongruent, neutral) or 2 (congruent, incongruent only)?
- **Trial count**: Standard 288 trials (3 blocks x 96) or custom?
- **Stimulus format**: Pre-rendered images or programmatically drawn arrows?
- **Response deadline**: Standard 1700 ms or custom?
- **Cue validity**: Spatial cues always valid (100%), or include invalid catch trials?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Cue                      │    │ Target + Flankers        │    │ ITI                      │
│ Content: + at center     │    │ Content: */**/spatial    │    │ Content: ←←←←← or →→→→→ │    │ Content: blank           │
│ Duration: variable       │    │ Duration: 100 ms         │    │ Duration: until key      │    │ Duration: variable        │
│ Response: none           │    │ Response: none           │    │ (deadline ~1700 ms)      │    │ Response: none           │
│ Condition: none          │    │ Condition: {cue_type}    │    │ Response: left/right key │    │ Condition: none          │
│ Data: none               │    │ Data: none               │    │ Condition: {flanker_type}│    │ Data: none               │
└──────────────────────────┘    └──────────────────────────┘    │ Data: rt, key, acc       │    └──────────────────────────┘
                                                                └──────────────────────────┘
```

## Data Analysis

Primary outcomes are the three network scores (alerting, orienting, executive control). Remove error trials and RT outliers (e.g., <200 ms or >3 SD). Analyze by computing mean RT for each condition and deriving the difference scores. Common findings: the three networks are largely independent; executive control deficits are associated with ADHD, schizophrenia, and aging.

## References

Fan, J., McCandliss, B. D., Sommer, T., Raz, A., & Posner, M. I. (2002). Testing the efficiency and independence of attentional networks. *Journal of Cognitive Neuroscience, 14*(3), 340–347. https://doi.org/10.1162/089892902317361886

## Do Not Assume

- Do not assume 4种线索类型全部使用 —— 部分简化版ANT仅保留2或3种线索类型（例如去掉双重线索或中性线索）。需确认用户的具体实验设计。
- Do not assume空间线索100%有效 —— 标准ANT中空间线索始终指向目标位置，但ANT-I变式引入无效线索试次，用于测量注意网络间的交互作用。需确认是否需要无效线索。
- Do not assume刺激必须使用预渲染PNG图片 —— PsychoPy可直接使用Polygon组件绘制箭头，或使用TextStim以Unicode箭头字符（← →）呈现刺激。预渲染图片方式需用户提供图片文件，编程绘制则需确认箭头尺寸、间距和颜色。
- Do not assume中性flanker必须是无方向线条 —— 部分实现以"---"线条作为中性条件，部分使用无箭头线段，部分版本完全不设中性条件（仅congruent和incongruent两种flanker类型）。
- Do not assume被试反应仅为左右箭头键 —— 部分实现使用键盘左右方向键，部分使用指定手指按键（如左手食指按F、右手食指按J）。需确认按键映射。
- Do not assume练习试次数为标准值 —— 标准ANT通常包含24个练习试次（1个block），但用户可能自定义练习次数或完全省略练习阶段。

## Condition File Columns

| Column | Type | Description |
|--------|------|-------------|
| cue_type | str | 线索类型：`"no_cue"`、`"center_cue"`、`"double_cue"`、`"spatial_cue"` |
| flanker_type | str | Flanker类型：`"congruent"`、`"incongruent"`、`"neutral"` |
| target_direction | str | 中央箭头的指向：`"left"` 或 `"right"` |
| correct_response | str | 正确按键：`"left"` 或 `"right"` |
| stimulus | str | 刺激图片文件名（如图片方式呈现），如 `"congLeft.png"` |

## Variants

- **ANT-I（Attention Network Test - Interaction）**：在标准ANT基础上引入无效空间线索试次，用于测量警觉网络与定向网络之间的交互作用。无效线索占比通常为17–25%，与flanker类型交叉平衡。参考 [eriksen-flanker.md](eriksen-flanker.md)。
- **Child ANT（儿童版ANT）**：将箭头刺激替换为彩色鱼图片（5条鱼排成一行，目标为中央鱼），鱼朝向左右代替箭头方向。线索由鱼出现前的气泡或水草动画替代，大幅降低认知负荷，适用于5–10岁儿童。
- **ANT-R（ANT-Revised）**：由Fan等人（2009）修订的优化版本，缩短了线索-目标间隔，调整了试次比例以平衡三个网络的信噪比。总试次数减少至144试次，更适合fMRI等神经影像实验。

## Example

### User Request

> "我要做一个注意网络测试（ANT）实验。屏幕中央始终显示注视点'+'。每个试次开始时先呈现线索：无线索（注视点不变）、中央线索（注视点变粗）、双重线索（上方和下方同时变粗）或空间线索（仅目标出现位置变粗）。线索持续100ms，之后注视点恢复400ms，然后在注视点上方或下方呈现5个水平排列的箭头，中央箭头向左或向右，两侧箭头与中央一致、相反或无方向线段。被试任务是在1700ms内按左或右键判断中央箭头方向。共3个block，每个block 96试次。用PsychoPy实现。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Cue                      │    │ Target + Flankers        │    │ ITI                      │
│ Content: +               │    │ Content: * / ** / spatial │    │ Content: ←←←←← or →→→→→ │    │ Content: blank          │
│ Duration: variable       │    │ Duration: 100 ms          │    │ Duration: until key      │    │ Duration: variable       │
│ (400-1600 ms random)     │    │ Response: none            │    │ (deadline 1700 ms)       │    │ (随机)                   │
│ Response: none           │    │ Condition: {cue_type}     │    │ Response: left/right key │    │ Response: none           │
│ Condition: none          │    │ Data: none                │    │ Condition: {flanker_type}│    │ Condition: none          │
│ Data: none               │    └──────────────────────────┘    │ Data: rt, key, acc       │    │ Data: none               │
└──────────────────────────┘                                    └──────────────────────────┘    └──────────────────────────┘
```

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| 实验名称 | Attention Network Task (ANT) |
| 平台 | PsychoPy |
| 任务类型 | 线索化flanker任务（注意网络测量） |
| 线索类型 | no_cue, center_cue, double_cue, spatial_cue |
| Flanker类型 | congruent, incongruent, neutral |
| 线索持续时间 | 100 ms |
| 线索-目标间隔 | 400 ms |
| 反应截止时间 | 1700 ms |
| Block数 | 3 blocks |
| 每Block试次数 | 96 trials |
| 总试次数 | 288 trials |
| 注视点-线索间隔 | 400-1600 ms 随机 |
| ITI | 未指定（待确认） |

### Missing Information

1. ITI时长未说明 → 将询问（固定还是随机范围？标准ANT的ITI通常为随机变化）
2. 是否包含练习阶段？标准ANT通常包含24个练习试次，但用户未提及 → 将询问
3. 箭头的具体尺寸、间距和视觉参数未说明 → 如使用Polygon绘制，需确认箭头大小、线宽、排列间距

### Critical Assumptions

- 空间线索100%有效（指向目标出现的实际位置），不包含无效线索试次
- 刺激使用PsychoPy Polygon组件编程绘制（无需预渲染PNG图片）
- 反应键为键盘左右方向键（Left / Right arrow keys）
- ITI默认随机400-1600 ms（与注视点持续时间范围一致，参照标准ANT）
- 注视点-线索间隔（cue前）默认随机400-1600 ms

### Code Architecture

```
ant.py
├── 参数配置（线索类型、flanker类型、持续时间、试次数、按键映射）
├── 窗口设置（全屏/窗口，背景色，单位）
├── 刺激组件预创建
│   ├── 注视点（TextStim: "+"）
│   ├── 线索刺激（TextStim: "*" 用于中央/双重/空间线索的各个位置）
│   ├── 箭头刺激（Polygon: 向左/向右箭头）+ 中性线段（Line）
│   └── 反馈文本（TextStim: 仅在练习阶段使用）
├── 条件文件生成（所有 cue_type × flanker_type × target_direction 组合，跨block平衡）
├── 实验阶段
│   ├── 指导语
│   ├── 练习阶段（24试次，含反馈）
│   └── 正式阶段（3 blocks × 96 trials）
├── 试次循环:
│   ├── 注视点（随机400-1600 ms）
│   ├── 线索（100 ms）
│   ├── 线索-目标间隔（400 ms，注视点恢复）
│   ├── 目标+flanker呈现（最大1700 ms或直到反应）
│   ├── 反馈（练习阶段：正确/错误/超时）
│   └── ITI（随机）
├── 数据保存：try/finally + CSV逐行写入
├── 退出控制：Escape键检查
└── 注意网络分数计算（实验结束后输出alerting/orienting/executive_control分数）
```

### Expected Data Columns

| Column | Type | Description |
|--------|------|-------------|
| cue_type | str | 线索类型：no_cue / center_cue / double_cue / spatial_cue |
| flanker_type | str | Flanker类型：congruent / incongruent / neutral |
| target_direction | str | 中央箭头指向：left / right |
| correct_response | str | 正确按键：left / right |
| rt | float | 反应时间（ms） |
| acc | int | 正确性：1=正确，0=错误 |
| alerting_score | float | 警觉网络分数：RT(no_cue) - RT(double_cue) |
| orienting_score | float | 定向网络分数：RT(center_cue) - RT(spatial_cue) |
| executive_control_score | float | 执行控制分数：RT(incongruent) - RT(congruent) |
