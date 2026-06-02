# Delay Discounting Task (Temporal Discounting)

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/delay-discounting) · reference

## When to Use

User mentions: Delay discounting, temporal discounting, intertemporal choice, impulsivity, 延迟折扣, 时间贴现. Measures the tendency to devalue rewards as a function of the delay until their receipt — the preference for smaller-sooner rewards over larger-later ones.

## Core Logic

Participants make a series of binary choices between a smaller reward available immediately (e.g., "$20 today") and a larger reward available after a delay (e.g., "$50 in 30 days"). The immediate amount, the delayed amount, and the delay length are systematically varied across trials. The key dependent variable is the indifference point at each delay — the immediate amount at which the participant is equally likely to choose either option (i.e., the subjective value of the delayed reward).

Delay periods typically range from days to years (e.g., 1 day, 1 week, 1 month, 6 months, 1 year, 5 years). By plotting subjective value against delay, the discounting rate (k) is estimated using a hyperbolic discounting function: V = A / (1 + kD), where V is subjective value, A is the delayed amount, D is delay, and k is the discounting rate. Higher k values indicate steeper discounting (greater impulsivity).

The task can be administered as a titration procedure (adjusting the immediate amount based on previous responses to converge on the indifference point) or as a full factorial design (all combinations of amounts and delays). This implementation uses a fixed choice set: each trial displays two options as labeled buttons (ButtonStim) side by side — e.g., "£5 now" vs. "£7 in 3 days". The condition file (`conditions.xlsx`) specifies the text labels in `amount1` and `amount2` columns. Participants click the button corresponding to their preferred option. No accuracy feedback is given, as there are no correct or incorrect answers — this is a preference measure. Trials are presented once in random order (`nReps=1.0`, `method='random'`).

## Must Confirm

- **Reward amounts**: What range of amounts? (e.g., $10-$100, or hypothetical larger sums?)
- **Delay values**: Which delay durations? (e.g., 1 day, 1 week, 1 month, 6 months, 1 year, 5 years)
- **Choice format**: Fixed choice pairs from a condition file, or adaptive titration?
- **Reward type**: Money, food, drugs, or other commodity?
- **Response mode**: Mouse click on labeled buttons, or keyboard selection?
- **Hypothetical vs. real**: Hypothetical choices, or one randomly selected trial is paid out for real?
- **No feedback**: Correct — no correct/incorrect answers in this paradigm.

## Trial Window Timeline

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Single Trial                                                          │
│                                                                       │
│ Content: two options as labeled buttons                              │
│   Left button: amount1 label (e.g., "£5 now")                        │
│   Right button: amount2 label (e.g., "£7 in 3 days")                 │
│ Duration: until click                                                 │
│ Response: mouse click on chosen button                               │
│ Condition: {amount1, amount2} from conditions.xlsx                   │
│ Data: chosen_button, RT                                               │
│                                                                       │
│ Note: no fixation, no feedback, no ITI — immediate advance to        │
│ next trial on response. Pure preference measure.                      │
└──────────────────────────────────────────────────────────────────────┘
```

## Data Analysis

Fit the hyperbolic discounting model to estimate k for each participant (or compute area under the curve, AUC, as a model-free alternative). Log-transform k due to positive skew. Compare k between clinical groups (substance use disorders, ADHD, gambling disorder, obesity) and controls. Steeper discounting is consistently associated with addictive and impulsive behaviors. Also examine whether discounting rate varies by reward type (money, food, drugs) in relevant populations.

## References

Mazur, J. E. (1987). An adjusting procedure for studying delayed reinforcement. In M. L. Commons, J. E. Mazur, J. A. Nevin, & H. Rachlin (Eds.), *Quantitative analyses of behavior, Vol. 5. The effect of delay and of intervening events on reinforcement value* (pp. 55–73). Lawrence Erlbaum.

Kirby, K. N., Petry, N. M., & Bickel, W. K. (1999). Heroin addicts have higher discount rates for delayed rewards than non-drug-using controls. *Journal of Experimental Psychology: General, 128*(1), 78–87. https://doi.org/10.1037/0096-3445.128.1.78
