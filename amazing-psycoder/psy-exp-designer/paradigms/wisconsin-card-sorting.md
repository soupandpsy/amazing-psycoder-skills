# Wisconsin Card Sorting Test (WCST)

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/wcst) · reference

## When to Use

User mentions: WCST, Wisconsin Card Sorting, set-shifting, cognitive flexibility, perseveration, 威斯康星卡片分类, 认知灵活性. The gold-standard neuropsychological test of executive function measuring the ability to form, maintain, and shift cognitive sets in response to changing reinforcement contingencies.

## Core Logic

Participants sort cards one at a time into one of four target piles. Each card varies on three dimensions: shape (e.g., triangle, star, cross, circle), color (e.g., red, green, yellow, blue), and number (1 to 4 symbols per card). The four target cards each represent a unique value on one dimension (e.g., one red triangle, two green stars, three yellow crosses, four blue circles). The participant is not told the sorting rule but receives feedback (correct/incorrect) after each sort.

The sorting rule (match by color, shape, or number) is initially set and maintained. After a criterion number of consecutive correct sorts (typically 10), the rule changes without warning. The participant must discover the new rule through trial and error using feedback alone. The core difficulty is suppressing the previously correct rule (set-shifting). Perseverative errors — continuing to sort by the old rule after it has changed — are the hallmark measure of cognitive inflexibility.

This implementation uses a nested two-loop design: an outer block loop (`chooseRule.xlsx`, 2 reps) sets the sorting rule, and an inner trial loop (`cards.xlsx`) presents cards in blocks of 7 forced trials (useRows selection). Each trial displays 4 reference cards at the top and 1 trial card below, all rendered as colored shapes at specified positions. A 1 s fixation precedes the card display, and the participant clicks on one of the 4 reference cards to indicate their sort. After each sort, feedback ("Correct!" or "Incorrect") is shown for 1 s. At the end of each block, the score is displayed for 3 s before the next block begins.

Key measures: number of categories completed (max 6), total errors, perseverative errors (continuing the old rule after a shift), failure to maintain set (losing the rule mid-category, i.e., 5+ correct followed by an error), and trials to complete the first category (initial conceptualization). The test continues until all 6 categories are completed or all 128 cards are used.

## Must Confirm

- **Stimulus dimensions**: Shape, color, and number — all three or a subset?
- **Number of dimensions and values**: 3 dimensions with 4 values each (shapes: triangle/star/cross/circle, colors: red/green/yellow/blue, numbers: 1/2/3/4)?
- **Trial cards**: How are trial cards generated — from a fixed deck (128 cards), or dynamically?
- **Trials per block**: Fixed number (e.g., 7 forced trials from chooseRule.xlsx) per rule, or continue until criterion (e.g., 10 consecutive correct)?
- **Response mode**: Mouse click on reference cards, or keyboard selection?
- **Feedback**: 1 s feedback after each trial, or no feedback?
- **Rule change**: How many rule shifts, and in what order?

## Trial Window Timeline

```text
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│ Window 1             │→ │ Window 2             │→ │ Window 3             │→ │ Window 4             │
│ Fixation             │  │ Card Sort            │  │ Feedback              │  │ Block End (every     │
│ Content: + at center │  │ Content: 4 reference │  │ Content: "Correct!"   │  │ 7 trials)            │
│ Duration: 1.0 s      │  │ cards (top) + 1      │  │ or "Incorrect"        │  │ Content: score       │
│ Response: none       │  │ trial card (bottom)  │  │ Duration: 1.0 s       │  │ Duration: 3.0 s      │
│ Data: none           │  │ Duration: until click│  │ Response: none        │  │ Response: none       │
│                      │  │ Response: click on   │  │ Data: none            │  │ Data: none           │
│                      │  │ a reference card     │  │                       │  │                      │
│                      │  │ Data: clicked_name,  │  │                       │  │                      │
│                      │  │ rt, acc              │  │                       │  │                      │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘
```

## Data Analysis

