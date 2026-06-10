# EAST (Extrinsic Affective Simon Task) Paradigm

> **Parent**: [psy-exp-designer](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [psychbruce/jspsych](https://github.com/psychbruce/jspsych) (Bao, 2020) · jsPsych 6.1.0

## When to Use

User mentions: EAST, Extrinsic Affective Simon Task, 外在情感西蒙任务, implicit attitudes, 内隐态度, single-target IAT. Use EAST when you need to measure implicit attitudes toward target categories without requiring complementary category pairs (unlike IAT). EAST measures implicit attitudes through the interaction between stimulus valence (attribute) and an extrinsic feature (color). Suitable for single-target attitude measurement, where IAT requires contrasting pairs.

## Core Logic

EAST presents participants with words that vary along two dimensions: **attribute** (positive/negative valence of white words) and **extrinsic feature** (ink color of target nouns: blue/green). Participants respond with two keys (F/J) mapped to a classification rule that stays constant throughout.

**Key mapping** (fixed throughout the entire experiment):
- **F key** (left) = Positive attribute words AND Blue-colored target words
- **J key** (right) = Negative attribute words AND Green-colored target words

This creates an implicit association: if the participant has a positive implicit attitude toward a target category (e.g., "flowers"), they will be faster to respond when flower words appear in blue (sharing the F key with "positive") than in green (sharing the J key with "negative").

### Trial Structure

Each trial consists of a nested timeline:
1. **Fixation** — 500 ms cross (+) with category label tags displayed at screen top-left and top-right (left tag maps to F, right tag maps to J)
2. **Stimulus classification** — Word presented at center. White words are classified by meaning (positive/negative). Colored words are classified by ink color (blue/green). Response: F or J key.
3. **Error feedback** — During practice blocks: green checkmark (correct) or red X (incorrect) with forced correction (must press correct key to advance). No feedback during test block.
4. **ITI** — Practice blocks: brief fixed interval. Test block: randomized 1–2 seconds (`Math.random() * 1000 + 1000`).

### Block Structure

1. **Practice Block 1 — Attribute Classification** (20 trials per stimulus): White words only. Classify as positive (F) or negative (J). Error feedback with forced correction. White background.
2. **Practice Block 2 — Color Classification** (20 trials per stimulus): Colored target nouns. Classify by ink color: blue (F) or green (J). Error feedback with forced correction. White background.
3. **Test Block — Combined** (40 trials per stimulus): Both white attribute words AND colored target words randomly interleaved. Same key mapping (F = positive/blue, J = negative/green). **No error feedback**. No forced correction. Black background with hidden cursor, larger font. Randomized ITI.

### Style Switching

The visual environment changes between practice and test:
- **Practice blocks**: White background, black text, normal cursor, 20pt font
- **Test block**: Black background, white text, hidden cursor, 32pt font — designed to increase immersion and reduce deliberate control

### EAST Effect

The EAST effect is computed separately for each target category x:

**EAST_x = RT(green, category x) - RT(blue, category x)**

- Positive EAST score: faster to respond when category x appears in blue (shares key with positive) — indicates implicit preference
- Negative EAST score: faster to respond when category x appears in green (shares key with negative) — indicates implicit aversion
- Zero: no differential association

The computation uses only correct trials from the test block (`formal == true`).

## Must Confirm

- **Target categories**: Which categories to measure attitudes toward? (e.g., flowers, insects, self, others) — EAST measures each independently
- **Attribute words**: Positive and negative word lists (language, number per category)?
- **Target exemplars**: How many exemplar words per target category?
- **Color mapping**: Blue=F/positive, Green=J/negative — or custom?
- **Trial counts**: Practice trials per stimulus, test trials per stimulus?
- **Key labels**: What category labels to display on screen?
- **ITI duration**: 试次间隔时间？各block是否不同？
- **OS & font**: 在什么操作系统运行？如使用中文词语，确认字体
- **Display**: 全屏还是窗口？词语大小和屏幕位置？
- **Instruction text**: 各block的指导语内容？

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Stimulus Classification  │    │ Error Feedback            │    │ ITI                      │
│ Content: + at center     │    │ Content: word at center  │    │ (practice blocks only)    │    │ Content: blank           │
│ + category tags (L/R)    │    │ white=by meaning,        │    │ Content: √ or X          │    │ Duration: 500 ms (prac)  │
│ Duration: 500 ms         │    │ colored=by ink color     │    │ + forced correction      │    │   1000-2000 ms (test)    │
│ Response: none           │    │ Duration: until key      │    │ Duration: until correct  │    │ Response: none           │
│ Condition: {tag_labels}  │    │ Response: F or J key     │    │   key pressed            │    │ Condition: none          │
│ Data: none               │    │ Condition: {stim_type,   │    │ Condition: none          │    │ Data: none               │
└──────────────────────────┘    │   stimulus, key_answer}  │    │ Data: none               │    └──────────────────────────┘
                                │ Data: rt, key, acc,      │    └──────────────────────────┘
                                │   stim_type, formal      │
                                └──────────────────────────┘
```

## Condition File Columns

| Column | Type | Description |
|--------|------|-------------|
| block | str | `"practice_attr"`, `"practice_color"`, or `"test"` |
| stim_type | str | `"attribute"` (white word, classify by meaning) or the target category name (e.g., `"flower"`, classify by ink color) |
| stimulus | str | The word to display |
| stim_color | str | `"white"` (attribute words), `"blue"`, or `"green"` (target words) |
| key_answer | str | `"F"` (positive/blue) or `"J"` (negative/green) |
| tag_left | str | Label displayed top-left (maps to F key) |
| tag_right | str | Label displayed top-right (maps to J key) |

## Data Output Columns

| Column | Type | Description |
|--------|------|-------------|
| block | str | Block type: `"practice_attr"`, `"practice_color"`, `"test"` |
| stim_type | str | `"attribute"` or target category name |
| stimulus | str | Word displayed |
| stim_color | str | `"white"`, `"blue"`, or `"green"` |
| key_answer | str | Expected correct key (`"F"` or `"J"`) |
| key | str | Key actually pressed |
| rt | float | Response time (ms) |
| acc | int | 1 = correct, 0 = error |
| formal | int | 1 = test block, 0 = practice block |

## Do Not Assume

- **Key mapping is not switchable**: Unlike IAT, the EAST key mapping (F=positive/blue, J=negative/green) stays fixed throughout — do NOT propose switching keys between blocks
- **Visual style switch is deliberate**: Practice (white bg, normal cursor, small font) → Test (black bg, hidden cursor, large font) is designed to increase automatic processing. Do NOT remove this without explicit user request
- **Each target category is independent**: EAST scores are computed per category, not pooled. Do NOT merge categories into a single analysis
- **Forced correction only in practice**: Error feedback with forced key press is required for practice blocks. Do NOT add to test block — it would disrupt the implicit measurement
- **ITI differs between blocks**: Practice has fixed brief ITI; test has randomized 1-2s ITI. Do NOT apply the same ITI to both

## Randomization Checks

- **Test block interleaving**: White attribute words and colored target words must be randomly interleaved (not blocked by stim_type)
- **Consecutive same-type limit**: No more than 3 consecutive trials of the same `stim_type` in the test block
- **Color balance**: Blue and green target words should appear with equal frequency within each target category
- **Trial order**: Within each block, trial order is randomized (shuffled) before presentation
- **Category count balance**: Each target category should have the same number of trials in the test block

## Common Failure Modes

| Failure | Symptom | Fix |
|---------|---------|-----|
| Feedback in test block | EAST effect disappears (participants slow down and correct errors) | Remove feedback + forced correction from test block; keep only in practice |
| No forced correction in practice | Participants fail to learn key mapping; high error rate in test block | Add forced correct-key-press requirement after wrong answer in practice |
| Visual style not switched | Test block feels like more practice; reduced automatic processing | Apply black background, hidden cursor, larger font in test block |
| Key mapping confusion with IAT | Designer treats EAST like IAT with key-switching blocks | Confirm key mapping is fixed; show mapping diagram in instructions |
| Computing pooled EAST score | EAST effect diluted across categories with opposite associations | Compute EAST_x per category; compare categories with paired tests |
| Fixed ITI in test block | Predictable rhythm; participant can anticipate next trial | Use randomized ITI (1-2 s) in test block only |
| Category label tags missing | Participant forgets which key corresponds to which category | Display category labels (top-left/right) during fixation window |

## Example

**User Request**:
> "做一个 EAST 实验，测量对花卉和昆虫的内隐态度。积极词20个，消极词20个，花卉词4个，昆虫词4个。按键映射：F=积极/蓝色，J=消极/绿色。"

**Timeline**:

```
┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│ Fixation             │ →  │ Classification       │ →  │ Error Feedback       │ →  │ ITI                  │
│ +  with tags         │    │ Word at center       │    │ (practice only)      │    │ blank                │
│ 500 ms               │    │ until key (F/J)      │    │ until correct key    │    │ 500ms / 1000-2000ms  │
│ no response          │    │ rt, key, acc         │    │ no data              │    │ no response          │
└──────────────────────┘    └──────────────────────┘    └──────────────────────┘    └──────────────────────┘
```

**Spec Table**:

| Parameter | Value |
|-----------|-------|
| Paradigm | EAST |
| Platform | PsychoPy / jsPsych |
| Target categories | 花卉 (flower), 昆虫 (insect) |
| Attribute words | 20 positive + 20 negative |
| Target exemplars | 4 per category |
| Key mapping | F = 积极/蓝色, J = 消极/绿色 |
| Practice 1 (Attribute) | 40 trials (20 pos + 20 neg), feedback + forced correction |
| Practice 2 (Color) | 40 trials (4花卉 × 5rep blue + 4花卉 × 5rep green + 4昆虫 × 5rep blue + 4昆虫 × 5rep green), feedback + forced correction |
| Test Block | 80 trials (20 attr + 30花卉 + 30昆虫, interleaved), no feedback, black bg |
| ITI | Practice: 500ms fixed; Test: 1000-2000ms random |
| Output | block, stim_type, stimulus, stim_color, key_answer, key, rt, acc, formal |
| Analysis | EAST_flower = RT(green, flower) - RT(blue, flower); EAST_insect = RT(green, insect) - RT(blue, insect) |

## Data Analysis

Filter to `formal == true` (test block only) and `correct == true`. For each target category x, compute mean RTs per color condition:
- `mean_rt_green_x` = mean RT for green-colored words of category x
- `mean_rt_blue_x` = mean RT for blue-colored words of category x
- `EAST_x = mean_rt_green_x - mean_rt_blue_x`

Repeat for each target category independently. Compare EAST scores across categories (e.g., flowers vs. insects) using paired t-tests. Positive scores indicate implicit preference; negative scores indicate implicit aversion. The EAST effect is typically smaller than the IAT effect but has the advantage of measuring attitudes toward single categories without requiring complementary pairs.

## References

De Houwer, J. (2003). The extrinsic affective Simon task. *Experimental Psychology, 50*(2), 77–85. https://doi.org/10.1026/1618-3169.50.2.77

De Houwer, J., & Eelen, P. (1998). An affective variant of the Simon paradigm. *Cognition and Emotion, 12*(1), 45–62.

Bao, H.-W.-S. (2020). jsPsych experiment demos in Chinese. https://github.com/psychbruce/jspsych
