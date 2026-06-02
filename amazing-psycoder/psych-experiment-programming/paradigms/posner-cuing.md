# Posner Cuing Task

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/posner) · reference

## When to Use

User mentions: Posner cuing, spatial cuing, covert attention, endogenous/exogenous attention, 波斯纳线索任务, 空间注意. Measures the ability to orient covert spatial attention in response to predictive or non-predictive cues, dissociating voluntary (endogenous) and reflexive (exogenous) orienting.

## Core Logic

Participants fixate on a central point and respond as quickly as possible to a target that appears in one of two (or more) peripheral locations. Before target onset, a cue directs attention to a location. On valid trials (typically ~80% of cued trials), the target appears at the cued location. On invalid trials (~20%), the target appears at the uncued location. Neutral trials (no directional cue) provide a baseline.

The cuing effect (invalid RT – valid RT) measures the cost-plus-benefit of spatial attention. Two cue types are typically used: peripheral cues (a brief flash at the target location, e.g., 50 ms) that elicit reflexive, exogenous attention shifting, and central symbolic cues (an arrow at fixation) that require voluntary, endogenous attention shifting. Peripheral cues produce rapid (peak ~100-150 ms) but transient facilitation followed by inhibition of return (IOR) at longer cue-target intervals (>300 ms). Central cues produce slower but sustained facilitation.

Key temporal parameter: stimulus onset asynchrony (SOA) between cue and target is varied (e.g., 100, 300, 500, 800 ms) to map the time course of attentional effects. Short SOAs with peripheral cues show facilitation; long SOAs show IOR (slower responses to cued vs. uncued locations).

## Data Analysis

Compute mean RT for valid, invalid, and neutral conditions. Test cuing effect (invalid – valid RT) and its subscores: benefit (neutral – valid), cost (invalid – neutral). Analyze cuing effect as a function of SOA and cue type. IOR is indexed by valid > invalid RT at long SOAs. Compare cuing effects between populations (e.g., reduced cuing effects in neglect, schizophrenia; altered IOR in ADHD).

## Must Confirm

- **Target type**: Gabor patch, simple shape, or letter? What visual properties (spatial frequency, contrast, size)?
- **Cue type**: Peripheral box cue (reflexive exogenous), central arrow (voluntary endogenous), or both?
- **Cue validity ratio**: What proportion valid vs invalid? (typically 80% valid / 20% invalid)
- **SOA values**: What cue-target onset asynchronies to use? (e.g., 100, 300, 500, 800 ms)
- **Trial counts**: How many trials per condition × SOA combination?
- **Response mapping**: Left/right arrow keys for left/right target? Or detection key (one key for any target)?

## Trial Window Timeline

From the psychtoolbox reference implementation (Gabor target, peripheral box cue):

```
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │ →  │ Window 5                 │
│ Fixation                 │    │ Cue                      │    │ CTI (Gap)                │    │ Target                   │    │ Response + ITI           │
│ Content: fixation dot    │    │ Content: box cue (L/R)   │    │ Content: fixation dot    │    │ Content: Gabor target    │    │ Content: blank grey      │
│ Duration: 500 ms         │    │ + fixation dot           │    │ Duration: 300 ms (CTI)   │    │ Duration: 150 ms         │    │ Duration: until keypress │
│ Response: none           │    │ Duration: 150 ms         │    │ Response: none           │    │ Response: none           │    │ Response: LeftArrow/     │
│ Condition: none          │    │ Response: none           │    │ Condition: {cue_pos}     │    │ Condition: {target_pos}  │    │   RightArrow             │
│ Data: none               │    │ Condition: {cue_pos}     │    │ Data: none               │    │ Data: none               │    │ Data: rt, correctness    │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

2×2 factorial design: cue position (left/right) × target position (left/right). Contingent = same location; Non-contingent = different location. Key parameter: Cue-Target Interval (CTI) — 300ms in reference implementation, varied in full paradigm.

## Condition File Structure

| Column | Values | Description |
|--------|--------|-------------|
| cue_pos | 0=left, 1=right | Position of the box cue |
| target_pos | 0=left, 1=right | Position of the Gabor target |
| correct_response | left/right | Expected key response |
| contingency | contingent/non-contingent | Whether cue and target share location |

Base matrix `[0 0 1 1; 0 1 0 1]` (4 combinations) repeated `numReps` times, then shuffled. `cue_pos == target_pos` → contingent; `cue_pos != target_pos` → non-contingent.

## References

Posner, M. I. (1980). Orienting of attention. *Quarterly Journal of Experimental Psychology, 32*(1), 3–25. https://doi.org/10.1080/00335558008248231

Posner, M. I., Snyder, C. R. R., & Davidson, B. J. (1980). Attention and the detection of signals. *Journal of Experimental Psychology: General, 109*(2), 160–174. https://doi.org/10.1037/0096-3445.109.2.160

Scarfe, P. (n.d.). Posner cuing experiment (Psychtoolbox demo). https://peterscarfe.com/poserCuingExperiment.html
