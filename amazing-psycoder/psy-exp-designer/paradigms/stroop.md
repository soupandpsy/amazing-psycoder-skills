# Stroop Paradigm

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)

## When to Use

User mentions: Stroop, color-word, Stroop interference, 斯特鲁普, 颜色词冲突. A classic cognitive control paradigm measuring the cost of conflicting semantic and perceptual information on response selection. The participant names the ink color of a word while ignoring its semantic meaning.

**This file covers the classic color-word Stroop and its direct variants (emotional Stroop, blocked/bilingual Stroop, numerical Stroop). For the Eriksen Flanker paradigm (center-surround arrow interference), see [eriksen-flanker.md](eriksen-flanker.md). For the Simon paradigm (spatial compatibility), see [simon.md](simon.md).**

## Core Logic

A color word (e.g., "RED", "GREEN", "BLUE") is displayed on screen, but the font color is independently controlled. The participant's task is to identify the font color while ignoring the word's meaning. This creates:

- **Congruent trials**: Word meaning matches font color (e.g., "RED" in red font)
- **Incongruent trials**: Word meaning conflicts with font color (e.g., "RED" in green font)
- **Neutral trials** (optional): Non-color word or symbol in colored ink, providing a baseline

The Stroop interference effect is the difference in RT/accuracy between incongruent and congruent conditions. If neutral trials are included, facilitation = RT_neutral − RT_congruent; interference = RT_incongruent − RT_neutral.

**Response mapping**: The key-to-color mapping must be learned by the participant and is held constant across all trials. The correct response depends on the ink color, not the word meaning. The mapping is typically 3 keys for 3 colors (e.g., left=red, down=green, right=blue).

## Must Confirm

1. **Color set**: How many ink colors? Which specific colors? (typically 3: red, green, blue)
2. **Stimulus set**: Which color words? Do they match the ink colors exactly?
3. **Response mapping**: Which key corresponds to each ink color?
4. **Congruency ratio**: 50:50 (congruent:incongruent), or include neutral trials? If neutral, what proportion?
5. **Stimulus modality**: Text-based (TextStim) or image-based (colored word images)?
6. **Trial count**: How many trials per condition? Total trials?
7. **Language**: Single language (classic), blocked bilingual, or emotional words?
8. **OS & font**: 在什么操作系统运行？如使用中文，确认字体路径（macOS: PingFang, Windows: msyh, Linux: Noto CJK）
9. **Display**: 全屏还是窗口？屏幕分辨率和背景颜色？
10. **Stimulus size**: 刺激文字大小（高度）和屏幕位置？
11. **ITI duration**: 试次间隔时间和变化范围？
12. **Instruction text**: 指导语内容？练习和正式阶段的过渡提示？

## Do Not Assume

- Do not assume 50:50 ratio — many studies use 33:33:33 with neutral trials
- Do not assume key mapping is obvious — participants must memorize 3+ color-key pairings
- Do not assume feedback is given throughout — formal blocks often omit trial-level feedback
- Do not assume all keys must be used equally — if one color appears more often, its key will be over-represented

## Condition File Columns

| Column | Type | Description |
|--------|------|-------------|
| word | str | The word text to display (color name) |
| ink_color | str | Font color of the word (RGB or name) |
| congruency | str | `"congruent"`, `"incongruent"`, or `"neutral"` |
| corrAns | str | Correct key name for this trial |

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Stroop Stimulus          │    │ Feedback (practice)      │    │ ITI                      │
│ Content: +               │    │ Content: color word      │    │ Content: correct/incorrect│   │ Content: blank           │
│ Duration: 500 ms         │    │ in colored ink           │    │ Duration: 500 ms         │    │ Duration: 500-1000 ms    │
│ Response: none           │    │ Duration: until key      │    │ Response: none           │    │ Response: none           │
│ Condition: none          │    │ (deadline ~2000 ms)      │    │ Condition: none          │    │ Condition: none          │
│ Data: none               │    │ Response: color-key map  │    │ Data: none               │    │ Data: none               │
│                          │    │ Condition: {word}/{ink}  │    │                           │    │                          │
│                          │    │ Data: rt, key, acc       │    │                           │    │                          │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | Condition | Data |
|--------|---------|----------|----------|-----------|------|
| Fixation | + | 500 ms | none | none | none |
| Stroop Stimulus | color word in colored ink | until key (deadline ~2000 ms) | color-key mapping | {word}, {ink_color} | rt, key, acc |
| Feedback | correct/incorrect/timeout | 500 ms | none | {corrAns} | none |
| ITI | blank | 500-1000 ms | none | none | none |

