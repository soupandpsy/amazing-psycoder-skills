# Condition File Generation Tool

> **Use when**: Phase 3 determines condition files need to be generated (user has no existing xlsx).
> **Output**: Python script that creates the xlsx file, OR LLM-generated xlsx content.

## Decision: Generate Via Script or Direct Write?

| User's technical level | Approach |
|------------------------|----------|
| Non-programmer | **Direct write** — the LLM writes the xlsx content directly using `openpyxl` and saves it. The user just provides a filename. |
| Programmer / reproducible | **Generate script** — produce a standalone `generate_conditions.py` that creates all xlsx files. User runs it once. |
| Simple design (< 50 trials) | Either approach works. Direct write is faster for the user. |
| Complex design (factorial, counterbalanced) | Generate script is preferred — easier to verify and re-run with parameter changes. |

**Default**: Direct write for practice blocks (simple), generate script for formal blocks.

## Direct Write Template

When generating an xlsx file directly, the LLM should:

1. Confirm the output filename and directory with the user
2. Write the file using `openpyxl`
3. Report: file path, row count, column names, condition distribution

```python
# LLM executes this to create the condition file
from openpyxl import Workbook
import os

output_path = "conditions/block_1.xlsx"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

wb = Workbook()
ws = wb.active

# Write header
columns = ['trial', 'stimulus', 'condition', 'correct_response']
for col_idx, col_name in enumerate(columns, 1):
    ws.cell(row=1, column=col_idx, value=col_name)

# Generate trials
# ... (paradigm-specific generation logic)

# Write data rows
for row_idx, trial in enumerate(trials, 2):
    for col_idx, col_name in enumerate(columns, 1):
        ws.cell(row=row_idx, column=col_idx, value=trial[col_name])

wb.save(output_path)
print(f"Created: {output_path} ({len(trials)} trials, {len(columns)} columns)")
```

## Standalone Generation Script Template

For reproducible condition generation, produce this script alongside the experiment code:

```python
#!/usr/bin/env python3
"""Condition file generator for <experiment_name>.

Usage: python generate_conditions.py
Output: conditions/*.xlsx

Edit the PARAMETERS section to adjust trial counts, ratios, etc.
"""

# ============================================================
# PARAMETERS — edit these to change the experimental design
# ============================================================
OUTPUT_DIR = "conditions"
N_PRACTICE = 20
N_FORMAL_PER_BLOCK = 60
N_BLOCKS = 2
GO_RATIO = 0.8         # proportion go trials
MAX_CONSECUTIVE_NOGO = 2
STIMULI_GO = ['X']
STIMULI_NOGO = ['O']
GO_KEY = 'space'
RANDOM_SEED = 42
# ============================================================

import random
import os
from openpyxl import Workbook

random.seed(RANDOM_SEED)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_go_nogo_trials(n_trials, go_ratio, max_consecutive_nogo):
    """Generate trial list with constraint: no more than max_consecutive_nogo nogo in a row."""
    n_go = int(n_trials * go_ratio)
    n_nogo = n_trials - n_go
    
    trial_types = ['go'] * n_go + ['nogo'] * n_nogo
    
    # Shuffle with constraint
    while True:
        random.shuffle(trial_types)
        # Check consecutive nogo constraint
        max_run = 0
        current_run = 0
        for t in trial_types:
            if t == 'nogo':
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        if max_run <= max_consecutive_nogo:
            break
    
    trials = []
    for i, ttype in enumerate(trial_types):
        stimulus = random.choice(STIMULI_GO) if ttype == 'go' else random.choice(STIMULI_NOGO)
        correct_response = GO_KEY if ttype == 'go' else ''
        trials.append({
            'trial': i + 1,
            'stimulus': stimulus,
            'condition': ttype,
            'correct_response': correct_response
        })
    return trials

# Generate practice
practice_trials = generate_go_nogo_trials(N_PRACTICE, GO_RATIO, MAX_CONSECUTIVE_NOGO)
_write_xlsx(practice_trials, f"{OUTPUT_DIR}/practice.xlsx",
            ['trial', 'stimulus', 'condition', 'correct_response'])

# Generate formal blocks
for block_num in range(1, N_BLOCKS + 1):
    formal_trials = generate_go_nogo_trials(N_FORMAL_PER_BLOCK, GO_RATIO, MAX_CONSECUTIVE_NOGO)
    _write_xlsx(formal_trials, f"{OUTPUT_DIR}/block_{block_num}.xlsx",
                ['trial', 'stimulus', 'condition', 'correct_response'])

print(f"Done. Generated {1 + N_BLOCKS} condition files in {OUTPUT_DIR}/")
```

## Paradigm-Specific Generation Rules

### Go/No-go
- Constraint: no more than 2 consecutive no-go trials
- Columns: `trial`, `stimulus`, `condition` (go/nogo), `correct_response` (key or empty)
- Verify: go ratio after generation

### Stroop / Eriksen Flanker / Simon
- Factorial design: words × ink_colors (Stroop), or target × congruency (Flanker, Simon)
- Constraint: no more than 3 consecutive same-response trials
- Columns: `trial`, `word`, `ink_color` (Stroop), `congruency`, `correct_response`
- Verify: congruency ratio (50:50 default), condition counts equal

### Stop-signal
- Stop trials randomly interspersed (typically 25%)
- Constraint: no more than 2 consecutive stop trials
- Columns: `trial`, `stimulus`, `is_stop`, `correct_response`
- SSD is tracked dynamically, NOT in condition file

### N-back
- Sequence must be generated with controlled match/lure distribution
- First N trials cannot be matches
- Columns: `trial`, `stimulus`, `is_match`, `is_lure`

### Task Switching
- Task sequence with controlled switch ratio
- First trial of each block is neither switch nor repeat
- Columns: `trial`, `target`, `task_name`, `is_switch`, `correct_response`

### Visual Search
- Set size × target_present factorial
- Target position randomized within display
- Columns: `trial`, `set_size`, `target_present`, `target_position`

## Validation After Generation

After writing the xlsx file, verify:
1. `print(df['condition'].value_counts())` — condition distribution matches design
2. `print(df.columns.tolist())` — all required columns present
3. `print(df.isnull().sum())` — no missing values in required columns
4. Constraint violations (e.g., `df['condition'].eq('nogo').rolling(3).sum().max() <= 2`)
