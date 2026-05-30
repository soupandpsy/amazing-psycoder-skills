# Balloon Analogue Risk Task (BART)

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/bart) · reference

## When to Use

User mentions: BART, balloon task, risk-taking, 气球模拟风险任务. A behavioral measure of risk-taking propensity in which participants inflate balloons to earn rewards, trading off the risk of bursting and losing earnings.

## Core Logic

On each trial, a balloon is displayed and the participant can repeatedly press a key to pump it up. Each pump increases the balloon's size and adds a small amount to a temporary reward counter. However, every pump also carries a risk: each balloon has a hidden explosion point, and if the participant exceeds it, the balloon bursts, all temporary earnings for that trial are lost, and a new balloon appears. The participant can choose to "cash out" at any point, transferring the temporary earnings to a permanent bank before the balloon would burst.

The explosion point for each balloon is drawn from a predetermined distribution. In the original Lejuez et al. (2002) paradigm, balloons burst according to a probability function; in the simplified demo, the explosion threshold (max pumps) is a random integer. Participants complete multiple balloons (typically 30). The critical question is how many pumps a participant makes on average, especially on trials where the balloon does not burst.

Key variables: number of pumps per balloon (adjusted), number of balloons burst, number of cash-outs, total earnings. The primary dependent measure is the adjusted average number of pumps (mean pumps on non-burst trials), which indexes risk-taking propensity independent of the balloon explosion threshold.

## Data Analysis

Filter out burst trials and compute mean pumps on remaining (non-burst) trials as the primary measure. Examine total earnings and number of explosions as secondary measures. Correlate adjusted pumps with self-report measures of sensation-seeking, impulsivity, and real-world risk behaviors (e.g., substance use, gambling). Variants introduce balloons with different colors/explosion profiles to examine sensitivity to risk probability.

## Must Confirm

- **Balloon count**: How many balloons? (typically 30)
- **Burst distribution**: What determines the explosion point — fixed probability per pump, random integer threshold, or fixed thresholds in conditions.xlsx?
- **Key mapping**: Which key for "pump" and which for "collect"?
- **Reward structure**: Reward per pump and what happens on burst?
- **Visual assets**: Balloon colors, background images, and burst sound?

## Trial Window Timeline

```
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Balloon Display          │    │ Pump Feedback             │    │ Outcome                  │
│ Content: balloon image   │    │ Content: balloon grows   │    │ Content: burst (sound)   │
│ + score + pump count     │    │ + score increments       │    │ OR collect confirmation  │
│ Duration: until key      │    │ Duration: 500 ms         │    │ Duration: 1000 ms        │
│ Response: pump/collect   │    │ Response: none           │    │ Response: none           │
│ Data: pump_count, score  │    │ Data: none               │    │ Data: burst (bool)       │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

Nested loop: outer loop over balloons, inner loop over pumps within each balloon. Balloon size increases with each pump via `balloon.setSize()`.

## References

Lejuez, C. W., Read, J. P., Kahler, C. W., Richards, J. B., Ramsey, S. E., Stuart, G. L., Strong, D. R., & Brown, R. A. (2002). Evaluation of a behavioral measure of risk taking: The Balloon Analogue Risk Task (BART). *Journal of Experimental Psychology: Applied, 8*(2), 75–84. https://doi.org/10.1037/1076-898X.8.2.75
