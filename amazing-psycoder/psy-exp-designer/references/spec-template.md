# Experiment Specification Template

Use this template to formalize an experiment before coding. Fill in what is known; flag what is missing.

> **Note**: For active use, the [experiment config YAML](config-schema.md) is the primary artifact. This template serves as a reference for the full specification structure — all fields here correspond to config YAML sections. The unified workflow progressively fills the config YAML through 5 phases.

## 1. Meta

| Field | Value |
|-------|-------|
| Experiment name | |
| Platform | PsychoPy / Psychtoolbox / jsPsych |
| Task type | Go/No-go / Navon / Priming / Stroop / Eriksen Flanker / Simon / Rating / Stop-signal / IAT / N-back / Dot-probe / Visual search / Task switching / EAST |

## 2. Sequence Structure

| Sequence | Execution | Windows | Description |
|----------|-----------|---------|-------------|
| Start | once | | Welcome screen, task explanation |
| Practice | loop × 20 | | Trials with feedback, can repeat |
| Main | loop × 80 | | Formal experiment trials |
| Rest | once | | Pause screen |
| End | once | | Thank you, debrief |

## 3. Sequence Details

- Sequence order (top to bottom):
- Per-sequence execution mode: once / loop + repetition count
- Per-sequence shuffle: yes / no
- Per-sequence show_in restriction: none / practice / formal

## 4. Trial Event Sequence

Represent each Sequence as an independent row with windows displayed as compact cards connected by arrows (→). Sequence order is top-to-bottom; window order is left-to-right.

```text
序列: Trial
  execution: loop (每个试次一次，重复 N 次)

  ┌─ Fixation ─┐  ┌─ Stimulus ───┐  ┌─ Response ────┐  ┌─ ITI ──────┐
  │ "+"        │  │ "{stimulus}" │  │ "{stimulus}"  │  │ ""         │
  │ 500ms      │→ │ 500ms        │→ │ until_key     │→ │ 500-800ms  │
  │ 无响应     │  │ 无响应       │  │ [f, j, k]     │  │ 无响应     │
  └────────────┘  └──────────────┘  └───────────────┘  └────────────┘
                                            RT: self
                                            数据: rt, key, acc

序列: Start       → execution: once     → [MISSING]
序列: Practice    → execution: loop×20  → 同上 + Feedback 窗口
序列: Main        → execution: loop×80  → 同上 (无 Feedback)
序列: Rest        → execution: once     → [MISSING]
序列: End         → execution: once     → [MISSING]
```

Then fill the supporting table for each window in the trial sequence:

| 窗口 | 内容 | 持续时间 | 响应 | 条件绑定 | 数据 |
|--------|---------|----------|----------|-----------------|------|
| Fixation | "+" | 500ms | 无 | 无 | onset |
| Stimulus | {stimulus} | 500ms | 无 | {stimulus} | onset |
| Response | {stimulus} | until_key | [f, j, k] | {stimulus}, {correct_response} | onset, rt, key, acc |
| Feedback | correct/incorrect | 500ms | 无 | 无 | 无 |
| ITI | "" | [500, 800] | 无 | 无 | 无 |

Mark unclear items as `[MISSING]` directly in the card and table. Do not invent values silently.

## 5. Stimulus

- Source: image files / text / shapes / generated
- File path / naming convention:
- Image size / position:
- Preload or generate per trial:

## 6. Response Rules

| Rule | Value |
|------|-------|
| Allowed keys | |
| Response deadline (ms) | |
| Correct answer mapping | |
| No-go rule (if applicable) | |
| Timeout handling | |

## 7. Randomization

- Within-sequence trial order: random / fixed / pseudorandom
- Between-sequence: same / re-randomize
- Counterbalancing: none / across subjects / within subject
- Constraints: no more than N consecutive same-condition trials

## 8. Data Output Contract

List the concrete column names that implement the semantic roles in [data-recording.md](data-recording.md): participant/session and trial identity, design/exposure, applicable raw response/timing/scoring, response status, and provenance. Add a linked event table for repeated within-trial events. State RT units/onset/event and missingness conventions explicitly; do not use numeric sentinels for missing RT.
