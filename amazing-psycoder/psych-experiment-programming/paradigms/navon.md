# Navon Paradigm

> **Structure ref**: [spec-template.md](../references/spec-template.md)
> **Standards**: [timing](../references/timing.md) · [data recording](../references/data-recording.md) · [randomization](../references/randomization.md) · [missing info](../references/missing-information.md) · [condition file](../references/condition-file.md)

## When to Use

User mentions: Navon, 整体局部, global/local, hierarchical letters, Navon task.

## Core Logic

Hierarchical letters (large letter made of small letters). Respond to either global or local level. Conditions: congruent (levels match), incongruent (levels differ), neutral (one level non-letter). 80–160 trials per condition.

This is an interference-based cognitive psychology paradigm. Large letters are composed of smaller letters, and the small and large letters may be the same (congruent) or different (incongruent). The key question is whether incongruence between levels affects reaction time to detect the large letter (global precedence) or the small letter (local interference). Navon (1977) originally demonstrated the global precedence effect — participants are faster to identify the global letter than the local letters, and global information interferes with local processing more than the reverse. A feedback routine is typically included, with multiple stimuli appearing and disappearing at different times within each trial.

## Must Confirm

Before generating Navon code, confirm ALL of these:

1. **Attended level**: blocked (one level per block) or trial-by-trial cued?
2. If cued: cue type? Verbal (`"GLOBAL"`/`"LOCAL"`), spatial (arrow), or symbolic?
3. **Target letters**: which letters? (e.g., H and S)
4. **Response mapping**: one key per target letter?
5. **CSI** (cue-stimulus interval): how long between cue and target?
6. **Stimulus source**: loaded from image files or generated in code? If files: naming convention? If generated: font/grid rule?
7. **Visual angle**: confirm global (~5°) and local (~0.5°) letter sizes; is monitor calibration available?
8. Congruency conditions: which exact combinations?
9. **ITI duration**: 试次间隔时间和变化范围？
10. **OS & font**: 在什么操作系统运行？如使用中文，确认字体
11. **Display**: 全屏还是窗口？屏幕分辨率？
12. **Instruction text**: 指导语内容？如何向被试说明整体/局部注意？

## Do Not Assume

- Do not assume blocked design — many use trial-by-trial cueing
- Do not assume cue is always valid — some include invalid-cue trials
- Do not assume letters are H and S — confirm
- Do not assume ~5° global / ~0.5° local — confirm visual angle
- Do not assume the stimulus source — Navon stimuli may be pre-rendered image files OR generated in code. Confirm before choosing the implementation approach

## Stimulus Source

Navon stimuli can come from either source — confirm which:

**Pre-rendered image files**: loaded via `visual.ImageStim`. Requires consistent file naming (e.g., `H_made_of_S.png`). Validate all files exist at startup.

**Programmatic generation**: create local letter via `visual.TextStim`, tile in a grid for global outline, compose with `visual.BufferImageStim` and cache. Used when visual angle or letter combinations need runtime control.

## Condition File Columns

Columns in the xlsx/csv file that drives each trial:

| Column | Type | Description |
|--------|------|-------------|
| global_letter | str | Large letter identity |
| local_letter | str | Small letter identity |
| congruency | str | `"congruent"` or `"incongruent"` |
| attended_level | str | `"global"` or `"local"` |

## Data Output Columns

| Column | Type | Description |
|--------|------|-------------|
| attended_level | str | `"global"` or `"local"` |
| global_letter | str | Large letter identity |
| local_letter | str | Small letter identity |
| congruency | str | `"congruent"`, `"incongruent"`, or `"neutral"` |
| cue_validity | str | `"valid"`, `"invalid"`, or `"neutral"` (if cued) |
| switch | int | 1 if attended level differs from previous trial |

## Data Analysis

Primary analysis for the Navon task involves comparing reaction times across congruency conditions:

- **Sort data by congruency** (congruent vs. incongruent) and compare mean reaction times. Incongruent trials typically yield slower RTs, reflecting interference between global and local processing levels.
- **Global precedence effect**: Compare RTs for global-level judgments vs. local-level judgments. Faster global RTs indicate the classic global precedence effect (Navon, 1977).
- **Interference asymmetry**: Compute the interference effect separately for each attended level (RT_incongruent - RT_congruent at global level vs. local level). Greater interference when attending to the local level supports global precedence.
- **Switch costs**: If using a trial-by-trial cued design, compare RTs on switch trials (attended level changes from previous trial) vs. repeat trials.

