# Children Flanker Task

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/children_flanker_task) · PsychoJS

## When to Use

User mentions: Children flanker, child flanker, fish flanker, kids attention task, 儿童侧翼任务, 儿童注意任务. A child-friendly adaptation of the Eriksen flanker paradigm using fish images instead of abstract arrows, designed for developmental populations and pediatric research.

## Core Logic

This is a flanker task adapted for children. Instead of arrows or letters, participants see a row of five fish. The central fish is the target; the four flanking fish (two on each side) point either in the same direction (congruent) or opposite direction (incongruent). The child presses the left or right arrow key to indicate the direction of the middle fish only, ignoring the flanking fish.

**Child-friendly design features**:
- Fish images (`leftFish.png`, `rightFish.png`) replace abstract arrow stimuli, making the task intuitive for young children
- A colorful, engaging background replaces neutral grey/black
- A progress counter (e.g., "Fish 12 / 48") is displayed throughout to maintain motivation
- Transparent spacer images (`transparent.png`) maintain consistent horizontal spacing even when fish are not present

**Trial structure**: fixation → five-fish display (center target + four flankers) → keypress response (left/right arrow) → ITI. The condition file (`conditions.csv`) defines each trial's target direction, flanker direction, and correct answer (`corrAns`).

**Two-phase design**:
1. **Practice block**: Trials with trial-level feedback (correct/incorrect text shown after each response). An instruction screen precedes practice.
2. **Main experimental block**: Trials without feedback. A gap/routine screen separates practice from the main phase.

**The Flanker effect**: Incongruent trials (target left, flankers right, or vice versa) yield slower and less accurate responses than congruent trials (all fish pointing the same direction). The flanker interference effect (incongruent RT – congruent RT) indexes selective attention and inhibitory control in children.

## Must Confirm

- **Age range**: What ages? (influences instruction wording, trial count, and response deadline)
- **Stimuli**: Fish images, animal images, or other child-friendly stimuli?
- **Trial count**: How many practice trials? How many experimental trials? (fewer for younger children)
- **Congruency ratio**: 50:50 congruent:incongruent, or include neutral condition?
- **Response deadline**: Child-friendly deadline (e.g., 3000 ms) or no deadline?
- **Feedback**: Practice-only feedback, or feedback throughout? Verbal encouragement between blocks?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Fish Stimuli             │    │ Feedback (practice only) │    │ ITI                      │
│ Content: + at center     │    │ Content: 5 fish in row   │    │ Content: correct/incorrect│   │ Content: blank           │
│ Duration: 500 ms         │    │ ←←←←← or ←←→←←           │    │ + progress counter       │    │ Duration: 500-1000 ms    │
│ Response: none           │    │ Duration: until key      │    │ Duration: 500 ms         │    │ Response: none           │
│ Condition: none          │    │ (deadline ~3000 ms)      │    │ Response: none           │    │ Condition: none          │
│ Data: none               │    │ Response: left/right key │    │ Condition: none          │    │ Data: none               │
└──────────────────────────┘    │ Condition: {congruency}  │    │ Data: none               │    └──────────────────────────┘
                                │ Data: rt, key, acc       │    └──────────────────────────┘
                                │   trial_counter          │
                                └──────────────────────────┘
