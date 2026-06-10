# Rating-to-Choice Task

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/rating_to_choice_task) · PsychoJS

## When to Use

User mentions: Rating to choice, two-phase preference, painting rating, adaptive choice, 评分转选择任务. A two-phase decision-making paradigm where participants first rate individual stimuli and then make pairwise choices between stimuli selected based on their own ratings, demonstrating dynamic stimulus selection driven by participant responses.

## Core Logic

The task comprises two sequential phases linked by the participant's own rating data:

**Phase 1 — Rating Phase**: Participants view a set of stimuli (e.g., paintings — European art and nature scenes from Unsplash and museum collections) one at a time and rate each on a 3-point scale. They press keys 1, 2, or 3 to assign a rating. Each rating-keypress is stored alongside the image filename. The rating data from this phase serves as input to Phase 2.

**Phase 2 — Choice Phase**: A comparison file (`conditions_choice_phase.xlsx`) specifies which rating-level comparisons to make: "1 vs 2", "2 vs 3", and "1 vs 3". The code dynamically selects one painting with each specified rating from the participant's Phase 1 data. Two paintings are displayed side by side: one that the participant rated at one level and one rated at another level. The participant presses '1' to choose the left image or '2' to choose the right image.

**Adaptive stimulus selection** is the key innovation: Phase 2 trials are not pre-determined but are constructed in real time from Phase 1 responses. If a participant gave no painting a particular rating (e.g., no painting was rated 3), a default placeholder image is used for that comparison instead, ensuring all comparison types can always be presented.

**Data collected**: For each Phase 2 trial — the images displayed (left and right), the participant's choice, the comparison type (1v2, 2v3, 1v3), and the ratings that triggered the pairing. This reveals whether participants show systematic preferences between stimuli they rated identically, or inconsistencies between stated ratings and revealed choices.

## Must Confirm

- **Stimuli**: Paintings (what style/domain?), product images, faces, or other? How many items in the stimulus set?
- **Rating scale**: 1-3 (3-point), 1-5 (5-point), 1-7, or continuous slider?
- **Comparison types**: Which rating differences to compare? (1v2, 2v3, 1v3, or all pairwise?)
- **Placeholder handling**: What to show when no stimulus was given a required rating? Default image or skip that comparison?
- **Phase sequencing**: Always rating-then-choice, or counterbalanced order?
- **Trial counts**: How many stimuli to rate? How many comparison trials?

## Trial Window Timeline

