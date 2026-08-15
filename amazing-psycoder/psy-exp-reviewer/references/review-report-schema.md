# Review and Evidence Contracts

v1.4.0 — unified, evidence-gated, and PsyCoder Studio-compatible.

## Purpose

PsyCoder Studio separates review, constrained Coder repair, runtime evidence,
and derived readiness so that a model cannot repair its own review, duplicate
large files inside a report, or self-certify readiness. A `RepairAttempt` is an
internal Worker record: it is accepted only after exact review, artifact, plan,
issue-ID, Model/asset hash, and runtime-path binding succeeds.
The executable JSON Schemas under `../../runtime/schemas/` are authoritative.

| Record | Producer | Contains | Must not contain |
|---|---|---|---|
| `ReviewReport` | Reviewer | scope, primitive findings, reviewed hashes | file content, repairs, counts, readiness |
| `RepairAttempt` | Coder, invoked by Worker | hash-bound allowlisted runtime replacements | ExperimentModel, assets, metadata, evidence, or unreviewed paths |
| `RuntimeEvidence` | target-machine workflow + reviewer inspection | structured observed tests and evidence paths | inferred or planned results |
| `ReadinessSnapshot` | deterministic backend | derived packaging/collection state | free-form model judgment |

## ReviewReport

Schema: `../../runtime/schemas/review-output.schema.json`.

```json
{
  "review_id": "review_018",
  "artifact_set_hash": "64 lowercase hex characters",
  "model_hash": "64 lowercase hex characters",
  "asset_set_hash": "64 lowercase hex characters",
  "mode": "code-audit",
  "scope": {
    "reviewed": ["experiment_model.json", "compilation_manifest.json", "source_map.json", "main.py"],
    "not_reviewed": ["target-machine timing"]
  },
  "issues": [
    {
      "id": "REV-001",
      "severity": "major",
      "category": "DesignFidelity",
      "message": "The response mapping differs from the frozen ExperimentModel@4.",
      "suggestion": "Fix the maintained compiler adapter, add a regression fixture, and regenerate from responses.mapping.",
      "file": "main.py",
      "line": 184,
      "evidence": ["ExperimentModel /presentation/windows/0 response key f maps to red; code maps f to green."]
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

The Worker accepts this record only inside a bounded repair round after a
hash-bound Reviewer report identifies blocking findings. It verifies the exact
review ID, prior artifact-set hash, Model hash, asset-set hash, blocking issue IDs, and
platform runtime path allowlist before applying any replacement. The saved
ExperimentModel, asset manifest, conditions, `_pipeline/` metadata, and prior evidence are
never mutable through this record. Every changed artifact set receives a new
hash and a fresh read-only review.

## RuntimeEvidence

Schema: `../../runtime/schemas/runtime-evidence.schema.json`.

Required tests for the generic experiment profile are:

- `launch_exit`
- `full_short_session`
- `data_integrity`
- `incremental_recovery`
- `timing_device_check`

All five checks are required exactly once for every supported Studio platform.
Every test records `result`, the exact procedure,
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
