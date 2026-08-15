# PsyCoder Studio Compiler-Adapter Contract

This compact contract is mandatory Amazing PsyCoder context for Studio runtime
verification and bounded repair proposals.

## Frozen authority and file ownership

- Implement only the supplied `ExperimentModel@4.0`; preserve its exact
  `modelHash` and `assetSetHash`.
- Never add, remove, reorder, or reinterpret scenes, elements, sequences,
  condition rows, responses, correctness, randomization, timing, data fields,
  resources, or verified advanced logic.
- Compile the Model directly. Function-local typed descriptors are allowed,
  but must not be persisted, transferred, edited, packaged as experiment
  semantics, or used as another authority.
- Write only the exact `allowed_runtime_paths` supplied by the host. Never
  write `_pipeline/`, model, conditions, compilation manifest, source map,
  evidence, or assets.
- The deterministic compiler owns the reference runtime. AI may inspect it and
  may return a candidate complete-file replacement only through the exact
  runtime-path allowlist.
- The current Studio host does not execute an independent semantic trace over
  arbitrary AI-authored Python, JavaScript, or MATLAB. Therefore a successful
  package may accept an AI generation or repair candidate only when every
  runtime byte is identical to the compiler reference. The host must reject,
  rather than re-hash, any changed runtime source.
- An allowlisted change may be enabled in a future host only after a separate,
  sandboxed executable conformance extractor proves equivalence for that exact
  target artifact. Reviewer prose or a Model-derived trace is not such proof.
- Never make a test pass by changing any Model semantics.

## Cross-platform scientific red lines

- No blocking sleep or blocking keyboard wait in a timed experiment loop.
- A response window has an explicit RT origin tied to the declared visible
  event.
- Escape/abort remains reachable in every interactive or timed phase.
- Completed trials are checkpointed incrementally; data is never saved only at
  experiment end.
- Correctness follows the declared fixed key or real condition-table column.
- Participant-visible CJK requires an explicit font strategy; strict metrics
  require a bound font asset.
- Apply the shared 1280x720 `contain` transform with center-pixel, Y-up model
  coordinates; do not stretch or silently change layout.

## Compiler evidence

- Emit window fragments, sequence units, and one complete experiment unit that
  map directly to Model JSON Pointers.
- Emit a `CompilationManifest`, source map, and test-only conformance trace for
  scene elements, coordinates, timing, keys, correctness, conditions, data,
  resources, and advanced logic.
- Do not claim collection readiness. That requires separately validated
  target-machine RuntimeEvidence bound to the final artifact-set hash.
