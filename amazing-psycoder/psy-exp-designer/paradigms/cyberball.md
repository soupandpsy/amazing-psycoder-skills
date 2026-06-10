# Cyberball (Social Exclusion Paradigm)

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/cyberball) · reference

## When to Use

User mentions: Cyberball, ostracism, social exclusion, social rejection, 赛博球, 社会排斥. A virtual ball-tossing game used to experimentally induce feelings of social inclusion or exclusion (ostracism).

## Core Logic

Participants are told they are playing an online ball-tossing game with two or three other participants (actually computer-controlled confederates). The game appears as a simple interface showing player icons. When a participant receives the ball, they click on one of the other players to throw the ball to them. Unbeknownst to the participant, the computer players follow a predetermined script dictating how often they toss the ball to the participant.

In the inclusion condition, the participant receives the ball roughly one-third of the time (equal participation). In the exclusion (ostracism) condition, the participant initially receives the ball a few times but is then excluded from play — the computer players toss the ball only among themselves. The paradigm is powerful: even brief (2-5 minute) exclusion reliably induces feelings of distress, lowered belonging, reduced self-esteem, reduced sense of meaningful existence, and reduced perceived control.

Typical design: 30-60 total throws, with the participant receiving 2-4 initial throws in the exclusion condition then none thereafter. Post-experiment, participants complete the Need-Threat Scale (assessing belonging, self-esteem, meaningful existence, and control) and a mood questionnaire. The Cyberball effect is remarkably robust — participants report distress even when told the other players are computer-controlled or from a despised outgroup.

## Must Confirm

- **Condition**: Inclusion, exclusion, or both? What percentage of throws does the participant receive in each condition?
- **Number of players**: 2 virtual players (total 3 including participant) or 3 virtual players?
- **Total throws**: How many total ball tosses? (typically 30-60)
- **Participant throw mechanism**: Mouse click on player icons, or keyboard selection?
- **Ball animation**: Animated ball movement between players, or instantaneous teleport?
- **Cover story**: Is the participant told they are playing with real people over the internet, or with a computer program?
- **Post-game measures**: Which questionnaires follow the game (Need-Threat Scale, mood, manipulation check)?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────────────────┐
│ Participant's Turn        │    │ Other Player's Turn (passive)        │
│ (ball_to == "choose")     │    │ (ball_to != "choose")                │
│                           │    │                                      │
│ Content: 3 player icons   │    │ Content: 3 player icons + ball at   │
│ + ball at participant     │    │ thrower position                     │
│ Duration: until click     │    │ Duration: 1 s (observation)          │
│ Response: click target    │    │ Response: none                       │
│ Data: chosen_player, RT   │    │ Data: ball_from, ball_to             │
├───────────────────────────┤    ├──────────────────────────────────────┤
│            ↓              │    │            ↓                         │
└───────────────────────────┘    └──────────────────────────────────────┘
                 ↓                              ↓
