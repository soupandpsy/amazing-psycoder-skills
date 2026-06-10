# Balloon Analogue Risk Task (BART)

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/bart) · reference

## When to Use

User mentions: BART, balloon task, risk-taking, 气球模拟风险任务. A behavioral measure of risk-taking propensity in which participants inflate balloons to earn rewards, trading off the risk of bursting and losing earnings.

## Core Logic

On each trial, a balloon is displayed and the participant can repeatedly press a key to pump it up. Each pump increases the balloon's size and adds a small amount to a temporary reward counter. However, every pump also carries a risk: each balloon has a hidden explosion point, and if the participant exceeds it, the balloon bursts, all temporary earnings for that trial are lost, and a new balloon appears. The participant can choose to "cash out" at any point, transferring the temporary earnings to a permanent bank before the balloon would burst.

The explosion point for each balloon is drawn from a predetermined distribution. In the original Lejuez et al. (2002) paradigm, balloons burst according to a probability function; in the simplified demo, the explosion threshold (max pumps) is a random integer. Participants complete multiple balloons (typically 30). The critical question is how many pumps a participant makes on average, especially on trials where the balloon does not burst.

Key variables: number of pumps per balloon (adjusted), number of balloons burst, number of cash-outs, total earnings. The primary dependent measure is the adjusted average number of pumps (mean pumps on non-burst trials), which indexes risk-taking propensity independent of the balloon explosion threshold.

## Data Analysis

Filter out burst trials and compute mean pumps on remaining (non-burst) trials as the primary measure. Examine total earnings and number of explosions as secondary measures. Correlate adjusted pumps with self-report measures of sensation-seeking, impulsivity, and real-world risk behaviors (e.g., substance use, gambling). Variants introduce balloons with different colors/explosion profiles to examine sensitivity to risk probability.

## Must Confirm

- **Balloon count**: How many balloons? (typically 30)
- **Burst distribution**: What determines the explosion point — fixed probability per pump, random integer threshold, or fixed thresholds in conditions.xlsx?
- **Key mapping**: Which key for "pump" and which for "collect"?
- **Reward structure**: Reward per pump and what happens on burst?
- **Visual assets**: Balloon colors, background images, and burst sound?

## Trial Window Timeline

