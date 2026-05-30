# Mental Rotation Task

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/mental_rotation) · PsychoJS

## When to Use

User mentions: Mental rotation, spatial cognition, visuospatial processing, 心理旋转, 空间认知. Measures the ability to mentally rotate two-dimensional or three-dimensional objects, a classic paradigm in spatial cognition research.

## Core Logic

Participants view two stimuli presented side by side and must judge whether they are the same (identical) or different (mirror images). One stimulus is rotated relative to the other by varying angular disparities (e.g., 0, 45, 90, 135, 180 degrees). The key finding is that reaction time increases approximately linearly with the angle of rotation, suggesting analog mental transformation.

**This implementation** uses letter-like shapes (e.g., 'F') presented at various orientations — a simplified version of Shepard & Metzler's (1971) classic 3D block-figure paradigm. The left stimulus shows the original letter; the right stimulus shows either the same letter (rotated) or its mirror-reversed version (also rotated). Participants press 's' for same (identical) and 'd' for different (mirror image).

**Condition file** (`MentalRot.csv`): Specifies rotation angle, which image file to display for the left and right positions (`F.png` and `FR.png` for mirror image), and the correct answer. The `TrialHandler` iterates over this file with random or sequential order.

**Trial structure**: Two instruction screens → fixation → stimulus pair (left + right images, until response) → optional feedback → ITI.

**Rotation angle manipulation**: The condition file systematically varies angular disparity. The classic finding is a linear RT increase from 0 to 180 degrees, with a symmetrical decrease from 180 to 360 degrees, producing a peak at 180 degrees.

## Must Confirm

- **Stimulus type**: Letter-like shapes (F, R, G), 3D block figures (Shepard-Metzler style), or abstract polygons?
- **Response mapping**: 's'/'d' for same/different, or arrow keys for left/right judgment, or different mapping?
- **Rotation angles**: Which angular disparities? (typically 0, 45, 90, 135, 180 degrees, in both clockwise and counterclockwise directions)
- **Mirror stimuli**: Is the "different" condition always a mirror image, or can it be a different letter entirely?
- **Trial count**: How many trials per angle? How many repetitions?
- **Practice**: Practice block with feedback before formal trials?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │ →  │ Window 4                 │
│ Fixation                 │    │ Stimulus Pair            │    │ Feedback (optional)      │    │ ITI                      │
│ Content: + at center     │    │ Content: F (left)        │    │ Content: correct/incorrect│   │ Content: blank           │
│ Duration: 500 ms         │    │   rotated F/R (right)    │    │ Duration: 500 ms         │    │ Duration: 500-1000 ms    │
│ Response: none           │    │ Duration: until key      │    │ Response: none           │    │ Response: none           │
│ Condition: none          │    │ Response: s=same, d=diff │    │ Condition: none          │    │ Condition: none          │
│ Data: none               │    │ Condition: {angle, pair} │    │ Data: none               │    │ Data: none               │
└──────────────────────────┘    │ Data: rt, key, acc       │    └──────────────────────────┘    └──────────────────────────┘
                                └──────────────────────────┘
```

## Data Analysis

Plot mean RT as a function of rotation angle (expect a peak-shaped function, linear increase peaking at 180 degrees, then decreasing back toward 0/360). Compute the mental rotation slope (ms/degree) via linear regression on same-pair trials. Compare slopes and intercepts between groups (e.g., sex differences — males typically show faster rotation speed). Also analyze accuracy, which tends to decrease at larger angular disparities.

## References

Shepard, R. N., & Metzler, J. (1971). Mental rotation of three-dimensional objects. *Science, 171*(3972), 701–703. https://doi.org/10.1126/science.171.3972.701

Gray, J. R., & Pasmanter, N. R. (2013). Mental rotation demo. Michigan State University.
