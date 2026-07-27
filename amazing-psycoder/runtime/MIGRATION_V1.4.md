# PsyCoder Studio v1.4.0 Migration

This is the website integration checklist for the unified Amazing PsyCoder
v1.4.0 contract. It is intentionally fail-closed: do not silently coerce an
older payload into the new generation path.

## Contract Matrix

| Boundary | Input | Output | Authority |
|---|---|---|---|
| Design Assistant | editable project state | `designer-output` commands | Backend applies commands while project is unlocked |
| Compiler | confirmed `PsyCoderExperimentSpecV2@2.4` | `ExecutionPlan@2.0` + canonical SHA-256 | Deterministic backend |
| Spec Interpreter | immutable Generation Envelope 2.0 | `interpreter-output` annotations | Read-only model |
| Platform Coder | envelope + plan hash | `artifact-output` | Model-owned allowlisted entry files only |
| Reviewer | plan + content-addressed artifact set | `review-output` | Read-only findings and hashes |
| Repair Controller | review issue IDs | `repair-attempt` | Coder, maximum two attempts |
| Runtime workflow | packaged artifact on target machine | `runtime-evidence` | Operator/test runner plus inspected evidence |
| Readiness Deriver | review + artifact gates + runtime evidence | `readiness-snapshot` | Deterministic backend only |

## Required Website Changes

### Frontend

1. Keep Design Assistant commands available only before confirmation/lock.
2. Display the proposed response event and RT anchor in research language and
   require explicit confirmation; store rationale and confirmation state.
3. On generation, show the immutable plan hash and artifact-set hash in the
   technical details panel.
4. Present separate states:
   - design confirmed;
   - static review passed / package available for smoke testing;
   - runtime evidence missing, failed, or blocked;
   - ready for collection.
5. Render issue counts from `review-output.issues`; never read model-supplied
   count/readiness fields.
6. Treat repaired output as a new artifact set and show its new review ID.

### Compiler and Generation API

1. Compile only confirmed specs to `ExecutionPlan@2.0`; use `sequences` and
   `windowIds`, not the retired `blocks` execution shape.
2. Reject duplicate IDs/orders, unreachable window references, unresolved RT
   anchors, target mismatch, and validation summaries with `valid != true` or
   `errorCount != 0`.
3. Canonicalize the plan exactly as documented in `PSYCODER_STUDIO.md`, compute
   SHA-256, and include `executionPlanHash` in every downstream request/record.
4. Validate every model response against its JSON Schema and
   `scripts/validate_studio_runtime.py` before persisting or applying it.
5. Merge model files with compiler-owned conditions, plan, config, README, and
   metadata only after platform allowlist and ownership checks pass.

### Reviewer and Repair Worker

1. Remove legacy fields such as `repairs_applied`, `issues_before_repair`,
   `issues_after_repair`, `unresolved_*`, and readiness booleans from Reviewer
   prompts, DTOs, and database writes.
2. Give the Reviewer immutable file bytes but accept only file hashes and
   findings in its response.
3. Invoke the Coder—not the Reviewer—for a repair. Bind each attempt to the
   source review ID, exact issue IDs, prior artifact hash, plan hash, platform,
   and attempt number.
4. Reject repairs to compiler-owned paths or `_pipeline/`; revalidate, hash,
   and re-review every accepted repair. Stop after attempt 2.

### Runtime Evidence and Readiness

1. Store runtime evidence independently from review output and bind it to the
   exact artifact-set hash.
2. Require `launch_exit`, `full_short_session`, `data_integrity`, and
   `incremental_recovery`; add `timing_device_check` when the design makes
   hardware/timing claims.
3. Derive `smoke_test_status`, packaging state, and collection readiness in one
   backend service. Do not accept these values from any model.
4. Render `audit_report.md` from the structured review/evidence records during
   packaging; the Reviewer does not write package files.

## Suggested Persistence Keys

Use immutable records or append-only versions for:

- `execution_plan_hash`
- `artifact_set_hash`
- `review_id`
- `source_review_id`
- `repair_attempt`
- `runtime_evidence_id`
- `readiness_snapshot_id`
- `contract_version = 1.4.0`

Never update an old review to “resolved.” Link the new artifact set and review
to their predecessors so the complete evidence chain remains auditable.

## Rollout

1. Deploy readers that understand both the legacy record and v1.4.0, but write
   only v1.4.0 for new jobs.
2. Add a deterministic migration compiler for saved editable projects.
3. Require user reconfirmation if migration changes or cannot prove the RT
   measurement contract, response mapping, order, conditions, or output rules.
4. Do not migrate an in-progress generation job in place; finish it under its
   original contract or restart from a freshly confirmed snapshot.
5. Remove legacy writes only after telemetry shows no active legacy jobs.

## Release Gate

Run:

```bash
python3 amazing-psycoder/scripts/validate_skills.py
python3 -m unittest discover -s amazing-psycoder/tests -v
python3 -m compileall -q amazing-psycoder/scripts amazing-psycoder/tests
```

Then exercise one valid and one deliberately invalid record for every runtime
schema, verify the two-attempt repair boundary, package a smoke-test candidate,
attach target evidence, and confirm that only the backend can produce a
collection-ready snapshot.
