# Delay Discounting Task (Temporal Discounting)

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/delay-discounting) · reference

## When to Use

User mentions: Delay discounting, temporal discounting, intertemporal choice, impulsivity, 延迟折扣, 时间贴现. Measures the tendency to devalue rewards as a function of the delay until their receipt — the preference for smaller-sooner rewards over larger-later ones.

## Core Logic

Participants make a series of binary choices between a smaller reward available immediately (e.g., "$20 today") and a larger reward available after a delay (e.g., "$50 in 30 days"). The immediate amount, the delayed amount, and the delay length are systematically varied across trials. The key dependent variable is the indifference point at each delay — the immediate amount at which the participant is equally likely to choose either option (i.e., the subjective value of the delayed reward).

Delay periods typically range from days to years (e.g., 1 day, 1 week, 1 month, 6 months, 1 year, 5 years). By plotting subjective value against delay, the discounting rate (k) is estimated using a hyperbolic discounting function: V = A / (1 + kD), where V is subjective value, A is the delayed amount, D is delay, and k is the discounting rate. Higher k values indicate steeper discounting (greater impulsivity).

The task can be administered as a titration procedure (adjusting the immediate amount based on previous responses to converge on the indifference point) or as a full factorial design (all combinations of amounts and delays). This implementation uses a fixed choice set: each trial displays two options as labeled buttons (ButtonStim) side by side — e.g., "£5 now" vs. "£7 in 3 days". The condition file (`conditions.xlsx`) specifies the text labels in `amount1` and `amount2` columns. Participants click the button corresponding to their preferred option. No accuracy feedback is given, as there are no correct or incorrect answers — this is a preference measure. Trials are presented once in random order (`nReps=1.0`, `method='random'`).

## Must Confirm

- **Reward amounts**: What range of amounts? (e.g., $10-$100, or hypothetical larger sums?)
- **Delay values**: Which delay durations? (e.g., 1 day, 1 week, 1 month, 6 months, 1 year, 5 years)
- **Choice format**: Fixed choice pairs from a condition file, or adaptive titration?
- **Reward type**: Money, food, drugs, or other commodity?
- **Response mode**: Mouse click on labeled buttons, or keyboard selection?
- **Hypothetical vs. real**: Hypothetical choices, or one randomly selected trial is paid out for real?
- **No feedback**: Correct — no correct/incorrect answers in this paradigm.

