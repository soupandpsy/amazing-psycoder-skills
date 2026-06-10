# Task Switching — PsychoPy

> **Parent**: [psy-exp-coder](../../SKILL.md) · [Implementation Guide](../spec/README.md)
> **Config reference**: [task-switching](../../../psy-exp-designer/paradigms/task-switching.md)
> **Status**: **CONFIG-DRIVEN** — no Pavlovia demo code found. Code generated from config YAML using the patterns below.

## Experiment Logic

Participants alternate between two (or more) tasks. A cue before each trial indicates which task to perform. The key measure is the **switch cost**: RT difference between switch trials (task differs from previous trial) and repeat trials (same task). Also measures mixing cost (all trials in mixed blocks vs single-task blocks).

## Trial Window Sequence

```
Fixation (500ms) → Cue (CSI duration) → Target (until response, merged) → Feedback → RCI (blank, until next trial)
```

- **CSI** (Cue-Stimulus Interval): Time from cue onset to target onset. Typically 100-600ms.
- **RCI** (Response-Cue Interval): Time from response to next cue. Typically 500-1500ms.

## Implementation Pattern

### Step 1: Task Definitions

```python
# From paradigm_config.tasks in config YAML
TASKS = [
    {
        'name': 'parity',
        'cue': '红色边框',  # or visual cue type
        'cue_color': 'red',
        'rule': 'odd_even',
        'response_mapping': {'f': 'odd', 'j': 'even'}
    },
    {
        'name': 'magnitude',
        'cue': '蓝色边框',
        'cue_color': 'blue',
        'rule': 'greater_less_5',
        'response_mapping': {'f': '>5', 'j': '<5'}
    }
]
```

### Step 2: Cue Presentation

```python
def show_cue(task, cue_color, csi_duration):
    """Present task cue. Cue can be a colored border, text label, or symbol."""
    # Option A: Colored border (rectangle around stimulus area)
    cue_rect = visual.Rect(win, width=6, height=6, lineColor=cue_color, lineWidth=5)
    cue_rect.draw()
    win.flip()
    core.wait(csi_duration / 1000.0)  # Short fixed duration, acceptable for cue-only
    
    # Option B: Text cue
    cue_text = visual.TextStim(win, text=task['cue'], color=cue_color, height=30)
    cue_text.draw()
    win.flip()
    core.wait(csi_duration / 1000.0)
```

### Step 3: Trial Loop with Switch/Repeat Tracking

```python
previous_task = None  # Track for switch vs repeat classification

for trial in trials:
    task = trial['task']  # which task for this trial
    
    # Determine switch vs repeat (first trial = neither)
    is_switch = None if previous_task is None else (task['name'] != previous_task['name'])
    previous_task = task
    
    # 1. Fixation
    show_fixation(FIXATION_DURATION)
    
    # 2. Cue
    show_cue(task, task['cue_color'], CSI)
    
    # 3. Target (merged stimulus + response)
    target_stim = visual.TextStim(win, text=str(trial['target']), height=40)
    target_stim.draw()
    win.callOnFlip(kb.clock.reset)
    win.callOnFlip(kb.clearEvents)
    win.flip()
    
    # 4. Response
    response = None
    rt = None
    timer = core.CountdownTimer(DEADLINE / 1000.0)
    while timer.getTime() > 0:
        keys = kb.getKeys(keyList=list(task['response_mapping'].keys()) + ['escape'], waitRelease=False, clear=False)
        if keys:
            if keys[0].name == 'escape':
                save_and_quit()
            response = keys[0].name
            rt = keys[0].rt * 1000
            break
    
    # 5. Accuracy based on task rule
    correct_answer = compute_correct_answer(trial['target'], task['rule'], task['response_mapping'])
    acc = 1 if response == correct_answer else 0
    
    # 6. RCI (blank screen)
    show_blank(RCI)
```

### Step 4: Correct Answer Computation

```python
def compute_correct_answer(target, rule, response_mapping):
    """Determine which key is correct based on the task rule."""
    if rule == 'odd_even':
        is_odd = (target % 2 == 1)
        answer_label = 'odd' if is_odd else 'even'
    elif rule == 'greater_less_5':
        answer_label = '>5' if target > 5 else '<5'
    elif rule == 'vowel_consonant':
        answer_label = 'vowel' if target.upper() in 'AEIOU' else 'consonant'
    else:
        raise ValueError(f"Unknown rule: {rule}")
    
    # Reverse-map: which key corresponds to this answer label?
    for key, label in response_mapping.items():
        if label == answer_label:
            return key
    return None
```

### Step 5: Trial Sequence Generation

```python
def generate_task_sequence(tasks, n_trials, switch_ratio=0.5):
    """
    Generate trial sequence with controlled switch ratio.
    
    switch_ratio: proportion of trials that are task switches (vs repeats)
    """
    # Distribute switch and repeat trials
    n_switches = int(n_trials * switch_ratio)
    n_repeats = n_trials - n_switches - 1  # -1 for first trial (neither)
    
    trial_types = ['switch'] * n_switches + ['repeat'] * n_repeats
    random.shuffle(trial_types)
    
    sequence = []
    current_task = random.choice(tasks)
    
    # First trial (not classified as switch or repeat)
    sequence.append({'task': current_task, 'is_switch': None})
    
    for trial_type in trial_types:
        if trial_type == 'switch':
            # Switch to a DIFFERENT task
            other_tasks = [t for t in tasks if t['name'] != current_task['name']]
            current_task = random.choice(other_tasks)
        # else: repeat = same task
        sequence.append({'task': current_task, 'is_switch': (trial_type == 'switch')})
    
    return sequence
```

### Key Edge Cases

- **Task cue encoding**: The cue must unambiguously indicate which task to perform. Common cues: colored borders, spatial location, explicit text labels, abstract symbols. Confirm cue type with user.
- **CSI/RCI timing**: Short CSI (100ms) → high switch cost (insufficient preparation). Long CSI (600ms+) → reduced switch cost (full preparation). The config should specify these values.
- **Stimulus-task overlap**: Use stimuli that are ambiguous (e.g., digits 1-9 excluding 5 for parity+magnitude tasks) so the same stimulus appears in both tasks, preventing task inference from stimulus identity.
- **Congruency**: On some trials, both tasks would yield the same response (congruent); on others, different responses (incongruent). Congruency effects are a secondary measure — mark in data.
- **First trial exclusion**: The first trial of each block has no previous task to compare against. Exclude from switch cost analysis.
- **Error trials**: Trials following an error may show post-error slowing. Track error history in data.

## Data Output Columns

Base columns + `task_name`, `is_switch` (1/0/None), `is_congruent` (1/0), `previous_task`, `csi`, `rci`, `switch_cost` (computed post-hoc per participant: mean RT_switch − mean RT_repeat)
