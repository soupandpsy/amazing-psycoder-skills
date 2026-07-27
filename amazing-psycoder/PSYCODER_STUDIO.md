# PsyCoder Studio Compatibility

This skill set defines the **professional context and integration contract** for PsyCoder Studio's AI generation pipeline. The machine-readable `runtime/` directory is authoritative for the capability profiles, schemas, and artifact contracts that a deployment may advertise. Prose cannot expand those profiles. The presence of these files does not prove that a website Worker, generator, reviewer, or packager is deployed or has passed end-to-end integration testing.

## Pipeline Integration

```text
Unlocked project
  └─ Design Assistant (pre-generation UI)
     Input: editable project state
     Output: designer-output commands applied by the backend
     Gate: user confirmation + deterministic compilation/validation

Worker receives an immutable Generation Envelope 2.0
  │
  ├─ Stage 1: Spec Interpreter
  │   Skill source: psy-exp-designer
  │   Input: immutable PsyCoderExperimentSpecV2@2.4 + ExecutionPlan@2.0 + plan hash
  │   Output: interpreter-output annotations tied to the same plan hash
  │   Contract: no commands, mutations, inferred runtime semantics, or replacement plan
  │
  ├─ Stage 2: AI Platform Coder + Deterministic Contract Baseline
  │   Skill source: psy-exp-coder
  │   Input: validated envelope + immutable ExecutionPlan
  │   Output: model-owned allowlisted files only; compiler-owned files are merged later
  │   Contract: every response echoes the plan hash; the Coder cannot change the
  │             ExecutionPlan, conditions, config, file ownership, or order
  │
  ├─ Stage 3: Read-only Reviewer
  │   Skill source: psy-exp-reviewer
  │   Input: immutable plan + content-addressed artifact set + target platform
  │   Output: primitive findings and reviewed file hashes only
  │   Contract: no rewritten files, repairs, issue counts, or readiness claims
  │
  ├─ Stage 3b: Constrained Coder Repair (only when blocking findings exist)
  │   Input: review ID + exact issue IDs + previous artifact hash + plan hash
  │   Output: model-owned allowlisted replacements under repair-attempt schema
  │   Contract: backend revalidates and re-reviews; maximum two attempts
  │
  ├─ Stage 4: Deterministic Validator and Readiness Deriver
  │   NOT a skill stage — pure code enforcement
  │   Checks: schema validity, hashes, file ownership, required files, safe paths,
  │           archive validity, issue severity counts, and structured RuntimeEvidence
  │   Output: backend-owned readiness-snapshot; models never self-certify readiness
  │
  └─ Stage 5: Artifact Packager
      Generates: project.zip with all files + immutable _pipeline/ metadata;
                 renders audit_report.md from the structured review record
```

This repository declares and validates three parallel capability-based profiles:
`psychopy-generated-text-v1`, `jspsych-generated-text-v1`, and
`psychtoolbox-generated-text-v1`. It also retains the optimized exact
`psychopy-color-word-stroop-v1` profile. The generic profiles accept custom
experiments only when their complete saved semantics fit the generated-text
contract in `runtime/capabilities.json`; platform or paradigm labels do not
expand that contract. Semantic, emotional, numerical, bilingual, and custom
Stroop-family experiments therefore need their own confirmed factors, windows,
correctness, timing, and data rules rather than inheriting classic Stroop logic.
A Studio deployment may advertise one of these profiles only after it loads the
matching contracts, passes Studio-side integration tests, and records the
required target-runtime evidence. Repository validation alone is not live
deployment evidence.

All generic profiles currently require generated factorial trial sources,
text/blank windows, one scored response window per trial, `rtOnset=self`, and
explicit condition-to-correct-key semantics. The shared canonical key set is a
single lowercase alphanumeric key plus `space` and `enter`; text color fields
must materialize to black, white, red, green, blue, yellow, gray, or grey.
An implementation conforming to this contract must reject unsupported media,
imports, timing, fields, keys, colors, or response mappings before creating a
run. Psychtoolbox remains static-verified until a
MATLAB/Psychtoolbox target-machine smoke test is attached. This deployment
boundary does not block standalone candidate generation; see `STANDALONE.md`.

## Skill Responsibility vs. Pipeline Responsibility

| Layer | Responsibility |
|-------|---------------|
| **Skill** | Professional standards: experiment semantics, API patterns, anti-patterns, quality gates, reference knowledge, data recording rules, platform-specific correctness |
| **Pipeline** | Immutable-plan enforcement, protected artifact ownership, runtime path allowlist, static/review gates, zip packaging, status tracking, Redis communication |

Skills define **the current contracts, checks, and evidence limits**. The pipeline enforces **which transition is blocked**; neither layer can infer unobserved runtime correctness.

## Stage-Aware Skill Routing

The Skill Reference Engine in PsyCoder Studio routes required documents by:

- `stage`: interpreter | code_generator | reviewer
- `platform`: psychopy | jspsych | psychtoolbox
- optional exact paradigm reference when one exists

Missing paradigm references never invalidate a custom design. They only remove
reference guidance. Required generation context is the canonical v2 snapshot,
compiled ExecutionPlan, platform adapter contract, and artifact contract. The
retired v1 `ExperimentSpec`, `canvas_state`, and `legacySpec` fields are not part
of new Studio jobs or packages.

Context allocation is deployment-owned. This skill contract imposes no fixed
per-stage token ceiling; correctness is enforced by schemas, artifact hashes,
deterministic gates, and bounded repair attempts.

## Review Gate Semantics

The psy-exp-reviewer defines findings; PsyCoder Studio derives separate
static-packaging and runtime-collection states from those findings and the
structured evidence. Counts and booleans are never accepted from a model:

- `static_review_passed`: backend count of current findings has zero critical AND zero major
- `ready_for_collection`: `static_review_passed` AND all required structured target-machine `RuntimeEvidence` records pass; `smoke_test_status` is derived from those records
- `not_ready_for_collection`: critical/major exist, or smoke evidence is missing/failed
- `ready_for_packaging`: derived from static review + complete files; may package a non-collection-ready build for smoke testing
- unresolved critical/major issues: `ready_for_packaging = false`; missing smoke evidence alone does not block a package whose purpose is runtime testing

The canonical machine contracts are listed in `runtime/manifest.json`:
`designer-output` is the only mutation-capable pre-lock contract;
`interpreter-output`, `review-output`, and `runtime-evidence` are immutable
evidence records; `repair-attempt` is Coder-only; and `readiness-snapshot` is
backend-only.

Reviewer never returns rewritten files; only the separately invoked Coder may
return an allowlisted repair attempt.

The Worker should run `scripts/validate_studio_runtime.py` (or an exact port of
its rules) at every record boundary. Execution-plan hashes use UTF-8 JSON with
sorted keys, no insignificant whitespace, `ensure_ascii=false`, and no NaN or
Infinity before SHA-256.

## Version

v1.4.0 — unified Generation Envelope 2.0 and ExecutionPlan 2.0 contract, 2026-07-23.
