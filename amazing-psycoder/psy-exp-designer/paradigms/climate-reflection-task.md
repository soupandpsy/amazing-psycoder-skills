# Climate Reflection Task

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/climate_reflection_task) · PsychoJS

## When to Use

User mentions: Climate reflection, environmental attitudes, climate change engagement, climate beliefs, 气候反思任务, 环境态度. A two-phase questionnaire paradigm designed to explore how exposure to climate information influences participants' engagement with and attitudes toward climate change issues.

## Core Logic

This is a reflection-and-reassessment paradigm, not a reaction-time task. It consists of three sequential phases:

**Phase 1 — Free Response**: Participants are presented with a series of open-ended questions about climate change from a spreadsheet (`climate_change_questions.xlsx`). Each question appears individually, and participants type their answer using a text input box (Enter to submit). All typed answers are stored as `answer.text`.

**Phase 2 — Information Exposure**: Participants read an informational passage about climate change, presented as a static text screen. This serves as the experimental manipulation — the content can be varied (e.g., scientific consensus information, personal impact narratives, solutions-focused messages) to test different intervention framings.

**Phase 3 — Reflection**: An introduction screen explains that participants will now review their previous answers. The second loop (`response_loop`) re-presents each original question alongside the participant's own Phase 1 answer. A slider component allows participants to rate how much they agree with their previous response on a continuous scale. This measures whether exposure to the informational passage shifted their attitudes toward their prior beliefs.

**Cross-phase data linkage**: The participant's typed answer from Phase 1 is stored and re-displayed during Phase 2/3. This requires tracking which answer corresponds to which question across experimental phases — a design pattern for any reflection/reassessment paradigm regardless of topic.

**Key measures**:
- Agreement ratings (do participants still stand by their original answers?)
- Pre-post shift in agreement (reflection ratings as a function of information exposure)
- Answer content analysis (qualitative coding of Phase 1 free responses)
- Individual differences in receptivity to climate information

## Must Confirm

- **Questions**: What climate change questions to ask? (e.g., beliefs about causes, personal concern, policy support, behavioral intentions)
- **Informational passage**: What content to present between phases? Scientific consensus text, narrative stories, statistical data, or multiple conditions?
- **Number of questions**: How many? (typically 5–10 for reasonable task duration)
- **Rating scale**: Continuous slider (0–100) or Likert scale (e.g., 1–7)?
- **Topic flexibility**: Climate change topic only, or adaptable to other attitude domains (vaccine beliefs, political attitudes, etc.)?
- **Control condition**: Include a no-information control group, or within-subjects pre-post only?

## Trial Window Timeline

```text
Phase 1 — Free Response:
┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │
│ Question                 │    │ Text Response            │
│ Content: question text   │    │ Content: text input box  │
│ Duration: until Enter    │    │ Duration: until Enter    │
│ Response: none           │    │ Response: free text      │
│ Data: this_question      │    │ Data: answer.text        │
└──────────────────────────┘    └──────────────────────────┘

Phase 2 — Information:
┌──────────────────────────┐
│ Information Passage      │
│ Content: climate text    │
│ Duration: self-paced     │
│   (press key to continue)│
│ Response: any key        │
│ Data: reading_time       │
└──────────────────────────┘

Phase 3 — Reflection:
┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │
│ Question + Prior Answer  │    │ Agreement Rating         │
│ Content: question +      │    │ Content: slider          │
│   "You answered: {text}" │    │   (0 = completely disagree│
│ Duration: self-paced     │    │    100 = completely agree)│
│ Response: none           │    │ Duration: until response │
│ Data: this_question,     │    │ Response: slider drag    │
│   previous_answer        │    │ Data: slider.response    │
└──────────────────────────┘    └──────────────────────────┘
```

## Data Analysis

Primary analysis compares agreement ratings across questions. Examine whether agreement shifts systematically after information exposure. Analyze free-text responses (Phase 1) using qualitative content analysis or NLP topic modeling. Test individual difference moderators (political orientation, environmental values, science literacy) on agreement change. Compare different information conditions (if multiple passages are used between subjects).

## References

Developed as part of climate change engagement research using the PsychoJS platform. Adaptable to any domain requiring reflection on prior beliefs after information exposure.

## Do Not Assume

