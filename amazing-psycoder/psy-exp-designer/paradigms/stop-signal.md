# Stop-Signal Paradigm

> **Structure ref**: [spec-template.md](../references/spec-template.md)
> **Standards**: [timing](../references/timing.md) · [data recording](../references/data-recording.md) · [randomization](../references/randomization.md) · [missing info](../references/missing-information.md) · [condition file](../references/condition-file.md)

## When to Use

User mentions: Stop-signal, 停止信号, SST, stop-signal task, SSRT, stop-signal reaction time.

## Core Logic

Participants respond to a "go" stimulus, but on a subset of trials a "stop" signal appears after a delay, instructing them to withhold the response. Measures the latency of the inhibitory process (SSRT).

Typical: 70–75% go trials, 25–30% stop trials. SSD (stop-signal delay) adapts based on performance — increases after successful stops, decreases after failed stops — to converge on ~50% stopping probability.

## Must Confirm

Before generating stop-signal code, confirm ALL of these:

1. **Go stimulus**: what is the go signal?
2. **Stop signal**: what is the stop signal? (tone, visual cue, color change?)
3. **Response mapping**: single key or choice RT? If choice, what are the go stimuli?
4. **SSD algorithm**: adaptive staircase? If so, step size (typically 50 ms)?
5. **Initial SSD**: starting delay (typically 250 ms)?
6. **SSD bounds**: minimum and maximum allowed SSD (typically 50 ms–800 ms)?
7. **Stop probability**: what fraction of trials have a stop signal? (typically 25–30%)
8. **Go trial deadline**: response deadline for go trials? (typically 1000–1500 ms)
9. **Feedback**: is inhibition performance feedback shown?
10. **ITI duration**: 试次间隔时间和变化范围？
11. **OS & font**: 在什么操作系统运行？如使用中文，确认字体
12. **Display**: 全屏还是窗口？刺激大小和屏幕位置？
13. **Instruction text**: 指导语内容？如何向被试说明停止信号？

## Do Not Assume

- Do not assume single go key — choice RT stop-signal uses two keys
- Do not assume fixed SSD — adaptive tracking is the standard method
- Do not assume a step size — confirm (50 ms is typical but varies)
- Do not assume SSDs are independent per subject — they should be tracked separately
- Do not assume feedback is shown — many SST designs omit it to avoid slowing
- Do not assume SSRT is calculated online — it's typically computed offline using the integration method

## SSRT Calculation (for reference)

SSRT is estimated from the go RT distribution and the SSD:
- Integration method: find the nth percentile of go RTs where n = p(respond|stop) × 100, subtract mean SSD
- This is an offline calculation. The experiment code should save sufficient data for it.

## Condition File Columns

Columns in the xlsx/csv file that drives each trial:

| Column | Type | Description |
|--------|------|-------------|
| stop_trial | int | 1 if stop signal present, 0 if not |
| ssd | float | Stop-signal delay (ms). Pre-filled for fixed SSD; `"adaptive"` for staircase |

## Data Output Columns

| Column | Type | Description |
|--------|------|-------------|
| trial_type | str | `"go"` or `"stop"` |
| ssd | float | Stop-signal delay (ms). `None` for go trials |
| stop_response | int | 1 if responded on stop trial, 0 if successfully inhibited |
| go_rt | float | RT on go trials (for SSRT calculation) |
| go_omission | int | 1 if no response on go trial |

## Randomization Checks

- Stop-signal trials must not cluster — distribute evenly within block
- Verify stop probability matches target (25–30%)

## Common Failure Modes

- Not implementing adaptive SSD tracking correctly (wrong step direction)
- Not recording SSD per trial (required for SSRT calculation)
- Using a fixed deadline that masks go RT distribution (go deadline should be generous enough to capture the full RT distribution)
- Not clearing keyboard buffer before each trial
- Confusing stop-signal with go/no-go — SST has an initial go response that must be cancelled

## References

Logan, G. D., & Cowan, W. B. (1984). On the ability to inhibit thought and action: A theory of an act of control. *Psychological Review*, *91*(3), 295–327. https://doi.org/10.1037/0033-295X.91.3.295

Logan, G. D., Schachar, R. J., & Tannock, R. (1997). Impulsivity and inhibitory control. *Psychological Science*, *8*(1), 60–64. https://doi.org/10.1111/j.1467-9280.1997.tb00545.x

