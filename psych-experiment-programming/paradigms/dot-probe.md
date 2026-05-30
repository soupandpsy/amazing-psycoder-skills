# Dot-Probe Paradigm

> **Structure ref**: [spec-template.md](../references/spec-template.md)
> **Standards**: [timing](../references/timing.md) · [data recording](../references/data-recording.md) · [randomization](../references/randomization.md) · [missing info](../references/missing-information.md) · [condition file](../references/condition-file.md)

## When to Use

User mentions: Dot-probe, 点探测, attentional bias, 注意偏向, visual probe, dot probe task, emotional dot-probe.

## Core Logic

Two stimuli (typically one emotional, one neutral) appear simultaneously at two locations. After they disappear, a probe dot appears at one of the locations. Participants respond to the dot (location or identity). Faster responses to probes replacing emotional stimuli (vs. neutral) indicate attentional bias toward threat/emotion.

Typical trial structure: Fixation (500 ms) → Stimulus pair (500 ms) → Probe dot (until response) → ITI.

Key conditions:
- **Congruent**: Probe replaces emotional/threat stimulus
- **Incongruent**: Probe replaces neutral stimulus
- **Neutral-neutral**: Both stimuli neutral (baseline)

Bias index = RT_incongruent - RT_congruent. Positive = vigilance toward threat; negative = avoidance.

## Must Confirm

Before generating dot-probe code, confirm ALL of these:

1. **Stimulus type**: emotional faces, emotional scenes, words, or other?
2. **Stimulus categories**: which emotion(s)? Threat (angry), positive (happy), or both?
3. **Stimulus presentation**: pairs (left/right) or above/below? Stimulus size and distance?
4. **SOA**: stimulus pair duration? (typically 500 ms; can be 100 ms subliminal or 1250 ms for disengagement)
5. **Probe type**: dot (location discrimination: left/right) or arrow (direction discrimination: up/down)?
6. **Response**: which keys for which probe location/type?
7. **Catch trials**: include neutral-neutral pairs? What proportion?
8. **Trial count**: how many per condition? (typically 32-64 per condition)
9. **Image format**: 刺激图片格式和文件命名规则？图片尺寸和视觉角度？
10. **ITI duration**: 试次间隔时间和变化范围？
11. **OS & font**: 在什么操作系统运行？如使用中文，确认字体
12. **Display**: 全屏还是窗口？屏幕分辨率？
13. **Instruction text**: 指导语内容？

## Do Not Assume

- Do not assume emotional faces — words, scenes, and bodies are also common
- Do not assume threat only — some studies include positive stimuli
- Do not assume 500 ms SOA — subliminal (~100 ms) and disengagement (~1250 ms) variants exist
- Do not assume dot location discrimination — arrow direction is an alternative
- Do not assume only congruent/incongruent pairs — neutral-neutral pairs are needed for bias baseline
- Do not assume trial count — dot-probe often needs more trials than RT tasks due to smaller effect sizes

## Condition File Columns

Columns in the xlsx/csv file that drives each trial:

| Column | Type | Description |
|--------|------|-------------|
| emotional_stimulus | str | Emotional stimulus filename |
| neutral_stimulus | str | Neutral stimulus filename |
| emotional_position | str | `"left"` or `"right"` |
| probe_position | str | `"left"` or `"right"` |
| congruency | str | `"congruent"` or `"incongruent"` |
| soa | int | Stimulus pair duration (ms) |

## Data Output Columns

| Column | Type | Description |
|--------|------|-------------|
| emotional_stimulus | str | Emotional stimulus filename |
| neutral_stimulus | str | Neutral stimulus filename |
| emotional_position | str | `"left"` or `"right"` |
| probe_position | str | `"left"` or `"right"` |
| congruency | str | `"congruent"`, `"incongruent"`, or `"neutral"` |
| soa | float | Stimulus pair duration (ms) |
| attentional_bias | float | RT_incongruent - RT_congruent (calculated per condition) |

## Data Analysis

Primary outcome measures for the dot-probe task:

- **Attentional bias score**: Bias = RT_incongruent - RT_congruent. Positive scores indicate vigilance toward threat (faster responses when probe replaces threat stimulus). Negative scores indicate avoidance (faster responses when probe replaces neutral stimulus).
- **Subgroup analysis**: Bias scores can be computed separately for different stimulus durations (e.g., 100 ms subliminal vs. 500 ms supraliminal) and for different emotion categories (e.g., angry vs. happy).
- **Neutral-neutral baseline**: RT on neutral-neutral trials provides a baseline to assess whether effects reflect facilitated engagement with threat or delayed disengagement from threat.
- **Variability analysis**: Some researchers compute the standard deviation of bias scores across trials as an index of attentional bias variability, which may be a more stable individual difference measure than the mean bias.

## Randomization Checks

