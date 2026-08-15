# PsyCoder Studio Compatibility

This skill set defines the professional context and integration contract for
PsyCoder Studio. The machine-readable `runtime/` directory is authoritative for
deployment capability profiles, schemas, artifact contracts, and evidence
boundaries. Prose cannot expand those profiles, and repository validation does not prove
that a live Worker or target laboratory machine is correct.

## Pipeline integration

```text
Editable ExperimentModel@4
  -> confirmed atomic Model transaction
  -> frozen Generation Envelope 4.0
     (jobSchemaVersion 2.0, modelHash, assetSetHash)
  -> deterministic direct compiler for the selected platform
  -> required AI interpretation and compiler-runtime inspection
  -> frozen-shell, additive fail-closed repair proof, deterministic validation and conformance gates
  -> independent read-only review
  -> at most three allowlisted runtime-kernel repair proposals, each fully revalidated and rereviewed
  -> package for target-machine smoke testing
  -> backend-derived collection readiness from structured RuntimeEvidence
```

`ExperimentModel@4.0` is the only persisted, editable, transmittable semantic
authority. The Canvas, jsPsych static/dynamic previews, window source, sequence
source, complete source, compilation manifest, source map, conformance trace,
and generated archive are derived evidence. They must never become a second
experiment fact or write semantics back into the Model.

The Generation Envelope 4.0 contains exactly the frozen Model, canonical model
hash, exact asset manifest and asset-set hash, target, compiler version, export
request, and validation summary. It contains no ExecutionPlan, compiled spec,
IR, duplicated experiment parameters, or template-derived defaults.

## Direct compilation and preview boundary

PsychoPy, jsPsych, and Psychtoolbox adapters directly consume the same frozen
Model. A compiler may build temporary typed objects inside one function, but
may not persist, transfer, expose for editing, or package them as experiment
semantics. Each adapter emits window fragments, sequence units, a complete
experiment unit, a compilation manifest, and a source map back to Model JSON
Pointers.

The browser uses jsPsych for shared static and interactive preview. Preview can
check scene content, order, reference-space position and size, bindings,
nominal timing, keys, and feedback transitions. It does not establish native
PsychoPy/Psychtoolbox frame timing, display refresh, input latency, codecs,
font metrics, or target-hardware readiness.

## Agent transactions

Direct user edits and Psycoder edits both become the same atomic Model
transaction. Every Agent command includes the base Model revision, frozen
scope, exact Model pointers, before/after summary, destructive flag, and
confirmation level. A changed revision rejects the proposal and requires a
reread or explicit rebase.

A selected window restricts changes to that window and explicit dependencies;
a selected sequence restricts changes to that sequence, its windows, and
explicit dependencies. No selection means whole-experiment scope, but Psycoder
must first confirm the experiment logic before proposing changes. Destructive
edits, scope expansion, table creation/import, and shared-dependency changes
require explicit confirmation. Any failure rolls back the entire transaction.

The Agent may inspect derived window, sequence, and complete source through the
source map. Semantic changes must return to the Model. A compiler defect enters
the system-fix path; the Agent cannot quietly edit generated source into a new
experiment fact.

The Worker does not treat an allowlist or newly computed hash as proof that
arbitrary AI-authored runtime preserves Model semantics. Model-derived window,
sequence, entrypoint, condition, resource, and data-contract source remains
frozen. Under repair profile 1.0, every executable reference statement in the
target runtime kernel must remain byte-identical and in the same order. Changed
AI runtime may add only host-recognized, position-bound fail-closed guard blocks
at their declared reference statements, or standalone comments; it cannot
delete, replace, reorder, relocate, or insert arbitrary executable behavior. The
host then reruns syntax and deterministic validation, rebinds evidence, and
requires an independent rereview.

## No silent experiment content

Neither skills nor compilers may create missing scientific content. In
particular, they must not silently add condition tables, columns, stimuli,
images, feedback text, response keys, correctness rules, repetitions, ITIs,
data fields, or English placeholder strings. An unbound fixed-content sequence
is valid. A condition binding must reference a real column in the sequence's
actual condition table. Unsupported advanced logic remains explicit and blocks
formal generation rather than being guessed or discarded.

## Generation, review, and repair

The primary Coder may replace only exact allowlisted runtime paths. The host
preserves the frozen shell and executable runtime baseline, verifies
model/asset hashes, checks the source
map and conformance trace, runs platform static and mock tests, hashes the
artifact set, and invokes an independent Reviewer. Reviewer never returns rewritten files.
It returns primitive hash-bound findings only.

Blocking implementation findings may enter at most three separate Coder repair
rounds. A repair cannot mutate the Model, asset manifest, conditions,
compilation metadata, source map, conformance evidence, or readiness evidence.
Every replacement is revalidated, rehashed, and independently rereviewed. A
run that still fails after three rounds fails closed and never produces a
successful downloadable build.

## Artifact and evidence contract

New packages contain:

```text
experiment_model.json
compilation_manifest.json
source_map.json
target runtime and window/sequence source units
resources
README.md
_pipeline/ AI interpretation, review, repair, and validation evidence
```

They do not contain `execution_plan.json`, `experiment_ir.json`, `window_ir`,
or `sequence_ir`. Historical packages remain downloadable archives and are not
reinterpreted by the new runtime.

The backend derives `ready_for_packaging` and `ready_for_collection`; no model
may self-certify them. Static success only permits packaging for target tests.
Collection additionally requires structured, hash-bound target-machine
RuntimeEvidence. A browser/user submission is `user_attested`; only an
authorized machine or reviewer workflow closes the collection gate.

The Worker must run `scripts/validate_studio_runtime.py` (or an exact port) at
every record boundary. Model and asset-set hashes use canonical UTF-8 JSON with
sorted keys, no insignificant whitespace, `ensure_ascii=false`, and no NaN or
Infinity before SHA-256.

## Skill responsibility vs pipeline responsibility

| Layer | Responsibility |
| --- | --- |
| Skill | Scientific and platform guidance, anti-patterns, quality gates, review knowledge, evidence limits |
| Pipeline | Model schema and scope enforcement, canonical hashes, direct compilation, source mapping, conformance, repair allowlists, packaging, task state, and readiness derivation |

Amazing PsyCoder is revisable professional guidance, not infallible authority.
If maintained guidance conflicts with the confirmed Model or reproducible
evidence, update and validate this source repository before synchronizing a
PsyCoder Studio Worker bundle.

## Version

v1.4.0 — Generation Envelope 4.0 and direct ExperimentModel@4 contract;
`jobSchemaVersion` 2.0, 2026-08-15.
