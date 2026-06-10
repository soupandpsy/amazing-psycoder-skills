# Writing Distraction Task

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: Custom paradigm · PsychoPy

## When to Use

User mentions: Writing distraction, dual-task writing, distractor interference, writing under distraction, 书写干扰. A dual-task paradigm that measures the effect of visual distractors on ongoing text production, combining continuous typing performance with intermittent distractor exposure.

## Core Logic

Participants type a word or phrase while intermittently being shown distracting images. The paradigm measures how distraction disrupts the continuity, speed, and accuracy of ongoing text production. This task bridges motor production, working memory maintenance, and distractor suppression, making it relevant for studying real-world interference effects (e.g., writing while notifications appear).

**Trial structure** -- each trial has four sequential phases:

1. **Word display phase** (2 s minimum + typing): A target word is shown on screen. The participant must type at least a specified number of letters (`n_distract`) from the word. Once they type enough characters, the phase advances. If they haven't typed enough letters within 2 seconds, the phase continues until they do.

2. **Distractor phase** (1 s): A distractor image is displayed for exactly 1 second. The participant's typing is interrupted by this visual distractor. The text they had typed so far is preserved.

3. **Continue writing phase** (5 s maximum): The original text typed so far is restored, and the participant continues typing from where they left off. They have up to 5 seconds to complete the word. The phase ends when they finish typing or when the 5-second timeout expires.

4. **Question phase** (until Y/N response): A yes/no question about the trial is displayed (e.g., "Did you notice the distractor?"). The participant responds with Y or N key.

**Cross-phase state**: The typed text is carried across phases via experiment-level variables. During the distractor phase, the text input is hidden; it is then restored for the continue-writing phase. The final text string (from word display + continue writing) is the primary performance measure.

**Condition file** (`conditions.xlsx`): Each row specifies `this_word` (the target word), `n_distract` (number of letters to type before the distractor appears), the distractor image filename, and the post-trial question. No per-trial feedback is given.

## Must Confirm

- **Word stimuli**: What words to use? Word length, frequency, language?
- **Distractor images**: What type of distractors? (emotional, neutral, task-relevant, or varied IAPS images)
- **n_distract**: How many letters must be typed before the distractor appears? Fixed or variable?
- **Phase timing**: Duration of distractor display (1 s), continue-writing timeout (5 s), and minimum word display time (2 s)?
- **Question content**: What yes/no question follows each trial?
- **Response collection**: Keyboard for typing + keyboard for Y/N, or mouse for Y/N?
- **Trial count**: How many trials? From a fixed CSV or procedurally generated?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Phase 1                  │ →  │ Phase 2                  │ →  │ Phase 3                  │ →  │ Phase 4                  │
│ Show Word + Type         │    │ Show Distractor          │    │ Continue Writing         │    │ Question Response        │
│ Content: target word +   │    │ Content: distractor      │    │ Content: existing text + │    │ Content: question text   │
│ textbox with typed chars │    │ image                    │    │ editable textbox         │    │ Duration: until Y/N key  │
│ Duration: min 2 s, then  │    │ Duration: 1 s            │    │ Duration: max 5 s        │    │ Response: 'y' or 'n' key │
│ until n_distract chars   │    │ Response: none (typing   │    │ (advances on completion) │    │ Data: key_resp.keys      │
│ typed                    │    │ suppressed)               │    │ Response: keyboard typing│    │                           │
│ Response: keyboard       │    │ Data: none               │    │ Data: full typed text    │    │                           │
│ Data: initial typed text │    │                           │    │                           │    │                           │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

## Data Analysis

Primary measures: typing speed (characters per second) in the continue-writing phase vs. word-display phase, error rate (deviations from target word), and completion rate (whether the word was fully typed). Compare performance on trials with distractors vs. baseline (if included). Analyze whether certain distractor types (emotional vs. neutral) differentially impair writing continuity. Y/N question responses provide a secondary measure of distractor awareness. Individual differences in working memory capacity or attentional control may moderate distraction effects.