Primary outcome: number of perseverative errors (the most sensitive index of frontal lobe dysfunction). Also analyze categories completed, total errors, failure to maintain set, and learning-to-learn (improvement across categories). The WCST is highly sensitive to prefrontal cortex damage, particularly dorsolateral prefrontal cortex. Perseverative errors are elevated in schizophrenia, Parkinson's disease, ADHD, and traumatic brain injury.

## References

Grant, D. A., & Berg, E. A. (1948). A behavioral analysis of degree of reinforcement and ease of shifting to new responses in a Weigl-type card-sorting problem. *Journal of Experimental Psychology, 38*(4), 404–411. https://doi.org/10.1037/h0059831

Heaton, R. K., Chelune, G. J., Talley, J. L., Kay, G. G., & Curtiss, G. (1993). *Wisconsin Card Sorting Test manual: Revised and expanded*. Psychological Assessment Resources.

## Do Not Assume

- Do not assume 10 连续正确即为完成分类。部分版本使用 6 或 8 个连续正确作为分类完成标准，确认标准数目。
- Do not assume 规则序列是固定的。颜色→形状→数量是常见顺序，但规则顺序可能随机化或由实验设计决定。
- Do not assume 所有三个维度都使用。简化版本可能只使用 2 个维度（如仅颜色和形状），确认维度数量。
- Do not assume 128 张卡片总是全部使用。部分版本在完成 6 个分类后提前终止，或仅使用 64 张卡片（WCST-64）。
- Do not assume 反馈仅为文字。确认反馈形式：文字（"正确"/"错误"）、声音、还是两者兼有。
- Do not assume 被试已知三个维度。部分实验在指导语中明确告知维度，部分则完全不告知，需确认指导语内容。

## Condition File Columns

驱动每次试次的 xlsx/csv 文件列：

| Column | Type | Description |
|--------|------|-------------|
| rule | str | 当前分类规则：`"color"`、`"shape"` 或 `"number"` |
| card_id | int | 卡片编号（1-128） |
| correct_target | str | 正确目标卡片标识（如 `"red_triangle"`） |
| block | int | 所属 block 编号（1-6，对应 6 个分类） |

## Variants

1. **标准 WCST（128 张卡片）**：原始版本，使用 128 张纸质卡片，3 个维度各 4 个值，最多完成 6 个分类。规则顺序固定（颜色→形状→数量→颜色→形状→数量）。参见 [config-schema](../references/config-schema.md)。

2. **简化版 MCST（Modified Card Sorting Test）**：仅使用 48 张卡片，排除那些与目标卡片共享多个属性的模糊卡片（如与正确目标同时匹配颜色和数量的卡片）。减少混淆，更适合临床人群，尤其是老年或认知障碍患者。参见 [go-nogo.md](go-nogo.md) 的反馈处理逻辑。

3. **计算机化 WCST-64**：仅使用 64 张卡片（每个规则一个 deck），缩短测试时间同时保持心理测量特性。适用于时间有限的筛查场景。

---

## Example

### User Request

> "我想做一个威斯康星卡片分类测验。屏幕上方显示4张目标卡片（分别是1个红色三角形、2个绿色星星、3个黄色十字、4个蓝色圆形），下方显示1张测试卡片。被试点击目标卡片来分类。每次点击后显示'正确'或'错误'反馈1秒。完成10个连续正确后自动切换规则。一共6个分类要完成，每次切换规则不提醒被试。测试前先做10个练习试次。使用PsychoPy。被试是中文母语者。"

### Trial Window Timeline

