# IAT (Implicit Association Test) Paradigm

> **Structure ref**: [spec-template.md](../references/spec-template.md)
> **Standards**: [timing](../references/timing.md) · [data recording](../references/data-recording.md) · [randomization](../references/randomization.md) · [missing info](../references/missing-information.md) · [condition file](../references/condition-file.md)

## When to Use

User mentions: IAT, 内隐联想测验, implicit association, 内隐态度, implicit bias, implicit association test.

## Core Logic

Participants sort stimuli into categories using two keys. When compatible categories share a key (e.g., Flower + Good on left key), responses are fast. When incompatible categories share a key (e.g., Insect + Good on left key), responses are slow. The difference (IAT effect, D-score) measures implicit association strength.

The IAT was originally developed by Greenwald et al. (1998). The standard PsychoPy implementation (Open IAT) provides a classic black/white versus positive/negative version, but is designed to be customizable for other category pairings. The implementation uses spreadsheet files (`.xlsx`) to define block orders and condition files for each block (e.g., `cong_train.xlsx`, `cong_test.xlsx`), located in a `resources/` folder. To adapt the task for different stimuli, researchers can modify the condition files to define new congruent/incongruent training and testing conditions.

Standard 7-block structure:

| Block | Trials | Task | Left Key | Right Key |
|-------|--------|------|----------|-----------|
| 1 | 20 | Target discrimination (practice) | Category A | Category B |
| 2 | 20 | Attribute discrimination (practice) | Attribute A | Attribute B |
| 3 | 20 | Compatible combined (practice) | Cat A + Att A | Cat B + Att B |
| 4 | 40 | Compatible combined (test) | Cat A + Att A | Cat B + Att B |
| 5 | 20 | Target discrimination reversed | Category B | Category A |
| 6 | 20 | Incompatible combined (practice) | Cat B + Att A | Cat A + Att B |
| 7 | 40 | Incompatible combined (test) | Cat B + Att A | Cat A + Att B |

## Must Confirm

Before generating IAT code, confirm ALL of these:

1. **Target categories**: What two categories? (e.g., Flower vs Insect)
2. **Attribute categories**: What two attributes? (e.g., Good vs Bad)
3. **Stimuli**: How many exemplars per category? Image files or text? Stimulus size?
4. **Block order**: Compatible-first or counterbalanced across subjects?
5. **Error handling**: Forced correction (must press correct key to proceed) or brief error feedback?
6. **Response deadline**: Fixed? Built-in error penalty? (typically 3000 ms or none)
7. **Trials per block**: Standard (20/20/20/40/20/20/40) or custom?
8. **D-score calculation**: Built-in or offline? Using improved algorithm (Greenwald et al., 2003)?
9. **ITI duration**: 试次间隔时间和变化范围？
10. **OS & font**: 在什么操作系统运行？如使用中文，确认字体
11. **Display**: 全屏还是窗口？类别标签是否始终显示在屏幕上？
12. **Instruction text**: 各block的指导语内容？如何说明按键映射变化？

## Do Not Assume

- Do not assume compatible-first block order — counterbalancing matters for validity
- Do not assume forced error correction — some designs use red-X feedback only
- Do not assume 7 blocks — some reduced versions use 5 blocks
- Do not assume stimulus count — confirm exemplars per category
- Do not assume key mapping — left/right assignment affects results
- Do not assume D-score is calculated during the experiment (offline is standard)

## Condition File Columns

Columns in the xlsx/csv file that drives each trial:

| Column | Type | Description |
|--------|------|-------------|
| block_num | int | IAT block number (1-7) |
| block_type | str | `"practice"` or `"test"` |
| block_condition | str | `"compatible"` or `"incompatible"` |
| category | str | Which category the stimulus belongs to |
| left_key_label | str | Label shown for left key |
| right_key_label | str | Label shown for right key |

## Data Output Columns

| Column | Type | Description |
|--------|------|-------------|
| block_type | str | `"practice"` or `"test"` |
| block_condition | str | `"compatible"` or `"incompatible"` |
| category_pair | str | Which categories share which key |
| error_trial | int | 1 if error response, 0 if correct |
| error_rt | float | RT after error correction (if forced correction used) |

## Data Analysis

The primary outcome measure for the IAT is the D-score (Greenwald et al., 2003):

- **D-score calculation (improved algorithm, Greenwald et al., 2003)**:
  1. Use data from Blocks 3, 4, 6, and 7 (combined blocks)
  2. Delete trials with RT > 10,000 ms
  3. Delete subjects with > 10% of trials faster than 300 ms (flags random fast responding; the entire dataset is considered invalid)
  4. **Error penalty**: For incorrect trials, replace the RT with the block's mean correct RT plus a 600 ms penalty. This accounts for the observation that errors are typically faster than correct responses and would otherwise bias the D-score downward.
  5. Compute pooled inclusive SD for all trials in Blocks 3 & 6, and separately for Blocks 4 & 7
  6. Compute mean RT difference (incompatible - compatible) for each pair of blocks
  7. Divide each difference by its pooled SD to obtain a practice D (from blocks 3 & 6) and a test D (from blocks 4 & 7)
  8. Average the two D-scores to obtain the overall D
- **Interpretation**: |D| < 0.15 = little to no effect; 0.15 <= |D| < 0.35 = slight effect; 0.35 <= |D| < 0.65 = moderate effect; |D| >= 0.65 = strong effect
- **Practice vs. test blocks**: The two D-scores should correlate reasonably well (internal consistency check). Large discrepancies may indicate careless responding or failure to understand the task.

