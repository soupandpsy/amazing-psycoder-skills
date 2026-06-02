# Go/No-go Paradigm

> **Structure ref**: [spec-template.md](../references/spec-template.md)
> **Standards**: [timing](../references/timing.md) · [data recording](../references/data-recording.md) · [randomization](../references/randomization.md) · [missing info](../references/missing-information.md) · [condition file](../references/condition-file.md)

## When to Use

User mentions: Go/No-go, 反应抑制, response inhibition, go/nogo task.

## Core Logic

Participants respond to "go" stimuli and withhold response to "no-go" stimuli. Measures response inhibition. Typical: 70–80% go, 20–30% no-go, 200–400 total trials, 20–40 practice.

The task is a widely-used measure of response inhibition. On go trials, participants press a designated key (typically the space bar) in response to a target stimulus. On no-go trials, participants must withhold their response. The standard implementation presents approximately 75% go trials and 25% no-go trials. Performance is measured via accuracy (correct go responses and correct no-go withholdings), commission errors (false alarms on no-go trials), omission errors (misses on go trials), and reaction time on correct go trials.

## Must Confirm

Before generating Go/No-go code, confirm ALL of these:

1. Which stimulus is the **go** signal, and which is the **no-go** signal?
2. What key is pressed on go trials? (Single key or different keys for different go stimuli?)
3. On no-go trials, is **no response** the correct answer? (accuracy=1 for withholding)
4. How is a false alarm coded? (key pressed on no-go → accuracy=0, commission_error=1)
5. How is a miss coded? (no key on go → accuracy=0, omission_error=1)
6. What is the go/no-go ratio? (typically 70:30 or 80:20)
7. Are consecutive no-go trials allowed? Max how many in a row?
8. Is feedback shown in practice only, formal only, both, or neither?
9. **Stimulus duration**: How long is the go/no-go stimulus displayed before timeout?
10. **Fixation duration**: How long is the fixation cross shown before each trial?
11. **ITI duration**: 试次间隔时间和变化范围？
12. **OS & font**: 在什么操作系统运行？如使用中文，确认字体路径
13. **Display**: 全屏还是窗口？刺激大小和屏幕位置？
14. **Instruction text**: 指导语内容？练习和正式阶段的过渡提示？

## Do Not Assume

- Do not assume the no-go correctness rule without confirmation. In a standard Go/No-go task, withholding response on no-go trials is correct. But confirm: how is no-go accuracy coded? How are false alarms recorded? Is any non-standard response rule used (e.g., different keys for go vs no-go)?
- Do not assume go uses a single key — two go types may map to two keys
- Do not assume a 20% no-go ratio — confirm explicitly
- Do not assume feedback exists — some paradigms intentionally omit it
- Do not assume consecutive no-go trials are allowed — cap at 1–2 typically
- Do not assume RT=NaN on no-go is an error — it's expected

## Condition File Columns

Columns in the xlsx/csv file that drives each trial:

| Column | Type | Description |
|--------|------|-------------|
| go_nogo | str | `"go"` or `"nogo"` |

## Data Output Columns

In addition to base spec columns:

| Column | Type | Description |
|--------|------|-------------|
| trial_type | str | `"go"` or `"nogo"` |
| commission_error | int | 1 if responded on no-go, else 0 |
| omission_error | int | 1 if no response on go, else 0 |

## Data Analysis

Primary outcome measures for the Go/No-go task:

- **Commission error rate**: Proportion of no-go trials on which the participant incorrectly responded. This is the primary index of response inhibition failure.
- **Omission error rate**: Proportion of go trials on which the participant failed to respond.
- **Go RT**: Mean reaction time on correct go trials. Faster go RTs paired with high commission errors may indicate a speed-accuracy trade-off.
- **Signal detection measures**: d' (sensitivity) and criterion (response bias) can be computed from hit rate (correct go responses) and false alarm rate (commission errors).

Key data columns: `stimulus` (stimulus identity on each trial), `acc` (1 = correct, 0 = incorrect), `rt` (response time in ms).

