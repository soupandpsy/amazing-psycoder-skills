# Condition File Standard

**→ Input**: xlsx/csv files that drive trial order. Each row = one trial. Columns feed `{column_name}` references in the config YAML.

> **Related**: [config-schema.md](config-schema.md) · [data-recording.md](data-recording.md)

> ⚠️ **LANGUAGE NOTE**: Example values in this document (e.g., `"正确"`, `"错误"`, `"太慢"` for feedback text) are Chinese-language placeholders. When generating condition files, use the equivalent text in the user's language. See [Language Consistency (Red Line)](../../psy-exp-coder/SKILL.md#language-consistency-red-line).

## File Format

- **Primary**: `.xlsx` (user-facing)
- **Alternative**: `.csv` (UTF-8, for scripted generation)
- Both are accepted; xlsx is preferred for non-programmers

## Common Base Columns

These columns are commonly used across paradigms. Column names can be adapted — the config YAML uses `{column_name}` references, so any column name works as long as it matches between the config and the condition file. For paradigm-specific columns, see the individual paradigm files linked below.

| Column | Type | Description |
|--------|------|-------------|
| trial | int | Trial number within the block (1-indexed) |
| stimulus | str | Stimulus filename or display text (may be named differently per paradigm, e.g., `word`, `prime`, `target`) |
| condition | str | Condition label for analysis grouping |
| correct_response | str | Expected key name, or empty for no-go |
| trial_type | str | Paradigm-specific trial type |
| deadline | int | Response deadline for this trial (ms) |

## Paradigm-Specific Columns

Each paradigm defines its own condition file columns in its paradigm file. See the `## Condition File Columns` section in the relevant paradigm:

- [Go/No-go](../paradigms/go-nogo.md#condition-file-columns)
- [Stop-signal](../paradigms/stop-signal.md#condition-file-columns)
- [Stroop](../paradigms/stroop.md#condition-file-columns)
- [Eriksen Flanker](../paradigms/eriksen-flanker.md#condition-file-columns)
- [Simon](../paradigms/simon.md#condition-file-columns)
- [Navon](../paradigms/navon.md#condition-file-columns)
- [Priming](../paradigms/priming.md#condition-file-columns)
- [Rating](../paradigms/rating.md#condition-file-columns)
- [IAT](../paradigms/iat.md#condition-file-columns)
- [N-back](../paradigms/n-back.md#condition-file-columns)
- [Dot-probe](../paradigms/dot-probe.md#condition-file-columns)
- [Visual Search](../paradigms/visual-search.md#condition-file-columns)
- [Task Switching](../paradigms/task-switching.md#condition-file-columns)
- [EAST](../paradigms/east.md#condition-file-columns)

## Variable Substitution

In the config YAML, `{column_name}` references a column in the condition file. At runtime, each trial's values are substituted:

```yaml
# config.yaml
content: "{stimulus}"
response: [{correct_response}]
```

```csv
# conditions.xlsx
trial, stimulus, correct_response
1, X, space
2, O,
3, X, space
```

Result: Trial 1 shows "X" and expects "space"; Trial 2 shows "O" and expects no response.

### Special substitution variables

| Variable | Source | Description |
|----------|--------|-------------|
| `{subject_id}` | Runtime input | Subject identifier |
| `{block_name}` | Block definition | Current block name |
| `{trial_number}` | Trial loop counter | Current trial index |
| `{feedback_text}` | Accuracy evaluation | `"正确"`, `"错误"`, or `"太慢"` |

## Validation Rules

Before using a condition file, verify:

1. All `{column_name}` references in config YAML exist in the condition file
2. No missing values in required columns
3. File paths in `stimulus` column (if referencing images) exist on disk
4. Trial numbering is consecutive and correct
5. Condition ratios match stated design (e.g., 80:20 go:nogo)
6. No more than N consecutive same-condition trials (if constraint specified)
