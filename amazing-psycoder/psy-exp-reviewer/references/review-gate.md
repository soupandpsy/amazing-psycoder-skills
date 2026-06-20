# Review Gate

v1.4 — PsyCoder Studio-compatible.

## Purpose

Define the hard gating rules that prevent packaging of experiment code that has unresolved critical or major issues. These rules are enforced by PsyCoder Studio's Stage 4 (Local Validator), not by the AI.

## Gate Rules

### Rule 1: Critical Block

```
IF unresolved_critical_count > 0:
    ready_for_packaging = false
    packaging MUST stop
    status = "failed"
    error_message = "Review gate blocked: {unresolved_critical_count} unresolved critical issues"
```

### Rule 2: Major Block (MVP)

```
IF unresolved_major_count > 0:
    ready_for_packaging = false
    packaging MUST stop
    status = "failed"
    error_message = "Review gate blocked: {unresolved_major_count} unresolved major issues"
```

### Rule 3: ready_for_packaging Block

```
IF ready_for_packaging == false:
    packaging MUST stop
    status = "failed"
    error_message = "Review gate blocked: ready_for_packaging is false"
```

### Rule 4: Missing reviewed_files

```
IF reviewed_files is empty or missing:
    packaging MUST stop
    status = "failed"
    error_message = "Review gate blocked: no reviewed_files provided"
```

## Skill vs. Pipeline Responsibility

| Layer | Responsibility |
|-------|---------------|
| **Skill (psy-exp-reviewer)** | Defines what is critical/major/minor. Sets `unresolved_critical_count` and `ready_for_packaging` based on professional review standards. |
| **Pipeline (Local Validator)** | Reads gate fields from review report. Enforces hard blocks. Does NOT make semantic judgments about code quality. |

## Why This Separation

- Skills are expert knowledge that evolves with psychology research standards
- Pipeline gates are engineering invariants that must not be bypassed
- AI can make mistakes in review — the gate provides a safety net
- If the review report is malformed or missing gate fields, packaging is blocked by default (fail-safe)

## Local Validator vs. Review Gate

| Check | Performed By | Type |
|-------|-------------|------|
| Required files exist | Local Validator | Structural |
| No path traversal (`../`) | Local Validator | Security |
| Content non-empty | Local Validator | Structural |
| Valid zip packagable | Local Validator | Structural |
| `unresolved_critical_count > 0` | Review Gate | Semantic gate |
| `ready_for_packaging = false` | Review Gate | Semantic gate |
| API correctness | psy-exp-reviewer skill | Professional standard |
| Platform anti-patterns | psy-exp-reviewer skill | Professional standard |

The Local Validator is NOT a semantic reviewer. It does not read code. It checks file structure, enforces the review gate, and ensures packaging safety.

## PsyCoder Studio Integration

In PsyCoder Studio's pipeline:

```
Stage 3: AI Code Reviewer
  → Output: ReviewReport (with gate fields)

Stage 4: Local Validator
  → Check: required files + path safety
  → Check: review gate (unresolved_critical, unresolved_major, ready_for_packaging)
  → If any gate fails → status = "failed", packaging blocked

Stage 5: Artifact Packager
  → Only reached if all gates pass
```