## Randomization Checks

- Stimuli within each block randomized without replacement
- No more than 3 consecutive same-category trials
- If block order is counterbalanced, assign by subject ID parity or predefined order file
- For within-block randomization: draw from pool without replacement, reshuffle when exhausted

## Common Failure Modes

- Not counterbalancing block order (compatible-first vs incompatible-first)
- Not recording which stimuli appeared on which trial
- Not handling forced error correction timing correctly (error RT contaminates D-score if not separated)
- Using too few exemplars per category (minimum 4, ideally 6+)
- Not implementing D-score algorithm correctly (use improved scoring: Greenwald et al., 2003)

## References

Greenwald, A. G., McGhee, D. E., & Schwartz, J. L. K. (1998). Measuring individual differences in implicit cognition: The implicit association test. *Journal of Personality and Social Psychology*, *74*(6), 1464–1480. https://doi.org/10.1037/0022-3514.74.6.1464

Greenwald, A. G., Nosek, B. A., & Banaji, M. R. (2003). Understanding and using the Implicit Association Test: I. An improved scoring algorithm. *Journal of Personality and Social Psychology*, *85*(2), 197–216. https://doi.org/10.1037/0022-3514.85.2.197

Peirce, J., Gray, J. R., Simpson, S., MacAskill, M., Hochenberger, R., Sogo, H., Kastman, E., & Lindelov, J. K. (2019). PsychoPy2: Experiments in behavior made easy. *Behavior Research Methods*, *51*, 195–203. https://doi.org/10.3758/s13428-018-01193-y

---

## Example

### User Request

> "我想做一个花-昆虫IAT实验。目标类别：花（玫瑰、郁金香、菊花、向日葵、百合）和昆虫（蜜蜂、苍蝇、蚂蚁、蜘蛛、蚊子），属性类别：积极词（快乐、爱、和平、美丽、自由）和消极词（死亡、战争、疾病、痛苦、仇恨）。相容条件：花+积极/昆虫+消极，不相容条件：花+消极/昆虫+积极。标准7个block结构，相容和不相容顺序在被试间平衡。错误时强制修正（必须按正确键才能继续）。所有刺激为文字。用PsychoPy。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Category Labels          │    │ Stimulus                 │    │ Error Feedback           │    │ ITI                      │
│ Content: 类别标签         │    │ Content: {stimulus}      │    │ Content: 红色X           │    │ Content: empty           │
│ Duration: until key      │    │ Duration: until key      │    │ Duration: 200 ms         │    │ Duration: 250 ms         │
│ Response: e/i            │    │ Response: e/i            │    │ Response: none           │    │ Response: none           │
│ File: none               │    │ File: none (text)        │    │ File: none               │    │ File: none               │
│ Condition: {category}    │    │ Condition: {stimulus}    │    │ Condition: none          │    │ Condition: none          │
│ Data: none               │    │ Data: rt, key, acc       │    │ Data: none               │    │ Data: none               │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | File/Folder | Condition | Data |
|--------|---------|----------|----------|-------------|-----------|------|
| Category Labels | 类别标签（如"花/积极"） | persistent | e/i | none | {category_labels} | none |
| Stimulus | 刺激词 | until key (deadline 3000 ms) | e/i | none (text) | {stimulus} | rt, key, acc |
| Error Feedback | 红色X（仅在错误时） | 200 ms | none (forced correction) | none | none | none |
| ITI | empty | 250 ms | none | none | none | none |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| Experiment name | Flower-Insect IAT |
| Platform | PsychoPy |
| Task type | IAT (Implicit Association Test) |
| Target categories | Flower (5) vs Insect (5) |
| Attribute categories | Positive (5) vs Negative (5) |
| Stimuli | 20 Chinese words, text-based |
| Block structure | Standard 7-block (20/20/20/40/20/20/40) |
| Error handling | Forced correction (red X + must press correct key) |
| Response mapping | E=left key, I=right key |
| Counterbalancing | Compatible-first vs incompatible-first by subject ID parity |
| D-score | Offline calculation (improved algorithm) |

### Assumptions

- Category labels displayed at top of screen throughout each block
- Forced correction: on error, red X shown 200 ms, stimulus stays until correct key pressed
- Block transition screens with instructions for new category-key mappings
- E/I keys mapped to left/right (standard for IAT on QWERTY keyboards)

### Missing Information

1. Stimulus type: text or image files? → "所有刺激为文字" — confirmed text-based
2. Key mapping: which side = which category? → will ask (E=left, I=right standard)
3. Response deadline not stated → assumed 3000 ms
4. Block-end feedback? → will ask

### Expected Code Architecture

```
iat_flower_insect.py
├── Parameters (categories, stimuli, block structure, keys)
├── Window setup
├── Stimulus preloading (TextStim for all 20 words + category labels)
├── Block order determination (counterbalanced by subject ID)
├── Block loop (7 blocks):
│   ├── Block instruction (category-key mapping)
│   ├── Trial loop:
│   │   ├── Category labels (persistent)
│   │   ├── Stimulus presentation (until key, deadline 3000 ms)
│   │   ├── Error check → forced correction if wrong key
│   │   └── ITI (250 ms)
│   └── Block-end feedback (accuracy, mean RT)
├── Data: try/finally CSV with incremental writes
```

### Expected Data Columns

Base columns + block_type, block_condition, error_trial, error_rt, category_pair