┌──────────────────────────────────────────────────────────────────────┐
│ Ball Animation (both trial types)                                     │
│ Content: 3 player icons + ball moving from start to end position      │
│ Duration: 3 s (linear interpolation per frame)                        │
│ Display: "You threw to Player X" or "Player X threw to Player Y"     │
│ Response: none                                                        │
│ Data: none                                                            │
└──────────────────────────────────────────────────────────────────────┘
```

## Data Analysis

Primary analyses compare inclusion vs. exclusion conditions on the Need-Threat Scale subscales and mood measures. Manipulation checks: perceived percentage of throws received, feelings of being ignored/excluded. Behavioral analyses (throw latency, choice of recipient) are secondary. Individual difference moderators (rejection sensitivity, social anxiety, attachment style) are often examined.

## References

Williams, K. D., Cheung, C. K. T., & Choi, W. (2000). Cyberostracism: Effects of being ignored over the Internet. *Journal of Personality and Social Psychology, 79*(5), 748–762. https://doi.org/10.1037/0022-3514.79.5.748

Williams, K. D., & Jarvis, B. (2006). Cyberball: A program for use in research on interpersonal ostracism and acceptance. *Behavior Research Methods, 38*(1), 174–180. https://doi.org/10.3758/BF03192765

## Do Not Assume

- Do not assume inclusion/exclusion 条件仅通过被试接球次数来区分。确认具体比例分布：包容条件下被试接球比例约为1/3（等量参与），排斥条件下被试仅在最初几次接到球（通常2-4次），之后完全不再接到球。
- Do not assume 虚拟玩家数量固定为2个。常见配置为2个虚拟玩家（总计3人）或3个虚拟玩家（总计4人），不同配置会影响排斥强度和生态效度。
- Do not assume 传球动画是瞬间完成的。有的实现使用线性插值动画（2-3秒），有的则使用瞬时"闪现"传球，动画方式和时长需明确确认。
- Do not assume 被试通过键盘选择传球目标。常见实现为鼠标点击玩家图标，也可能使用键盘数字键（1、2、3对应玩家），输入方式影响反应时数据的采集方式。
- Do not assume 实验后问卷可省略。Need-Threat Scale（归属感、自尊、意义性存在、控制感四个分量表）和心情问卷是Cyberball范式的标准组成部分，缺失则难以评估排斥操纵的有效性。
- Do not assume 指导语中称"与真实玩家对战"是默认选项。有研究明确告知被试对手为计算机程序，但排斥效应仍然显著；指导语的覆盖故事直接影响实验伦理和事后解释（debriefing）流程。

## Condition File Columns

| Column | Type | Description |
|--------|------|-------------|
| condition | str | `"inclusion"` 或 `"exclusion"`，决定被试接球的比例分布 |
| total_throws | int | 总传球次数（通常30-60次） |
| participant_throws | int | 被试在整个游戏中接到球的次数 |
| throw_sequence | str | 传球顺序的预定义脚本（JSON数组或逗号分隔的列表），指定每一轮哪个玩家传球给哪个玩家 |

## Variants

- **标准 Cyberball（3人版）**：2个虚拟玩家 + 1个被试，共3人参与。总传球次数通常为30-60次，包含包容和排斥两种条件。这是最经典的版本（Williams et al., 2000），效应量最稳定。相关范式参考：[ultimatum-game.md](ultimatum-game.md)（社会决策范式）。
- **Cyberball 4人版**：3个虚拟玩家 + 1个被试，共4人参与。增加一个虚拟玩家可操纵群体排斥（集体排斥 vs. 部分排斥），用于研究群体认同和排斥的交互效应。也可设置两个虚拟玩家排斥被试、另一个不排斥的条件。
- **fMRI 版 Cyberball**：适配功能磁共振成像环境，通常在block设计中将包容block和排斥block交替呈现，增加jitter time（2-8秒随机间隔）。用于研究社会排斥相关的神经激活区域，特别是前扣带皮层（ACC）和前脑岛的活动（Eisenberger et al., 2003）。相关范式参考：[dot-probe.md](dot-probe.md)（社会认知偏向范式）。

## Example

### User Request

> "我要做一个Cyberball社会排斥实验，使用PsychoPy。3个玩家（被试+2个虚拟玩家），总共30次传球。排斥条件下，被试只在第2、5次传球时接到球，之后再也接不到球。包容条件下，被试接到10次球（均匀分布在整个游戏中）。被试通过鼠标点击另外两个玩家的头像来传球。球需要有移动动画（2秒动画）。实验前有指导语，告诉被试他们正在和另外两个在线参与者一起玩一个心理想象训练游戏。实验后包含12题的Need-Threat Scale和4题的心情问卷（7点Likert量表）。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────────────────┐
│ 被试传球回合              │    │ 虚拟玩家传球回合（被动观察）          │
│ (ball_to == "choose")     │    │ (ball_to != "choose")                │
│                           │    │                                      │
│ 内容: 3个玩家图标         │    │ 内容: 3个玩家图标 + 球在传球者位置   │
│ + 球在被试位置            │    │                                      │
│ 时长: 直到点击 (无限制)   │    │ 时长: 1 秒（观察窗口）               │
│ 响应: 鼠标点击目标玩家    │    │ 响应: 无                              │
│ 显示文本: "该你了！"      │    │ 显示文本: "Player X 正在传球..."     │
│ 数据: chosen_player, RT   │    │ 数据: ball_from, ball_to              │
├───────────────────────────┤    ├──────────────────────────────────────┤
│            ↓              │    │            ↓                         │
└───────────────────────────┘    └──────────────────────────────────────┘
                 ↓                              ↓
┌──────────────────────────────────────────────────────────────────────┐
│ 传球动画（两种回合共用）                                              │
│ 内容: 3个玩家图标 + 球从起点到终点线性移动                            │
│ 时长: 2 秒（每秒60帧线性插值）                                        │
│ 显示文本: "你传给了 Player X" 或 "Player X 传给了 Player Y"          │
│ 响应: 无                                                              │
│ 数据: 无                                                              │
└──────────────────────────────────────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────────────────────────────────────┐
│ 试次间间隔（ITI）                                                     │
│ 内容: 3个玩家图标（静止）                                            │
│ 时长: 500 ms                                                          │
│ 响应: 无                                                              │
│ 数据: 无                                                              │
└──────────────────────────────────────────────────────────────────────┘
```

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| 实验名称 | Cyberball 社会排斥实验 |
| 平台 | PsychoPy |
| 范式类型 | Cyberball（社会排斥/社会接纳） |
| 玩家数量 | 3（1名被试 + 2名虚拟玩家） |
| 总传球次数 | 30 |
| 排斥条件接球次数 | 2次（第2、第5次传球） |
| 包容条件接球次数 | 10次（均匀分布） |
| 传球方式 | 鼠标点击玩家图标 |
| 球动画时长 | 2秒（线性插值） |
| 覆盖故事 | "与在线参与者进行心理想象训练游戏" |
| 实验后问卷 | Need-Threat Scale（12题）+ 心情问卷（4题），7点Likert |

