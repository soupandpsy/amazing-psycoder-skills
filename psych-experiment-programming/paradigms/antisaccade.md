# Antisaccade Task

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/antisaccade) · PsychoJS

## When to Use

User mentions: Antisaccade, anti-saccade, inhibitory control, oculomotor inhibition, 反眼跳任务. Measures the ability to inhibit a reflexive prosaccade toward a peripheral cue and instead generate a voluntary saccade to the opposite location.

## Core Logic

On each trial, a central fixation cross is presented, followed by a brief peripheral cue flash on one side of the screen. After the cue disappears, a target stimulus (often a letter or arrow) appears on the opposite side. The participant must rapidly identify the target by pressing the correct key. The critical manipulation is that the target appears in the opposite hemifield from the cue, requiring inhibition of the prepotent reflexive saccade toward the sudden-onset cue.

Trials are driven by a condition file (`conditions.xlsx`) specifying cue position, target identity, and correct answer for each trial. Trials are randomly shuffled. The cue-target asynchrony and stimulus durations are precisely controlled using frame-accurate timing.

**Response modes**: The participant selects their input method at experiment start — keyboard (left/right arrow keys or letter keys), mouse click (click on target location), or hover (move cursor to target location). This multi-modal input design accommodates different hardware setups and populations.

**Trial structure**: fixation (variable duration, typically 1000–2000 ms) → peripheral cue (brief flash, typically 200 ms) → target at opposite location (brief, typically 100–150 ms, often masked) → response window. Accuracy is determined by comparing the participant's key response to the `corr_ans` column from the condition file. Response time is measured from target onset.

**Conditions**: Typically a mix of prosaccade trials (target same side as cue) and antisaccade trials (target opposite side as cue). The antisaccade error rate (incorrect saccades toward the cue on antisaccade trials) and the latency difference between correct antisaccades and prosaccades (antisaccade cost) are the central dependent measures.

## Must Confirm

- **Response mode**: Keyboard, mouse click, or hover? Which specific keys for keyboard mode?
- **Stimulus identity**: Are targets letters (requiring letter identification), arrows (directional judgment), or simple dots (detection only)?
- **Trial mix**: What proportion of prosaccade vs. antisaccade trials? 50:50 or different ratio?
- **Timing parameters**: Fixation duration, cue duration, target duration, and response deadline?
- **Masking**: Is the target masked (e.g., by a visual pattern) after offset, or does it simply disappear?
- **Eye-tracking integration**: Is this a manual-response-only version, or does it require eye-tracking for saccade measurement?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Peripheral Cue           │    │ Target                   │    │ ITI / Response Window     │
│ Content: + at center     │    │ Content: dot/square      │    │ Content: letter/arrow    │    │ Content: blank           │
│ Duration: 1000-2000 ms   │    │ Duration: ~200 ms        │    │ Duration: 100-150 ms     │    │ Duration: until response │
│ Response: none           │    │ Response: none           │    │ Response: key/click/hover│    │ Response: none           │
│ Condition: none          │    │ Condition: cue_position  │    │ Condition: target_id     │    │ Condition: none          │
│ Data: none               │    │ Data: none               │    │ Data: rt, key, acc       │    │ Data: none               │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

## Data Analysis

Key measures: antisaccade error rate (proportion of trials where response was toward the cue side), antisaccade latency vs. prosaccade latency (antisaccade cost), and accuracy of target identification. Analyze condition differences (prosaccade vs. antisaccade) via paired t-tests or repeated-measures ANOVA. Higher error rates and longer latencies on antisaccade trials index poorer inhibitory control. Typical findings show patients with frontal lobe damage, schizophrenia, or ADHD have elevated antisaccade error rates.

## References

Hallett, P. E. (1978). Primary and secondary saccades to goals defined by instructions. *Vision Research, 18*(10), 1279–1296. https://doi.org/10.1016/0042-6989(78)90218-3

Munoz, D. P., & Everling, S. (2004). Look away: The anti-saccade task and the voluntary control of eye movement. *Nature Reviews Neuroscience, 5*(3), 218–228. https://doi.org/10.1038/nrn1345
