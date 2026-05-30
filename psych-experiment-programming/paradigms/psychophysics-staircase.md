# Psychophysics Staircase (Adaptive Threshold Estimation)

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/staircase_demo) · PsychoJS

## When to Use

User mentions: Staircase, psychophysics, adaptive threshold, orientation discrimination, just noticeable difference, 心理物理阶梯法, 自适应阈值. An adaptive psychophysical procedure that efficiently estimates sensory thresholds by adjusting stimulus intensity based on the participant's recent performance.

## Core Logic

The staircase procedure adaptively changes the difficulty of a perceptual discrimination task to converge on a participant's threshold. This implementation is a custom staircase (no built-in `MultiStairHandler`) that measures the minimal orientation difference at which a participant can distinguish between two tilted gratings.

**Task**: On each trial, two grating images are presented — one on the left and one on the right. One grating is tilted slightly clockwise, the other counterclockwise. The participant must indicate which side has the clockwise-tilted grating by pressing the left or right arrow key (2AFC — two-alternative forced choice).

**Staircase parameters** (all configurable in code):
- **Starting value**: 70 degrees (large initial orientation difference, easy to discriminate)
- **Step sizes**: [10, 5, 2, 1, 0.5] degrees — progressively finer steps across successive reversals for precise threshold estimation
- **Up/Down rule**: 1-up 1-down (converges to 50% threshold). Each correct response decreases the difference (makes it harder); each incorrect response increases the difference (makes it easier).
- **Number of reversals**: 5 — the staircase stops after 5 direction changes
- **Bounds**: min 0 degrees, max 90 degrees
- **Direction tracking**: Starts in "down" direction (decreasing orientation difference after correct responses)

**Reversals and threshold**: A "reversal" occurs when the staircase changes direction (from decreasing to increasing, or vice versa). The threshold is calculated as the average of the stimulus levels (orientation differences) at all reversal points. The first few reversals are sometimes excluded to allow the staircase to settle.

**Common staircase rules**:
- 1-up 1-down → converges to 50% threshold
- 2-up 1-down → converges to ~70.7% threshold (most common for detection tasks)
- 3-up 1-down → converges to ~79.4% threshold

**Safety limits**: A maximum number of trials (e.g., 100) serves as a safety net if the required number of reversals is not met.

## Must Confirm

- **Perceptual dimension**: Orientation discrimination (grating tilt), contrast detection, motion coherence, auditory frequency, or other?
- **Up/Down rule**: 1-up 1-down (50% threshold), 2-up 1-down (~70.7%), or 3-up 1-down (~79.4%)?
- **Starting value**: Large initial difference (easy) or near-threshold (faster convergence)?
- **Step sizes**: What step size sequence? Single fixed step or decreasing sequence?
- **Number of reversals**: How many reversals before stopping? (5-8 typical)
- **Maximum trials**: Safety limit on total trials?
- **Threshold calculation**: Average of all reversal values, or exclude first N reversals?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Grating Pair             │    │ Feedback (optional)      │    │ ITI                      │
│ Content: + at center     │    │ Content: 2 tilted        │    │ Content: correct/incorrect│   │ Content: blank           │
│ Duration: 500 ms         │    │   gratings (L and R)     │    │ Duration: 300 ms         │    │ Duration: 500 ms         │
│ Response: none           │    │ Duration: until key      │    │ Response: none           │    │ Response: none           │
│ Condition: none          │    │ Response: left/right key │    │ Condition: none          │    │ Condition: none          │
│ Data: none               │    │ Condition: {level}       │    │ Data: none               │    │ Data: none               │
└──────────────────────────┘    │   (orientation difference)│    └──────────────────────────┘    └──────────────────────────┘
                                │ Data: rt, key, acc,      │
                                │   level, direction       │
                                └──────────────────────────┘
```

## Data Analysis

The primary output is the threshold estimate (mean of reversal values). Plot the staircase trajectory (stimulus level vs. trial number) to visualize convergence. The threshold represents the just-noticeable difference (JND) for the perceptual dimension tested. Compare thresholds between conditions or groups. Check that the staircase converged (stable oscillation around threshold by final reversals) and that the number of trials was sufficient.

## References

Cornsweet, T. N. (1962). The staircase-method in psychophysics. *The American Journal of Psychology, 75*(3), 485–491. https://doi.org/10.2307/1419876

Levitt, H. (1971). Transformed up-down methods in psychoacoustics. *The Journal of the Acoustical Society of America, 49*(2B), 467–477. https://doi.org/10.1121/1.1912375
