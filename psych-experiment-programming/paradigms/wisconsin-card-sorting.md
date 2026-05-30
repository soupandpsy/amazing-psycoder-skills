# Wisconsin Card Sorting Test (WCST)

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/wcst) · reference

## When to Use

User mentions: WCST, Wisconsin Card Sorting, set-shifting, cognitive flexibility, perseveration, 威斯康星卡片分类, 认知灵活性. The gold-standard neuropsychological test of executive function measuring the ability to form, maintain, and shift cognitive sets in response to changing reinforcement contingencies.

## Core Logic

Participants sort cards one at a time into one of four target piles. Each card varies on three dimensions: shape (e.g., triangle, star, cross, circle), color (e.g., red, green, yellow, blue), and number (1 to 4 symbols per card). The four target cards each represent a unique value on one dimension (e.g., one red triangle, two green stars, three yellow crosses, four blue circles). The participant is not told the sorting rule but receives feedback (correct/incorrect) after each sort.

The sorting rule (match by color, shape, or number) is initially set and maintained. After a criterion number of consecutive correct sorts (typically 10), the rule changes without warning. The participant must discover the new rule through trial and error using feedback alone. The core difficulty is suppressing the previously correct rule (set-shifting). Perseverative errors — continuing to sort by the old rule after it has changed — are the hallmark measure of cognitive inflexibility.

This implementation uses a nested two-loop design: an outer block loop (`chooseRule.xlsx`, 2 reps) sets the sorting rule, and an inner trial loop (`cards.xlsx`) presents cards in blocks of 7 forced trials (useRows selection). Each trial displays 4 reference cards at the top and 1 trial card below, all rendered as colored shapes at specified positions. A 1 s fixation precedes the card display, and the participant clicks on one of the 4 reference cards to indicate their sort. After each sort, feedback ("Correct!" or "Incorrect") is shown for 1 s. At the end of each block, the score is displayed for 3 s before the next block begins.

Key measures: number of categories completed (max 6), total errors, perseverative errors (continuing the old rule after a shift), failure to maintain set (losing the rule mid-category, i.e., 5+ correct followed by an error), and trials to complete the first category (initial conceptualization). The test continues until all 6 categories are completed or all 128 cards are used.

## Must Confirm

- **Stimulus dimensions**: Shape, color, and number — all three or a subset?
- **Number of dimensions and values**: 3 dimensions with 4 values each (shapes: triangle/star/cross/circle, colors: red/green/yellow/blue, numbers: 1/2/3/4)?
- **Trial cards**: How are trial cards generated — from a fixed deck (128 cards), or dynamically?
- **Trials per block**: Fixed number (e.g., 7 forced trials from chooseRule.xlsx) per rule, or continue until criterion (e.g., 10 consecutive correct)?
- **Response mode**: Mouse click on reference cards, or keyboard selection?
- **Feedback**: 1 s feedback after each trial, or no feedback?
- **Rule change**: How many rule shifts, and in what order?

## Trial Window Timeline

```text
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│ Window 1             │→ │ Window 2             │→ │ Window 3             │→ │ Window 4             │
│ Fixation             │  │ Card Sort            │  │ Feedback              │  │ Block End (every     │
│ Content: + at center │  │ Content: 4 reference │  │ Content: "Correct!"   │  │ 7 trials)            │
│ Duration: 1.0 s      │  │ cards (top) + 1      │  │ or "Incorrect"        │  │ Content: score       │
│ Response: none       │  │ trial card (bottom)  │  │ Duration: 1.0 s       │  │ Duration: 3.0 s      │
│ Data: none           │  │ Duration: until click│  │ Response: none        │  │ Response: none       │
│                      │  │ Response: click on   │  │ Data: none            │  │ Data: none           │
│                      │  │ a reference card     │  │                       │  │                      │
│                      │  │ Data: clicked_name,  │  │                       │  │                      │
│                      │  │ rt, acc              │  │                       │  │                      │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘
```

## Data Analysis

Primary outcome: number of perseverative errors (the most sensitive index of frontal lobe dysfunction). Also analyze categories completed, total errors, failure to maintain set, and learning-to-learn (improvement across categories). The WCST is highly sensitive to prefrontal cortex damage, particularly dorsolateral prefrontal cortex. Perseverative errors are elevated in schizophrenia, Parkinson's disease, ADHD, and traumatic brain injury.

## References

Grant, D. A., & Berg, E. A. (1948). A behavioral analysis of degree of reinforcement and ease of shifting to new responses in a Weigl-type card-sorting problem. *Journal of Experimental Psychology, 38*(4), 404–411. https://doi.org/10.1037/h0059831

Heaton, R. K., Chelune, G. J., Talley, J. L., Kay, G. G., & Curtiss, G. (1993). *Wisconsin Card Sorting Test manual: Revised and expanded*. Psychological Assessment Resources.
