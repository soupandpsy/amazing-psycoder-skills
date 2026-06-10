# Phone a Friend Task

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/phone_a_friend) · reference

## When to Use

User mentions: Phone a friend, hint task, cue validity, general knowledge task, ECSoP, 朋友求助任务. A general knowledge task where participants can optionally request hints ("phone a friend"), with half of the hints being correct and half incorrect. Measures trust in external information and the influence of cue validity on belief updating.

## Core Logic

Participants are presented with a series of general knowledge questions and respond by typing an answer. On each question, they may choose to "phone a friend" to receive a hint. Each participant has exactly 10 hint opportunities across the entire task, of which 5 hints are valid (correct) and 5 are invalid (incorrect), randomly interleaved. After receiving a hint, the participant may revise their answer.

The critical manipulation is the validity of the hints: participants do not know in advance whether a given hint is correct or incorrect, so they must decide when to trust external information. The task tracks whether participants are more likely to request hints for difficult questions, whether they incorporate hints into their answers, and whether they detect that some hints are systematically incorrect.

On each trial, participants see a question, an editable textbox for typing their answer, a "Phone a friend" button, and a call tracker showing remaining hints. The trial is open-ended: participants can either type an answer and press Enter to submit, or click the hint button to request a hint. If a hint is requested, the trial transitions to a hint display screen showing the question, the hint text (labeled as a friend's answer), and a new editable textbox. The participant then submits their final answer by pressing Enter.

The cue validity list is pre-shuffled at experiment start: exactly 5 valid and 5 invalid hints are randomly ordered. On each hint request, the next cue type is popped from this list (sampling without replacement), and the corresponding valid or invalid hint text from the condition file is displayed. After all 10 hints are exhausted, a warning screen ("YOU HAVE NO CALLS LEFT") is shown for 1 second, and the hint button is disabled. Key variables: number of hints used, willingness to use hints for difficult vs. easy questions, answer accuracy before and after hints, how often participants follow valid vs. invalid hints, and individual differences in hint-seeking behavior. This task was developed following discussions at ESCOP 2025.

## Must Confirm

- **Question content**: General knowledge trivia, domain-specific questions, or custom item set?
- **Total hints**: 10 hints (5 valid + 5 invalid), or different count/ratio?
- **Answer format**: Free-text entry, or multiple choice?
- **Hint presentation**: Display as "friend's answer" text, or other framing?
- **Hint timing**: Is the pre-hint answer collected before the hint is shown, or is the answer only collected after?
- **Trial count**: Total number of questions (should exceed hint count so participants must choose when to use hints)?

## Trial Window Timeline

```text
┌─────────────────────────────────┐     ┌──────────────────────────────────┐
│ Window 1: Question + Answer     │     │ Window 2: Hint + Revised Answer  │
│ (if participant submits         │     │ (if participant clicks           │
│  without hint)                  │     │  "Phone a friend" button)        │
│                                 │     │                                  │
│ Content: question text +        │     │ Content: question text +         │
│ editable answer box +           │ ──→ │ hint text + new answer box +    │
│ "Phone a friend" button +       │     │ calls remaining counter          │
│ calls remaining counter         │     │ Duration: until Enter pressed    │
│ Duration: until Enter pressed   │     │ Response: free-text entry        │
│ Response: free-text entry       │     │ Data: answer_2.text, hint_shown, │
│ Data: answer.text, key_resp     │     │ cue_type, this_hint, n_calls     │
└─────────────────────────────────┘     └──────────────────────────────────┘
                                                 │
                    ┌────────────────────────────┘
                    ↓
     ┌──────────────────────────────────┐
     │ Window 3: No Calls Left          │
     │ (when n_calls >= 10)             │
     │                                  │
     │ Content: "YOU HAVE NO CALLS      │
     │ LEFT" warning                    │
     │ Duration: 1 s                    │
     │ Response: none                   │
     └──────────────────────────────────┘
```

## Data Analysis

Analyze hint usage rate, accuracy change after hints (comparing valid vs. invalid hint trials), and whether participants show differential weighting of valid vs. invalid hints. Examine individual differences in hint-seeking (e.g., related to overconfidence, trust, or need for cognition). Compare pre-hint and post-hint accuracy.

## References

Developed based on discussions with Paulina Pietrak at ESCOP 2025. Images by Rudy Issa.

## Do Not Assume

- Do not assume hints are always valid — this paradigm has exactly 5 valid and 5 invalid hints, randomly interleaved. The 50% validity rate is part of the experimental manipulation.
- Do not assume participants know the hint validity ratio — in the standard paradigm, participants are not informed about the 50% validity rate; they must learn it implicitly through experience.
- Do not assume every trial will use a hint — participants have limited hints (10 total) and must strategically choose when to request them. Most trials typically proceed without hints.
- Do not assume the hint button is always available — the button must be disabled after all 10 hints are exhausted, and a "no calls left" warning should be shown for 1 second.
- Do not assume participants must request a hint before answering — participants can submit their answer immediately without requesting a hint. The pre-hint answer and post-hint answer are separate data points that must be tracked independently.
- Do not assume the answer format is multiple choice — the standard phone-a-friend paradigm uses free-text entry, which requires string matching or manual scoring rather than key-press accuracy.

## Condition File Columns

| Column | Type | Description |
|--------|------|-------------|
| question_id | str | 问题编号，如 `Q01`、`Q02` |
| question_text | str | 问题内容（常识问题文本） |
| valid_answer | str | 正确答案（用于字符串匹配评分） |
| valid_hint | str | 有效提示文本（朋友给出的正确答案） |
| invalid_hint | str | 无效提示文本（朋友给出的错误答案） |

## Variants

- **线索有效性告知版（Informed Validity）**：实验开始前明确告知参与者只有一半提示是正确的，与不告知版本对比，考察外显信念对提示信任度的影响。参考 [trust-game.md](trust-game.md)。
- **多来源求助版（Multi-Source Hints）**：将单一"朋友"扩展为多个信息来源（如专家、AI助手、同伴），参与者可选择向不同来源求助。用于考察信息来源可信度对求助行为的差异化影响。
- **确定性反馈版（Deterministic Feedback）**：每次提交答案后立即显示正确答案并给出准确与否的反馈，使参与者能追踪提示有效性的累积证据。考察反馈对线索信任更新的促进作用。

---

## Example

### User Request

> "我要做一个'向朋友求助'实验。屏幕上每次呈现一个常识问题，被试在文本框中输入答案。每个问题旁有一个'向朋友求助'按钮，被试可随时点击获取提示。总共10次求助机会，其中5次提示正确、5次提示错误，随机打乱。收到提示后可修改答案。求助用完则按钮变灰不可用。一共30道题，先5道练习题。使用PsychoPy实现。"

### Trial Window Timeline

```text
┌─────────────────────────────────┐    ┌──────────────────────────────────┐    ┌──────────────────────────────────┐
│ Window 1: 问题 + 作答            │    │ Window 2: 提示 + 修订答案          │    │ Window 3: 求助次数用尽提示         │
│                                 │    │                                  │    │                                  │
│ Content: question_text +        │    │ Content: question_text +         │    │ Content: "您的求助次数已用完"      │
│ Textbox 答题框 +                │    │ hint_text + 新 Textbox 答题框 +  │    │                                  │
│ "向朋友求助" 按钮 +             │ →  │ 剩余求助次数显示                  │ →  │ Duration: 1 s                     │
│ 剩余求助次数显示                 │    │ Duration: 直到按 Enter            │    │ Response: none                    │
│ Duration: 直到按 Enter 或        │    │ Response: free-text entry        │    │ Data: none                        │
│ 点击求助按钮                     │    │ Data: answer_2.text, hint_shown, │    └──────────────────────────────────┘
│ Response: free-text entry       │    │ cue_type, this_hint, n_calls     │
│ Data: answer_1.text, rt_1       │    └──────────────────────────────────┘
└─────────────────────────────────┘
```

| Window | Content | Duration | Response | Condition | Data |
|--------|---------|----------|----------|-----------|------|
| 问题+作答 | question_text, Textbox, 求助按钮, 剩余次数 | 直到 Enter 或点击求助 | free-text Entry | {question_id} | answer_1.text, rt_1, hint_requested |
| 提示+修订答案 | question_text, hint_text, Textbox, 剩余次数 | 直到 Enter | free-text Entry | {cue_type, hint_text} | answer_2.text, rt_2, hint_shown, cue_type, this_hint |
| 求助次数用尽 | "您的求助次数已用完" | 1 s | none | none | none |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| 实验名称 | 向朋友求助任务（Phone a Friend Task） |
| 平台 | PsychoPy |
| 任务类型 | 常识问答 + 可选线索求助 |
| 问题数量 | 30题（正式） + 5题（练习） |
| 求助总次数 | 10次 |
| 有效提示数 | 5次 |
| 无效提示数 | 5次 |
| 提示效度比例 | 50% |
| 答案格式 | 自由文本输入 |
| 阶段 | 指导语 → 练习(5) → 正式(30) |

### Missing Information

1. 问题内容来源未说明 → 将询问（是否提供自定义题库CSV/Excel文件？还是使用内置默认常识题？）
2. 答案评分方式未说明 → 将询问（字符串精确匹配？模糊匹配？还是需要人工事后评分？）
3. 求助按钮的视觉样式和位置未说明 → 将询问（按钮在问题下方还是右侧？按钮大小和颜色？）

### Critical Assumptions

- 求助按钮在每次答题前均可用（除非10次已用完），参与者可自主决定是否求助
- 提示效度列表在实验启动时预洗牌（5有效+5无效随机排列，不放回抽样），确保每个参与者遇到的有效/无效提示顺序不同
- 自由文本答案使用字符串精确匹配评分（忽略大小写和首尾空格），中文答案使用全角/半角统一后再匹配
- 练习阶段不提供求助功能（仅用于熟悉界面和答题流程）

### Code Architecture

```
phone_a_friend.py
├── 参数配置（总求助次数、有效/无效比例、问题数量、文本匹配容差）
├── 窗口设置（全屏/窗口，背景色，中文字体加载）
├── 条件文件加载（CSV: question_id, question_text, valid_answer, valid_hint, invalid_hint）
├── 提示效度列表生成（5 valid + 5 invalid → shuffle → pop on each request）
├── 刺激组件预创建
│   ├── 问题文本（TextStim）
│   ├── 提示文本（TextStim）
│   ├── 答题框（TextBox）
│   ├── 求助按钮（Rect + TextStim 组合）
│   ├── 剩余次数显示（TextStim: "剩余求助：X 次"）
│   └── 求助用完警告（TextStim: "您的求助次数已用完"）
├── 实验阶段
│   ├── 指导语（解释任务、求助机制、按键操作）
│   ├── 练习阶段（5题，无求助功能）
│   └── 正式阶段（30题）
├── 试次循环:
│   ├── Window 1: 问题呈现 + 答题框 + 求助按钮
│   │   ├── 检测 Enter 键 → 收集 answer_1，跳转 ITI
│   │   └── 检测求助按钮点击 → 弹出下一个提示（valid/invalid），进入 Window 2
│   ├── Window 2: 提示呈现 + 新答题框（仅当求助时触发）
│   │   ├── 显示 hint_text
│   │   ├── 收集 answer_2（Enter 提交）
│   │   └── 更新 n_calls
│   ├── Window 3: 求助用完警告（当 n_calls >= 10 时，显示 1 秒）
│   └── ITI（500-1000 ms 随机）
├── 数据保存：try/finally + CSV 逐行写入
│   ├── 试次级：question_id, answer_1, answer_2, hint_requested, hint_shown, cue_type, n_calls, acc_1, acc_2
│   └── 汇总级：total_hints_used, validity_detection_score
└── 退出控制：Escape 键全程检测
```

### Expected Data Columns

| Column | Type | Description |
|--------|------|-------------|
| question_id | str | 问题编号 |
| answer_1 | str | 求助前答案（若未求助则为最终答案） |
| answer_2 | str | 求助后答案（若未求助则为空字符串） |
| hint_requested | int | 是否点击了求助按钮（0/1） |
| hint_shown | str | 实际展示的提示文本（未求助则为空字符串） |
| cue_type | str | 提示类型：`valid` / `invalid` / `none` |
| n_calls | int | 累计已用求助次数（含当前试次） |
| acc_1 | int | 求助前准确率（1 = 正确, 0 = 错误） |
| acc_2 | int | 求助后准确率（1 = 正确, 0 = 错误, NaN = 未求助） |
| rt_1 | float | 求助前反应时（ms） |
| rt_2 | float | 求助后反应时（ms，未求助则为 NaN） |
