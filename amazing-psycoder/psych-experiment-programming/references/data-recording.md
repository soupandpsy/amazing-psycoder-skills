# Data Recording Standard

**→ Output**: CSV data files written by the experiment code. Each row = one trial. Applies to all experiments, regardless of platform or paradigm.

## Required Base Columns

Every experiment must record these columns per trial:

| Column | Type | Description |
|--------|------|-------------|
| subject_id | str | Subject identifier |
| block | int | Block number (1-indexed) |
| trial | int | Trial number within block (1-indexed) |
| condition | str | Condition label |
| stimulus | str | Stimulus filename or ID |
| correct_response | str | Expected key (or `""` for no-go) |
| response | str | Actual key pressed (or `""` for timeout) |
| rt | float | Reaction time in milliseconds (empty if timeout) |
| accuracy | int | 1=correct, 0=incorrect, -1=timeout |
| timestamp | str | ISO 8601 timestamp of trial onset |

## Saving Rules

1. **Save incrementally** — write and flush after every trial or at minimum every block. Do not defer all writes to the end.
2. **Use `try/finally`** — wrap the main experiment in try/finally to guarantee file closure even on crash or escape quit.
3. **Filename convention**: `data/sub-{subject_id}_{task_name}_{date}.csv`
4. **CSV format**: Use `csv.DictWriter` with `newline=''` for cross-platform compatibility
5. **Encoding**: UTF-8 with BOM only on Windows; UTF-8 without BOM elsewhere

## Accuracy Coding

- **1**: correct response within deadline
- **0**: incorrect response within deadline
- **-1**: no response (timeout)

For paradigms with no-go trials, accuracy on no-go trials:
- No response on no-go: accuracy=1 (correct rejection)
- Response on no-go: accuracy=0 (commission error / false alarm)

## NaN Handling

- Missing RT (timeout, correct no-go withholding): record as empty string `''` in CSV, not `'None'` or `'NaN'`
- Analysis code should handle empty RT values, not the experiment code

## Cross-platform Notes

- macOS/Linux: lines end with `\n`
- Windows: `csv.DictWriter` handles this automatically; no special handling needed
