# Bilingual (Blocked) Stroop Task

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/bilingual_stroop) · PsychoJS

## When to Use

User mentions: Bilingual Stroop, blocked Stroop, cross-language Stroop, 双语斯特鲁普. A variant of the classic Stroop task using blocked language conditions to compare the magnitude of Stroop interference across a participant's native and non-native languages.

## Core Logic

Participants report the display color of words while ignoring their semantic meaning, which may be congruent or incongruent with the ink color. The bilingual blocked version presents two language blocks — one in each language (e.g., English and Maori). The key prediction is that the Stroop effect (incongruent RT – congruent RT) will be larger in the more fluent language, because word reading is more automatic in that language, producing greater interference with color naming.

**Counterbalancing**: Participants are assigned to Group A or Group B at experiment start. Group A sees Language 1 first, then Language 2; Group B sees the reverse order. This controls for order effects.

**Block structure**: For each language, a block-level instruction screen explains the task in that language. Then a trial loop presents the stimuli. Two separate condition files (`english.xlsx` and `maori.xlsx`, or equivalent for your languages) define the stimuli for each language block.

**Trial structure**: fixation → color-word stimulus (the word in its ink color) → keypress response → ITI. Participants press one of three keys to indicate the ink color (e.g., 'r' for red, 'g' for green, 'b' for blue). The same three-key mapping is used across both language blocks; only the word language changes.

**Stimuli**: Color words (e.g., RED, GREEN, BLUE) presented in colored ink. Each trial is classified by: language (L1 vs L2), word meaning (color name), ink color, and congruency (congruent: word = ink; incongruent: word != ink).

## Must Confirm

- **Language pair**: Which two languages? (e.g., English/Maori, Chinese/English, French/German)
- **Color set**: Which ink colors? How many? (typically 3: red, green, blue)
- **Response keys**: Which keys map to which colors? (e.g., r/g/b for red/green/blue)
- **Counterbalancing**: Between-subjects (Group A/B) or within-subjects (all participants do both orders)?
- **Trial count per block**: How many trials per language? Congruency ratio? (50:50 or with neutral trials?)
- **Practice**: Practice before each language block, or one combined practice at the start?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Stroop Stimulus          │    │ Feedback (optional)      │    │ ITI                      │
│ Content: +               │    │ Content: color word       │    │ Content: correct/incorrect│   │ Content: blank           │
│ Duration: 500-1000 ms    │    │ Duration: until key      │    │ Duration: 500 ms         │    │ Duration: 500-1000 ms    │
│ Response: none           │    │ Response: r/g/b keys     │    │ Response: none           │    │ Response: none           │
│ Condition: none          │    │ Condition: {lang, word,  │    │ Condition: none          │    │ Condition: none          │
│ Data: none               │    │  ink_color, congruency}  │    │ Data: none               │    │ Data: none               │
└──────────────────────────┘    │ Data: rt, key, acc       │    └──────────────────────────┘    └──────────────────────────┘
                                └──────────────────────────┘