## References

No canonical reference yet -- this is a custom paradigm. Adapt analyses from dual-task interference literature (e.g., Pashler, 1994) and writing process research.

## Do Not Assume

- Do not assume 干扰呈现时间固定为 1 秒。部分变式要求干扰持续至被试恢复输入，或使用 staircase 调整干扰时长。务必确认干扰阶段的确切持续时间及是否可变。
- Do not assume 输入语言为英文。若目标词为中文，需处理输入法（IME）兼容性（候选词窗口可能遮挡刺激，输入组合键可能被误判为反应键），并明确使用 `keyboard.Keyboard` 收集字符而非 `event.getKeys`。
- Do not assume 干扰类型仅为图片。干扰物可能是闪烁文本、声音、视频片段或弹窗通知，需确认干扰刺激的模态与文件格式。
- Do not assume 每次试次后一定呈现问题阶段。部分变式仅在部分试次后提问（如随机抽取 25%），或完全省略问题以缩短实验时长。务必确认问题出现的频率和逻辑。
- Do not assume `n_distract` 为试次级变量。它可能作为全局固定参数（所有试次相同），此时无需在条件文件中逐行指定。
- Do not assume 书写阶段的输入框始终可见。在干扰阶段，输入框可能被隐藏、禁用或覆盖。需明确每个阶段输入框的可见性与可编辑状态，确保跨阶段文本状态传递正确。

## Condition File Columns

| Column | Type | Description |
|--------|------|-------------|
| this_word | str | 目标词，被试需输入的词语 |
| n_distract | int | 干扰出现前需输入的最少字符数 |
| distractor | str | 干扰图片文件名（含扩展名） |
| question | str | 试次后呈现的是/否问题文本 |

## Variants

- **文本干扰书写（Text-based distraction）**: 干扰物为屏幕上闪现的无关文字或词汇（而非图片），考察语义干扰对书写连续性的影响。刺激生成逻辑参见 [stroop.md](stroop.md) 的词汇干扰部分。
- **听觉干扰书写（Auditory distraction writing）**: 干扰刺激为听觉通道呈现（如突发噪音、无关语音），被试在打字的同时通过耳机接收干扰。需额外配置音频播放组件及声音文件路径，参见 [oddball.md](oddball.md) 的听觉刺激参数。
- **情绪干扰书写（Emotional distraction writing）**: 系统操控干扰物的情绪效价（负性 vs. 中性图片，通常选自 IAPS 或 CAPS 图片库），考察情绪显著性对书写中断的调节效应。条件文件需增加 `valence` 列标记干扰图片的情绪类别。

---

## Example

### User Request