**Phase 1 — Rating:**
```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Stimulus                 │    │ Rating Prompt            │    │ ITI                      │
│ Content: painting image  │    │ Content: rating scale    │    │ Content: blank           │
│ Duration: until key      │    │   (1-3) with labels      │    │ Duration: 500 ms         │
│ Response: none           │    │ Duration: until key      │    │ Response: none           │
│ Condition: {image_file}  │    │ Response: 1, 2, or 3     │    │ Condition: none          │
│ Data: image_filename     │    │ Data: rating_value       │    │ Data: none               │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

**Phase 2 — Choice:**
```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Stimulus Pair            │    │ Response                 │    │ ITI                      │
│ Content: 2 paintings     │    │ Content: selection prompt │    │ Content: blank           │
│   (left: rated X,        │    │ Duration: until key      │    │ Duration: 500 ms         │
│    right: rated Y)       │    │ Response: 1=left, 2=right│    │ Response: none           │
│ Duration: until key      │    │ Condition: {comparison}  │    │ Condition: none          │
│ Condition: {comparison}  │    │ Data: choice, rt          │    │ Data: none               │
│ Data: left_img, right_img│    └──────────────────────────┘    └──────────────────────────┘
└──────────────────────────┘
```

## Data Analysis

Analyze rating distributions (histogram of Phase 1 ratings). In Phase 2, examine reaction time and choice proportions for each comparison type. Test for preference consistency: does choice in Phase 2 align with rating differences from Phase 1? Analyze cases where rated-equal items produce systematic choices (revealed preference diverging from stated preference). Compare different comparison types (1v2, 2v3, 1v3) for choice difficulty (RT, decision confidence).

## References

No specific publication — this is a methodology demo illustrating dynamic stimulus selection based on participant responses. Adaptable to preference testing, decision-making, and value-based choice studies.

## Do Not Assume

- Do not assume 所有刺激在评级阶段都获得了全部评级等级——参与者可能只使用了部分评分等级（如仅使用1和2，而从未使用3），需处理缺失等级时选择阶段如何构建试次
- Do not assume 选择阶段的对比类型已预先固定——对比类型（如1v2, 2v3, 1v3）由条件文件定义，但实际可用的图片对取决于参与者的评级分布，需在代码中动态匹配
- Do not assume 占位刺激可以随意使用而不影响数据质量——当某评级等级无对应刺激而使用占位图时，该试次的行为数据可能不具有可比性，需在数据分析中标记
- Do not assume 左右位置不影响选择偏好——需对刺激的左右位置进行试次内随机化或跨试次平衡，并在数据中记录实际呈现位置
- Do not assume 评级阶段和选择阶段使用相同的时间参数——两个阶段的刺激呈现时间、反应窗口和ITI可能需要不同的设置

## Condition File Columns

选择阶段条件文件的列（评级阶段通常无需条件文件，直接遍历图片列表）：

| Column | Type | Description |
|--------|------|-------------|
| comparison_type | str | 对比类型标签，如 "1v2"、"2v3"、"1v3" |
| left_rating | int | 左侧刺激应具有的目标评级等级 |
| right_rating | int | 右侧刺激应具有的目标评级等级 |
| num_trials | int | 该对比类型每种位置排列的重复次数 |

## Variants

- **标准双阶段评分转选择（Standard Two-Phase Rating-to-Choice）**：参与者先完成所有刺激的评分，然后根据评分结果进行配对选择。评分阶段与选择阶段在时间上完全分离。这是本文件描述的核心范式。
- **试次级评分转选择（Trial-by-Trial Rating-to-Choice）**：在每个试次中，参与者先对一个新刺激评分，随即在当前已评分的刺激中进行选择，评分与选择交替进行。适用于研究即时偏好一致性与学习效应。可参考 [adaptive-choice](adaptive-choice.md) 范式。
- **多轮评分转选择（Multi-Round Rating-to-Choice）**：参与者进行多轮"评分-选择"循环，每轮的选择结果反馈到下一轮的刺激集或评分参考中。适用于研究偏好动态演化和选择诱导的偏好改变（choice-induced preference change）。

---

## Example

### User Request

> "我想做一个评分转选择实验。第一阶段让被试对30张抽象画图片用1到5分进行喜好度评分。第二阶段根据评分结果，展示评分差至少为2的图片对（例如评分1 vs 评分3、评分2 vs 评分4等），让被试按键选择更喜欢的图片。每种对比类型做8个试次。如果某评分等级没有对应图片，则跳过包含该等级的所有对比类型。用PsychoPy，全屏模式。"

### Trial Window Timeline

```text
Phase 1 — Rating（30 trials）:
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ 图片刺激                 │    │ 评分界面                 │    │ ITI                      │
│ Content: 抽象画图片      │    │ Content: 1-5分量表       │    │ Content: blank           │
│ Duration: until key      │    │   (1=非常不喜欢,        │    │ Duration: 500 ms         │
│ Response: none           │    │    5=非常喜欢)           │    │ Response: none           │
│ Condition: {image_file}  │    │ Duration: until key      │    │ Condition: none          │
│ Data: image, onset       │    │ Response: 1,2,3,4,5      │    │ Data: none               │
└──────────────────────────┘    │ Data: rating, rt          │    └──────────────────────────┘
                                └──────────────────────────┘

