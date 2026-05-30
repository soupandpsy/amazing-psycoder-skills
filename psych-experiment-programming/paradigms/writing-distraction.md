# Writing Distraction Task

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: Custom paradigm · PsychoPy

## When to Use

User mentions: Writing distraction, dual-task writing, distractor interference, writing under distraction, 书写干扰. A dual-task paradigm that measures the effect of visual distractors on ongoing text production, combining continuous typing performance with intermittent distractor exposure.

## Core Logic

Participants type a word or phrase while intermittently being shown distracting images. The paradigm measures how distraction disrupts the continuity, speed, and accuracy of ongoing text production. This task bridges motor production, working memory maintenance, and distractor suppression, making it relevant for studying real-world interference effects (e.g., writing while notifications appear).

**Trial structure** -- each trial has four sequential phases:

1. **Word display phase** (2 s minimum + typing): A target word is shown on screen. The participant must type at least a specified number of letters (`n_distract`) from the word. Once they type enough characters, the phase advances. If they haven't typed enough letters within 2 seconds, the phase continues until they do.

2. **Distractor phase** (1 s): A distractor image is displayed for exactly 1 second. The participant's typing is interrupted by this visual distractor. The text they had typed so far is preserved.

3. **Continue writing phase** (5 s maximum): The original text typed so far is restored, and the participant continues typing from where they left off. They have up to 5 seconds to complete the word. The phase ends when they finish typing or when the 5-second timeout expires.

4. **Question phase** (until Y/N response): A yes/no question about the trial is displayed (e.g., "Did you notice the distractor?"). The participant responds with Y or N key.

**Cross-phase state**: The typed text is carried across phases via experiment-level variables. During the distractor phase, the text input is hidden; it is then restored for the continue-writing phase. The final text string (from word display + continue writing) is the primary performance measure.

**Condition file** (`conditions.xlsx`): Each row specifies `this_word` (the target word), `n_distract` (number of letters to type before the distractor appears), the distractor image filename, and the post-trial question. No per-trial feedback is given.

## Must Confirm

- **Word stimuli**: What words to use? Word length, frequency, language?
- **Distractor images**: What type of distractors? (emotional, neutral, task-relevant, or varied IAPS images)
- **n_distract**: How many letters must be typed before the distractor appears? Fixed or variable?
- **Phase timing**: Duration of distractor display (1 s), continue-writing timeout (5 s), and minimum word display time (2 s)?
- **Question content**: What yes/no question follows each trial?
- **Response collection**: Keyboard for typing + keyboard for Y/N, or mouse for Y/N?
- **Trial count**: How many trials? From a fixed CSV or procedurally generated?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Phase 1                  │ →  │ Phase 2                  │ →  │ Phase 3                  │ →  │ Phase 4                  │
│ Show Word + Type         │    │ Show Distractor          │    │ Continue Writing         │    │ Question Response        │
│ Content: target word +   │    │ Content: distractor      │    │ Content: existing text + │    │ Content: question text   │
│ textbox with typed chars │    │ image                    │    │ editable textbox         │    │ Duration: until Y/N key  │
│ Duration: min 2 s, then  │    │ Duration: 1 s            │    │ Duration: max 5 s        │    │ Response: 'y' or 'n' key │
│ until n_distract chars   │    │ Response: none (typing   │    │ (advances on completion) │    │ Data: key_resp.keys      │
│ typed                    │    │ suppressed)               │    │ Response: keyboard typing│    │                           │
│ Response: keyboard       │    │ Data: none               │    │ Data: full typed text    │    │                           │
│ Data: initial typed text │    │                           │    │                           │    │                           │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

## Data Analysis

Primary measures: typing speed (characters per second) in the continue-writing phase vs. word-display phase, error rate (deviations from target word), and completion rate (whether the word was fully typed). Compare performance on trials with distractors vs. baseline (if included). Analyze whether certain distractor types (emotional vs. neutral) differentially impair writing continuity. Y/N question responses provide a secondary measure of distractor awareness. Individual differences in working memory capacity or attentional control may moderate distraction effects.

## References

No canonical reference yet -- this is a custom paradigm. Adapt analyses from dual-task interference literature (e.g., Pashler, 1994) and writing process research.