### Missing Information

1. 指导语的具体文本内容未提供 → 需确认指导语措辞（是否提示"心理想象训练"、是否提及"反应速度"等干扰任务描述）
2. 心情问卷的具体题目未提供 → 需确认4个题目的维度和措辞（例如：高兴-悲伤、放松-紧张、愉悦-不悦、兴奋-平静）
3. 玩家头像/图标的具体样式未提供 → 需确认：卡通人物剪影、字母标签、还是照片？图标大小、颜色、屏幕位置？

### Critical Assumptions

- 虚拟玩家的传球延迟固定为1秒观察窗口 + 2秒动画，被试回合无时间限制
- 指导语中的覆盖故事在实验结束后会在debriefing中揭示真相（伦理要求），debriefing文本需额外提供
- 鼠标点击的有效区域为玩家图标的边界框内，点击空白区域无效且不记录

### Code Architecture

```
cyberball.py
├── 参数配置（condition, total_throws, participant_throws, throw_sequence, animation_duration）
├── 窗口初始化（全屏/窗口模式，背景色）
├── 刺激预加载
│   ├── 玩家图标（3个圆形/头像，屏幕位置：左-中-右或三角形排列）
│   ├── 球的图标（小球图形）
│   └── 文本刺激（状态提示文本）
├── 条件文件加载
│   ├── throw_sequence 预定义脚本（JSON格式）
│   └── condition 标签（inclusion / exclusion）
├── 实验阶段
│   ├── 指导语阶段
│   │   ├── 覆盖故事文本展示
│   │   └── 等待空格键继续
│   ├── 传球游戏循环（30个回合）
│   │   ├── if ball_to == "choose"（被试回合）
│   │   │   ├── 显示球在被试位置
│   │   │   ├── 显示"该你了！"提示
│   │   │   ├── 等待鼠标点击（记录RT和chosen_player）
│   │   │   └── 进入动画阶段
│   │   └── else（虚拟玩家回合）
│   │       ├── 显示球在传球者位置
│   │       ├── 显示"Player X 正在传球..."提示
│   │       ├── 等待1秒观察窗口
│   │       └── 进入动画阶段
│   ├── 传球动画（2秒线性插值，球从起点移动到终点）
│   ├── ITI（500 ms静止画面）
│   └── 数据记录（每轮：trial_number, condition, ball_from, ball_to, chosen_player, rt, animation_start/end）
├── 实验后问卷阶段
│   ├── Need-Threat Scale（12题，7点Likert，4个分量表各3题）
│   └── 心情问卷（4题，7点Likert）
├── Debriefing阶段（揭示真实实验目的，获得知情同意确认）
└── 数据保存（CSV格式，incremental write + final save）
```

### Expected Data Columns

| Column | Type | Description |
|--------|------|-------------|
| trial_number | int | 传球顺序编号（1-30） |
| condition | str | `"inclusion"` 或 `"exclusion"` |
| ball_from | str | 传球发起者（`"player_1"`, `"player_2"`, `"participant"`） |
| ball_to | str | 传球目标（`"player_1"`, `"player_2"`, `"choose"`） |
| is_participant_turn | int | 是否为被试回合（1=被试传球回合, 0=虚拟玩家回合） |
| chosen_player | str | 被试选择的传球目标（仅在被试回合有值，否则为 `NaN`） |
| rt | float | 被试反应时（ms），从球出现到鼠标点击（仅在被试回合有值） |
| animation_duration | float | 传球动画实际时长（秒） |
| throw_text_displayed | str | 该回合显示的提示文本 |
| need_threat_belonging | float | 归属感分量表均分（1-7） |
| need_threat_self_esteem | float | 自尊分量表均分（1-7） |
| need_threat_meaningful | float | 意义性存在分量表均分（1-7） |
| need_threat_control | float | 控制感分量表均分（1-7） |
| mood_valence | float | 心情效价均分（1-7） |
