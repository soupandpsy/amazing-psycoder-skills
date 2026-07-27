# Review Gate

v1.4.0 — unified, evidence-gated, and PsyCoder Studio-compatible.

## Purpose

Define fail-closed backend derivation rules. The Reviewer supplies only
primitive findings and reviewed file hashes. It never supplies issue counts,
repair state, `ready_for_packaging`, `smoke_test_status`, or
`ready_for_collection`.

## Gate Rules

### Rule 1: Critical Block

```text
critical_count = count(current_review.issues where severity == "critical")
IF critical_count > 0:
    static_review_passed = false
    ready_for_packaging = false
    ready_for_collection = false
    packaging MUST stop
```

### Rule 2: Major Block (MVP)

```text
major_count = count(current_review.issues where severity == "major")
IF major_count > 0:
    static_review_passed = false
    ready_for_packaging = false
    ready_for_collection = false
    packaging MUST stop
```

Counts are derived from the current immutable review; they are not accepted as
model output. A repair creates a new content-addressed artifact set and requires
a fresh review. Findings are never mutated to `resolved`.

### Rule 3: Static Packaging Derivation

```text
static_review_passed =
    critical_count == 0
    AND major_count == 0

ready_for_packaging =
    static_review_passed
    AND artifact_contract_passed
    AND reviewed_scope_complete
    AND all_reviewed_hashes_match
```

`ready_for_packaging` is written only to the backend-owned
`ReadinessSnapshot`. Packaging may produce a candidate for target-machine
testing; it does not imply collection readiness.

### Rule 4: Artifact Identity and Path Safety

```text
IF reviewed_files is empty:
    packaging MUST stop
ELSE IF reviewed_files does not cover every required in-scope artifact:
    packaging MUST stop
ELSE IF review.artifact_set_hash != current_artifact_set_hash:
    packaging MUST stop
ELSE IF review.execution_plan_hash != immutable_execution_plan_hash:
    packaging MUST stop
ELSE IF any path is absolute, contains a backslash, traverses a parent,
        is unreadable, violates ownership, or its SHA-256 mismatches:
    packaging MUST stop
```

Review reports contain hashes, not duplicated file content. Compiler-owned
artifacts and `_pipeline/` metadata can never be replaced by a Coder repair.

### Rule 5: Runtime Readiness

```text
required_runtime_checks = {
    "launch_exit",
    "full_short_session",
    "data_integrity",
    "incremental_recovery"
}

IF a config-dependent hardware/timing claim exists:
    required_runtime_checks += {"timing_device_check"}

smoke_test_status =
    "passed" only if every required check has a validated passing record
    "failed" if any required check failed
    "blocked" if any required check is blocked
    "missing" otherwise

ready_for_collection =
    ready_for_packaging
    AND smoke_test_status == "passed"
```

Every passing `RuntimeEvidence` record must match the current artifact hash and
include the exact target environment, procedure, timestamps, observer, and
inspectable evidence paths. A summary assertion is not evidence.

## Skill vs. Pipeline Responsibility

| Layer | Responsibility |
|-------|---------------|
| **Reviewer skill** | Defines professional checks and emits evidence-based Critical/Major/Minor findings plus reviewed file hashes. |
| **Coder repair** | Replaces only authorized model-owned files for explicit issue IDs; maximum two attempts. |
| **Pipeline validator** | Validates schemas, paths, ownership, hashes, required artifacts, and static checks; computes counts and readiness. |
| **Target workflow** | Produces structured observed `RuntimeEvidence`; never inferred from source inspection. |

## PsyCoder Studio Integration

```text
Stage 3: Read-only Reviewer
  -> ReviewReport(findings + hashes)

Optional Stage 3b: Coder Repair
  -> RepairAttempt(authorized model-owned files)
  -> validate -> new artifact hash -> new review

Stage 4: Deterministic Validator
  -> derive counts, static state, smoke state, and ReadinessSnapshot
  -> block on malformed records, identity mismatch, unsafe paths, or findings

Stage 5: Artifact Packager
  -> package only when ready_for_packaging is derived true
```
