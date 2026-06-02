# Priming Paradigm

> **Structure ref**: [spec-template.md](../references/spec-template.md)
> **Standards**: [timing](../references/timing.md) · [data recording](../references/data-recording.md) · [randomization](../references/randomization.md) · [missing info](../references/missing-information.md) · [condition file](../references/condition-file.md)

## When to Use

User mentions: Priming, 启动, prime-target, masked prime, semantic priming, affective priming.

## Core Logic

A prime stimulus briefly precedes a target. Measures prime influence on target processing. Variants: semantic, affective, masked, response, negative priming.

## Must Confirm

Before generating priming code, confirm ALL of these:

1. **Priming type**: semantic, affective, masked, response, negative?
2. **Prime visibility**: masked (subliminal, ~20–60 ms) or visible (supraliminal)?
3. If masked: forward mask? Backward mask? Mask type?
4. **Prime-target relationship**: congruent/incongruent? Related/unrelated?
5. **SOA**: fixed or varied? What value/range?
6. **Response type**: lexical decision, categorization, evaluation?
7. **Catch trials**: prime visibility checks?
8. **Prime-only condition**: baseline measurement?
9. **ITI duration**: 试次间隔时间和变化范围？
10. **OS & font**: 在什么操作系统运行？如使用中文刺激，确认字体
11. **Display**: 全屏还是窗口？刺激大小和屏幕位置？
12. **Instruction text**: 指导语内容？

## Do Not Assume

- Do not assume forward + backward mask — some omit one or both
- Do not assume one SOA — priming effects vary with SOA
- Do not assume congruent/incongruent labeling — may be related/unrelated
- Do not assume prime duration — masked 20–60 ms, supraliminal 200–500 ms
- Do not assume response is about the target — in response priming, prime carries response info
- Do not assume target is always visible — some designs degrade target visibility

## Timing Precision

Masked priming requires frame-accurate timing:
- Use `win.flip()` for duration control, not `core.wait()`
- Validate with photodiode if prime is intended subliminal
- LCD pixel response time may make 16.7 ms primes partially visible

## Condition File Columns

Columns in the xlsx/csv file that drives each trial:

| Column | Type | Description |
|--------|------|-------------|
| prime | str | Prime stimulus identity |
| target | str | Target stimulus identity |
| prime_type | str | `"related"`, `"unrelated"`, or `"neutral"` |
| soa | int | Stimulus onset asynchrony (ms) |
| mask_present | int | 1 if mask used, 0 if not |

## Data Output Columns

| Column | Type | Description |
|--------|------|-------------|
| prime | str | Prime stimulus identity |
| target | str | Target stimulus identity |
| prime_type | str | `"congruent"`, `"incongruent"`, or `"neutral"` |
| soa | float | Stimulus onset asynchrony (ms) |
| prime_duration | float | Prime presentation duration (ms) |
| mask_type | str | `"forward"`, `"backward"`, `"none"`, or `"both"` |

## Randomization Checks

- Prime-target pairings must be counterbalanced (each target paired with each prime type equally)
- No more than 3 consecutive same-response trials
- Related/unrelated ratio balanced per block
- Verify SOA distribution if SOA is varied

## Common Failure Modes

- Using `core.wait()` for prime duration instead of frame counting
- Not clearing keyboard buffer between prime and target
- Marking all fast RTs as errors (masked priming can produce very fast RTs)

## References

Forster, K. I., & Davis, C. (1984). Repetition priming and frequency attenuation in lexical access. *Journal of Experimental Psychology: Learning, Memory, and Cognition*, *10*(4), 680–698. https://doi.org/10.1037/0278-7393.10.4.680

Meyer, D. E., & Schvaneveldt, R. W. (1971). Facilitation in recognizing pairs of words: Evidence of a dependence between retrieval operations. *Journal of Experimental Psychology*, *90*(2), 227–234. https://doi.org/10.1037/h0031564