```

## Data Analysis

Compare the Stroop interference effect (incongruent RT – congruent RT) between language conditions. Use a 2 (language: fluent vs. less fluent) x 2 (congruency: congruent vs. incongruent) repeated-measures ANOVA. The interaction term tests whether the Stroop effect differs by language. Follow up with simple effects tests. Also report accuracy (error rate) as a secondary measure.

## References

Stroop, J. R. (1935). Studies of interference in serial verbal reactions. *Journal of Experimental Psychology, 18*(6), 643–662. https://doi.org/10.1037/h0054651

## Do Not Assume

- Do not assume the two languages use the same color words — verify the exact word set for each language (e.g., English: RED/GREEN/BLUE; Chinese: 红/绿/蓝). Different languages may use different numbers of words or different translation conventions.
- Do not assume a single condition file drives both language blocks — the bilingual blocked design typically uses two separate condition files (one per language). Confirm whether the user has prepared both files before generating code.
- Do not assume counterbalancing is done via random assignment — the Pavlovia demo uses explicit Group A/B assignment at runtime. Confirm whether between-subjects counterbalancing (group assignment) or within-subjects (all participants see both orders) is preferred.
- Do not assume the response key mapping is identical across languages — while the standard design uses the same three-key mapping for both blocks, some designs may use different key mappings per language (e.g., first-letter mapping in each language). Confirm explicitly.
- Do not assume neutral trials exist — the standard bilingual Stroop uses only congruent and incongruent trials (50:50). If the user wants neutral trials (e.g., colored squares or non-color words), the condition file and analysis must be adjusted.
- Do not assume the Stroop effect direction — in the less fluent language, the interference effect may be reduced or even reversed. The analysis should handle both possibilities rather than assuming a fixed direction.

## Condition File Columns

Columns in the xlsx/csv file that drives each trial (one file per language):

| Column | Type | Description |
|--------|------|-------------|
| word | str | 颜色词文本（如 `RED`、`红`） |
| ink_color | str | 墨水颜色名称（如 `red`、`red`） |
| congruency | str | `"congruent"` 或 `"incongruent"` |

## Variants

- **经典双语组块 Stroop（Classic Bilingual Blocked Stroop）**：两个语言各为一个独立 block，block 内包含一致和不一致试次。参与者按固定或被试间平衡的顺序完成两个语言 block。详见本文件。
- **混合双语 Stroop（Mixed Bilingual Stroop）**：两种语言的试次在同一个 block 内随机混合呈现。相比组块设计，混合设计可以考察语言切换成本对 Stroop 效应的调节作用。代码生成时需在条件文件中增加 `language` 列以标记每个试次的语言。
- **情绪双语 Stroop（Emotional Bilingual Stroop）**：将 Stroop 刺激替换为情绪词（正面/负面/中性），考察双语者对情绪词的注意偏向及其跨语言差异。需额外确认情绪词词库和效价评分。可参考情绪 Stroop 相关范式文件。

## Example

### User Request

> "我要做一个双语Stroop实验。两种语言是中文和英文，中文作为母语，英文作为第二语言。颜色有红、绿、蓝三种，按键用r/g/b对应颜色。每个语言block 60个试次，一致和不一致各30个。采用被试间平衡，一半先做中文后做英文，一半反过来。实验前有一个统一的练习block（12个试次）。用PsychoPy实现。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ 注视点                   │    │ Stroop 刺激              │    │ 反馈（仅练习阶段）       │    │ 试次间隔                 │
│ Content: +               │    │ Content: 颜色词           │    │ Content: 正确/错误       │    │ Content: 空白            │
│ Duration: 500 ms         │    │ Duration: 直到按键       │    │ Duration: 500 ms         │    │ Duration: 500-800 ms     │
│ Response: 无             │    │ Response: r/g/b 键       │    │ Response: 无             │    │ Response: 无             │
│ Condition: 无            │    │ Condition: {word,        │    │ Condition: 无            │    │ Condition: 无            │
│ Data: 无                 │    │  ink_color, congruency,  │    │ Data: 无                 │    │ Data: 无                 │
│                          │    │  language}               │    │                          │    │                          │
│                          │    │ Data: rt, key, acc       │    │                          │    │                          │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | 内容 | 持续时间 | 反应 | 条件 | 数据 |
|--------|------|----------|------|------|------|
| 注视点 | + | 500 ms | 无 | 无 | 无 |
| Stroop 刺激 | 颜色词（红/绿/蓝 或 RED/GREEN/BLUE） | 直到按键（无截止时间） | r/g/b 键 | {word, ink_color, congruency, language} | rt, key, acc |
| 反馈 | 正确/错误（仅练习） | 500 ms | 无 | 无 | 无 |
| ITI | 空白 | 500-800 ms 随机 | 无 | 无 | 无 |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| 实验名称 | 中英双语 Stroop 任务 |
| 平台 | PsychoPy |
| 任务类型 | 双语组块 Stroop（Bilingual Blocked Stroop） |
| 语言1（母语） | 中文（红、绿、蓝） |
| 语言2（第二语言） | 英文（RED、GREEN、BLUE） |
| 颜色集 | 红、绿、蓝（red、green、blue） |
| 反应按键 | r→红/red, g→绿/green, b→蓝/blue |
| 每语言试次数 | 60（30 congruent + 30 incongruent） |
| 平衡方式 | 被试间：Group A 先中后英，Group B 先英后中 |
| 练习试次 | 12 个（统一练习） |
| 阶段 | 指导语 → 练习(12) → Block1(60) → Block2(60) → 结束 |

### Missing Information

1. 指导语内容未说明 → 需确认中文和英文 block 前的指导语具体内容（是否用对应语言呈现指导语？）
2. 反馈阶段未提及 → 已假设仅练习阶段有反馈，正式阶段无反馈（标准 Stroop 做法）
3. 练习阶段的试次构成未说明 → 需确认练习是双语混合还是仅用一种语言？一致/不一致比例？

### Critical Assumptions

- 练习 block 使用双语混合试次（中文和英文各半），帮助参与者熟悉两种语言的按键映射
- 正式 block 无试次级反馈，仅 block 间有短暂休息提示
- 按键映射在两种语言 block 中保持一致（r/g/b 对应三种颜色），不随语言变化
- 刺激以随机顺序呈现，无连续 3 个以上相同一致性的试次
- 无反应截止时间（response-terminated），参与者按键后立即进入下一窗口

### Code Architecture

```
bilingual_stroop.py
├── 参数定义（语言顺序、颜色映射、按键、试次数、时间参数）
├── 窗口设置（全屏/窗口、背景色、单位）
├── 刺激预加载（TextStim × 2：中文和英文颜色词；Polygon 注视点）
├── 条件文件加载（chinese.xlsx, english.xlsx）
├── 被试分组（奇偶编号 → Group A/B）
├── 实验阶段：
│   ├── 指导语（通用 + 语言特定）
│   ├── 练习 block（12 试次，有反馈）
│   │   ├── 注视点（500 ms）
│   │   ├── Stroop 刺激（直到按键）
│   │   ├── 反馈（500 ms）
│   │   └── ITI（500-800 ms 随机）
│   ├── Block 1（按分组顺序的第一个语言，60 试次）
│   │   ├── Block 指导语
│   │   └── 试次循环（注视点 → 刺激 → ITI）
│   └── Block 2（按分组顺序的第二个语言，60 试次）
│       ├── Block 指导语
│       └── 试次循环（注视点 → 刺激 → ITI）
├── 数据保存：try/finally + 逐行写入 CSV
└── 结束画面
```

### Expected Data Columns

| Column | Type | Description |
|--------|------|-------------|
| participant | str | 被试编号 |
| group | str | 分组（A 或 B） |
| language | str | 试次语言（`"chinese"` 或 `"english"`） |
| block_type | str | 阶段类型（`"practice"` 或 `"formal"`） |
| block_num | int | Block 编号（1 或 2，练习为 0） |
| trial_num | int | Block 内试次编号 |
| word | str | 呈现的颜色词文本 |
| ink_color | str | 墨水颜色名称 |
| congruency | str | 一致性（`"congruent"` 或 `"incongruent"`） |
| correct_key | str | 正确按键（`"r"` / `"g"` / `"b"`） |
| key_pressed | str | 参与者实际按键 |
| rt | float | 反应时（ms） |
| acc | int | 正确率（1 = 正确，0 = 错误） |
