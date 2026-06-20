# PsyCoder Studio Compatibility

This skill set is the designated **professional context source** for PsyCoder Studio's three-stage AI generation pipeline. PsyCoder Studio uses a Skill Reference Engine to route relevant skill documents into each pipeline stage.

## Pipeline Integration

```
Worker receives generation job
  │
  ├─ Stage 1: AI Experiment Interpreter
  │   Skill source: psy-exp-designer
  │   Input:  CanvasState + Module Settings + Natural Language Notes
  │   Output: ExperimentSpec + human-readable description + assumptions/warnings/conflicts
  │   Contract: The spec must be complete enough for platform code generation
  │
  ├─ Stage 2: AI Platform Code Generator
  │   Skill source: psy-exp-coder
  │   Input:  ExperimentSpec + targetPlatform + paradigm
  │   Output: GeneratedFilesOutput (main.py, conditions.csv, README.md, audit_report.md, experiment_config.json)
  │   Contract: All platform-specific API patterns from spec/README.md Canonical Skeleton
  │              All 9 quality-gate checks applied before delivering files
  │
  ├─ Stage 3: AI Code Reviewer / Repair
  │   Skill source: psy-exp-reviewer
  │   Input:  ExperimentSpec + GeneratedFilesOutput + targetPlatform
  │   Output: ReviewReport (issues_before_repair, repairs_applied, issues_after_repair, reviewed_files)
  │   Contract: issues_before_repair and issues_after_repair MUST be separated
  │              reviewed_files MUST be the complete final repaired files
  │              repair_notes do NOT prove resolution
  │
  ├─ Stage 4: Local Validator (hard-rule gate)
  │   NOT a skill stage — pure code enforcement
  │   Checks: required files exist, non-empty, no path traversal, valid zip
  │   Review Gate: if unresolved_critical > 0 → BLOCK packaging
  │                if unresolved_major > 0 → BLOCK packaging (MVP rule)
  │                if ready_for_packaging=false → BLOCK packaging
  │
  └─ Stage 5: Artifact Packager
      Generates: project.zip with all files + _pipeline/ metadata
```

## Skill Responsibility vs. Pipeline Responsibility

| Layer | Responsibility |
|-------|---------------|
| **Skill** | Professional standards: API patterns, anti-patterns, quality gates, paradigm logic, data recording rules, platform-specific correctness |
| **Pipeline** | Hard gates: file existence, path safety, review gate enforcement, zip packaging, status tracking, Redis communication |

Skills define **what is correct**. Pipeline enforces **what is blocked**.

## Stage-Aware Skill Routing

The Skill Reference Engine in PsyCoder Studio routes documents by:

- `stage`: interpreter | code_generator | reviewer
- `platform`: psychopy | jspsych | psychtoolbox
- `paradigm`: stroop | flanker | gonogo | nback | ...

Token budgets per stage: Interpreter 3K, Code Generator 6K, Reviewer 4K.

## Review Gate Semantics

The psy-exp-reviewer defines readiness standards. PsyCoder Studio enforces them as packaging gates:

- `ready_for_collection`: zero critical AND zero major → can proceed to packaging
- `not_ready_for_collection`: critical or major exist → MUST block packaging
- `ready_for_packaging`: pipeline-level gate derived from `ready_for_collection`
- `unresolved_critical_count > 0`: `ready_for_packaging = false`

## Version

v1.4 — PsyCoder Studio-compatible, 2026-06-21.
