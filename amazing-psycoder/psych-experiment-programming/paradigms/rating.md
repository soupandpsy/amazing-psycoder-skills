# Rating Paradigm

> **Structure ref**: [spec-template.md](../references/spec-template.md)
> **Standards**: [timing](../references/timing.md) · [data recording](../references/data-recording.md) · [randomization](../references/randomization.md) · [missing info](../references/missing-information.md) · [condition file](../references/condition-file.md)

## When to Use

User mentions: Rating, 评分, Likert, VAS, visual analog scale, subjective rating, valence rating, arousal rating, preference rating.

## Core Logic

Participants rate stimuli on one or more dimensions. Used for subjective judgment, emotion assessment, preference measurement, or stimulus validation. Not an RT task — response time is secondary.

## Must Confirm

1. **Rating type**: Likert (discrete) or VAS (continuous)?
2. **Likert**: How many points? (typically 5, 7, or 9) What are the anchors?
3. **VAS**: What are the line endpoints? (e.g., "Not at all" to "Extremely")
4. **Rating dimension(s)**: valence, arousal, preference, confidence, familiarity?
5. **Multiple ratings**: does each stimulus get rated on multiple dimensions sequentially, or one dimension per block?
6. **Self-paced or timed**: does the rating have a deadline?
7. **Response device**: keyboard, mouse, touchscreen?
8. **Trial structure**: stimulus first then rating, or both on same screen?
9. **OS & font**: 在什么操作系统运行？如使用中文量表，确认字体
10. **Display**: 全屏还是窗口？量表文字大小和屏幕位置？
11. **Instruction text**: 指导语内容？量表锚点说明文字？

## Do Not Assume

- Do not assume 7-point Likert — confirm the exact scale
- Do not assume anchors — "1=very negative, 7=very positive" vs "1=very positive, 7=very negative" matters enormously
- Do not assume self-paced — some rating tasks impose deadlines to prevent deliberation
- Do not assume single dimension — multi-dimensional ratings are common (e.g., valence + arousal)
- Do not assume keyboard input — VAS often uses mouse or touch
- Do not assume trial count — rating tasks may have fewer trials than RT tasks (20–100 per condition)

## Condition File Columns

Columns in the xlsx/csv file that drives each trial:

| Column | Type | Description |
|--------|------|-------------|
| stimulus | str | Stimulus filename |
| rating_dimension | str | Which dimension to rate (if multi-dim) |
| scale_min | int | Minimum scale value |
| scale_max | int | Maximum scale value |
| anchor_low | str | Low-end anchor label |
| anchor_high | str | High-end anchor label |

## Data Output Columns

| Column | Type | Description |
|--------|------|-------------|
| stimulus | str | Stimulus identity |
| rating | float | Rating value |
| rating_dimension | str | Which dimension was rated |
| rating_rt | float | Time to make rating (ms) — secondary, not primary |
| scale_type | str | `"likert"` or `"vas"` |

## Randomization Checks

- Stimulus order randomized within each rating dimension block
- No more than 3 consecutive same-valence stimuli (if valence known in advance)
- Multi-dimensional ratings: dimension order counterbalanced across subjects

## Common Failure Modes

- Treating rating RT as a primary measure when it's not
- Not confirming anchor direction (which end is high?)
- Using forced-choice RT response code for a rating task
- Not recording which dimension was rated on multi-dimension trials

## References

Bradley, M. M., & Lang, P. J. (1994). Measuring emotion: The Self-Assessment Manikin and the semantic differential. *Journal of Behavior Therapy and Experimental Psychiatry*, *25*(1), 49–59. https://doi.org/10.1016/0005-7916(94)90063-9

Likert, R. (1932). A technique for the measurement of attitudes. *Archives of Psychology*, *22*(140), 5–55.

Wewers, M. E., & Lowe, N. K. (1990). A critical review of visual analogue scales in the measurement of clinical phenomena. *Research in Nursing & Health*, *13*(4), 227–236. https://doi.org/10.1002/nur.4770130405

---

## Example

### User Request

> "我想做一个情绪图片评分实验。从IAPS图片库选了60张图片（20正性、20中性、20负性），每张图片呈现后，被试需要在两个维度上评分：效价（1=非常负性, 9=非常正性）和唤醒度（1=非常平静, 9=非常激动）。9点Likert量表，用鼠标点击数字。图片呈现3秒后量表才出现（防止冲动评分），量表不限时。两个维度的评分顺序在被试间平衡。用PsychoPy。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Image Only               │    │ Rating - Valence         │    │ Rating - Arousal         │
│ Content: +               │    │ Content: IAPS图片        │    │ Content: 图片+量表        │    │ Content: 图片+量表        │
│ Duration: 500 ms         │    │ Duration: 3000 ms        │    │ Duration: self-paced     │    │ Duration: self-paced     │
│ Response: none           │    │ Response: none           │    │ Response: mouse 1-9      │    │ Response: mouse 1-9      │
│ File: none               │    │ File: stimuli/iaps/*.jpg │    │ File: none               │    │ File: none               │
│ Condition: none          │    │ Condition: {stimulus}    │    │ Condition: none          │    │ Condition: none          │
│ Data: none               │    │ Data: none               │    │ Data: valence_rating, rt │    │ Data: arousal_rating, rt │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | File/Folder | Condition | Data |
|--------|---------|----------|----------|-------------|-----------|------|
| Fixation | + | 500 ms | none | none | none | none |
| Image Only | IAPS图片 | 3000 ms (mandatory viewing) | none | stimuli/iaps/*.jpg | {stimulus} | none |
| Rating - Valence | 图片 + Likert 1-9 | self-paced | mouse click 1-9 | none | none | valence_rating, valence_rt |
| Rating - Arousal | 图片 + Likert 1-9 | self-paced | mouse click 1-9 | none | none | arousal_rating, arousal_rt |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| Experiment name | IAPS Emotion Rating Task |
| Platform | PsychoPy |
| Task type | Rating (9-point Likert) |
| Rating dimensions | Valence (1-9), Arousal (1-9) |
| Scale anchors | Valence: 1=非常负性, 9=非常正性 / Arousal: 1=非常平静, 9=非常激动 |
| Stimulus source | IAPS images (60 total: 20 pos, 20 neu, 20 neg) |
| Mandatory viewing | 3000 ms before rating scale appears |
| Dimension order | Counterbalanced across subjects |
| Phases | Instruction → 60 rating trials (no practice needed for rating) |

### Missing Information

1. IAPS image filenames not provided → will ask for file list or naming convention
2. ITI not stated → will ask
3. Dimension counterbalancing: automated by subject ID parity or manual assignment?

### Assumptions

- No ITI between the two rating windows (valence → arousal flows directly)
- ITI between trials: 1000 ms (design assumption, flagged)
- Mouse response: click on a 1-9 horizontal scale with labeled anchors
- No more than 3 consecutive same-valence stimuli

### Expected Code Architecture

```
emotion_rating.py
├── Parameters (IAPS directory, anchors, timing, counterbalance)
├── Window setup
├── Load and preload 60 IAPS images
├── Generate trial order (constrained: ≤3 same valence consecutive)
├── Trial loop:
│   ├── Fixation (500 ms)
│   ├── Image-only viewing (3000 ms mandatory)
│   ├── Valence rating (self-paced, mouse)
│   ├── Arousal rating (self-paced, mouse)
│   └── ITI (1000 ms)
├── Data: try/finally CSV with incremental writes
```

### Expected Data Columns

Base columns + stimulus, valence_rating, valence_rt, arousal_rating, arousal_rt, scale_type