Data output includes an Excel file with trial-level data; group by congruence condition for analysis.

## Randomization Checks

- Equal trial count per congruency condition within each block
- If attending level switches trial-by-trial: no more than 3-4 consecutive same-level trials
- Counterbalance cue validity if invalid-cue trials are used

## Common Failure Modes

- Assuming the wrong stimulus source without confirmation (pre-rendered images vs. code-generated)
- Not caching generated stimuli when using the code-generation approach (re-generating per trial causes jitter)
- Confusing global/local letter identity with congruency

## References

Navon, D. (1977). Forest before trees: The precedence of global features in visual perception. *Cognitive Psychology*, *9*(3), 353–383. https://doi.org/10.1016/0010-0285(77)90012-3

Navon, D. (2003). What does a compound letter tell the psychologist's mind? *Acta Psychologica*, *114*(3), 273–309. https://doi.org/10.1016/j.actpsy.2003.06.002

---

## Example

### User Request

> "我需要做一个Navon实验。被试看到由小字母组成的大字母，任务是判断大字母是H还是S。H按F键，S按J键。小字母也可能是H或S，但不需要判断。一致条件（大小字母相同）和冲突条件（大小字母不同）各半。先20个练习，再4个正式block各40个trial。整体字母大约5度视角，局部字母约0.5度。用PsychoPy完成。"

### Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Navon Target             │    │ Feedback                 │    │ ITI                      │
│ Content: +               │    │ Content: Navon大字       │    │ Content: 正确/错误        │    │ Content: empty           │
│ Duration: 500 ms         │    │ Duration: until key      │    │ Duration: 500 ms         │    │ Duration: [MISSING]      │
│ Response: none           │    │ Response: f/j            │    │ Response: none           │    │ Response: none           │
│ File: none               │    │ File: [MISSING]          │    │ File: none               │    │ File: none               │
│ Condition: none          │    │ Condition: {letter}      │    │ Condition: {correct_resp}│    │ Condition: none          │
│ Data: none               │    │ Data: rt, key, acc       │    │ Data: none               │    │ Data: none               │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

| Window | Content | Duration | Response | File/Folder | Condition | Data |
|--------|---------|----------|----------|-------------|-----------|------|
| Fixation | + | 500 ms | none | none | none | none |
| Navon Target | 大字母+小字母 | until key (deadline [MISSING]) | f=H, j=S | [MISSING] | {letter} | rt, key, acc |
| Feedback | 正确/错误 | 500 ms | none | none | {correct_response} | none |
| ITI | empty | [MISSING] | none | none | none | none |

### Parsed Experiment Specification

| Field | Value |
|-------|-------|
| Experiment name | Navon Global/Local Task |
| Platform | PsychoPy |
| Task type | Navon (global-level, blocked) |
| Attended level | Global only (大字母) |
| Target letters | H → F, S → J |
| Congruency conditions | Congruent (H/H, S/S), Incongruent (H/S, S/H) |
| Ratio | 50:50 congruent:incongruent |
| Stimulus size | Global ~5° VA, Local ~0.5° VA |
| Phases | Instruction → Practice(20) → Block1-4(40 each) |

### Missing Information

1. Response deadline not stated → will ask (Navon tasks are typically slower, 2000-3000 ms)
2. ITI not stated → will ask
3. Feedback not mentioned → will ask: practice only, formal only, or both?
4. Stimulus source not stated → will ask: pre-rendered images or code-generated?

### Assumptions

- Blocked design (global level only — user said "判断大字母", no switching)
- Equal trial count per condition within each block (20 congruent + 20 incongruent)
- No neutral condition (only congruent and incongruent)

### Expected Code Architecture

```
navon_global.py
├── Parameters section
├── Window setup (units='deg' for visual angle)
├── Stimulus setup (confirm source: images or generated)
├── Instruction + practice + 4 formal blocks
├── Data: try/finally CSV
```

### Expected Data Columns

Base columns + global_letter, local_letter, congruency, attended_level