```

## Data Analysis

Compute flanker interference scores for RT (incongruent RT – congruent RT) and accuracy. Children typically show larger interference effects than adults, reflecting developing inhibitory control. Analyze age-related changes in the flanker effect. Error trials and post-error trials are important for understanding response monitoring development. Compare to adult flanker norms to assess developmental trajectories.

## References

Eriksen, B. A., & Eriksen, C. W. (1974). Effects of noise letters upon the identification of a target letter in a nonsearch task. *Perception & Psychophysics, 16*(1), 143–149. https://doi.org/10.3758/BF03203267

Rueda, M. R., Fan, J., McCandliss, B. D., Halparin, J. D., Gruber, D. B., Lercari, L. P., & Posner, M. I. (2004). Development of attentional networks in childhood. *Neuropsychologia, 42*(8), 1029–1040. https://doi.org/10.1016/j.neuropsychologia.2003.12.012

## 不要假设

- 不要假设刺激一定是鱼类图片 —— 儿童版Flanker可能使用箭头、动物或其他儿童友好刺激，需明确确认具体图片素材（leftFish.png / rightFish.png 或其他）
- 不要假设一致与不一致试次比例为50:50 —— 需明确确认比例，部分研究可能包含中性条件（如鱼朝上/朝下），影响条件文件生成逻辑
- 不要假设反应键一定是键盘左右箭头 —— 对于更小年龄的儿童（3-4岁），可能使用左右两侧的大按钮、触摸屏或游戏手柄
- 不要假设练习阶段一定有反馈 —— 需确认反馈策略：仅练习反馈（标准做法）、全程反馈、或无反馈（部分研究有意省略以避免反馈干扰）
- 不要假设儿童版无反应截止时间 —— 儿童版通常设置较长的截止时间（如3000 ms），但需确认具体数值，无截止可能导致试次过长
- 不要假设两阶段设计（练习+正式）一定适用 —— 部分实验可能包含多个正式block、中间休息提示、或"游戏化"过渡界面

## 条件文件列

条件文件（csv/xlsx）中驱动每个试次所需的列：

| 列名 | 类型 | 描述 |
|------|------|------|
| congruency | str | `"congruent"` 或 `"incongruent"`，目标鱼与侧翼鱼方向是否一致 |
| target_dir | str | `"left"` 或 `"right"`，中间目标鱼的方向 |
| corrAns | str | `"left"` 或 `"right"`，正确按键答案（与target_dir相同） |

## 变体

- **标准箭头Flanker**：使用箭头（←←←←← 或 ←←→←←）作为刺激的原始Eriksen范式，适用于成人及青少年被试。反应截止时间较短（1000-1500 ms），无儿童友好设计元素。参见 [eriksen-flanker.md](eriksen-flanker.md)
- **鱼类Flanker（儿童版）**：使用鱼类图片替代箭头，配合彩色背景和进度计数器，适用于3-8岁儿童。即本文档所述版本。反应截止时间较长（~3000 ms），包含试次进度显示以维持儿童动机
- **情绪Flanker**：使用情绪面孔或情绪词汇作为侧翼干扰刺激，测量情绪信息对注意控制的干扰效应。常见于发展心理学和临床研究中评估情绪调节与认知控制的交互

---

## 示例

### 用户请求

> "我要做一个儿童Flanker任务，被试是5-7岁儿童。屏幕中央呈现一排5条鱼，中间那条是目标鱼，孩子需要判断中间鱼朝向并按对应方向键。两侧鱼方向可能与中间一致或不一致。先20个练习trial带反馈，再3个正式block各40个trial。注视点500ms，刺激呈现直到按键（最长3000ms），ITI随机800-1200ms。用PsychoPy。"

### 试次窗口时间线

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ 窗口1                     │ →  │ 窗口2                     │ →  │ 窗口3                     │ →  │ 窗口4                     │
│ 注视点                    │    │ 鱼类刺激                  │    │ 反馈（仅练习阶段）          │    │ ITI                      │
│ 内容: +                  │    │ 内容: 5条鱼一排           │    │ 内容: 正确/错误 + 进度     │    │ 内容: 空白               │
│ 时长: 500 ms             │    │ 时长: 直到按键            │    │ 时长: 500 ms              │    │ 时长: 800-1200 ms         │
│ 反应: 无                 │    │ (截止 3000 ms)            │    │ 反应: 无                  │    │ 反应: 无                 │
│ 条件: 无                 │    │ 反应: 左/右键             │    │ 条件: 无                  │    │ 条件: 无                 │
│ 数据: 无                 │    │ 条件: {congruency}        │    │ 数据: 无                  │    │ 数据: 无                 │
└──────────────────────────┘    │ 数据: rt, key, acc,       │    └──────────────────────────┘    └──────────────────────────┘
                                │       trial_counter        │
                                └──────────────────────────┘
```

