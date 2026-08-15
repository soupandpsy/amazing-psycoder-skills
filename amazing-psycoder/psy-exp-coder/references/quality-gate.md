# Post-Generation Quality Gate

This gate applies to PsyCoder Studio Model@4 generation and to standalone
experiment-code work. It preserves the scientific reliability principles of
Amazing PsyCoder without forcing every paradigm into one cargo-cult source
template.

## Authority and evidence

1. In Studio mode, the frozen `ExperimentModel@4`, `modelHash`, and
   `assetSetHash` are the only experiment-semantic authority.
2. The deterministic compiler produces the reference runtime, window and
   sequence units, source map, compilation manifest, and conformance trace.
3. AI interpretation, runtime inspection, review, and repair proposals are
   evidence-producing stages. They cannot change the frozen Model or
   compiler-owned evidence files.
4. Runtime entry files are compiler-hash-bound. Until an independent executable
   trace proves semantic equivalence, an AI replacement must be byte-identical
   to the compiler-bound semantic source.
5. A changed semantic source without independently verified trace equivalence
   fails closed. A reviewer assertion is not sufficient evidence.

## Deterministic gate

The deterministic gate must verify all of the following before packaging:

- Model schema, revision, canonical hash, asset-set hash, and target platform.
- Real condition-table columns and real project assets; no invented bindings.
- Every manifest source unit exists and matches its declared output hash.
- Every generated unit maps back to valid Model JSON Pointers.
- Flow, timing, response keys, continue keys, correct-answer sources, data
  writes, resource references, and advanced logic match the frozen Model.
- Platform syntax and static validation pass.
- TypeScript and Python conformance traces agree for the same Model fixture.
- No default stimuli, feedback, condition tables, response keys, implicit ITI,
  or compatibility values were introduced.

## Scientific runtime gate

Review the generated runtime for the properties that syntax alone cannot prove:

- Abort and cleanup remain reachable in every active phase.
- RT uses the declared onset and the target platform's event timestamp.
- When a key is both a response and continue key, the response is recorded
  before the window ends.
- Completed trials are persisted incrementally outside timing-critical regions.
- Images, fonts, audio, and other declared resources are resolved and preloaded
  before use.
- The shared display contract and coordinate transform are applied consistently.
- Randomization is reproducible when a fixed-random order is requested.
- Only Model-declared condition and data fields appear in the runtime.
- In `incremental_trial` mode, no two windows in one sequence may write the
  same response, RT, accuracy, or onset output field, and a single
  `window_id` field cannot represent a multi-window sequence. Such drafts may
  remain editable in Studio, but formal generation must fail closed until the
  user selects `incremental_window` or leaves one explicit writer.

Do not require rigid section counts, function names, comment headers, trial
templates, or paradigm-specific boilerplate. A blank Model window compiles to a
blank scene; an unconfigured feature compiles to no feature.

## AI review and repair

- Interpreter, coder, reviewer, and repair stages must report the exact
  `modelHash` and `assetSetHash` they received.
- Unresolved Critical or Major findings block delivery.
- Repair is limited to the explicit artifact allowlist and a maximum of three
  rounds.
- A changed-source repair is restricted to the target runtime kernel. The
  Model-derived window, sequence, entrypoint, condition, resource, and
  data-contract shell remains byte-identical.
- Repair profile 1.0 preserves every executable reference statement byte for
  byte and in order. It permits only host-recognized additive fail-closed guard
  blocks at their declared reference statements, or standalone comments;
  deletion, replacement, reordering, relocation, or arbitrary new execution is
  rejected.
- The host then verifies syntax, Model/asset bindings, regenerated output
  hashes, deterministic diagnostics, and a fresh independent review.
  Recomputing hashes alone never makes a candidate acceptable.
- Every repair records the issue identifiers, before/after file hashes, and the
  reviewer decision that requested it.
- After every repair, rerun deterministic validation and an independent review.
- If round three still fails, the generation run fails and retains diagnostics;
  it must not publish a successful artifact.

## Final readiness

Passing static, semantic-hash, and review gates makes an artifact eligible for
target-machine testing. It does not by itself establish collection readiness.
PsychoPy and Psychtoolbox still require target-machine smoke evidence for timing,
input, display, fonts, and hardware. jsPsych requires a complete browser run and
deployment-environment evidence.
