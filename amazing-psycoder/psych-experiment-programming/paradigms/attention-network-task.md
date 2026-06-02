# Attention Network Task (ANT)

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/attention_network_task) · PsychoJS

## When to Use

User mentions: ANT, attention network test, alerting, orienting, executive control, Fan task, 注意网络任务. A combined cued reaction time and flanker task that measures three independent attentional networks — alerting, orienting, and executive control — within a single 30-minute session.

## Core Logic

Participants respond to the direction (left or right) of a central arrow target flanked by four other arrows. The flankers can be congruent (same direction as target), incongruent (opposite direction), or neutral (lines without directional information). Target onset is preceded by one of four cue conditions:

- **No cue**: No warning signal (baseline)
- **Center cue**: Fixation point changes briefly (provides temporal alerting but no spatial information)
- **Double cue**: Both possible target locations cued simultaneously (measures alerting — temporal warning without spatial information)
- **Spatial cue**: Valid cue at the exact target location (measures orienting — spatial attention benefit)

Each trial: cue (100 ms) → fixation (400 ms) → target + flankers (max 1700 ms or until response). Participants press left or right arrow key based on the central arrow direction, ignoring flankers. Stimuli are pre-rendered as PNG images (`congLeft.png`, `incongRight.png`, etc.) covering all cue-target-flanker combinations. The condition file (`cond.xlsx`) specifies which stimulus image to display and the correct key response per trial.

**Trial count**: Typically 288 trials total (3 blocks of 96). All combinations of cue type (4) and flanker type (3) are presented, balanced across blocks.

**Attentional network scores** are computed by subtracting reaction times between specific conditions:
- **Alerting effect** = RT(no cue) – RT(double cue). Larger positive values indicate stronger alerting.
- **Orienting effect** = RT(center cue) – RT(spatial cue). Larger positive values indicate stronger orienting.
- **Executive control effect** = RT(incongruent) – RT(congruent). Larger values indicate poorer conflict resolution.

## Must Confirm

- **Cue type design**: Full ANT (4 cue types: no cue, center, double, spatial) or simplified version?
- **Flanker types**: 3 levels (congruent, incongruent, neutral) or 2 (congruent, incongruent only)?
- **Trial count**: Standard 288 trials (3 blocks x 96) or custom?
- **Stimulus format**: Pre-rendered images or programmatically drawn arrows?
- **Response deadline**: Standard 1700 ms or custom?
- **Cue validity**: Spatial cues always valid (100%), or include invalid catch trials?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Cue                      │    │ Target + Flankers        │    │ ITI                      │
│ Content: + at center     │    │ Content: */**/spatial    │    │ Content: ←←←←← or →→→→→ │    │ Content: blank           │
│ Duration: variable       │    │ Duration: 100 ms         │    │ Duration: until key      │    │ Duration: variable        │
│ Response: none           │    │ Response: none           │    │ (deadline ~1700 ms)      │    │ Response: none           │
│ Condition: none          │    │ Condition: {cue_type}    │    │ Response: left/right key │    │ Condition: none          │
│ Data: none               │    │ Data: none               │    │ Condition: {flanker_type}│    │ Data: none               │
└──────────────────────────┘    └──────────────────────────┘    │ Data: rt, key, acc       │    └──────────────────────────┘
                                                                └──────────────────────────┘
```

## Data Analysis

Primary outcomes are the three network scores (alerting, orienting, executive control). Remove error trials and RT outliers (e.g., <200 ms or >3 SD). Analyze by computing mean RT for each condition and deriving the difference scores. Common findings: the three networks are largely independent; executive control deficits are associated with ADHD, schizophrenia, and aging.

## References

Fan, J., McCandliss, B. D., Sommer, T., Raz, A., & Posner, M. I. (2002). Testing the efficiency and independence of attentional networks. *Journal of Cognitive Neuroscience, 14*(3), 340–347. https://doi.org/10.1162/089892902317361886
