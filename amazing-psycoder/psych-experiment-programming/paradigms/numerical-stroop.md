# Numerical Stroop Task

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/numerical_stroop) · reference

## When to Use

User mentions: Numerical Stroop, number Stroop, physical vs. semantic comparison, Henik task, 数字斯特鲁普. A variant of the Stroop task using numerical magnitude comparison, measuring interference between the physical size and semantic value of digits.

## Core Logic

Participants compare two numbers and indicate which is "greater" under two different task conditions. In semantic trials, participants must choose the numerically larger number while ignoring the physical size of the digits (e.g., the digit "3" printed in large font vs. "5" in small font — the correct answer is "5" based on value, ignoring size). In physical trials, participants must choose the physically larger number while ignoring its numerical value (e.g., large "3" vs. small "5" — the correct answer is "3" based on size, ignoring value).

Congruent trials are those where physical size and numerical value align (e.g., large "5" vs. small "3" — "5" is both physically and numerically larger). Incongruent trials create conflict between the two dimensions (e.g., large "3" vs. small "5"). The key prediction is that incongruent trials produce longer RTs than congruent trials, with larger interference effects in the semantic task (reflecting the automatic, difficult-to-suppress processing of numerical magnitude).

This is a close replication of Henik & Tzelgov (1982). The task is organized into blocks, each driven by a row in `blockDefinitions.xlsx` specifying the instruction text, practice condition file, and main condition file. This allows easy switching between semantic and physical comparison blocks within a single experiment.

Each trial follows a precisely timed sequence: fixation cross ("+") at center for 100 ms, then at 200 ms two number stimuli appear simultaneously at positions (-0.075, 0) and (0.075, 0) in height units. The key manipulation is that each trial condition provides four parameters: `number1`/`number2` (the digit strings) and `size1`/`size2` (the physical font heights). In congruent trials the physically larger digit is also numerically larger; in incongruent trials the physically larger digit is numerically smaller, creating response conflict. Participants respond with 'a' (left) or 'k' (right). Practice trials show 1s feedback ("Correct!" or "Oops! That was wrong"); main trials proceed without feedback.

## Must Confirm

- **Task conditions**: Both semantic ("which is numerically larger?") and physical ("which is physically larger?") conditions, or just one?
- **Blocking**: Conditions blocked (one instruction per block) or interleaved?
- **Stimulus pairs**: Which digit pairs to use? (e.g., 1-9 with varying physical sizes)
- **Response keys**: 'a'/'k' (left/right), arrow keys, or other mapping?
- **Size manipulation**: How many physical size levels per digit? (e.g., two sizes creating congruent/incongruent/neutral)
- **Practice**: Include practice trials with feedback before each block?
- **Trial count**: How many trials per congruency condition per block?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Fixation                 │    │ Number Stimuli           │    │ Feedback (practice only)  │
│ Content: + at center     │    │ Content: two digits      │    │ Content: "Correct!" or    │
│ Duration: 100 ms         │    │ at different font sizes  │    │ "Oops! That was wrong"    │
│ Response: none           │    │ positions: ±0.075        │    │ Duration: 1 s              │
│ Data: none               │    │ starts at t=200 ms       │    │ Response: none            │
│                          │    │ Duration: until response │    │ Data: none                │
│                          │    │ Response: 'a' or 'k' key│    │                           │
│                          │    │ Data: rt, key, acc       │    │                           │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

## Data Analysis

Compare mean RT for congruent vs. incongruent trials within each task condition (semantic, physical). Expect larger interference in semantic comparison. Use a 2 (task: semantic vs. physical) x 2 (congruency: congruent vs. incongruent) repeated-measures ANOVA. Analyze the interaction to determine the locus of the numerical Stroop effect.

## References

Henik, A., & Tzelgov, J. (1982). Is three greater than five: The relation between physical and semantic size in comparison tasks. *Memory & Cognition, 10*(4), 389–395. https://doi.org/10.3758/BF03202431

Stroop, J. R. (1935). Studies of interference in serial verbal reactions. *Journal of Experimental Psychology, 18*(6), 643–662. https://doi.org/10.1037/h0054651