## Randomization Checks

- Verify go/no-go ratio after shuffling
- No more than 2 consecutive no-go trials (adjust if needed)

## Common Failure Modes

- Incorrect accuracy coding on no-go trials
- Using `event.getKeys(maxWait=...)` instead of `keyboard.Keyboard` in timed loop
- No Escape check during response window

## References

Donders, F. C. (1969). On the speed of mental processes. *Acta Psychologica*, *30*, 412–431. (Original work published 1868)

Simmonds, D. J., Pekar, J. J., & Mostofsky, S. H. (2008). Meta-analysis of Go/No-go tasks demonstrating that fMRI activation associated with response inhibition is task-dependent. *Neuropsychologia*, *46*(1), 224–232. https://doi.org/10.1016/j.neuropsychologia.2007.07.015

Verbruggen, F., & Logan, G. D. (2008). Response inhibition in the stop-signal paradigm. *Trends in Cognitive Sciences*, *12*(11), 418–424. https://doi.org/10.1016/j.tics.2008.07.005

---

## Example

### User Request

> "我要做一个Go/No-go实验。屏幕中央呈现字母X或O，看到X尽快按空格键反应（go试次），看到O不反应（no-go试次）。80% go试次，20% no-go试次。字母呈现500 ms，反应窗口1500 ms。先20个练习trial，再4个正式block各50个trial。ITI随机500-800 ms。用PsychoPy。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Stimulus                 │    │ Response                 │    │ ITI                      │
│ Content: +               │    │ Content: X or O          │    │ Content: X or O          │    │ Content: empty           │
│ Duration: 500 ms         │    │ Duration: 500 ms         │    │ Duration: until key      │    │ Duration: 500-800 ms      │
│ Response: none           │    │ Response: none           │    │ Response: space          │    │ Response: none           │
│ File: none               │    │ File: none (text)        │    │ File: none               │    │ File: none               │
│ Condition: none          │    │ Condition: {stimulus}    │    │ Condition: {correct_resp}│    │ Condition: none          │
│ Data: none               │    │ Data: none               │    │ Data: rt, key, acc       │    │ Data: none               │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | File/Folder | Condition | Data |
|--------|---------|----------|----------|-------------|-----------|------|
| Fixation | + | 500 ms | none | none | none | none |
| Stimulus | X or O | 500 ms | none | none (text) | {stimulus} | none |
| Response | X or O | until key (deadline 1500 ms) | space | none | {correct_response} | rt, key, acc |
| ITI | empty | 500-800 ms random | none | none | none | none |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| Experiment name | Letter Go/No-go Task |
| Platform | PsychoPy |
| Task type | Go/No-go (response inhibition) |
| Go stimulus | X (press space) |
| No-go stimulus | O (withhold) |
| Go ratio | 80% |
| No-go ratio | 20% |
| Stimulus duration | 500 ms |
| Response deadline | 1500 ms |
| Phases | Instruction → Practice(20) → Block1-4(50 each) |

### Missing Information

1. Fixation not stated → assumed 500 ms (design assumption, flagged)
2. Feedback not mentioned → will ask (practice/formal/both/neither?)

### Assumptions

- Single go stimulus (X) mapped to space key
- No more than 2 consecutive no-go trials
- Feedback in practice only (standard Go/No-go practice)
- Anticipatory RT threshold: 100 ms
- No trial-level feedback in formal blocks

### Expected Code Architecture

```
gonogo.py
├── Parameters (go_key, deadline, ratio, timing)
├── Window setup
├── Stimulus preloading (TextStim for X/O)
├── Generate condition table (80:20 go:nogo)
├── Trial loop:
│   ├── Fixation (500 ms)
│   ├── Stimulus (500 ms — X or O)
│   ├── Response window (deadline 1500 ms, space key)
│   ├── Feedback (practice only)
│   └── ITI (500-800 ms random)
├── Data: try/finally CSV with incremental writes
```

### Expected Data Columns

Base columns + trial_type, commission_error, omission_error
