# Review and Evidence Contracts

v1.4.0 — unified, evidence-gated, and PsyCoder Studio-compatible.

## Purpose

PsyCoder Studio uses four separate records so that a model cannot repair its
own review, duplicate large files inside a report, or self-certify readiness.
The executable JSON Schemas under `../../runtime/schemas/` are authoritative.

| Record | Producer | Contains | Must not contain |
|---|---|---|---|
| `ReviewReport` | Reviewer | scope, primitive findings, reviewed hashes | file content, repairs, counts, readiness |
| `RepairAttempt` | Coder | allowlisted model-owned replacement files | compiler-owned files, a new plan, readiness |
| `RuntimeEvidence` | target-machine workflow + reviewer inspection | structured observed tests and evidence paths | inferred or planned results |
| `ReadinessSnapshot` | deterministic backend | derived packaging/collection state | free-form model judgment |

## ReviewReport

Schema: `../../runtime/schemas/review-output.schema.json`.

```json
{
  "review_id": "review_018",
  "artifact_set_hash": "64 lowercase hex characters",
  "execution_plan_hash": "64 lowercase hex characters",
  "mode": "code-audit",
  "scope": {
    "reviewed": ["execution_plan.json", "main.py", "conditions.csv"],
    "not_reviewed": ["target-machine timing"]
  },
  "issues": [
    {
      "id": "REV-001",
      "severity": "major",
      "category": "DesignFidelity",
      "message": "The response mapping differs from the immutable plan.",
      "suggestion": "Regenerate the model-owned entrypoint from responses.mapping.",
      "file": "main.py",
      "line": 184,
      "evidence": ["ExecutionPlan response key f maps to red; code maps f to green."]
    }
  ],
  "reviewed_files": [
    {
      "path": "main.py",
      "sha256": "64 lowercase hex characters"
    }
  ],
  "summary": "One blocking design-fidelity issue.",
  "reviewed_at": "2026-07-23T10:30:00+08:00"
}
```

Issue counts are computed from `issues[].severity`. A report is immutable and
describes exactly one `artifact_set_hash`. After a repair, recompute every file
hash and run a new review with a new ID. There are no
`issues_before_repair`, `issues_after_repair`, or `repairs_applied` fields.

## ReviewIssue

Each finding records an ID, evidence-based severity, category, message,
actionable suggestion, safe project-relative file path, optional line, and
inspectable evidence. A finding never carries a model-controlled `resolved`
flag. It ceases to block only when a fresh review of a new artifact set no
longer reports it.

### Severity

- `critical`: the artifact cannot safely launch/exit/save, or primary-outcome
  integrity is systematically compromised.
- `major`: implementation materially diverges from the confirmed design,
  required data are missing, or an important runtime behavior is wrong.
- `minor`: maintainability, documentation, or polish issue that does not alter
  scientific interpretation or participant/data safety.

Severity follows impact, scope, recoverability, and testability—not a fixed
percentage or the mere presence of an anti-pattern.

## FileObject

Review reports store only a safe project-relative `path` and the `sha256` of
the exact bytes reviewed. They never duplicate file content. The backend
resolves the content-addressed artifact set, verifies every hash, and rejects
absolute paths, parent traversal, backslashes, unreadable files, or scope/hash
mismatches.

## RepairAttempt

Schema: `../../runtime/schemas/repair-attempt.schema.json`.

A Coder repair is authorized by one review ID and explicit issue IDs, declares
the target `platform`, echoes the input artifact and plan hashes, and may
replace only model-owned allowlisted paths. `_pipeline/`, the ExperimentSpec, ExecutionPlan, conditions, compiler
README/config, and prior evidence are protected. The backend permits at most
two attempts, re-runs structural/static validation, creates a new artifact-set
hash, and requests a new read-only review.

## RuntimeEvidence

Schema: `../../runtime/schemas/runtime-evidence.schema.json`.

Required tests for the generic experiment profile are:

- `launch_exit`
- `full_short_session`
- `data_integrity`
- `incremental_recovery`

Add `timing_device_check` whenever timing precision, audio, triggers, eye
tracking, specialized input, display calibration, or another hardware claim
depends on the target system. Every test records `result`, the exact procedure,
target OS/runtime/hardware, timestamps, and non-empty `evidence_paths`.
Statements such as “it ran fine,” planned procedures, model inference, or a
missing evidence path are not passing evidence.

## ReadinessSnapshot

Schema: `../../runtime/schemas/readiness-snapshot.schema.json`.

The backend derives:

```text
static_review_passed =
  current review has zero critical and zero major findings

ready_for_packaging =
  static_review_passed
  AND artifact ownership/path/hash/required-file checks pass

smoke_test_status =
  passed only when every required RuntimeEvidence test passes

ready_for_collection =
  ready_for_packaging AND smoke_test_status == passed
```

Missing runtime evidence may still allow packaging for smoke testing; it never
allows collection readiness. Contradictory booleans are rejected by schema and
the derivation logic.

## Fail-Closed Rules

- Invalid or incomplete ReviewReport → no gate transition.
- Unsafe path, hash mismatch, or incomplete reviewed scope → packaging blocked.
- Any current Critical or Major finding → packaging blocked.
- Missing/failed/blocked required RuntimeEvidence → collection blocked.
- A Reviewer response containing file rewrites, repair claims, counts, or
  readiness fields → schema rejection.