## Data Analysis

Compare mean RT for congruent vs. incongruent conditions. Use paired t-test or repeated-measures ANOVA:

- **Stroop interference effect**: RT_incongruent − RT_congruent
- **Error rates**: Compare error rates across congruency conditions
- **Neutral baseline** (if included): Facilitation = RT_neutral − RT_congruent; Interference = RT_incongruent − RT_neutral

## Variants

### Bilingual Stroop

Blocks stimuli by language (e.g., English block then Maori block). Tests whether Stroop interference differs by language fluency — the more fluent language typically shows larger interference because word reading is more automatic. See [bilingual-stroop.md](bilingual-stroop.md) for full spec.

### Numerical Stroop

Replaces color words with digits of varying physical sizes. Two dimensions: numerical magnitude (semantic) and physical size (perceptual). Participants switch between "which is numerically larger?" and "which is physically larger?" blocks. The key manipulation: congruent (large digit also physically larger) vs. incongruent (large digit physically smaller). Based on Henik & Tzelgov (1982). See [numerical-stroop.md](numerical-stroop.md) for full spec.

### Emotional Stroop

Uses emotionally valenced words (e.g., "DEATH", "HAPPY") instead of color words. Slower color-naming for threat-related words in anxious populations indexes attentional bias. The paradigm structure is identical to classic Stroop; only the word set differs.

### lab.js Variant

An implementation using the [lab.js](https://lab.js.org/) framework (not PsychoPy/PsychoJS). Available at the [Pavlovia labjs_stroop demo](https://gitlab.pavlovia.org/demos/labjs_stroop). Uses HTML-based templating (`lab.html.Screen`) with dynamic parameters. Trial structure: fixation (500ms) → Stroop stimulus (1500ms max, response-terminated) → feedback. Response keys: 'r', 'g', 'b', 'o' for red, green, blue, orange. 16 color-word combinations via `templateParameters`. The paradigm-level design is identical to standard Stroop; only the implementation framework differs.

## References

MacLeod, C. M. (1991). Half a century of research on the Stroop effect: An integrative review. *Psychological Bulletin*, *109*(2), 163–203. https://doi.org/10.1037/0033-2909.109.2.163

Stroop, J. R. (1935). Studies of interference in serial verbal reactions. *Journal of Experimental Psychology*, *18*(6), 643–662. https://doi.org/10.1037/h0054651

## Example

### User Request

> "我想做一个Stroop实验。屏幕上呈现汉字'红'、'绿'、'蓝'，每个字的墨水颜色可能是红、绿、蓝之一。被试判断墨水颜色（不是字义），红色按F，绿色按J，蓝色按K。一致条件（字义=墨水颜色）和不一致条件（字义≠墨水颜色）各半。先指导语，然后20个练习trial（有反馈），然后4个正式block各48个trial（无反馈）。刺激呈现直到按键，反应窗口2000 ms，ITI随机600-900 ms。用PsychoPy。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Stroop Stimulus          │    │ Feedback                 │    │ ITI                      │
│ Content: +               │    │ Content: 色词(如"红")    │    │ Content: 正确/错误        │    │ Content: empty           │
│ Duration: 500 ms         │    │ Duration: until key      │    │ Duration: 500 ms         │    │ Duration: 600-900 ms     │
│ Response: none           │    │ Response: f/j/k          │    │ Response: none           │    │ Response: none           │
│ File: none               │    │ File: none (text)        │    │ File: none               │    │ File: none               │
│ Condition: none          │    │ Condition: {word}/{ink}  │    │ Condition: {corrAns}     │    │ Condition: none          │
│ Data: none               │    │ Data: rt, key, acc       │    │ Data: none               │    │ Data: none               │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| Experiment name | Color-Word Stroop Task |
| Platform | PsychoPy |
| Target dimension | Ink color (红/绿/蓝) |
| Distractor dimension | Word meaning (红/绿/蓝) |
| Response mapping | F=红色, J=绿色, K=蓝色 |
| Congruency ratio | 50:50 congruent:incongruent |
| Conditions | 3 words × 3 ink colors = 9 factorial conditions |
| Blocks | Practice(20) → Block1-4(48 each) |
| Data columns | word, ink_color, congruency, rt, key, acc |
