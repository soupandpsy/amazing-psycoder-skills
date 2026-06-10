# Ultimatum Game

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/ultimatum) · reference

## When to Use

User mentions: Ultimatum game, UG, fairness, social decision-making, economic game, 最后通牒游戏, 公平博弈. A two-player economic game that measures fairness preferences and the willingness to incur personal costs to punish unfair treatment.

## Core Logic

The participant (Responder) is told they are paired with another player (Proposer), who has been given a sum of money to split. The Proposer makes an offer specifying how much the Responder receives (e.g., "Proposer gets $7, you get $3"). The Responder can either accept the offer (both players receive the proposed amounts) or reject it (neither player receives anything). The rational self-interest prediction is that Responders should accept any non-zero offer. In reality, low offers (typically below 20-30% of the total) are rejected at high rates, demonstrating fairness-driven punishment.

Key manipulations: the stake size (total amount to split), the identity of the Proposer (human vs. computer), the context (e.g., earned vs. windfall endowment), and whether the game is one-shot or repeated. Offers are typically presented as pre-determined splits (e.g., $5:$5 fair, $8:$2 unfair, $9:$1 very unfair), though some versions involve real-time human proposers.

This implementation frames the participant as the Responder. A simulated "connection" sequence (6 s total: 4 s "connecting to other player..." + 2 s "Connected!") enhances the cover story. On each trial, the proposed split is displayed (amount out of 10 pounds total), and the participant clicks an "Accept" or "Reject" button (mouse-based ButtonStim). After the choice, the outcome is displayed: both players' earnings if accepted, or "You rejected the offer. Nobody gets anything." if rejected. A fairness check (`offer >= amount/2`) is used to categorize offers as fair or unfair.

Typical design: offers range from 0 to the full stake, with standard offers being 5:5 (fair), 7:3/8:2 (unfair), and 9:1/10:0 (very unfair). Earnings accumulate across trials. The key behavioral measure is the rejection rate at each offer level.

## Must Confirm

- **Stake amount**: How much money to split? (typically 10 units, e.g., $10 or 10 pounds)
- **Offer set**: Which specific offer splits to present? (e.g., 5:5, 7:3, 8:2, 9:1)
- **Player role**: Participant always as Responder, or does the role alternate?
- **Cover story**: "Connected to another player" simulation, or transparent about pre-programmed offers?
- **Proposer identity**: Human (with photo/name), computer algorithm, or anonymous?
- **Response mode**: Mouse click on Accept/Reject buttons, or keyboard response?
- **Outcome display**: Show earnings after each trial, or only at the end?
- **Post-trial ratings**: Collect fairness judgments or emotion ratings after each offer?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Connection Simulation    │    │ Offer + Decision         │    │ Outcome Display          │
│ Content: "Connecting to  │    │ Content: proposed split  │    │ Content: earnings or     │
│ other player..." (4 s)   │    │ (e.g., "Proposer: £7     │    │ "Nobody gets anything"   │
│ then "Connected!" (2 s)  │    │ You: £3") + Accept/      │    │ Duration: ~2 s            │
│ Duration: 6 s total      │    │ Reject buttons           │    │ Response: none            │
│ Response: none           │    │ Duration: until click    │    │ Data: none                │
│ Data: none               │    │ Response: mouse click    │    │                           │
│                          │    │ Data: choice, RT, offer  │    │                           │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

## Data Analysis

The primary dependent variable is the acceptance rate as a function of offer amount. Plot acceptance rate against offer size (or fairness level). Typically, acceptance rates increase with offer size, with a sharp drop-off below 30-40%. Compare acceptance rates between conditions (e.g., human vs. computer proposer — higher rejection of unfair human offers indexes social preferences). Individual differences (e.g., trait agreeableness, psychopathy, autism) correlate with rejection rates. Rejection rates are also used to index negative reciprocity and anger-driven punishment.

## References

Guth, W., Schmittberger, R., & Schwarze, B. (1982). An experimental analysis of ultimatum bargaining. *Journal of Economic Behavior & Organization, 3*(4), 367–388. https://doi.org/10.1016/0167-2681(82)90011-7

Camerer, C. F. (2003). *Behavioral game theory: Experiments in strategic interaction*. Princeton University Press.

## Do Not Assume

- Do not assume 参与者始终是Responder角色 — 部分变体交替角色或让参与者担任Proposer，需明确确认角色分配方式
- Do not assume 提议者是人类 — 计算机/算法作为提议者是常见操作，用于区分社会偏好与风险偏好。需确认提议者身份（真人照片/姓名、匿名、或计算机算法）
- Do not assume 分配方案是预先编程的 — 部分实现涉及实时人类提议者，需联网配对或使用虚拟玩家逻辑
- Do not assume 接受/拒绝是唯一的因变量 — 部分设计在每个试次后收集公平性评分或情绪评定，需确认是否需要试次后评分
- Do not assume 总金额固定为10单位 — 不同研究使用不同面额（如$10、£10、100元、100积分），需明确确认赌注金额和货币单位
- Do not assume 连接模拟环节是必需的 — 部分实验明确告知参与者分配方案是预先设定的，跳过连接动画以缩短实验时长

## Condition File Columns

| Column | Type | Description |
|--------|------|-------------|
| proposer_amount | int/float | 提议者获得的金额 |
| responder_amount | int/float | 参与者（Responder）获得的金额 |
| total_stake | int/float | 本轮总分配金额 |
| fairness | str | 公平性分类（`"fair"`, `"unfair"`, `"very_unfair"`） |
| proposer_id | str | 提议者身份标签（`"human"` 或 `"computer"`） |

## Variants

