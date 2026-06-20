# Review Report Schema

v1.4 — PsyCoder Studio-compatible.

## Purpose

Define the structured output format for the AI Code Reviewer stage in PsyCoder Studio's three-stage pipeline. All fields marked `[GATE]` are used by the pipeline's Stage 4 (Local Validator) to decide whether to block packaging.

## ReviewReport

```json
{
  "readiness_label": "ready_for_collection | ready_after_minor_fixes | not_ready_for_collection",
  "ready_for_collection": true,
  "ready_for_packaging": true,
  "critical": 0,
  "major": 0,
  "minor": 0,
  "unresolved_critical_count": 0,
  "unresolved_major_count": 0,
  "issues_before_repair": [],
  "repairs_applied": [],
  "issues_after_repair": [],
  "reviewed_files": [],
  "summary": ""
}
```

### Field Definitions

| Field | Type | Required | [GATE] | Description |
|-------|------|----------|--------|-------------|
| `readiness_label` | string | ✅ | — | One of: `ready_for_collection`, `ready_after_minor_fixes`, `not_ready_for_collection` |
| `ready_for_collection` | boolean | ✅ | — | Zero critical AND zero major |
| `ready_for_packaging` | boolean | ✅ | ✅ | Derived gate: false if unresolved issues remain |
| `critical` | integer | ✅ | — | Total critical issues found (before repair) |
| `major` | integer | ✅ | — | Total major issues found (before repair) |
| `minor` | integer | ✅ | — | Total minor issues found (before repair) |
| `unresolved_critical_count` | integer | ✅ | ✅ | Pipeline MUST block packaging if > 0 |
| `unresolved_major_count` | integer | ✅ | ✅ | Pipeline SHOULD block packaging if > 0 (MVP rule: MUST block) |
| `issues_before_repair` | ReviewIssue[] | ✅ | — | All issues found on first pass |
| `repairs_applied` | string[] | ✅ | — | Description of each repair applied |
| `issues_after_repair` | ReviewIssue[] | ✅ | — | Issues remaining after repair (unresolved ones) |
| `reviewed_files` | FileObject[] | ✅ | — | Complete final files (repaired where possible) |
| `summary` | string | ✅ | — | Human-readable summary |

## ReviewIssue

```json
{
  "severity": "critical | major | minor",
  "category": "Timing | Response | Data | Feedback | Safety | Completeness",
  "message": "What is wrong",
  "suggestion": "How to fix it",
  "file": "main.py",
  "line_hint": "approximate area",
  "resolved": false
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `severity` | string | ✅ | `critical`, `major`, or `minor` |
| `category` | string | ✅ | Issue category |
| `message` | string | ✅ | Clear description of the problem |
| `suggestion` | string | ✅ | How to fix (actionable) |
| `file` | string | ✅ | Which file the issue is in |
| `line_hint` | string | — | Approximate area for human debugging |
| `resolved` | boolean | ✅ | Whether this issue was resolved after repair |

## Severity Definitions

### Critical

- Code will not run or will crash mid-experiment
- Data integrity is compromised (wrong RT source, missing columns, lost trials)
- Escape/abort is broken (participant cannot quit)
- Platform anti-pattern present (e.g., `time.sleep()` in PsychoPy)
- Required file is missing or empty
- Quality Gate item 1-9 failure

### Major

- Experiment logic does not match spec (wrong block structure, wrong timing)
- Response mapping incorrect
- Feedback logic wrong (practice feedback shown in formal blocks or vice versa)
- Missing required data fields
- No participant dialog
- No error handling for missing files

### Minor

- Missing README run instructions
- Missing pilot checklist
- Hardcoded values that should be parameters
- No inline comments in generated code
- Code style inconsistencies

## Gate Contract

The pipeline's Stage 4 (Local Validator) reads these fields from the review report:

| Condition | Action |
|-----------|--------|
| `ready_for_packaging = false` | **BLOCK** — do not package |
| `unresolved_critical_count > 0` | **BLOCK** — do not package |
| `unresolved_major_count > 0` | **BLOCK** — do not package (MVP) |
| `reviewed_files` is empty or missing | **BLOCK** — do not package |
| All gates pass | Proceed to Stage 5 (Packaging) |
