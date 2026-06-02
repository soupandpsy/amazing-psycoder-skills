# Continuous Performance Test (CPT)

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/continuous_performance_test) · PsychoJS

## When to Use

User mentions: CPT, continuous performance test, sustained attention, vigilance, 持续注意测试, 连续表现测试. Measures sustained attention and vigilance over an extended period by requiring participants to respond to frequent go stimuli while withholding responses to infrequent no-go targets.

## Core Logic

This implementation is a go/no-go CPT variant. Participants view a rapid stream of letter stimuli presented one at a time. They must press the spacebar for every letter **except** the target letter 'X'. This inverts the typical CPT structure (where the target is rare and requires a response) — here the target 'X' requires response **inhibition**, making it a measure of both sustained attention and inhibitory control.

**Trial structure**: fixation cross (1000 ms) → letter stimulus (1000 ms) → next trial. The keyboard is monitored during the letter presentation window. Each trial's condition comes from `conditions.xlsx` with columns specifying the letter to display and the correct answer (`corrAns`: 'space' for go trials, 'none' for no-go/X trials).

**Accuracy logic**: Two-path accuracy check. When a key is pressed, the response is compared against `corrAns`. When no key is pressed, the code checks whether `corrAns` is 'none' (correct withholding on X trials). A `correct_counter` accumulates correct trials and is displayed as the final score.

**Trial count and target frequency**: The condition file defines the sequence. The target 'X' typically appears on 20–30% of trials. A trial counter (e.g., "Trial 12 / 120") is shown throughout the experiment to provide participant pacing.

**Key dependent variables**:
- **Omission errors**: Failing to press spacebar on non-X trials (indexes inattention)
- **Commission errors**: Pressing spacebar on X trials (indexes impulsivity / inhibitory failure)
- **Reaction time**: For correct go responses; RT variability over time indexes attentional fluctuation
- **d-prime**: Signal detection measure combining hits and false alarms

## Must Confirm

- **CPT variant**: Go/no-go (this version: respond to all except X), X-CPT (respond only to X), AX-CPT (respond to X only when preceded by A), or Identical Pairs?
- **Stimulus type**: Letters (single uppercase), digits, or shapes?
- **Trial count**: Total number of trials? (needs to be substantial, 100–300+, to tax sustained attention)
- **Stimulus and fixation durations**: 1000 ms each, or custom?
- **Response key**: Spacebar for all go responses, or specific keys?
- **No-go target**: Single letter 'X', or multiple no-go stimuli?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │
│ Fixation                 │    │ Letter Stimulus          │
│ Content: + at center     │    │ Content: letter (A-Z)    │
│ Duration: 1000 ms        │    │ Duration: 1000 ms        │
│ Response: none           │    │ Response: spacebar       │
│ Condition: none          │    │ (withhold on X)          │
│ Data: none               │    │ Condition: {letter}      │
└──────────────────────────┘    │ Data: rt, key, acc,      │
                                │   omission/commission     │
                                └──────────────────────────┘
```

## Data Analysis

Key measures: omission errors (misses), commission errors (false alarms), mean RT (and RT variability/SD), signal detection measures (d', criterion). Performance decline across blocks indexes the vigilance decrement. Examine commission errors as a behavioral index of impulsivity/inhibitory control, and omissions/RT variability as indices of inattention. The CPT is widely used in ADHD assessment; elevated commission errors and RT variability are characteristic.

## References

Rosvold, H. E., Mirsky, A. F., Sarason, I., Bransome, E. D., Jr., & Beck, L. H. (1956). A continuous performance test of brain damage. *Journal of Consulting Psychology, 20*(5), 343–350. https://doi.org/10.1037/h0043220

Cohen, J. D., Barch, D. M., Carter, C., & Servan-Schreiber, D. (1999). Context-processing deficits in schizophrenia: Converging evidence from three theoretically motivated cognitive tasks. *Journal of Abnormal Psychology, 108*(1), 120–133. https://doi.org/10.1037/0021-843X.108.1.120