- **经典最后通牒博弈 (Classic Ultimatum Game)**：单次匿名博弈，参与者固定为Responder角色，对一系列预先设定的分配方案做出接受或拒绝决策。分配方案通常包含公平（5:5）、不公平（7:3、8:2）和非常不公平（9:1、10:0）等梯度水平。这是最常用的实现方式，本文档主要描述此变体。
- **独裁者博弈 (Dictator Game)**：Proposer单方面决定分配方案，Responder无权拒绝，只能被动接受。用于测量纯粹的利他偏好和公平动机，排除策略性考虑和惩罚动机。可交叉参考 [dictator-game.md](dictator-game.md)（如该文件存在）。
- **多轮重复最后通牒博弈 (Repeated Ultimatum Game)**：同一对参与者进行多轮博弈，角色固定或交替轮换。用于考察声誉建立、互惠策略和学习效应。每次试次后可能需要显示累积收益。可交叉参考 [trust-game.md](trust-game.md)（如该文件存在）。

---

## Example

### User Request

> "我想用PsychoPy做一个最后通牒博弈实验。参与者作为回应者，每次看到分配方案：提议者获得多少，自己获得多少，总金额为100元。分配方案包括：提议者50元/自己50元（公平）、提议者70元/自己30元（不公平）、提议者90元/自己10元（非常不公平）。每种方案出现10次，共30试次，随机顺序。试次开始前先模拟连接其他玩家（3秒），然后呈现分配方案，屏幕下方有两个按钮'接受'和'拒绝'，用鼠标点击。如果接受，显示双方收益；如果拒绝，显示'双方收益均为0'。结果呈现2秒。试次间隔500-800ms随机。无练习试次。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ 连接模拟                  │    │ 分配方案 + 决策           │    │ 结果呈现                  │    │ ITI                      │
│ Content: "正在连接        │    │ Content: "提议者获得:     │    │ Content: 双方收益（接受） │    │ Content: 空白            │
│ 其他玩家..."              │    │ ¥70, 您获得: ¥30"        │    │ 或 "双方收益均为0元"      │    │ Duration: 500-800 ms     │
│ Duration: 3 s             │    │ + 接受/拒绝按钮           │    │ （拒绝）                  │    │ Response: none           │
│ Response: none            │    │ Duration: until click     │    │ Duration: 2 s             │    │ Data: none               │
│ Data: none                │    │ Response: 鼠标点击        │    │ Response: none            │    │                           │
│                           │    │ Data: choice, RT, offer   │    │ Data: none                │    │                           │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | File/Folder | Condition | Data |
|--------|---------|----------|----------|-------------|-----------|------|
| 连接模拟 | "正在连接其他玩家..." | 3 s | none | none | none | none |
| 分配方案+决策 | 分配金额 + 接受/拒绝按钮 | until mouse click | 鼠标点击 | none | {proposer_amount, responder_amount} | choice, rt, offer |
| 结果呈现 | 双方收益 或 "双方收益均为0元" | 2 s | none | none | none | none |
| ITI | 空白 | 500-800 ms random | none | none | none | none |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| 实验名称 | 最后通牒博弈任务 |
| 平台 | PsychoPy |
| 任务类型 | 最后通牒博弈 (Ultimatum Game) |
| 参与者角色 | Responder（回应者） |
| 总金额 | 100元 |
| 分配方案 | 50:50（公平）、70:30（不公平）、90:10（非常不公平） |
| 每方案试次数 | 10次 |
| 总试次数 | 30 |
| 试次顺序 | 随机 |
| 响应方式 | 鼠标点击接受/拒绝按钮 |
| 连接模拟 | 3秒 |
| 结果呈现 | 2秒 |
| ITI | 500-800ms随机 |

### Missing Information

1. 提议者身份未明确 → 需确认是"匿名人类玩家"还是"计算机算法"（影响封面故事文本和连接模拟后的呈现方式）
2. 是否需要在实验结束后显示累积总收益 → 影响结果汇总界面的设计
3. 指导语内容未提供 → 需确认指导语文本、是否明确告知分配方案为预先设定

### Critical Assumptions

- 提议者为匿名人类玩家，连接模拟用于增强封面故事的可信度（默认设计假设）
- 实验结束后不显示累积总收益，仅呈现致谢页面
- 指导语使用标准最后通牒博弈指导语模板，包含角色说明和规则解释
- 无试次后公平性评分或情绪评定

### Code Architecture

```
ultimatum_game.py
├── 参数设置 (total_stake=100, offers, n_repeats, timing)
├── 窗口初始化 (全屏/窗口)
├── 刺激预加载 (TextStim for 分配文本, ButtonStim for 接受/拒绝)
├── 条件表生成 (3种方案 × 10次 = 30试次, 随机排列)
├── 连接模拟 (3秒, TextStim)
├── 试次循环:
│   ├── 分配方案呈现 + 接受/拒绝按钮
│   ├── 鼠标点击响应 (记录 choice, rt)
│   ├── 结果呈现 (2秒, 根据选择显示收益)
│   └── ITI (500-800ms 随机)
├── 致谢页面
└── 数据保存: try/finally CSV 增量写入
```

### Expected Data Columns

| Column | Type | Description |
|--------|------|-------------|
| trial_index | int | 试次序号 (0-based) |
| proposer_amount | float | 提议者获得金额 |
| responder_amount | float | 参与者获得金额 |
| total_stake | float | 本轮总金额 |
| fairness | str | 公平性分类 (`"fair"`, `"unfair"`, `"very_unfair"`) |
| choice | str | 参与者的选择 (`"accept"` 或 `"reject"`) |
| rt | float | 反应时间 (秒) |
| outcome_self | float | 参与者本轮实际收益 |
| outcome_proposer | float | 提议者本轮实际收益 |