Verbruggen, F., & Logan, G. D. (2008). Response inhibition in the stop-signal paradigm. *Trends in Cognitive Sciences*, *12*(11), 418–424. https://doi.org/10.1016/j.tics.2008.07.005

Verbruggen, F., Aron, A. R., Band, G. P., Beste, C., Bissett, P. G., Brockett, A. T., ... & Boehler, C. N. (2019). A consensus guide to capturing the ability to inhibit actions and impulsive behaviors in the stop-signal task. *eLife*, *8*, e46323. https://doi.org/10.7554/eLife.46323

---

## Example

### User Request

> "我要做一个停止信号任务。被试对箭头方向做按键反应：左箭头按F，右箭头按J。在25%的试次中，箭头出现后会有一个声音信号（750Hz纯音），表示需要停止反应。停止信号延迟（SSD）用自适应阶梯法，初始250 ms，步长50 ms，范围50-800 ms。正式实验4个block各80个trial，开始前有30个练习trial。箭头呈现直到按键或到1000 ms截止，ITI随机800-1200 ms。用PsychoPy。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Go Stimulus              │    │ Feedback                 │    │ ITI                      │
│ Content: +               │    │ Content: ← or →          │    │ Content: 正确/错误        │    │ Content: empty           │
│ Duration: 500 ms         │    │ Duration: until key      │    │ Duration: 500 ms         │    │ Duration: 800-1200 ms     │
│ Response: none           │    │ Response: f/j            │    │ Response: none           │    │ Response: none           │
│ File: none               │    │ File: none (text)        │    │ File: none               │    │ File: none               │
│ Condition: none          │    │ Condition: {arrow_dir}   │    │ Condition: {correct_resp}│    │ Condition: none          │
│ Data: none               │    │ Data: rt, key, acc, ssd  │    │ Data: none               │    │ Data: none               │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | File/Folder | Condition | Data |
|--------|---------|----------|----------|-------------|-----------|------|
| Fixation | + | 500 ms | none | none | none | none |
| Go Stimulus | ← or → (+ 750Hz tone if stop) | until key (deadline 1000 ms) | f=左, j=右 (withhold on stop) | none (text) | {arrow_dir} | rt, key, acc, ssd, stop_trial |
| Feedback | 正确/错误/太慢 | 500 ms | none | none | {correct_response} | none |
| ITI | empty | 800-1200 ms random | none | none | none | none |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| Experiment name | Stop-Signal Task (Arrows) |
| Platform | PsychoPy |
| Task type | Stop-signal |
| Go stimulus | Left arrow (←) or Right arrow (→) |
| Stop signal | 750Hz pure tone, auditory |
| Response mapping | F=左箭头, J=右箭头 |
| Stop probability | 25% of trials |
| SSD algorithm | Adaptive staircase, independent per subject |
| Initial SSD | 250 ms |
| SSD step size | 50 ms |
| SSD bounds | 50 ms–800 ms |
| Go deadline | 1000 ms |
| Phases | Instruction → Practice(30) → Block1-4(80 each) |

### Missing Information

1. Fixation not stated → assumed 500 ms (design assumption, flagged)
2. Feedback in practice only or formal too? → will ask
3. Stop-signal duration? → assumed 100 ms tone

### Assumptions

- Stop signal is auditory (750Hz tone, 100 ms duration)
- Two independent SSD staircases (one per go response direction) — standard approach
- Equal left/right arrow frequency within go and stop trials
- No feedback in formal blocks (avoids slowing responses)
- Keyboard response prioritized over tone onset for stop trials
- Anticipatory RT threshold: 100 ms

### Expected Code Architecture

```
stop_signal.py
├── Parameters (SSD params, keys, timing, stop probability)
├── Window setup + sound preloading (750Hz tone via sound.Sound)
├── SSD tracking: ssd = 250 ms initial, ±50 ms per staircase
├── Trial loop:
│   ├── Fixation (500 ms)
│   ├── Arrow onset (kb.clock reset via callOnFlip)
│   ├── [If stop trial] Schedule tone after current SSD
│   ├── Response window (deadline 1000 ms)
│   ├── Update SSD: increase 50 ms if stop success, decrease 50 ms if fail
│   ├── Feedback (if applicable, 500 ms)
│   └── ITI (800-1200 ms random)
├── Data: try/finally CSV with incremental writes
```

### Expected Data Columns

Base columns + trial_type, ssd, stop_response, go_rt, go_omission
