# Review Gate

v1.4.0 — unified, evidence-gated, and PsyCoder Studio-compatible.

## Purpose

Define fail-closed backend derivation rules. The Reviewer supplies only primitive findings and reviewed file hashes. It never supplies issue counts, repair state, `ready_for_packaging`, `smoke_test_status`, or `ready_for_collection`.

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

Counts are derived from the current immutable review; they are not accepted as model output. In Studio, a blocking compiler defect fails the run. Repair the maintained adapter with a regression test and regenerate a new content-addressed artifact set for a fresh review. Findings are never mutated to `resolved` and the reviewed runtime is never patched in place by a model.

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

`ready_for_packaging` is written only to the backend-owned `ReadinessSnapshot`. Packaging may produce a candidate for target-machine testing; it does not imply collection readiness.

### Rule 4: Artifact Identity and Path Safety

```text
IF reviewed_files is empty:
    packaging MUST stop
ELSE IF reviewed_files does not cover every required in-scope artifact:
    packaging MUST stop
ELSE IF review.artifact_set_hash != current_artifact_set_hash:
    packaging MUST stop
ELSE IF review.model_hash != immutable_model_hash:
    packaging MUST stop
ELSE IF review.asset_set_hash != immutable_asset_set_hash:
    packaging MUST stop
ELSE IF any path is absolute, contains a backslash, traverses a parent,
        is unreadable, violates ownership, or its SHA-256 mismatches:
    packaging MUST stop
```

Review reports contain hashes, not duplicated file content. Studio `_pipeline/` metadata is host-owned. Runtime files may be replaced only by the separate Coder through a hash-bound allowlist; the Reviewer itself never rewrites files.

### Rule 5: Runtime Readiness

```text
required_runtime_checks = {
    "launch_exit",
    "full_short_session",
    "data_integrity",
    "incremental_recovery",
    "timing_device_check"
}

smoke_test_status =
    "passed" only if every required check has a validated passing record
    "failed" if any required check failed
    "blocked" if any required check is blocked
    "missing" otherwise

ready_for_collection =
    ready_for_packaging
    AND smoke_test_status == "passed"
```

All five checks are required exactly once because every supported experiment depends on display/input timing at its declared target. Every passing `RuntimeEvidence` record must match the current artifact hash and include the exact target environment, procedure, timestamps, observer, and inspectable evidence paths. The record is append-only and every evidence file has a server-computed SHA-256 digest. `user_attested` submissions remain useful triage records but cannot produce `smoke_test_status = "passed"`; that requires `machine_verified` or `reviewer_verified` evidence issued by an authenticated backend workflow. A summary assertion is not evidence.

## Skill vs. Pipeline Responsibility

| Layer | Responsibility |
| --- | --- |
| **Reviewer skill** | Defines professional checks and emits evidence-based Critical/Major/Minor findings plus reviewed file hashes. |
| **Constrained repair** | Separate Coder replaces only allowlisted runtime paths; host revalidates and re-reviews the new artifact set. Recurring defects also receive a maintained adapter regression fix. |
| **Pipeline validator** | Validates schemas, paths, ownership, hashes, required artifacts, and static checks; computes counts and readiness. |
| **Target workflow** | Produces structured observed `RuntimeEvidence`; never inferred from source inspection. |

## PsyCoder Studio Integration

```text
Stage 3: Read-only Reviewer
  -> ReviewReport(findings + hashes)

Optional Stage 3b: Adapter Defect Recovery
  -> fail current generation
  -> fix maintained adapter + regression test
  -> deploy -> regenerate -> new artifact hash -> new review

Stage 4: Deterministic Validator
  -> derive counts, static state, smoke state, and ReadinessSnapshot
  -> block on malformed records, identity mismatch, unsafe paths, or findings

Stage 5: Artifact Packager
  -> package only when ready_for_packaging is derived true
```
