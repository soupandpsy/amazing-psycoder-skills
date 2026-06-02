# Change Detection Task

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/change-detection) · PsychoJS

## When to Use

User mentions: Change detection, visual working memory, VWM, change blindness, 变化检测, 视觉工作记忆. Measures the capacity and precision of visual working memory by testing whether observers can detect changes between a study array and a test probe.

## Core Logic

Participants view a brief study array containing multiple colored circles at fixed angular positions around a central fixation point. After a short retention interval, a test array is presented that is either identical to the study array (no-change trial) or has one item whose color changed (change trial). Participants respond whether they detected a change (same/different judgment).

**Two-phase design**:

1. **Change Detection Phase**: Participants judge whether any circle changed color. This phase measures basic VWM capacity — can they detect the presence of a change?
2. **Localisation Phase**: Participants identify which specific circle changed. This provides a more sensitive assay of VWM precision — do they know which item changed, not just that something changed?

Each phase has its own instructions, trial loop, and condition files. The set size (number of circles, typically 2–8) varies across trials to parametrically manipulate memory load.

**Stimuli**: Colored circles rendered programmatically at calculated angular positions around fixation (evenly spaced). Colors are specified by RGB values from CSV condition files. Circle positions stay consistent; colors change per trial.

**Trial structure**: fixation (500 ms) → memory array (100–500 ms) → blank retention interval (900–1000 ms) → test array/probe (until response, typically 2000 ms deadline). A progress counter is shown to track trial position within the session.

**Capacity estimation**: VWM capacity (k) is estimated using the formula k = N * (H – FA) / (1 – FA), where N is set size, H is hit rate (correct change detection), and FA is false alarm rate (incorrectly reporting a change on no-change trials).

## Must Confirm

- **Phases**: Both change-detection and localisation phases, or just one?
- **Set sizes**: Which set sizes to include? (typically 2, 4, 6, 8)
- **Stimulus type**: Colored circles, oriented bars, complex shapes, or other?
- **Change type**: Color change only, or also position/orientation changes?
- **Trial count per set size**: How many change and no-change trials per set size?
- **Array duration**: How long is the memory array displayed? Brief (100 ms) to prevent verbal encoding, or longer?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Memory Array             │    │ Retention Interval       │    │ Test Array / Response    │
│ Content: + at center     │    │ Content: N colored circles│   │ Content: blank           │    │ Content: N circles       │
│ Duration: 500 ms         │    │ Duration: 100-500 ms     │    │ Duration: 900-1000 ms    │    │ Duration: until key      │
│ Response: none           │    │ Response: none           │    │ Response: none           │    │ (deadline ~2000 ms)      │
│ Condition: none          │    │ Condition: {set_size}    │    │ Condition: none          │    │ Response: same/diff key  │
│ Data: none               │    │ Data: none               │    │ Data: none               │    │ Condition: {change_type} │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    │ Data: rt, key, acc       │
                                                                                                └──────────────────────────┘
```

## Data Analysis

Primary measure is working memory capacity (k) estimated from hit and false alarm rates at each set size. Also analyze overall accuracy and response time as a function of set size. Individual differences in k correlate with fluid intelligence, academic performance, and attentional control. For the localisation phase, analyze which-position accuracy as a function of set size.

## References

Luck, S. J., & Vogel, E. K. (1997). The capacity of visual working memory for features and conjunctions. *Nature, 390*(6657), 279–281. https://doi.org/10.1038/36846

Pashler, H. (1988). Familiarity and visual change detection. *Perception & Psychophysics, 44*(4), 369–378. https://doi.org/10.3758/BF03210419
