# N-back — PsychoPy

> **Parent**: [psy-exp-coder](../../SKILL.md) · [Implementation Guide](../spec/README.md)
> **Config reference**: [n-back](../../../psy-exp-designer/paradigms/n-back.md)
> **Status**: **CONFIG-DRIVEN** — no Pavlovia demo code found. Code generated from config YAML using the patterns below.

## Experiment Logic

A sequence of stimuli is presented one at a time. For each stimulus, the participant judges whether it matches the stimulus presented N positions back in the sequence. N typically varies across blocks (1-back, 2-back, 3-back). Measures working memory updating and maintenance.

## Trial Window Sequence

```
Fixation (500ms) → Stimulus (500ms) → Response (deadline 2000ms, merged) → Feedback (practice) → ITI (1000ms fixed)
```

Response window uses the merged pattern: stimulus appears, participant responds with match/non-match key. For dual n-back (visual + auditory), both modalities present simultaneously.

## Implementation Pattern

### Step 1: Stimulus Sequence Generation (Critical)

The key challenge in n-back is generating the stimulus sequence with controlled match/lure properties BEFORE the experiment starts:

```python
import random, csv

def generate_nback_sequence(n_level, n_trials, match_ratio=0.33, lure_type='none'):
    """
    Generate n-back stimulus sequence.
    
    n_level: 1, 2, or 3 (how far back to compare)
    n_trials: total trials in block
    match_ratio: proportion of match trials (typically 0.33)
    lure_type: 'none', 'n-1', 'n+1', or 'both' (lure = near-match distractor)
    
    Returns list of dicts: [{trial, stimulus, is_match, is_lure}, ...]
    """
    stimuli_pool = list('ABCDEFGHJKLMNPQRSTUVWXYZ')  # exclude easily confused letters
    n_matches = int(n_trials * match_ratio)
    n_lures = int(n_trials * 0.15) if lure_type != 'none' else 0
    n_non_matches = n_trials - n_matches - n_lures
    
    # First N trials cannot be match (no N-back history)
    sequence = []
    for i in range(n_level):
        sequence.append({'stimulus': random.choice(stimuli_pool), 'is_match': False, 'is_lure': False})
    
    # Distribute match, lure, and non-match trials
    trial_types = (['match'] * n_matches + ['lure'] * n_lures + ['non_match'] * n_non_matches)
    random.shuffle(trial_types)
    
    for trial_type in trial_types:
        if trial_type == 'match':
            # Match = same stimulus as N positions back
            stim = sequence[-n_level]['stimulus']
            sequence.append({'stimulus': stim, 'is_match': True, 'is_lure': False})
        elif trial_type == 'lure':
            # Lure = stimulus from n-1 or n+1 positions back (partial match trap)
            offset = - (n_level - 1) if lure_type in ('n-1', 'both') and random.random() < 0.5 else - (n_level + 1)
            if abs(offset) <= len(sequence):
                stim = sequence[offset]['stimulus']
            else:
                stim = random.choice(stimuli_pool)
            sequence.append({'stimulus': stim, 'is_match': False, 'is_lure': True})
        else:
            # Non-match: any stimulus not matching N-back
            stim = random.choice([s for s in stimuli_pool if s != sequence[-n_level]['stimulus']])
            sequence.append({'stimulus': stim, 'is_match': False, 'is_lure': False})
    
    random.shuffle(sequence[n_level:])  # reshuffle after first N (which stay fixed)
    return sequence
```

**Critical**: The sequence MUST be generated before the trial loop. Do NOT compute matches on-the-fly during trials — it breaks randomization control.

### Step 2: Match Detection Logic

```python
# Inside trial loop
# current_stimulus is the current trial's stimulus letter
# n_back_stimulus is the stimulus from N trials ago

n_back_stimulus = trial_history[-n_level]['stimulus']  # n_level = 1, 2, or 3
is_match = (current_stimulus == n_back_stimulus)

# Accuracy: key 'f' = match, key 'j' = non-match (confirm mapping with user)
if is_match:
    correct = (response == 'f')
else:
    correct = (response == 'j')
```

### Step 3: Trial History Ring Buffer

```python
trial_history = []  # FIFO buffer of last N+1 stimuli

for trial in trials:
    current_stimulus = trial['stimulus']
    
    # Present stimulus...
    
    if len(trial_history) >= n_level:
        n_back_stimulus = trial_history[-n_level]['stimulus']
        is_match = (current_stimulus == n_back_stimulus)
        is_lure = trial.get('is_lure', False)
    else:
        is_match = False
        is_lure = False
    
    trial_history.append({'stimulus': current_stimulus, 'is_match': is_match})
```

### Step 4: Block Structure

```python
# Each n-level is a separate block with its own generated sequence
for n_level in [1, 2, 3]:  # or from paradigm_config.n_levels
    sequence = generate_nback_sequence(n_level, trials_per_block, ...)
    run_block(sequence, n_level)
    show_rest_screen()
```

### Key Edge Cases

- **First N trials**: Cannot be match trials (no N-back history). Mark these in data as `n_back_available: false`.
- **Lure trials**: Stimulus that appeared n-1 or n+1 positions back. These provoke false alarms and are a key measure of WM precision. If `lure_type: none` in config, skip lure generation.
- **Dual n-back**: Present visual AND auditory stimuli simultaneously. Two independent sequences. Participant responds separately (e.g., left hand for visual match, right hand for auditory match). Much more complex — confirm with user if they want this variant.
- **Stimulus pool**: Use letters (consonants only, no vowels to avoid word formation), spatial positions (8 locations around fixation), or images.

## Data Output Columns

Base columns + `n_level`, `stimulus`, `n_back_stimulus`, `is_match`, `is_lure`

## Analysis Notes

- **d' (d-prime)**: `d' = Z(hit_rate) - Z(false_alarm_rate)`. Hits = correctly identified matches. False alarms = "match" response on non-match trials.
- **Lure false alarm rate**: Separately track FA rate on lure vs non-lure trials.
