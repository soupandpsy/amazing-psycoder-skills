# Eriksen Flanker — PsychoPy

> **Parent**: [psy-exp-coder](../../SKILL.md) · [Implementation Guide](../spec/README.md)
> **Config reference**: [eriksen-flanker](../../../psy-exp-designer/paradigms/eriksen-flanker.md)
> **Status**: **CONFIG-DRIVEN** — no dedicated Pavlovia demo code found. See [Stroop](stroop.md) for a child-friendly fish variant. Code generated from config YAML using the patterns below.

## Experiment Logic

Five stimuli appear in a horizontal row: a central target arrow/letter flanked by two distractors on each side. The participant responds to the central target direction (e.g., left-pointing arrow → press left key) while ignoring the flankers. Congruent trials: flankers point the same direction as target. Incongruent trials: flankers point opposite direction. The interference cost (incongruent RT − congruent RT) measures selective attention.

## Trial Window Sequence

```
Fixation (500ms) → Flanker Array (until key, merged) → Feedback (practice) → ITI (500-800ms)
```

Standard: 5 items horizontal. Center = target. Left 2 + Right 2 = flankers.

## Implementation Pattern

### Step 1: Flanker Array Stimuli

Create 5 `TextStim` or `ImageStim` objects arranged horizontally:

```python
FLANKER_POSITIONS = [
    (-2.0, 0),  # Far left
    (-1.0, 0),  # Near left
    (0.0, 0),   # Center (target)
    (1.0, 0),   # Near right
    (2.0, 0),   # Far right
]

def create_flanker_array(win, target_direction, flanker_direction, stimulus_type='arrow'):
    """Create 5 stimuli for the flanker display."""
    arrows = {'left': '←', 'right': '→'}
    letters = {'left': 'H', 'right': 'S'}  # Example letter mapping
    
    if stimulus_type == 'arrow':
        target_char = arrows[target_direction]
        flanker_char = arrows[flanker_direction]
    else:
        target_char = letters[target_direction]
        flanker_char = letters[flanker_direction]
    
    stimuli = []
    for i, (x, y) in enumerate(FLANKER_POSITIONS):
        if i == 2:  # Center = target
            stim = visual.TextStim(win, text=target_char, pos=(x, y), height=1.0,
                                   color='white', bold=True)
        else:  # Flankers
            stim = visual.TextStim(win, text=flanker_char, pos=(x, y), height=1.0,
                                   color='white', bold=False)
        stimuli.append(stim)
    return stimuli
```

### Step 2: Congruency Condition

```python
for trial in trials:
    if trial['congruency'] == 'congruent':
        target_dir = flanker_dir = trial['target_direction']
    else:  # incongruent
        target_dir = trial['target_direction']
        flanker_dir = 'left' if target_dir == 'right' else 'right'
    
    stimuli = create_flanker_array(win, target_dir, flanker_dir)
```

### Step 3: Response Collection (Merged Pattern)

```python
kb = keyboard.Keyboard()
RESPONSE_KEYS = ['left', 'right']  # arrow keys, or 'f'/'j'

# Draw all stimuli
for stim in stimuli:
    stim.draw()
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

# Accuracy
correct_key = 'left' if trial['target_direction'] == 'left' else 'right'
acc = 1 if response == correct_key else 0
```

### Step 4: Condition Table

```csv
trial, target_direction, congruency, correct_response
1, left, congruent, left
2, left, incongruent, left
3, right, congruent, right
4, right, incongruent, right
```

### Key Edge Cases

- **Flanker spacing**: Closer spacing → stronger interference. Standard: 1 degree visual angle between items. Adjust based on viewing distance.
- **Target-flanker onset synchrony**: All items must appear on the SAME frame. Don't draw target then flankers sequentially.
- **Arrow vs letter stimuli**: Arrows produce larger interference effects. Letters require learned mapping but avoid symbolic compatibility effects.
- **Response mapping**: Arrow keys (left/right) have natural spatial compatibility with arrow stimuli. Letter keys (f/j) avoid this confound. Confirm with user.
- **Children variant**: Replace arrows with fish images. Fish facing left/right. See [Children Flanker in stroop.md](stroop.md) for the image-based approach.
- **Neutral condition**: Some designs include a neutral condition (flankers that are neither congruent nor incongruent, e.g., squares instead of arrows). The neutral RT serves as a baseline.

## Data Output Columns

Base columns + `target_direction`, `flanker_direction`, `congruency`, `interference_cost` (incongruent RT − congruent RT, computed post-hoc)
