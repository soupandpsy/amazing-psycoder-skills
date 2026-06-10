# Navon — PsychoPy

> **Parent**: [psy-exp-coder](../../SKILL.md) · [Implementation Guide](../spec/README.md)
> **Config reference**: [navon](../../../psy-exp-designer/paradigms/navon.md)
> **Status**: **CONFIG-DRIVEN** — no Pavlovia demo code found. Code generated from config YAML using the patterns below.

## Experiment Logic

Participants see large (global) letters composed of small (local) letters. On each trial they identify either the global or local letter while ignoring the other level. The attended level can be fixed (blocked) or cued (trial-by-trial). Measures global precedence / local interference effects.

## Trial Window Sequence

```
Fixation (500ms) → Stimulus (until key, merged) → Feedback (practice only, 500ms) → ITI (500-800ms)
```

The stimulus is a large letter made of small letters (e.g., a large "H" made of small "S" letters). Response is a keypress identifying the letter at the attended level.

## Implementation Pattern

### Step 1: Build Hierarchical Letter Stimuli

Navon letters cannot use a single `TextStim` — the global and local letters must be different. Two approaches:

**Approach A — Nested TextStim (simplest, works for fixed sizes)**:
```python
# Global letter (large)
global_stim = visual.TextStim(win, text=global_letter, height=2.0, pos=(0, 0), color='white')
# Local letters arranged in a grid to form the global shape
# Pre-generate local letter positions as a bitmap mask of the global letter
# OR render local letters individually at grid positions within the global letter outline
```

**Approach B — Pre-rendered images (recommended for reliability)**:
Generate Navon stimulus images offline (Python/PIL script), save as PNG files, load with `ImageStim`. This is the recommended approach for production experiments. The image filenames encode the condition: `H_S.png` = global H made of local S.

If the user cannot pre-generate images, use Approach C — build a `visual.BufferImageStim` by drawing local letters onto a virtual buffer at positions that form the global letter shape. This is complex but avoids external dependencies.

**Approach C — BufferImageStim (runtime generation)**:
```python
from psychopy import visual
import numpy as np

def create_navon_stimulus(win, global_letter, local_letter, grid_size=(5, 5)):
    """Render a Navon figure: global letter shape filled with local letters."""
    # Define global letter template (5x7 dot matrix or similar)
    templates = {
        'H': [(0,3),(1,3),(2,3),(3,3),(4,3),(0,0),(1,0),(2,0),(3,0),(4,0),(2,1),(2,2)],  # H shape
        'S': [(0,0),(1,0),(2,0),(3,0),(4,0),(0,1),(0,2),(2,1),(2,2),(4,1),(4,2),(0,3),(1,3),(2,3),(3,3),(4,3),(1,4),(2,4),(3,4)]  # S shape
    }
    # Build buffer: for each (row, col) in the global template, draw local_letter
    # Use visual.BufferImageStim or draw to a temporary window
    ...
```

**What to ask the user**: "Navon 刺激是用图片文件还是代码实时生成？如果用图片，文件命名规则是什么？"

### Step 2: Condition Table

```csv
trial, global_letter, local_letter, attended_level, correct_response
1, H, S, global, f
2, H, S, local, j
3, S, H, global, j
4, S, H, local, f
```

### Step 3: Response Logic (Merged Pattern)

```python
kb = keyboard.Keyboard()
# Stimulus presentation
stim.draw()  # or image.draw() for pre-rendered
win.callOnFlip(kb.clock.reset)
win.callOnFlip(kb.clearEvents)
win.flip()

response = None
rt = None
timer = core.CountdownTimer(DEADLINE / 1000.0)
while timer.getTime() > 0:
    keys = kb.getKeys(keyList=RESPONSE_KEYS + ['escape'], waitRelease=False, clear=False)
    if keys:
        if keys[0].name == 'escape':
            save_and_quit()
        response = keys[0].name
        rt = keys[0].rt * 1000
        break

# Accuracy: response matches correct_response for the attended_level
acc = 1 if response == condition['correct_response'] else 0
```

### Key Edge Cases

- **Global precedence effect**: Global letters are processed faster. Counterbalance attended level across blocks or randomize trial-by-trial.
- **Consistent/inconsistent**: A trial is "consistent" when global and local letters are the same (H made of H), "inconsistent" when different (H made of S). Ensure both types appear.
- **Letter set size**: Typically 2 target letters (H, S). Response mapping: left key = H, right key = S (or f/j). Confirm mapping with user.

## Data Output Columns

Base columns + `global_letter`, `local_letter`, `attended_level`, `consistency` (consistent/inconsistent)
