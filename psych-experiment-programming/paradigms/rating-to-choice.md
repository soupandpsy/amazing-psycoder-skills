# Rating-to-Choice Task

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/rating_to_choice_task) · PsychoJS

## When to Use

User mentions: Rating to choice, two-phase preference, painting rating, adaptive choice, 评分转选择任务. A two-phase decision-making paradigm where participants first rate individual stimuli and then make pairwise choices between stimuli selected based on their own ratings, demonstrating dynamic stimulus selection driven by participant responses.

## Core Logic

The task comprises two sequential phases linked by the participant's own rating data:

**Phase 1 — Rating Phase**: Participants view a set of stimuli (e.g., paintings — European art and nature scenes from Unsplash and museum collections) one at a time and rate each on a 3-point scale. They press keys 1, 2, or 3 to assign a rating. Each rating-keypress is stored alongside the image filename. The rating data from this phase serves as input to Phase 2.

**Phase 2 — Choice Phase**: A comparison file (`conditions_choice_phase.xlsx`) specifies which rating-level comparisons to make: "1 vs 2", "2 vs 3", and "1 vs 3". The code dynamically selects one painting with each specified rating from the participant's Phase 1 data. Two paintings are displayed side by side: one that the participant rated at one level and one rated at another level. The participant presses '1' to choose the left image or '2' to choose the right image.

**Adaptive stimulus selection** is the key innovation: Phase 2 trials are not pre-determined but are constructed in real time from Phase 1 responses. If a participant gave no painting a particular rating (e.g., no painting was rated 3), a default placeholder image is used for that comparison instead, ensuring all comparison types can always be presented.

**Data collected**: For each Phase 2 trial — the images displayed (left and right), the participant's choice, the comparison type (1v2, 2v3, 1v3), and the ratings that triggered the pairing. This reveals whether participants show systematic preferences between stimuli they rated identically, or inconsistencies between stated ratings and revealed choices.

## Must Confirm

- **Stimuli**: Paintings (what style/domain?), product images, faces, or other? How many items in the stimulus set?
- **Rating scale**: 1-3 (3-point), 1-5 (5-point), 1-7, or continuous slider?
- **Comparison types**: Which rating differences to compare? (1v2, 2v3, 1v3, or all pairwise?)
- **Placeholder handling**: What to show when no stimulus was given a required rating? Default image or skip that comparison?
- **Phase sequencing**: Always rating-then-choice, or counterbalanced order?
- **Trial counts**: How many stimuli to rate? How many comparison trials?

## Trial Window Timeline

**Phase 1 — Rating:**
```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Stimulus                 │    │ Rating Prompt            │    │ ITI                      │
│ Content: painting image  │    │ Content: rating scale    │    │ Content: blank           │
│ Duration: until key      │    │   (1-3) with labels      │    │ Duration: 500 ms         │
│ Response: none           │    │ Duration: until key      │    │ Response: none           │
│ Condition: {image_file}  │    │ Response: 1, 2, or 3     │    │ Condition: none          │
│ Data: image_filename     │    │ Data: rating_value       │    │ Data: none               │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

**Phase 2 — Choice:**
```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Stimulus Pair            │    │ Response                 │    │ ITI                      │
│ Content: 2 paintings     │    │ Content: selection prompt │    │ Content: blank           │
│   (left: rated X,        │    │ Duration: until key      │    │ Duration: 500 ms         │
│    right: rated Y)       │    │ Response: 1=left, 2=right│    │ Response: none           │
│ Duration: until key      │    │ Condition: {comparison}  │    │ Condition: none          │
│ Condition: {comparison}  │    │ Data: choice, rt          │    │ Data: none               │
│ Data: left_img, right_img│    └──────────────────────────┘    └──────────────────────────┘
└──────────────────────────┘
```

## Data Analysis

Analyze rating distributions (histogram of Phase 1 ratings). In Phase 2, examine reaction time and choice proportions for each comparison type. Test for preference consistency: does choice in Phase 2 align with rating differences from Phase 1? Analyze cases where rated-equal items produce systematic choices (revealed preference diverging from stated preference). Compare different comparison types (1v2, 2v3, 1v3) for choice difficulty (RT, decision confidence).

## References

No specific publication — this is a methodology demo illustrating dynamic stimulus selection based on participant responses. Adaptable to preference testing, decision-making, and value-based choice studies.