```text
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│ Window 1             │→ │ Window 2             │→ │ Window 3             │→ │ Window 4             │
│ 注视点               │  │ 卡片分类              │  │ 反馈                  │  │ 分类完成提示          │
│ Content: + at center │  │ Content: 4 目标卡片   │  │ Content: "正确！"     │  │ Content: "分类完成！  │
│ Duration: 1.0 s      │  │ (上排) + 1 测试卡片   │  │ 或 "错误"            │  │ 即将开始新规则..."    │
│ Response: none       │  │ (下排)               │  │ Duration: 1.0 s      │  │ Duration: 2.0 s      │
│ Data: none           │  │ Duration: until click │  │ Response: none       │  │ Response: none       │
│                      │  │ Response: click on    │  │ Data: none           │  │ Data: none           │
│                      │  │ a target card        │  │                       │  │                      │
│                      │  │ Data: clicked_target, │  │                       │  │                      │
│                      │  │ rt, acc, rule        │  │                       │  │                      │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘
```

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| 实验名称 | 威斯康星卡片分类测验（WCST） |
| 平台 | PsychoPy |
| 任务类型 | 认知灵活性 / 定势转换（set-shifting） |
| 目标卡片 | 1红三角 / 2绿星 / 3黄十字 / 4蓝圆（上排） |
| 测试卡片 | 每次1张，下方居中呈现 |
| 维度 | 3个（颜色、形状、数量），各4个值 |
| 反应方式 | 鼠标点击目标卡片 |
| 反馈 | 文字"正确"/"错误"，持续 1 s |
| 分类完成标准 | 10 个连续正确 |
| 总分类数 | 6 个 |
| 规则切换 | 自动、无提醒 |
| 阶段 | 指导语 → 练习(10试次) → 正式测验(最多128试次) |

### Missing Information

1. 注视点持续时间未说明 → 默认 1.0 s（需与用户确认）
2. 试次间隔（ITI）未提及 → 需确认是否有 ITI 及其持续时间
3. 练习阶段的反馈方式未说明 → 需确认练习阶段是否与正式阶段反馈一致

### Critical Assumptions

- 规则顺序为颜色→形状→数量→颜色→形状→数量（标准 WCST 顺序）
- 练习阶段同样显示反馈，持续 1 s
- 注视点为黑色"+"，居中呈现
- 被试响应无时间限制（until click），但需记录 RT
- 练习阶段卡片从标准 128 张中选取前 10 张，不切换规则

### Code Architecture

```
wcst.py
├── 参数（dimensions, n_correct_to_shift=10, n_categories=6, n_practice=10）
├── 窗口设置（全屏/窗口，分辨率）
├── 刺激预加载
│   ├── 4 个目标卡片（TextStim/ShapeStim + 颜色填充）
│   ├── 128 张测试卡片（按维度生成所有组合）
│   └── 反馈文字（"正确！"/"错误"）
├── 条件表生成（card_id, shape, color, number, rule, correct_target）
├── 主循环
│   ├── 规则管理（当前规则、连续正确计数、已完成分类数）
│   ├── 试次循环
│   │   ├── 注视点（1.0 s）
│   │   ├── 显示目标卡片 + 测试卡片（等待点击）
│   │   ├── 判断正确/错误（匹配当前规则的目标卡片）
│   │   ├── 反馈（1.0 s）
│   │   └── 检查是否达到 10 个连续正确 → 切换规则
│   └── 终止条件：6 个分类完成 或 128 张卡片用完
├── 数据保存：try/finally CSV，逐行写入
└── 退出：Escape 键监听
```

### Expected Data Columns

| Column | Type | Description |
|--------|------|-------------|
| card_id | int | 卡片编号（1-128） |
| trial_index | int | 试次序号（全局） |
| block | int | 当前分类编号（1-6） |
| rule | str | 当前分类规则（color/shape/number） |
| shape | str | 测试卡片形状 |
| color | str | 测试卡片颜色 |
| number | int | 测试卡片符号数量 |
| correct_target | str | 正确目标卡片标识 |
| clicked_target | str | 被试点击的目标卡片标识 |
| acc | int | 正确=1，错误=0 |
| rt | float | 反应时间（ms） |
| consecutive_correct | int | 当前连续正确计数 |
| perseverative_error | int | 固着错误=1（按旧规则对当前规则错），否则=0 |
| category_completed | int | 该试次所属分类是否已完成（1=是） |