- Do not assume the informational passage is the same for all participants — between-subjects manipulation with different passage types (e.g., 科学共识, 个人叙事, 解决方案导向) is the core experimental design; a single-passage within-subjects design weakens causal inference.
- Do not assume participants will fully read the informational passage — reading time must be recorded (`reading_time`) as a manipulation check; participants who skim or skip the passage dilute the experimental manipulation.
- Do not assume the reflection rating uses a 0–100 continuous slider — some implementations use Likert scales (e.g., 1–7) or bipolar scales (−3 to +3); the scale type affects whether parametric or non-parametric analyses are appropriate.
- Do not assume all Phase 1 questions must reappear in Phase 3 — some designs include filler questions that are asked but not reflected upon, or randomly sample a subset for reflection to reduce demand characteristics.
- Do not assume the topic is climate change — the paradigm structure (自由回答 → 信息暴露 → 反思重评) is domain-general and equally applicable to vaccine attitudes, political beliefs, AI risk perception, or any attitude object.
- Do not assume Phase 2 always precedes Phase 3 — some control-group designs place the informational passage after reflection (Phase 2 and Phase 3 swapped) to establish a no-exposure baseline.

## Condition File Columns

Columns in the xlsx/csv file that drives each trial:

| Column | Type | Description |
|--------|------|-------------|
| question_id | str | 问题唯一标识符，用于跨阶段数据链接（如 `"Q01"`, `"Q02"`） |
| question_text | str | Phase 1 和 Phase 3 呈现的问题文本 |
| question_category | str | 问题类别（如 `"belief"`, `"concern"`, `"policy"`, `"behavior"`），用于分维度分析 |

## Variants

### 多信息条件变体

将被试随机分配到不同的信息短文条件（如科学共识组 vs. 个人叙事组 vs. 中性对照组），Phase 2 根据分组呈现不同内容。核心问题是不同信息框架对态度改变的差异化影响。条件分配需在实验前通过随机化或拉丁方确定。

### 通用态度反思任务

将气候议题替换为其他态度对象（疫苗态度、政治态度、AI风险感知等），保持相同的 "自由回答 → 信息暴露 → 反思重评" 三阶段结构。问题集和信息短文内容随主题变化，但代码架构完全复用。可参考 [rating.md](rating.md) 了解单次态度评分的范式差异。

### 简化双阶段变体

省略 Phase 1 的自由回答环节，直接让被试阅读信息短文后进行 Likert 态度评分（即仅保留 Phase 2 + Phase 3 的评分部分）。适用于只需测量态度变化方向而非反思深度的场景。代码更简单，但失去了文本分析的数据维度。

## Example

### User Request

> "我想做一个气候反思实验。被试先回答5个关于气候变化的问题（比如你相信气候变化正在发生吗？你愿意改变生活习惯吗？等等），每个问题单独显示，用文本框输入答案，按回车提交。然后所有被试阅读一段科学共识短文（介绍97%气候科学家认同人类活动导致全球变暖）。之后重新呈现每个问题，同时显示被试之前自己的答案，让被试用一个0-100的滑块评价自己有多同意之前的回答（0=完全不同意, 100=完全同意）。5个问题随机顺序呈现。用PsychoPy。被试为大学生，在macOS上运行。"

### Trial Window Timeline