- Equal probe left/right frequency within each condition
- Equal emotional stimulus left/right frequency
- No more than 3 consecutive same-probe-position trials
- Stimuli drawn without replacement from each category pool, reshuffle when exhausted
- Verify congruency ratio after shuffle

## Common Failure Modes

- Not counterbalancing emotional stimulus position (left/right must be equal)
- Not recording both stimuli identities (needed to verify stimulus-specific effects)
- Confusing probe location with emotional stimulus location
- Too few trials per condition (dot-probe effect sizes are small; need adequate power)
- Not including neutral-neutral baseline trials (bias cannot be properly indexed without them)
- Using SOA too short for the LCD refresh rate (stimulus pair may not be fully rendered)

## References

MacLeod, C., Mathews, A., & Tata, P. (1986). Attentional bias in emotional disorders. *Journal of Abnormal Psychology*, *95*(1), 15–20. https://doi.org/10.1037/0021-843X.95.1.15

Bar-Haim, Y., Lamy, D., Pergamin, L., Bakermans-Kranenburg, M. J., & van IJzendoorn, M. H. (2007). Threat-related attentional bias in anxious and nonanxious individuals: A meta-analytic study. *Psychological Bulletin*, *133*(1), 1–24. https://doi.org/10.1037/0033-2909.133.1.1

Posner, M. I., Snyder, C. R., & Davidson, B. J. (1980). Attention and the detection of signals. *Journal of Experimental Psychology: General*, *109*(2), 160–174. https://doi.org/10.1037/0096-3445.109.2.160

---

## Example

### User Request

> "我想做一个情绪点探测实验。刺激为愤怒面孔和中性面孔配对（左右呈现），呈现500 ms后消失，一个探针点出现在左侧或右侧。被试判断点的位置，左按F，右按J。60对面孔图片，每个pair出现2次（左右平衡），共120个trial。其中80个愤怒-中性对，40个中性-中性对。先20个练习，然后2个正式block各60个trial。探针呈现到按键，截止2000 ms。ITI随机500-1000 ms。用PsychoPy。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Face Pair                │    │ Probe Dot                │    │ ITI                      │
│ Content: +               │    │ Content: 左右面孔         │    │ Content: ●               │    │ Content: empty           │
│ Duration: 500 ms         │    │ Duration: 500 ms         │    │ Duration: until key      │    │ Duration: 500-1000 ms     │
│ Response: none           │    │ Response: none           │    │ Response: f/j            │    │ Response: none           │
│ File: none               │    │ File: stimuli/faces/     │    │ File: none               │    │ File: none               │
│ Condition: none          │    │ Condition: {emo}/{neu}   │    │ Condition: {probe_pos}   │    │ Condition: none          │
│ Data: none               │    │ Data: none               │    │ Data: rt, key, acc       │    │ Data: none               │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | File/Folder | Condition | Data |
|--------|---------|----------|----------|-------------|-----------|------|
| Fixation | + | 500 ms | none | none | none | none |
| Face Pair | 左右面孔 | 500 ms | none | stimuli/faces/ | {emotional}, {neutral} | none |
| Probe Dot | ● (左或右) | until key (deadline 2000 ms) | f=左, j=右 | none | {probe_position} | rt, key, acc |
| ITI | empty | 500-1000 ms random | none | none | none | none |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| Experiment name | Emotional Dot-Probe Task |
| Platform | PsychoPy |
| Task type | Dot-probe (attentional bias) |
| Stimulus type | Angry and neutral face pairs |
| SOA | 500 ms |
| Trial count | 120 total (80 angry-neutral + 40 neutral-neutral) |
| Probe type | Dot, left/right discrimination |
| Response mapping | F=左, J=右 |
| Phases | Instruction → Practice(20) → Block1-2(60 each) |

### Missing Information

1. Fixation not stated → assumed 500 ms
2. Face image file naming convention → will ask
3. Image size and position → will ask

### Assumptions

- Images preloaded at startup (120+ image files)
- Left/right positions at fixed x coordinates (e.g., ±5° visual angle)
- Dot is a small filled circle (~0.5° diameter)
- Neutral-neutral pairs as baseline (40 trials)
- Emotional face position counterbalanced (50% left, 50% right)

### Expected Code Architecture

```
dot_probe_emotional.py
├── Parameters (SOA, positions, probe size, timing)
├── Window setup (units='deg')
├── Load face pair list → generate condition table
│   ├── 60 pairs × 2 repetitions = 120 trials
│   ├── Counterbalance: emotional left/right, probe left/right
│   └── 80 angry-neutral + 40 neutral-neutral
├── Preload all face images
├── Trial loop:
│   ├── Fixation (500 ms)
│   ├── Face pair (500 ms)
│   ├── Probe dot (until response, deadline 2000 ms)
│   └── ITI (500-1000 ms random)
├── Data: try/finally CSV with incremental writes
```

### Expected Data Columns

Base columns + emotional_stimulus, neutral_stimulus, emotional_position, probe_position, congruency, soa