## Trial Window Timeline

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Single Trial                                                          │
│                                                                       │
│ Content: two options as labeled buttons                              │
│   Left button: amount1 label (e.g., "£5 now")                        │
│   Right button: amount2 label (e.g., "£7 in 3 days")                 │
│ Duration: until click                                                 │
│ Response: mouse click on chosen button                               │
│ Condition: {amount1, amount2} from conditions.xlsx                   │
│ Data: chosen_button, RT                                               │
│                                                                       │
│ Note: no fixation, no feedback, no ITI — immediate advance to        │
│ next trial on response. Pure preference measure.                      │
└──────────────────────────────────────────────────────────────────────┘
```

## Data Analysis

Fit the hyperbolic discounting model to estimate k for each participant (or compute area under the curve, AUC, as a model-free alternative). Log-transform k due to positive skew. Compare k between clinical groups (substance use disorders, ADHD, gambling disorder, obesity) and controls. Steeper discounting is consistently associated with addictive and impulsive behaviors. Also examine whether discounting rate varies by reward type (money, food, drugs) in relevant populations.

## References

Mazur, J. E. (1987). An adjusting procedure for studying delayed reinforcement. In M. L. Commons, J. E. Mazur, J. A. Nevin, & H. Rachlin (Eds.), *Quantitative analyses of behavior, Vol. 5. The effect of delay and of intervening events on reinforcement value* (pp. 55–73). Lawrence Erlbaum.

Kirby, K. N., Petry, N. M., & Bickel, W. K. (1999). Heroin addicts have higher discount rates for delayed rewards than non-drug-using controls. *Journal of Experimental Psychology: General, 128*(1), 78–87. https://doi.org/10.1037/0096-3445.128.1.78

## Do Not Assume

- 不要假设奖励类型一定是金钱。延迟折扣任务中的奖励可以是食物、香烟、酒精、毒品或其他商品。不同奖励类型的折扣率可能存在系统性差异（如物质使用者对毒品的折扣率显著高于金钱）。在生成代码前，必须确认奖励的具体类型。
- 不要假设选择格式一定是固定选择集。虽然多数实现使用预定义的条件文件罗列所有金额-延迟组合（全因子设计），但也有研究采用自适应滴定程序——即时金额根据前序选择动态调整以逼近无差异点。务必确认用户期望的是哪种格式。
- 不要假设所有试次都是假设性选择。在一些设计中，实验结束后会随机抽取一个试次按参与者的选择实际兑现（真实支付），这可能产生不同于纯假设选择的折扣率。确认是否包含真实支付试次。
- 不要假设即时选项总是在左侧。即时选项与延迟选项的左右位置应在试次间进行平衡（counterbalancing），以控制位置偏好偏差。确认条件文件是否已包含位置平衡的试次，或是否需要代码在运行时随机化左右位置。
- 不要假设没有反应时间限制。虽然偏好测量任务通常不设反应截止时间，但某些实现会设置最大反应窗口（如 4000 ms），并对低于预期阈值的过快反应（如 RT < 200 ms）进行标记或剔除。确认是否需要反应时间限制。
- 不要假设所有延迟使用相同的时间单位。延迟可能以天、周、月或年为单位。条件文件的列命名及后续数据分析（如 k 值的量纲）必须与实际使用的单位一致。确认延迟的时间单位。

## Condition File Columns

条件文件（xlsx/csv）中定义每个试次选择对的列：

| Column | Type | Description |
|--------|------|-------------|
| amount1 | str | 左侧按钮的文本标签（如 "现在 ¥20" 或 "¥20 today"） |
| amount2 | str | 右侧按钮的文本标签（如 "30天后 ¥50" 或 "¥50 in 30 days"） |
| delay_days | int | 延迟天数（延迟选项的等待时间，若单位为非天则相应调整列名） |
| immediate_amount | float | 即时选项的金额数值（用于后续 k 值拟合） |
| delayed_amount | float | 延迟选项的金额数值（用于后续 k 值拟合） |

## Variants

- **固定选择集延迟折扣 (Fixed-Choice Delay Discounting)**：最常用的实现方式。所有即时金额、延迟金额和延迟时间的组合预先在条件文件中指定，以随机顺序呈现。每个试次为独立的二元选择，无适应性调整。数据分析通过拟合双曲线折扣模型 V = A / (1 + kD) 估计 k 值，或计算曲线下面积 (AUC) 作为无模型替代指标。本文件主要描述此变体。
- **滴定/调整延迟折扣 (Titrating/Adjusting Delay Discounting)**：即时奖励金额根据参与者在同一延迟条件下的前序选择动态调整，以逼近无差异点。例如，若参与者选择延迟奖励，则下次提高即时金额；若选择即时奖励，则降低即时金额。参考 Mazur (1987) 的调整程序。此变体可减少试次总数，但需要更复杂的试次间逻辑。可交叉参考 [staircase.md](staircase.md)。
- **跨商品延迟折扣 (Cross-Commodity Delay Discounting)**：同一参与者对不同奖励类型（如金钱、食物、香烟、酒精）分别完成延迟折扣任务。每种商品在独立的 block 中呈现，或将商品类型作为试次条件变量。用于考察折扣率的领域特异性（domain specificity）。可交叉参考 [concurrent-schedule.md](concurrent-schedule.md)。

---

## Example

### User Request

> "我要做一个延迟折扣实验，用PsychoPy。屏幕左右各有一个按钮，左边是即时较小奖励（如'现在获得 ¥30'），右边是延迟较大奖励（如'90天后获得 ¥100'）。延迟奖励金额固定为 ¥100。延迟时间包括7天、30天、90天、180天、365天五个水平。每个延迟水平下，即时金额从 ¥10 到 ¥95 变化（以¥5为步长）。所有试次随机呈现。试次间有500ms的注视点'+'。实验开始前显示指导语，结束后显示致谢。参与者用鼠标点击按钮选择。无反馈。无练习试次。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Fixation                 │    │ Choice Display           │    │ ITI                      │
│ Content: +               │    │ Content: 左右两个按钮    │    │ Content: 空白            │
│ Duration: 500 ms         │    │ 左: 即时奖励文本         │    │ Duration: 500 ms         │
│ Response: none           │    │ 右: 延迟奖励文本         │    │ Response: none           │
│ File: none               │    │ Duration: 直到点击       │    │ File: none               │
│ Condition: none          │    │ Response: 鼠标点击按钮   │    │ Condition: none          │
│ Data: none               │    │ File: none               │    │ Data: none               │
│                          │    │ Condition: {amount1,      │    │                          │
│                          │    │   amount2, delay_days}    │    │                          │
│                          │    │ Data: chosen_button,      │    │                          │
│                          │    │   choice_rt,              │    │                          │
│                          │    │   chose_immediate         │    │                          │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | File/Folder | Condition | Data |
|--------|---------|----------|----------|-------------|-----------|------|
| Fixation | + | 500 ms | none | none | none | none |
| Choice Display | 左右按钮 (即时 vs 延迟) | 直到鼠标点击 | 鼠标点击左/右按钮 | none | {amount1, amount2, delay_days, immediate_amount, delayed_amount} | chosen_button, choice_rt, chose_immediate |
| ITI | 空白 | 500 ms | none | none | none | none |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| Experiment name | 延迟折扣任务 (Delay Discounting Task) |
| Platform | PsychoPy |
| Task type | 延迟折扣 / 跨期选择 (Delay Discounting / Intertemporal Choice) |
| Reward type | 金钱 (¥) |
| Delayed amount | 固定 ¥100 |
| Delay levels | 7, 30, 90, 180, 365 天（5个水平） |
| Immediate amounts | ¥10–¥95（步长 ¥5，共18个水平） |
| Total trials | ~90 (5 delays × 18 immediate amounts; 立即金额超过延迟金额的组合保留) |
| Choice format | 固定选择集 (fixed choice set)，随机呈现 |
| Fixation duration | 500 ms |
| ITI duration | 500 ms |
| Response mode | 鼠标点击按钮 (ButtonStim) |
| Phases | Instruction → Formal trials → End thanks |

### Missing Information

1. 按钮的左右位置是否需要平衡（counterbalancing）——同一对金额和延迟是否需要在左右位置各出现一次？当前描述未明确说明，需确认。
2. 指导语的具体内容未提供 —— 需确认指导语文本、是否包含示例试次、以及过渡提示的措辞。
3. 是否需要对过快反应（如 RT < 200 ms）进行标记或剔除？需确认最低反应时阈值。

### Critical Assumptions

- 即时金额变化范围为 ¥10–¥95，以 ¥5 为步长，共 18 个即时金额 × 5 个延迟 = 90 个试次。即时金额超过延迟金额的组合（如 ¥95 现在 vs ¥100 在 7 天后）仍保留在设计中，因为这是合理的偏好测量（极端情况下可能全选即时选项，反映极高的折扣率）。
- 无练习试次，直接进入正式实验。这与用户描述一致。
- 左右位置不进行试次内随机化——按钮文本由条件文件的 amount1（左）和 amount2（右）列直接确定。若需要左右平衡，条件文件中需包含交换位置的额外行。
- 无反馈、无 ITI 注视点以外的额外间隔。试次间直接推进。
- 按钮文本标签的格式（如 "现在 ¥30" vs "90天后 ¥100"）由条件文件的 amount1/amount2 列定义，代码直接读取并显示，不做额外格式化。

### Code Architecture

```
delay_discounting.py
├── Parameters (n_trials, fixation_dur=0.5, iti_dur=0.5, delayed_amount=100)
├── Window setup (全屏或窗口)
├── Stimulus preloading (TextStim for fixation +, ButtonStim × 2 for choice options)
├── Load condition file (conditions.xlsx: amount1, amount2, delay_days, immediate_amount, delayed_amount)
├── Instruction screen (指导语)
├── Formal trial loop:
│   ├── Fixation (500 ms: +)
│   ├── Choice display (直到鼠标点击: 左按钮=即时, 右按钮=延迟)
│   ├── Record response (chosen_button, RT, chose_immediate)
│   └── ITI (500 ms: 空白)
├── End thanks screen
├── Data: try/finally CSV with incremental writes
```

### Expected Data Columns

| Column | Type | Description |
|--------|------|-------------|
| amount1 | str | 左侧按钮文本（如 "现在 ¥30"） |
| amount2 | str | 右侧按钮文本（如 "90天后 ¥100"） |
| delay_days | int | 延迟天数 |
| immediate_amount | float | 即时奖励金额 (¥) |
| delayed_amount | float | 延迟奖励金额 (¥) |
| chosen_button | str | 被点击的按钮标签（"left" / "right"） |
| choice_rt | float | 选择反应时（秒） |
| chose_immediate | int | 1=选择即时奖励, 0=选择延迟奖励 |
