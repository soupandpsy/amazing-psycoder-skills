# Numerical Stroop Task

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/numerical_stroop) · reference

## When to Use

User mentions: Numerical Stroop, number Stroop, physical vs. semantic comparison, Henik task, 数字斯特鲁普. A variant of the Stroop task using numerical magnitude comparison, measuring interference between the physical size and semantic value of digits.

## Core Logic

Participants compare two numbers and indicate which is "greater" under two different task conditions. In semantic trials, participants must choose the numerically larger number while ignoring the physical size of the digits (e.g., the digit "3" printed in large font vs. "5" in small font — the correct answer is "5" based on value, ignoring size). In physical trials, participants must choose the physically larger number while ignoring its numerical value (e.g., large "3" vs. small "5" — the correct answer is "3" based on size, ignoring value).

Congruent trials are those where physical size and numerical value align (e.g., large "5" vs. small "3" — "5" is both physically and numerically larger). Incongruent trials create conflict between the two dimensions (e.g., large "3" vs. small "5"). The key prediction is that incongruent trials produce longer RTs than congruent trials, with larger interference effects in the semantic task (reflecting the automatic, difficult-to-suppress processing of numerical magnitude).

This is a close replication of Henik & Tzelgov (1982). The task is organized into blocks, each driven by a row in `blockDefinitions.xlsx` specifying the instruction text, practice condition file, and main condition file. This allows easy switching between semantic and physical comparison blocks within a single experiment.

Each trial follows a precisely timed sequence: fixation cross ("+") at center for 100 ms, then at 200 ms two number stimuli appear simultaneously at positions (-0.075, 0) and (0.075, 0) in height units. The key manipulation is that each trial condition provides four parameters: `number1`/`number2` (the digit strings) and `size1`/`size2` (the physical font heights). In congruent trials the physically larger digit is also numerically larger; in incongruent trials the physically larger digit is numerically smaller, creating response conflict. Participants respond with 'a' (left) or 'k' (right). Practice trials show 1s feedback ("Correct!" or "Oops! That was wrong"); main trials proceed without feedback.

## Must Confirm

- **Task conditions**: Both semantic ("which is numerically larger?") and physical ("which is physically larger?") conditions, or just one?
- **Blocking**: Conditions blocked (one instruction per block) or interleaved?
- **Stimulus pairs**: Which digit pairs to use? (e.g., 1-9 with varying physical sizes)
- **Response keys**: 'a'/'k' (left/right), arrow keys, or other mapping?
- **Size manipulation**: How many physical size levels per digit? (e.g., two sizes creating congruent/incongruent/neutral)
- **Practice**: Include practice trials with feedback before each block?
- **Trial count**: How many trials per congruency condition per block?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Fixation                 │    │ Number Stimuli           │    │ Feedback (practice only)  │
│ Content: + at center     │    │ Content: two digits      │    │ Content: "Correct!" or    │
│ Duration: 100 ms         │    │ at different font sizes  │    │ "Oops! That was wrong"    │
│ Response: none           │    │ positions: ±0.075        │    │ Duration: 1 s              │
│ Data: none               │    │ starts at t=200 ms       │    │ Response: none            │
│                          │    │ Duration: until response │    │ Data: none                │
│                          │    │ Response: 'a' or 'k' key│    │                           │
│                          │    │ Data: rt, key, acc       │    │                           │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

## Data Analysis

Compare mean RT for congruent vs. incongruent trials within each task condition (semantic, physical). Expect larger interference in semantic comparison. Use a 2 (task: semantic vs. physical) x 2 (congruency: congruent vs. incongruent) repeated-measures ANOVA. Analyze the interaction to determine the locus of the numerical Stroop effect.

## References

Henik, A., & Tzelgov, J. (1982). Is three greater than five: The relation between physical and semantic size in comparison tasks. *Memory & Cognition, 10*(4), 389–395. https://doi.org/10.3758/BF03202431

Stroop, J. R. (1935). Studies of interference in serial verbal reactions. *Journal of Experimental Psychology, 18*(6), 643–662. https://doi.org/10.1037/h0054651

## Do Not Assume

