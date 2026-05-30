# Children Flanker Task

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/children_flanker_task) · PsychoJS

## When to Use

User mentions: Children flanker, child flanker, fish flanker, kids attention task, 儿童侧翼任务, 儿童注意任务. A child-friendly adaptation of the Eriksen flanker paradigm using fish images instead of abstract arrows, designed for developmental populations and pediatric research.

## Core Logic

This is a flanker task adapted for children. Instead of arrows or letters, participants see a row of five fish. The central fish is the target; the four flanking fish (two on each side) point either in the same direction (congruent) or opposite direction (incongruent). The child presses the left or right arrow key to indicate the direction of the middle fish only, ignoring the flanking fish.

**Child-friendly design features**:
- Fish images (`leftFish.png`, `rightFish.png`) replace abstract arrow stimuli, making the task intuitive for young children
- A colorful, engaging background replaces neutral grey/black
- A progress counter (e.g., "Fish 12 / 48") is displayed throughout to maintain motivation
- Transparent spacer images (`transparent.png`) maintain consistent horizontal spacing even when fish are not present

**Trial structure**: fixation → five-fish display (center target + four flankers) → keypress response (left/right arrow) → ITI. The condition file (`conditions.csv`) defines each trial's target direction, flanker direction, and correct answer (`corrAns`).

**Two-phase design**:
1. **Practice block**: Trials with trial-level feedback (correct/incorrect text shown after each response). An instruction screen precedes practice.
2. **Main experimental block**: Trials without feedback. A gap/routine screen separates practice from the main phase.

**The Flanker effect**: Incongruent trials (target left, flankers right, or vice versa) yield slower and less accurate responses than congruent trials (all fish pointing the same direction). The flanker interference effect (incongruent RT – congruent RT) indexes selective attention and inhibitory control in children.

## Must Confirm

- **Age range**: What ages? (influences instruction wording, trial count, and response deadline)
- **Stimuli**: Fish images, animal images, or other child-friendly stimuli?
- **Trial count**: How many practice trials? How many experimental trials? (fewer for younger children)
- **Congruency ratio**: 50:50 congruent:incongruent, or include neutral condition?
- **Response deadline**: Child-friendly deadline (e.g., 3000 ms) or no deadline?
- **Feedback**: Practice-only feedback, or feedback throughout? Verbal encouragement between blocks?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Fish Stimuli             │    │ Feedback (practice only) │    │ ITI                      │
│ Content: + at center     │    │ Content: 5 fish in row   │    │ Content: correct/incorrect│   │ Content: blank           │
│ Duration: 500 ms         │    │ ←←←←← or ←←→←←           │    │ + progress counter       │    │ Duration: 500-1000 ms    │
│ Response: none           │    │ Duration: until key      │    │ Duration: 500 ms         │    │ Response: none           │
│ Condition: none          │    │ (deadline ~3000 ms)      │    │ Response: none           │    │ Condition: none          │
│ Data: none               │    │ Response: left/right key │    │ Condition: none          │    │ Data: none               │
└──────────────────────────┘    │ Condition: {congruency}  │    │ Data: none               │    └──────────────────────────┘
                                │ Data: rt, key, acc       │    └──────────────────────────┘
                                │   trial_counter          │
                                └──────────────────────────┘
```

## Data Analysis

Compute flanker interference scores for RT (incongruent RT – congruent RT) and accuracy. Children typically show larger interference effects than adults, reflecting developing inhibitory control. Analyze age-related changes in the flanker effect. Error trials and post-error trials are important for understanding response monitoring development. Compare to adult flanker norms to assess developmental trajectories.

## References

Eriksen, B. A., & Eriksen, C. W. (1974). Effects of noise letters upon the identification of a target letter in a nonsearch task. *Perception & Psychophysics, 16*(1), 143–149. https://doi.org/10.3758/BF03203267

Rueda, M. R., Fan, J., McCandliss, B. D., Halparin, J. D., Gruber, D. B., Lercari, L. P., & Posner, M. I. (2004). Development of attentional networks in childhood. *Neuropsychologia, 42*(8), 1029–1040. https://doi.org/10.1016/j.neuropsychologia.2003.12.012
