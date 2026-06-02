# Choice Reaction Time Task

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/choice_reaction_time) · PsychoJS

## When to Use

User mentions: Choice reaction time, CRT, choice RT, Hick's law, 选择反应时. Measures the speed of decision-making when participants must discriminate among multiple stimuli and select the corresponding response — unlike simple RT (one stimulus, one response), choice RT requires both stimulus discrimination and response selection.

## Core Logic

Participants respond to visual targets that appear at one of several possible screen positions. The target can be one of multiple stimulus types (e.g., cross, square, plus), each mapped to a different response. The task requires both stimulus identification (which shape?) and response selection (which key/position?), making it a measure of decision complexity beyond simple detection.

**This implementation** uses 3 target shapes (cross, square, plus) that appear at 4 possible positions arranged around the screen. Each shape is associated with a specific keyboard response: C, V, or B keys. Additionally, mouse clicks on the target position are accepted as a valid response. This dual-modality design allows measuring both stimulus-identity-driven (keyboard) and location-driven (mouse) response selection.

**Position cueing**: Before the target appears, outline placeholder tiles are shown at all 4 possible positions for 500 ms, cuing the participant to the possible target locations. The target then appears at one position for a brief 200 ms display window, requiring rapid encoding.

**Variable onset timing**: The target onset time (`onsetTime`) varies per trial as specified in the condition file, introducing temporal uncertainty and preventing anticipatory responses. Reaction time is calculated relative to this onset (`RT = keyResp.rt - onsetTime`).

**Two-block design**: Practice block (1 repetition of conditions) with detailed feedback showing RT, response type, and accuracy after each trial, followed by the experimental block (2 repetitions) with the same feedback. The practice and main blocks share the same trial structure and condition logic.

**Multi-alternative choice design**: 3 possible stimulus shapes, each mapped to a specific key. This is the key difference from simple RT (one stimulus, one key) -- the participant must recognize which shape appeared and select the correct response from multiple options. Hick's Law predicts that RT increases logarithmically with the number of response alternatives.

## Must Confirm

- **Stimulus shapes**: How many shapes, and which ones? (cross, square, plus -- or custom)
- **Stimulus positions**: How many locations on screen, and where?
- **Response modality**: Keyboard only, mouse only, or both? Which keys map to which shapes?
- **Target duration**: Brief flash (200 ms) or response-terminated display?
- **Onset timing**: Fixed SOA, variable from condition file, or immediate?
- **Position cueing**: Show position tiles before target (500 ms), or no pre-cue?
- **Trial count**: How many practice repetitions? How many experimental repetitions?
- **Feedback content**: RT, accuracy, response type -- or accuracy only?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Position Cues            │    │ Target Display           │    │ Feedback                 │
│ Content: 4 outline tiles │    │ Content: shape (cross/   │    │ Content: RT, response    │
│ at target positions      │    │ square/plus) at one      │    │ type, accuracy           │
│ Duration: 500 ms         │    │ position                  │    │ Duration: ~1 s            │
│ Response: none           │    │ Duration: 200 ms         │    │ Response: none           │
│ Data: none               │    │ Response: key (C/V/B) or │    │ Data: none               │
│                          │    │ mouse click on position  │    │                           │
│                          │    │ Data: rt (from onsetTime)│    │                           │
│                          │    │ key, acc, response_type  │    │                           │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
```

## Data Analysis

Primary measure is mean RT as a function of number of response alternatives (Hick's Law: RT = a + b * log2(N), where N is the number of choices). Compare RT across different stimulus shapes. Analyze accuracy, which should be high (>90%) for healthy adults. Choice RT is slower than simple RT by approximately 100-150 ms (the time cost of stimulus discrimination and response selection). For the dual-modality version, compare keyboard vs. mouse response RTs to assess modality effects on response selection. Check temporal uncertainty effects by analyzing RT as a function of onset variability. Individual differences in CRT correlate with general cognitive ability and processing speed.

## References

Hick, W. E. (1952). On the rate of gain of information. *Quarterly Journal of Experimental Psychology, 4*(1), 11-26. https://doi.org/10.1080/17470215208416600