- Do not assume the task order (semantic first, then physical) is fixed — the Henik & Tzelgov (1982) original design uses blocked conditions with a fixed order, but some replications counterbalance the order across participants. Confirm whether the user wants counterbalanced blocks or a fixed sequence.
- Do not assume the same size-level mapping applies to all digits — in the standard design, each digit pair uses two physical sizes (large/small) that create congruent and incongruent pairings. If the user wants more than two size levels (e.g., small/medium/large to create neutral trials), the condition file structure and analysis must be adjusted accordingly.
- Do not assume digit pairs use single-digit numbers only — the standard Numerical Stroop uses digits 1–9, but some variants use two-digit numbers (e.g., 12 vs. 24) to investigate numerical distance effects. Confirm the digit range before generating the condition file.
- Do not assume "a" and "k" are the default response keys — the Pavlovia demo uses 'a'/'k' for left/right responses, but the user may prefer arrow keys, 'f'/'j', or another mapping. Always confirm the response key layout.
- Do not assume practice trials use the same condition file as formal trials — in the Pavlovia demo, practice and main blocks have separate condition files (`numstroop_practice_sem.xlsx` vs. `numstroop_main_sem.xlsx`). Confirm whether the user has prepared separate practice condition files or expects them to be automatically generated.
- Do not assume the interference effect is symmetric — the semantic interference effect (physical size interfering with numerical judgment) is typically larger than the reverse (numerical value interfering with physical size judgment). The analysis code should handle both within-task and between-task comparisons without assuming the direction of asymmetry.

## Condition File Columns

Columns in the xlsx/csv file that drives each trial (one file per task condition):

| Column | Type | Description |
|--------|------|-------------|
| number1 | int/str | 左侧呈现的数字（如 `3`、`5`） |
| number2 | int/str | 右侧呈现的数字（如 `5`、`3`） |
| size1 | float | 左侧数字的物理字号高度（如 `0.1`、`0.08`） |
| size2 | float | 右侧数字的物理字号高度（如 `0.08`、`0.1`） |
| congruency | str | `"congruent"`（物理大小与数值大小一致）或 `"incongruent"`（物理大小与数值大小冲突） |

## Variants

- **经典数值 Stroop（Classic Numerical Stroop）**：基于 Henik & Tzelgov (1982) 的原始设计，参与者分别完成语义比较（判断哪个数字数值更大）和物理比较（判断哪个数字物理尺寸更大）两个组块任务。每个组块内包含一致和不一致试次。详见本文件。
- **大小一致性任务（Size Congruity Task）**：数值 Stroop 的泛化版本，使用其他可量化维度（如面积、亮度、数量）替代物理字号，考察不同维度间的一致性效应。刺激参数（尺寸、亮度等）需在条件文件中以额外列的方式定义，代码需适配多维度刺激呈现。可参考 Eriksen Flanker 任务中刺激维度的定义方式。
- **发展性数值 Stroop（Developmental Numerical Stroop）**：针对儿童或特殊人群（如发展性计算障碍）的简化版本，通常使用更少的数字对（如 1–5 而非 1–9），更大的物理尺寸差异，并加入中性试次（neutral trials，两个数字物理尺寸相同但数值不同）以减少任务难度。需额外确认适用年龄段和数字范围。

## Example

### User Request

> "我要做一个数值Stroop实验。屏幕左右两边各呈现一个数字，两个数字物理大小不同。在语义任务中，被试判断哪个数字的数值更大，忽略物理大小；在物理任务中，判断哪个数字物理尺寸更大，忽略数值。数字使用1-9之间的数字对（排除相同数字配对），字体大小分大(0.12)和小(0.06)两种。每个任务block包含80个试次，一致/不一致各40个。先做语义block，后做物理block。每个block前有16个练习试次。按键用左右箭头键。用PsychoPy实现。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ 注视点                   │    │ 数字刺激对               │    │ 反馈（仅练习阶段）       │
│ Content: +               │    │ Content: 两个数字         │    │ Content: "正确！" 或     │
│ Duration: 100 ms         │    │ 分别以不同字号呈现        │    │ "哦哦，答错了！"          │
│ Response: 无             │    │ 位置: 左侧(-0.075,0)     │    │ Duration: 1000 ms        │
│ Condition: 无            │    │       右侧(0.075,0)      │    │ Response: 无             │
│ Data: 无                 │    │ Duration: 直到按键       │    │ Condition: 无            │
│                          │    │ Response: left/right 键  │    │ Data: 无                 │
│                          │    │ Condition: {number1,     │    │                          │
│                          │    │  number2, size1, size2,  │    │                          │
│                          │    │  congruency}             │    │                          │
│                          │    │ Data: rt, key, acc       │    │                          │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | 内容 | 持续时间 | 反应 | 条件 | 数据 |
|--------|------|----------|------|------|------|
| 注视点 | + | 100 ms | 无 | 无 | 无 |
| 数字刺激 | 两个数字（不同字号），左右并排呈现 | 直到按键（无截止时间） | 左箭头键 / 右箭头键 | {number1, number2, size1, size2, congruency, task_type} | rt, key, acc |
| 反馈 | "正确！" / "哦哦，答错了！"（仅练习） | 1000 ms | 无 | 无 | 无 |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| 实验名称 | 数值 Stroop 任务 |
| 平台 | PsychoPy |
| 任务类型 | 数值 Stroop（Numerical Stroop / Size Congruity Task） |
| 任务条件 | 语义比较（数值更大） + 物理比较（尺寸更大），组块呈现 |
| 数字范围 | 1–9（排除相同数字配对） |
| 物理尺寸 | 大字号（0.12）、小字号（0.06） |
| 反应按键 | 左箭头键（←）、右箭头键（→） |
| 每 block 试次数 | 80（40 congruent + 40 incongruent） |
| 任务顺序 | 固定：先语义后物理 |
| 练习试次 | 每 block 前 16 个 |
| 阶段 | 指导语 → 练习(语义, 16) → 语义 Block(80) → 休息 → 练习(物理, 16) → 物理 Block(80) → 结束 |