Neely, J. H. (1977). Semantic priming and retrieval from lexical memory: Roles of inhibitionless spreading activation and limited-capacity attention. *Journal of Experimental Psychology: General*, *106*(3), 226–254. https://doi.org/10.1037/0096-3445.106.3.226

---

## Example

### User Request

> "我要做一个掩蔽启动实验。先呈现500 ms的前掩蔽（#####），然后呈现40 ms的启动词（可能是目标词的近义词或无关词），然后立即呈现目标词。被试的任务是判断目标词是真词还是假词（词汇判断），真词按F，假词按J。启动词和目标词都是中文双字词。SOA固定60 ms。先30个练习，然后3个正式block各60个trial。用PsychoPy。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │ →  │ Window 5                 │
│ Forward Mask             │    │ Prime                    │    │ Target                   │    │ Feedback                 │    │ ITI                      │
│ Content: #####           │    │ Content: 启动词           │    │ Content: 目标词           │    │ Content: 正确/错误        │    │ Content: empty           │
│ Duration: 500 ms         │    │ Duration: 40 ms          │    │ Duration: until key      │    │ Duration: 500 ms         │    │ Duration: 1000 ms        │
│ Response: none           │    │ Response: none           │    │ Response: f/j            │    │ Response: none           │    │ Response: none           │
│ File: none               │    │ File: none (text)        │    │ File: none (text)        │    │ File: none               │    │ File: none               │
│ Condition: none          │    │ Condition: {prime}       │    │ Condition: {target}      │    │ Condition: {correct_resp}│    │ Condition: none          │
│ Data: none               │    │ Data: none               │    │ Data: rt, key, acc       │    │ Data: none               │    │ Data: none               │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | File/Folder | Condition | Data |
|--------|---------|----------|----------|-------------|-----------|------|
| Forward Mask | ##### | 500 ms | none | none | none | none |
| Prime | 启动词 | 40 ms (frame-counted) | none | none (text) | {prime} | none |
| Target | 目标词 | until key (deadline 3000 ms) | f=真词, j=假词 | none (text) | {target} | rt, key, acc |
| Feedback | 正确/错误 | 500 ms | none | none | {correct_response} | none |
| ITI | empty | 1000 ms | none | none | none | none |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| Experiment name | Masked Semantic Priming (Chinese) |
| Platform | PsychoPy |
| Task type | Masked priming (lexical decision) |
| Forward mask | ##### (500 ms) |
| Prime duration | 40 ms |
| SOA | 60 ms |
| Target duration | Until response, deadline 3000 ms |
| Prime-target relationship | Related (近义词) vs Unrelated (无关词) |
| Response | Lexical decision: F=真词, J=假词 |
| Stimuli | Chinese two-character words |
| Phases | Instruction → Practice(30) → Block1-3(60 each) |

### Missing Information / Questions

1. Backward mask? Not mentioned → assumed none (prime → target directly)
2. Prime visibility check? Not mentioned → will ask: "是否需要启动词可见性检查试次？"
3. Word list: user needs to provide or confirm word pairs
4. Nonword ratio? Not stated → will ask: "假词试次占多少比例？"

### Assumptions

- No backward mask (prime → target directly, SOA=60 ms: 40 ms prime + 20 ms gap)
- Frame-accurate timing: prime = 2 frames at 60Hz (~33 ms) or 3 frames (~50 ms)
- Chinese font: PingFang.ttc (macOS)
- ITI: 1000 ms fixed
- No trial-level feedback in formal blocks

### Expected Code Architecture

```
masked_priming.py
├── Parameters (word list path, timing in frames, font config)
├── Window setup
├── Load word list → generate condition table
├── Preload masks and text stims
├── Trial loop:
│   ├── Forward mask (500 ms, frame-counted)
│   ├── Prime (40 ms, frame-counted)
│   ├── Target (until response, deadline 3000 ms)
│   └── ITI (1000 ms)
├── Data: try/finally CSV with incremental writes
```

### Expected Data Columns

Base columns + prime, target, prime_type, soa, prime_duration, mask_type