Phase 2 — Choice（对比类型 × 8 trials，左右位置平衡）:
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ 图片对                   │    │ 选择界面                 │    │ ITI                      │
│ Content: 左右两张抽象画  │    │ Content: "按1选左       │    │ Content: blank           │
│   左: rated X             │    │   按2选右"              │    │ Duration: 500 ms         │
│   右: rated Y             │    │ Duration: until key      │    │ Response: none           │
│ Duration: until key      │    │ Response: 1=左, 2=右     │    │ Condition: none          │
│ Response: none           │    │ Condition: {comparison}  │    │ Data: none               │
│ Condition: {comparison}  │    │ Data: choice, rt          │    └──────────────────────────┘
│ Data: left_img, right_img│    └──────────────────────────┘
└──────────────────────────┘
```

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| 实验名称 | 评分转选择任务 |
| 平台 | PsychoPy |
| 刺激类型 | 抽象画图片 |
| 刺激数量 | 30张 |
| 评分量表 | 1-5分（喜好度） |
| 评分标签 | 1=非常不喜欢, 5=非常喜欢 |
| 对比规则 | 评分差 ≥ 2 |
| 每种对比类型试次数 | 8（左右位置各半） |
| 缺失等级处理 | 跳过包含该等级的所有对比类型 |
| 显示模式 | 全屏 |

### Missing Information

1. 对比类型的具体列表未明确——评分差≥2可能包含"1v3, 1v4, 1v5, 2v4, 2v5, 3v5"等，需确认是否全部纳入还是仅选择部分
2. 评级阶段图片呈现顺序未指定——随机顺序还是固定顺序？是否所有被试使用相同顺序？
3. 选择阶段若某对比类型可用图片对数量不足8对，是重复使用还是减少试次？重复使用时同一图片对是否可多次出现？

### Critical Assumptions

- 假设评分差≥2的对比类型默认包含所有可能组合（1v3, 1v4, 1v5, 2v4, 2v5, 3v5），而非仅相邻等级差为2的组合
- 假设评级阶段无反馈，选择阶段也无试次间反馈（仅记录选择数据）
- 假设选择阶段每种对比类型固定8个试次，左右位置在试次内随机化（各占50%），而非用条件文件预先指定

### Code Architecture

```
rating_to_choice.py
├── 实验初始化（窗口全屏、时钟、颜色、字体）
├── 参数配置（n_images=30, rating_scale=1-5, min_rating_diff=2, n_trials_per_comparison=8）
├── 加载刺激图片列表（从指定文件夹或条件文件读取文件名）
├── Phase 1: 评分阶段
│   ├── 随机化图片呈现顺序
│   ├── 逐试次循环（30 trials）
│   │   ├── Window 1: 呈现图片（until keypress 跳过 → Window 2）
│   │   ├── Window 2: 呈现评分量表 + 记录按键（1-5）和 RT
│   │   ├── Window 3: ITI（500 ms）
│   │   └── 将 {image, rating, rt} 存入 rating_data 列表
│   └── 构建评级分布：统计每个等级的图片列表
├── Phase 2: 选择阶段
│   ├── 构建对比类型列表：根据 rating_data 和 min_rating_diff 生成所有有效对比
│   ├── 过滤：跳过任一等级无图片的对比类型
│   ├── 动态构建试次列表（每种对比 × n_trials_per_comparison）
│   │   ├── 每个试次随机选取对应等级的各1张图片
│   │   ├── 随机化左右位置（50% 概率交换）
│   │   └── 若某对比类型可用配对不足，按最大可用配对数生成试次
│   ├── 随机化试次顺序
│   └── 逐试次循环
│       ├── Window 1: 呈现左右图片对（until keypress → Window 2）
│       ├── Window 2: 呈现选择提示 + 记录按键（1/2）和 RT
│       ├── Window 3: ITI（500 ms）
│       └── 将 {left_img, right_img, left_rating, right_rating, comparison_type, choice, rt} 存入 choice_data 列表
├── 数据保存（.csv）
│   ├── rating_data.csv（phase, trial, image, rating, rt）
│   └── choice_data.csv（phase, trial, left_img, right_img, left_rating, right_rating, comparison_type, choice, rt）
└── Escape 退出检查（每个窗口均检查）
```

### Expected Data Columns

Phase 1 — 评分阶段：

| Column | Type | Description |
|--------|------|-------------|
| participant_id | str | 被试编号 |
| phase | str | "rating" |
| trial_index | int | 评分阶段试次序号（1-30） |
| image | str | 图片文件名 |
| rating | int | 评分值（1-5） |
| rt | float | 评分反应时（毫秒） |

Phase 2 — 选择阶段：

| Column | Type | Description |
|--------|------|-------------|
| participant_id | str | 被试编号 |
| phase | str | "choice" |
| trial_index | int | 选择阶段试次序号 |
| left_image | str | 左侧图片文件名 |
| right_image | str | 右侧图片文件名 |
| left_rating | int | 左侧图片在评分阶段的评价值 |
| right_rating | int | 右侧图片在评分阶段的评价值 |
| comparison_type | str | 对比类型（如 "1v3", "2v4"） |
| rating_diff | int | 评分差绝对值 |
| choice | int | 选择结果（1=左, 2=右） |
| rt | float | 选择反应时（毫秒） |