```text
Phase 1 — Free Response (循环5题):
┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │
│ 问题呈现                  │    │ 文本输入                  │
│ Content: {question_text} │    │ Content: 文本框           │
│ Duration: self-paced     │    │ Duration: until Enter     │
│ Response: none           │    │ Response: free text       │
│ File: none               │    │ File: none               │
│ Condition: {question_id} │    │ Condition: {question_id} │
│ Data: question_id        │    │ Data: answer.text        │
└──────────────────────────┘    └──────────────────────────┘

Phase 2 — Information (全被试统一):
┌──────────────────────────┐
│ 信息短文                  │
│ Content: 科学共识短文      │
│ Duration: self-paced     │
│   (按任意键继续)           │
│ Response: any key        │
│ Data: reading_time       │
└──────────────────────────┘

Phase 3 — Reflection (循环5题):
┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │
│ 问题 + 先前回答           │    │ 一致性评分                │
│ Content: {question_text} │    │ Content: 滑块 0-100      │
│   "你之前的回答：{text}"   │    │ Duration: until response │
│ Duration: self-paced     │    │ Response: slider drag    │
│ Response: key to continue│    │   + click to confirm     │
│ Condition: {question_id} │    │ Condition: {question_id} │
│ Data: question_id,       │    │ Data: agreement_rating   │
│   previous_answer        │    │                          │
└──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | File/Folder | Condition | Data |
|--------|---------|----------|----------|-------------|-----------|------|
| P1-问题 | {question_text} | self-paced (任意键) | none | none | {question_id} | question_id |
| P1-输入 | 文本框 | until Enter | 自由文本 | none | {question_id} | answer.text |
| P2-短文 | 科学共识短文 | self-paced (任意键) | any key | none | none | reading_time |
| P3-回顾 | {question_text} + "你之前的回答：{text}" | self-paced (任意键) | none | none | {question_id} | question_id, previous_answer |
| P3-评分 | 滑块 0-100 | until confirm | slider drag + click | none | {question_id} | agreement_rating |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| 实验名称 | 气候反思任务（科学共识条件） |
| 平台 | PsychoPy |
| 任务类型 | Climate Reflection Task（态度反思重评） |
| 问题数量 | 5 题（随机顺序） |
| 问题内容 | 气候变化信念、个人关注、生活习惯、政策支持、行为意愿 |
| 信息条件 | 单一条件（科学共识短文），全被试统一 |
| Phase 1 输入方式 | 文本框，Enter 提交 |
| Phase 3 评分方式 | 连续滑块 0–100，拖动后点击确认 |
| 被试群体 | 大学生 |
| 操作系统 | macOS（字体：PingFang） |
| 实验阶段 | 指导语 → Phase 1(5题) → Phase 2(短文) → Phase 3(5题) → 结束 |

### Missing Information

1. 信息短文的具体内容未提供 — 需要完整文本（约200–500字）或确认是否由实验者自行准备
2. 滑块确认方式未明确 — 是拖动即记录还是需要点击"确认"按钮？当前假定为拖动后点击确认
3. Phase 3 中是否允许被试修改之前的回答？当前假定仅评分、不可修改原答案

### Critical Assumptions

- 5个问题在 Phase 1 和 Phase 3 中各呈现一次，Phase 1 顺序随机化，Phase 3 使用相同随机顺序以保证被试能一一对应
- 信息短文为单一条件，无被试间随机分组；若需多条件比较，需扩展为被试间设计
- 文本框输入不做字数限制，但建议在指导语中提示"不少于20字"以保证回答质量
- 滑块初始位置设为 50（中性），避免初始值对被试评分产生锚定效应

### Code Architecture

```
climate_reflection.py
├── 导入模块（psychopy.gui, visual, event, data, core）
├── 参数配置（窗口大小、字体、颜色、问题文件路径、短文文本）
├── 窗口初始化（全屏/窗口，背景色）
├── 读取问题文件（conditions.xlsx → question_id, question_text）
├── 问题顺序随机化
├── Phase 1 — 自由回答循环：
│   ├── 显示问题文本
│   ├── 文本输入框（visual.TextBox2 / 自定义 text input）
│   ├── 监听 Enter 键提交
│   └── 记录 answer.text + question_id + rt_phase1
├── Phase 2 — 信息短文：
│   ├── 显示短文文本（visual.TextStim，多行）
│   ├── 监听任意键继续
│   └── 记录 reading_time
├── Phase 3 — 反思评分循环：
│   ├── 显示问题文本 + "你之前的回答：{answer.text}"
│   ├── 显示滑块（visual.Slider, 0–100, 初始=50）
│   ├── 监听滑块拖动 + 确认点击
│   └── 记录 agreement_rating + rt_phase3
├── 结束界面
├── 数据保存：try/finally CSV，增量写入
│   ├── 基础列：participant, date, expName
│   ├── Phase 1 列：question_id, answer_text, rt_phase1
│   ├── Phase 2 列：reading_time
│   └── Phase 3 列：agreement_rating, rt_phase3
```

### Expected Data Columns

| Column | Type | Description |
|--------|------|-------------|
| participant | str | 被试编号 |
| question_id | str | 问题编号（跨阶段匹配键） |
| question_text | str | 问题文本 |
| question_category | str | 问题类别 |
| answer_text | str | Phase 1 自由回答文本 |
| rt_phase1 | float | Phase 1 回答反应时（ms） |
| reading_time | float | Phase 2 短文阅读时间（ms） |
| agreement_rating | float | Phase 3 一致性评分（0–100） |
| rt_phase3 | float | Phase 3 评分反应时（ms） |