> "我想做一个书写干扰实验。屏幕上方显示一个两字中文词，下方是输入框。被试开始打字，当打到第二个字的第一笔时，屏幕中央弹出一张干扰图片持续1秒，然后图片消失，被试继续打完这个词。试次结束后问'你是否注意到干扰图片？'按Y或N。共60个试次，词语从词表中随机抽取。用PsychoPy实现。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ 阶段1：词语呈现+初始输入    │ →  │ 阶段2：干扰呈现             │ →  │ 阶段3：继续书写             │ →  │ 阶段4：问题回答             │
│ Content: 目标词 + 输入框    │    │ Content: 干扰图片           │    │ Content: 已有文本 + 输入框   │    │ Content: 问题文本           │
│ Duration: 最少2 s,         │    │ Duration: 1 s              │    │ Duration: 最多5 s           │    │ Duration: 直到 Y/N 按键    │
│ 直到输入≥2个字符            │    │ Response: none (输入禁用)   │    │ (完成后自动结束)             │    │ Response: 'y' 或 'n' 键    │
│ Response: keyboard         │    │ Data: none                 │    │ Response: keyboard          │    │ Data: key_resp.keys        │
│ Data: 初始输入文本           │    │                            │    │ Data: 完整输入文本           │    │                             │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| 阶段 | Content | Duration | Response | File | Condition | Data |
|------|---------|----------|----------|------|-----------|------|
| 词语呈现+初始输入 | 目标词 + 文本输入框 | 最少2 s, 直到输入≥2个字符 | keyboard | none | {this_word} | 初始输入文本 |
| 干扰呈现 | 干扰图片 | 1 s | none（输入禁用） | {distractor} | none | none |
| 继续书写 | 已有文本 + 输入框 | 最多5 s（完成后结束） | keyboard | none | none | 完整输入文本 |
| 问题回答 | 问题文本 | 直到 Y/N 按键 | 'y', 'n' | none | {question} | key_resp.keys, rt |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| 实验名称 | 中文书写干扰任务 |
| 平台 | PsychoPy |
| 任务类型 | 书写干扰（双任务） |
| 目标刺激 | 两字中文词（从词表随机抽取） |
| 干扰刺激 | 图片文件 |
| 干扰触发条件 | 输入≥2个字符（第二个字第一笔） |
| 干扰呈现时长 | 1 s |
| 继续书写时限 | 5 s |
| 试次后问题 | "你是否注意到干扰图片？"（Y/N） |
| 试次数 | 60 |
| 阶段结构 | 词语呈现 → 干扰 → 继续书写 → 问题 |

### Missing Information

1. **词表未提供** — 未指定具体词语列表或词表文件路径。需明确使用哪个词表，或提供词条清单。
2. **干扰图片未指定** — 未说明干扰图片来源（IAPS编号 / 自定义图片文件夹路径），以及图片的情绪类别或内容类型。
3. **练习试次未提及** — 是否包含练习阶段？练习试次数及是否给予反馈未说明。

### Critical Assumptions

- 中文输入使用 `keyboard.Keyboard` 收集字符级输入，`event.getKeys` 无法正确处理中文输入法组合键。
- 干扰图片为全屏中央呈现，输入框位于屏幕下方，目标词位于上方。布局为默认上下排列。
- 60试次从词表中无放回随机抽取；若词表不足60词，则循环抽取（有放回）。

### Code Architecture

```
writing_distraction.py
├── 参数区（字符数阈值、阶段时长、窗口尺寸）
├── 条件文件生成（从词表随机抽取60个目标词，分配干扰图片与问题）
├── 刺激预加载（目标词TextStim、问题TextStim、干扰图片ImageStim）
├── 输入框组件（PsychoPy TextBox / 自定义文本累积组件）
├── 试次循环:
│   ├── 阶段1: 呈现目标词 + 启用输入框（最小2 s, 直到字符数≥阈值）
│   ├── 阶段2: 显示干扰图片1 s（禁用输入框，保存当前文本）
│   ├── 阶段3: 恢复输入框与已输入文本（最多5 s, 回车或字符数达标结束）
│   ├── 阶段4: 呈现问题，等待 Y/N 按键
│   └── 保存试次数据
├── 结束界面（致谢语）
└── 数据保存: try/finally CSV 增量写入
```

### Expected Data Columns

| Column | Type | Description |
|--------|------|-------------|
| this_word | str | 目标词 |
| n_distract | int | 干扰触发字符阈值 |
| distractor | str | 干扰图片文件名 |
| init_text | str | 阶段1结束时的已输入文本 |
| final_text | str | 阶段3结束时的完整输入文本 |
| correct | int | 最终文本是否与目标词完全匹配（1/0） |
| char_count_phase1 | int | 阶段1输入字符数 |
| char_count_phase3 | int | 阶段3输入字符数 |
| typing_speed_phase1 | float | 阶段1打字速度（字符/秒） |
| typing_speed_phase3 | float | 阶段3打字速度（字符/秒） |
| question_resp | str | 问题回答（'y' / 'n'） |
| question_rt | float | 问题反应时（秒） |