```
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Balloon Display          │    │ Pump Feedback             │    │ Outcome                  │
│ Content: balloon image   │    │ Content: balloon grows   │    │ Content: burst (sound)   │
│ + score + pump count     │    │ + score increments       │    │ OR collect confirmation  │
│ Duration: until key      │    │ Duration: 500 ms         │    │ Duration: 1000 ms        │
│ Response: pump/collect   │    │ Response: none           │    │ Response: none           │
│ Data: pump_count, score  │    │ Data: none               │    │ Data: burst (bool)       │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

Nested loop: outer loop over balloons, inner loop over pumps within each balloon. Balloon size increases with each pump via `balloon.setSize()`.

## Do Not Assume

- Do not assume the burst rule is a fixed probability per pump. In the original Lejuez BART, each pump has a probability of bursting; in simplified implementations, a pre-determined integer threshold (max pumps) is drawn per balloon. Confirm which burst distribution the user wants.
- Do not assume the pump key is always the space bar. In some setups, the pump key may be different from the collect key. Confirm both key mappings.
- Do not assume 30 balloons is the default for every experiment — the count may vary by study design or age group (e.g., 10 balloons for children, 90 for pharmacological studies).
- Do not assume all balloons share the same explosion profile. Some variants assign different burst probabilities or max-pump distributions to different balloon colors/conditions. Confirm if balloons are homogeneous or heterogeneous.
- Do not assume the reward per pump is a fixed amount. It may vary across conditions or increment non-linearly. Confirm the monetary or point reward structure, including what happens on burst (partial loss, total loss of trial earnings).
- Do not assume there is no practice phase. Some designs include 2–5 practice balloons to familiarize participants with the pump/collect mechanics before the formal task.

## Condition File Columns

Columns in the xlsx/csv file that define each balloon's hidden parameters:

| Column | Type | Description |
|--------|------|-------------|
| balloon_id | int | Balloon/round number (1..n_balloons) |
| max_pumps | int | Hidden explosion threshold for this balloon |
| reward_per_pump | float | Points or monetary increment per pump |
| balloon_color | str | Balloon color (if color-condition variant) |

## Variants

- **标准BART (Standard BART)**: 原始Lejuez et al. (2002)版本，每个气球有固定的爆炸概率（如1/128），每次充气后根据该概率决定是否爆炸。爆炸点为隐藏变量，参与者无法直接观察到。
- **多颜色BART (Multi-color BART)**: 不同颜色的气球对应不同的爆炸概率分布。例如红色气球平均爆炸点较低（高风险），蓝色气球平均爆炸点较高（低风险）。用于考察参与者对风险概率的敏感性和学习效应。可交叉参考 [risk-task.md](risk-task.md)。
- **自动充气BART (Automatic-pump BART)**: 气球以固定间隔自动充气，参与者只需决定何时停止并兑现。去除了按键频率这一混淆变量，更纯粹地测量风险决策的时间动态。可交叉参考 [stop-signal.md](stop-signal.md)。

## References

Lejuez, C. W., Read, J. P., Kahler, C. W., Richards, J. B., Ramsey, S. E., Stuart, G. L., Strong, D. R., & Brown, R. A. (2002). Evaluation of a behavioral measure of risk taking: The Balloon Analogue Risk Task (BART). *Journal of Experimental Psychology: Applied, 8*(2), 75–84. https://doi.org/10.1037/1076-898X.8.2.75

---

## Example

### User Request

> "我想用PsychoPy做一个BART实验。屏幕中央呈现一个红色气球，按空格键给气球充气，每次充气球变大一点并加0.5分。每个气球有一个隐藏的爆炸上限（在1到128之间随机整数）。如果充气次数超过这个上限，气球爆炸，该轮得分清零。参与者可以随时按Enter键"收钱"，把当前得分转入永久账户。总共30个气球。在正式实验前有3个练习气球。每次充气后显示反馈100 ms。爆炸或收钱后显示结果2000 ms。气球爆炸时播放爆炸音效。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Balloon Display          │    │ Pump Feedback            │    │ Outcome                  │    │ ITI                      │
│ Content: 气球图像        │    │ Content: 气球变大       │    │ Content: 爆炸动画/音效  │    │ Content: 空白           │
│ + 当前得分 + 充气次数    │    │ + 得分增加动画          │    │ 或 "已收钱" 提示        │    │ Duration: 500 ms         │
│ Duration: 直到按键       │    │ Duration: 100 ms         │    │ Duration: 2000 ms        │    │ Response: none           │
│ Response: 空格(充气)     │    │ Response: none           │    │ Response: none           │    │ File: none               │
│ 或 Enter(收钱)           │    │ File: none               │    │ File: burst_sound.wav    │    │ Condition: none          │
│ File: balloon.png        │    │ Condition: none          │    │ Condition: none          │    │ Data: none               │
│ Condition: {balloon_id}  │    │ Data: none               │    │ Data: burst (bool),      │    │                          │
│ Data: pump_count, acc    │    │                          │    │ trial_earnings           │    │                          │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | File/Folder | Condition | Data |
|--------|---------|----------|----------|-------------|-----------|------|
| Balloon Display | 气球图像 + 当前得分 + 充气次数 | 直到按键 | 空格(充气) / Enter(收钱) | balloon.png | {balloon_id} | pump_count, accumulated_score |
| Pump Feedback | 气球变大 + 得分增加动画 | 100 ms | none | none | none | none |
| Outcome | 爆炸动画/音效 或 "已收钱" 提示 | 2000 ms | none | burst_sound.wav | none | burst (bool), trial_earnings |
| ITI | 空白 | 500 ms | none | none | none | none |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| Experiment name | Balloon Analogue Risk Task |
| Platform | PsychoPy |
| Task type | BART (risk-taking) |
| Balloon count | 30 formal + 3 practice |
| Burst rule | Random integer threshold (1–128) per balloon |
| Pump key | Space (空格键) |
| Collect key | Enter (回车键) |
| Reward per pump | 0.5 分 |
| Burst consequence | 当前轮得分清零 |
| Pump feedback duration | 100 ms |
| Outcome duration | 2000 ms |
| ITI | 500 ms |
| Phases | Instruction → Practice(3) → Formal(30) |

### Missing Information

1. 气球图像文件路径及规格未说明 → 需确认 balloon.png 尺寸、颜色、背景要求
2. 爆炸音效具体文件及格式未提供 → 需确认 burst_sound.wav 路径或使用默认音效
3. 是否需要在气球爆炸前显示充气次数反馈 → 需确认试次间是否显示累计充气次数

### Assumptions

- 爆炸阈值为均匀分布的随机整数（1–128），而非基于概率函数，已在请求中明确
- 每轮结束后气球图像自动重置为初始大小，无平滑过渡动画
- 爆炸后得分为0，而非部分扣除；收钱后得分全数转入永久账户
- 练习气球数据不纳入最终分析，但存储以供检查

### Expected Code Architecture

```
bart.py
├── Parameters (n_balloons=30, n_practice=3, max_pumps_range=128, reward_per_pump=0.5)
├── Window setup (全屏或窗口)
├── Stimulus preloading (balloon.png, burst_sound.wav)
├── Generate condition file (balloon_id, max_pumps, reward_per_pump)
├── Practice loop (3 balloons)
├── Formal trial loop (30 balloons):
│   ├── Balloon display (直到按键: 空格充气 / Enter收钱)
│   ├── Pump feedback (100 ms: 气球变大 + 得分增加)
│   ├── Outcome (2000 ms: 爆炸/收钱结果)
│   │   └── 若充气次数 > max_pumps → burst=True, trial_earnings=0, 播放音效
│   │   └── 若按Enter → burst=False, trial_earnings 转入永久账户
│   └── ITI (500 ms)
├── Data: try/finally CSV with incremental writes
```

### Expected Data Columns

Base columns + balloon_id, trial_type, pump_count, burst, trial_earnings, total_earnings

| Column | Type | Description |
|--------|------|-------------|
| balloon_id | int | 气球编号 (1–30) |
| trial_type | str | `"practice"` or `"formal"` |
| pump_count | int | 该气球的总充气次数 |
| burst | int | 1=爆炸, 0=主动收钱 |
| trial_earnings | float | 该轮实际得分（爆炸为0） |
| total_earnings | float | 累计永久账户得分 |
| adjusted_pumps | float | 非爆炸试次的平均充气次数（分析时计算） |
| max_pumps | int | 该气球的隐藏爆炸阈值（实验记录用） |