| 窗口 | 内容 | 时长 | 反应 | 条件 | 数据 |
|------|------|------|------|------|------|
| 注视点 | + | 500 ms | 无 | 无 | 无 |
| 鱼类刺激 | 5条鱼（←←←←← 或 ←←→←←） | 直到按键（截止 3000 ms） | 左/右键 | {congruency} | rt, key, acc, trial_counter |
| 反馈（仅练习） | 正确/错误文字 + 进度计数 | 500 ms | 无 | 无 | 无 |
| ITI | 空白 | 800-1200 ms 随机 | 无 | 无 | 无 |

### 解析的实验规范

| 字段 | 值 |
|------|-----|
| 实验名称 | 儿童鱼类Flanker任务 |
| 平台 | PsychoPy |
| 任务类型 | Flanker任务（选择性注意 / 抑制控制） |
| 刺激类型 | 鱼类图片（leftFish.png, rightFish.png） |
| 一致条件 | 目标鱼与侧翼鱼方向相同（←←←←←） |
| 不一致条件 | 目标鱼与侧翼鱼方向相反（←←→←←） |
| 练习试次 | 20（带试次级反馈） |
| 正式试次 | 3个block × 40试次 = 120 |
| 一致/不一致比例 | 50:50（各60个正式试次） |
| 注视点时长 | 500 ms |
| 反应截止时间 | 3000 ms |
| ITI | 800-1200 ms 随机 |
| 阶段顺序 | 指导语 → 练习(20) → 休息提示 → 正式Block1-3(各40) |

### 缺失信息

1. 一致/不一致试次的具体比例未明确 —— 假设50:50，需向用户确认
2. 鱼类图片素材来源未说明 —— 需确认使用默认素材还是用户自定义图片
3. 练习与正式阶段之间的过渡界面未提及 —— 需确认是否有休息提示或鼓励语

### 关键假设

- 一致与不一致试次比例为50:50，不超过2个连续不一致试次
- 练习阶段使用试次级反馈（正确/错误文字 + 进度计数），正式阶段无反馈
- 鱼类图片使用默认素材（leftFish.png, rightFish.png），背景使用彩色自然主题背景

### 代码架构

```
children_flanker.py
├── 参数设置（反应键、截止时间、比例、时长、试次计数）
├── 窗口设置（全屏/窗口、背景色/图片）
├── 刺激预加载（leftFish.png, rightFish.png, 注视点, 反馈文本, 进度文本）
├── 生成条件表（一致:不一致 = 50:50，随机排列，每个block独立）
├── 指导语界面（儿童友好措辞 + 图示）
├── 练习循环（20试次）：
│   ├── 注视点（500 ms）
│   ├── 鱼类刺激（5条鱼，直到按键或3000 ms截止）
│   ├── 反馈（正确/错误 + 进度计数，500 ms）
│   └── ITI（800-1200 ms 随机）
├── 休息/过渡界面
├── 正式block循环（3 × 40试次）：
│   ├── 注视点（500 ms）
│   ├── 鱼类刺激（5条鱼，直到按键或3000 ms截止）
│   └── ITI（800-1200 ms 随机）
├── 数据保存：try/finally 增量写入CSV
└── 结束界面（感谢语 + 完成提示）
```

### 预期数据列

| 列名 | 类型 | 描述 |
|------|------|------|
| congruency | str | `"congruent"` 或 `"incongruent"` |
| target_dir | str | `"left"` 或 `"right"`，目标鱼方向 |
| rt | float | 反应时（毫秒），从刺激呈现到按键 |
| acc | int | 正确为1，错误为0 |
| trial_counter | int | 当前试次计数编号 |
| block_type | str | `"practice"` 或 `"formal"` |
| block_num | int | Block编号（练习=0，正式=1/2/3） |
