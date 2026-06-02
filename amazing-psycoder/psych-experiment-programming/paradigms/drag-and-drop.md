# Drag and Drop Puzzle Task

> **Parent**: [psych-experiment-programming](../SKILL.md)
> **Config reference**: [config-schema](../references/config-schema.md)
> **Source**: [Pavlovia demos](https://gitlab.pavlovia.org/demos/drag_and_drop) · PsychoJS

## When to Use

User mentions: Drag and drop, puzzle task, pattern matching, spatial arrangement, 拖放任务, 拼图任务. A pattern-matching puzzle task using drag-and-drop interaction, demonstrating mouse-based stimulus manipulation for spatial reasoning, problem-solving, or visuospatial ability assessment.

## Core Logic

Participants view a target pattern (e.g., a black-and-white design) displayed above an empty grid. Draggable puzzle pieces (black and white squares) are positioned around the grid. Participants must click and drag each piece from its starting position into the correct grid cell to recreate the target pattern.

**Trial structure**: target design image displayed above grid → participant drags black/white pieces into grid cells → when satisfied, clicks "Continue" button → feedback (correct/incorrect + completion time) → next trial. The condition file (`conditions.xlsx`) defines the target design image and the correct arrangement (which cells should be black vs. white).

**Drag-and-drop mechanics**: PsychoJS `visual.ImageStim` components are created with `setDraggable(true)`. Piece positions are tracked via each stimulus's `.pos` property. The grid is defined using pixel coordinates (`units: 'pix'` for precise positioning). Each trial has 9 grid cells (3x3 arrangement), each requiring either a black or white piece.

**Accuracy verification**: When the participant clicks "Continue", the code compares the final dragged positions of black and white pieces against the target pattern cells defined in the condition file columns (`a1` through `a9`, or equivalent grid labels). The trial is marked correct only if all pieces are in their correct positions.

**Completion time**: A trial timer runs from trial onset until the "Continue" button is clicked. Time taken and accuracy are displayed as feedback.

## Must Confirm

- **Grid layout**: 3x3 grid (9 cells), or different size? Rectangular or irregular?
- **Puzzle complexity**: Black/white binary pieces, color pieces, or more complex pattern pieces?
- **Target designs**: Pre-made design images or programmatically generated patterns?
- **Trial count**: How many puzzles to solve?
- **Interaction mode**: Mouse drag-and-drop, touchscreen, or both?
- **Feedback**: Full accuracy feedback (all-or-nothing) or partial credit (number of pieces correct)?

## Trial Window Timeline

```text
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ Window 1                 │ →  │ Window 2                 │ →  │ Window 3                 │
│ Puzzle Assembly          │    │ Feedback                 │    │ ITI                      │
│ Content: target design   │    │ Content: correct/incorrect│   │ Content: blank           │
│   above grid + draggable │    │   + completion time      │    │ Duration: 1000 ms        │
│   black/white pieces     │    │ Duration: 2000 ms        │    │ Response: none           │
│ Duration: self-paced     │    │ Response: none           │    │ Condition: none          │
│   (click Continue to end)│    │ Condition: none          │    │ Data: none               │
│ Response: mouse drag     │    │ Data: none               │    └──────────────────────────┘
│ Condition: {design_id}   │    └──────────────────────────┘
│ Data: piece_positions,   │
│   completion_time        │
└──────────────────────────┘
```

## Data Analysis

Primary measures: completion time (time to solve each puzzle), accuracy (proportion of correctly solved puzzles), and error patterns (which grid cells had incorrect pieces). Analyze learning effects across trials (faster completion on later puzzles). Individual differences in visuospatial ability can be inferred from accuracy and speed. Mouse trajectories (piece drag paths) provide process-tracing data on solution strategies.

## References

This paradigm demonstrates drag-and-drop interaction capabilities in PsychoJS/PsychoPy. Adaptable to visuospatial ability testing, puzzle-solving research, and any paradigm requiring spatial manipulation of on-screen elements.