### Missing Information

1. 指导语内容未说明 → 需确认语义任务和物理任务各自的指导语具体措辞（如"请判断哪个数字的数值更大，按左或右键"）
2. ITI（试次间隔）未提及 → 需确认试次间是否有间隔时间及具体时长（200–500 ms 随机？还是直接进入下一个试次？）
3. Block 间休息未说明 → 需确认语义 block 结束后是否有休息提示，以及休息时长是否由被试自主控制

### Critical Assumptions

- ITI 默认为 300 ms（注视点出现前），与 Pavlovia 参考实现保持一致
- Block 间有自主控制休息提示（按空格键继续）
- 数字刺激从注视点偏移 200 ms 后呈现（同 Pavlovia 参考实现：注视点 100 ms → 空白 200 ms 后刺激出现）
- 左右位置与按键映射一致（左侧刺激对应左箭头键，右侧刺激对应右箭头键），刺激位置固定不随机交换
- 无反应截止时间（response-terminated），参与者按键后立即进入下一窗口

### Code Architecture

```
numerical_stroop.py
├── 参数定义（任务顺序、字号映射、按键、试次数、时间参数）
├── 窗口设置（全屏/窗口、背景色、单位=height）
├── 刺激预加载（TextStim × 2：左数字和右数字；多边形注视点 +）
├── 条件文件加载/生成（semantic_practice.xlsx, semantic_main.xlsx, physical_practice.xlsx, physical_main.xlsx）
├── 实验阶段：
│   ├── 指导语（通用 + 语义任务特定）
│   ├── 语义练习 block（16 试次，有反馈）
│   │   ├── 注视点（100 ms）
│   │   ├── 数字刺激对（200 ms 后呈现，直到按键）
│   │   ├── 反馈（1000 ms）
│   │   └── ITI（300 ms）
│   ├── 语义正式 block（80 试次，无反馈）
│   │   ├── Block 指导语
│   │   └── 试次循环（注视点 → 数字刺激 → ITI）
│   ├── 休息提示（按空格继续）
│   ├── 物理练习 block（16 试次，有反馈）
│   │   └── 同上结构
│   └── 物理正式 block（80 试次，无反馈）
│       └── 同上结构
├── 数据保存：try/finally + 逐行写入 CSV
└── 结束画面
```

### Expected Data Columns

| Column | Type | Description |
|--------|------|-------------|
| participant | str | 被试编号 |
| task_type | str | 任务类型（`"semantic"` 或 `"physical"`） |
| block_type | str | 阶段类型（`"practice"` 或 `"formal"`） |
| trial_num | int | Block 内试次编号 |
| number1 | int | 左侧数字的数值 |
| number2 | int | 右侧数字的数值 |
| size1 | float | 左侧数字的字号高度 |
| size2 | float | 右侧数字的字号高度 |
| congruency | str | 一致性（`"congruent"` 或 `"incongruent"`） |
| correct_side | str | 正确答案所在侧（`"left"` 或 `"right"`） |
| correct_key | str | 正确按键（`"left"` 或 `"right"`） |
| key_pressed | str | 参与者实际按键 |
| rt | float | 反应时（ms） |
| acc | int | 正确率（1 = 正确，0 = 错误） |
