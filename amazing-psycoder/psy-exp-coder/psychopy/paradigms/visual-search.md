# Visual Search — PsychoPy

> **Parent**: [psy-exp-coder](../../SKILL.md) · [Implementation Guide](../spec/README.md)
> **Config reference**: [visual-search](../../../psy-exp-designer/paradigms/visual-search.md)
> **Status**: **CONFIG-DRIVEN** — no Pavlovia demo code found. Code generated from config YAML using the patterns below.

## Experiment Logic

Participants search for a target among distractors. Set size (number of items) varies. Two search types: feature search (target pops out — RT flat across set sizes) and conjunction search (target defined by feature combination — RT increases linearly with set size). The slope of RT × set size is the primary measure.

## Trial Window Sequence

```
Fixation (500ms) → Search Display (until key) → Feedback (practice) → ITI (500-800ms)
```

Search display shows all items simultaneously. Response is "target present" or "target absent" (two keys). Typical: 50% target-present trials.

## Implementation Pattern

### Step 1: Display Layout

```python
import math, random

def generate_positions(set_size, layout='circle', radius=5.0):
    """Generate (x, y) positions for set_size items."""
    positions = []
    if layout == 'circle':
        for i in range(set_size):
            angle = (2 * math.pi * i / set_size) - math.pi / 2  # start from top
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            positions.append((x, y))
        # Add small random jitter to avoid perfect symmetry
        positions = [(x + random.uniform(-0.3, 0.3), y + random.uniform(-0.3, 0.3)) for x, y in positions]
    
    elif layout == 'grid':
        cols = math.ceil(math.sqrt(set_size))
        rows = math.ceil(set_size / cols)
        for i in range(set_size):
            row = i // cols
            col = i % cols
            x = (col - (cols - 1) / 2) * 1.5  # 1.5 deg spacing
            y = (row - (rows - 1) / 2) * 1.5
            positions.append((x, y))
    
    elif layout == 'random':
        # Random positions within a circular area, min separation enforced
        for i in range(set_size):
            while True:
                angle = random.uniform(0, 2 * math.pi)
                r = random.uniform(0, radius)
                x, y = r * math.cos(angle), r * math.sin(angle)
                # Check min separation from existing positions
                if all(math.hypot(x - px, y - py) > 1.0 for px, py in positions):
                    positions.append((x, y))
                    break
    
    return positions
```

### Step 2: Stimulus Creation

```python
def create_search_display(win, condition, stimulus_folder, set_size):
    """
    Create all stimuli for the search display.
    
    Feature search: target differs from distractors on ONE dimension (e.g., color)
    Conjunction search: target is a specific combination (e.g., red AND vertical among red-horizontal and green-vertical)
    """
    if condition['search_type'] == 'feature':
        # All same shape, target has unique color
        target_color = 'red'
        distractor_color = 'green'
        target_shape = distractor_shape = 'T'
    elif condition['search_type'] == 'conjunction':
        # Target: red-vertical. Distractors: red-horizontal + green-vertical
        # Shared features prevent pop-out
        ...
    
    stimuli = []
    positions = generate_positions(set_size, layout=condition.get('display_layout', 'circle'))
    
    target_pos = random.randint(0, set_size - 1) if condition['target_present'] else None
    
    for i in range(set_size):
        if i == target_pos:
            # Target
            stim = visual.TextStim(win, text='T', pos=positions[i], color=target_color, height=0.8)
        else:
            # Distractor
            stim = visual.TextStim(win, text='T', pos=positions[i], color=distractor_color, height=0.8)
        stimuli.append(stim)
    
    return stimuli, target_pos
```

### Step 3: Trial Loop

```python
# Pre-create all stimuli at startup for each set size/condition combination
# to avoid per-trial creation overhead

for trial in trials:
    show_fixation(500)
    
    set_size = trial['set_size']
    stimuli, target_idx = preloaded_displays[(set_size, trial['target_present'])]
    
    # Draw all items simultaneously
    for stim in stimuli:
        stim.draw()
    win.callOnFlip(kb.clock.reset)
    win.callOnFlip(kb.clearEvents)
    win.flip()
    
    # Response collection (merged pattern)
    response = None
    rt = None
    timer = core.CountdownTimer(DEADLINE / 1000.0)
    while timer.getTime() > 0:
        keys = kb.getKeys(keyList=['f', 'j', 'escape'], waitRelease=False, clear=False)
        if keys:
            if keys[0].name == 'escape':
                save_and_quit()
            response = keys[0].name  # 'f' = present, 'j' = absent
            rt = keys[0].rt * 1000
            break
    
    # Accuracy
    correct_response = 'f' if trial['target_present'] else 'j'
    acc = 1 if response == correct_response else 0
```

### Key Edge Cases

- **Stimulus preloading is critical**: With set sizes up to 12+ items, creating `TextStim` or `ImageStim` objects per trial causes frame drops. Pre-generate all display configurations at startup and store as lists of stimuli.
- **Target position randomization**: Target (when present) must appear at random positions, not always the same location. Track target position in data for spatial analysis.
- **Minimal separation**: For random layouts, enforce minimum inter-item spacing to prevent overlap.
- **Feature vs conjunction**: The config `search_type` field determines the distractor generation strategy. Feature search = distractors differ on one dimension. Conjunction = distractors share one feature with the target each.
- **Set size balanced across block**: Ensure each set size appears equally often within each block.

## Data Output Columns

Base columns + `set_size`, `target_present`, `search_type`, `target_position`, `rt_slope` (regression slope computed post-hoc per participant)
