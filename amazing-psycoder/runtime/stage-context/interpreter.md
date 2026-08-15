# PsyCoder Studio Interpreter Contract

This compact contract is mandatory Amazing PsyCoder context for the Studio
Interpreter. The machine-readable `runtime/` schemas and deterministic host
validators are the enforcement boundary.

## Authority

- Input is a validated Generation Envelope 4.0 with `jobSchemaVersion=2.0`,
  the exact frozen `ExperimentModel@4.0`, its canonical `modelHash`, and the
  exact frozen asset manifest plus `assetSetHash`.
- `ExperimentModel@4.0` is the only experiment fact. Canvas views, preview
  descriptors, source units, compilation manifests, traces, skill examples,
  paradigm names, and conversation history are never semantic authority.
- Missing semantics stay missing and block formal generation. Never invent a
  condition table, column, stimulus, response key, feedback string, field,
  timing rule, or platform behavior.

## Allowed output

- Return interpreter annotations only, bound to both supplied hashes.
- Every annotation identifies a real Model JSON Pointer and uses
  `source="frozen_model"`.
- Explain represented semantics and explicit unsupported declarations. Do not
  return commands, replacement Model, generated code, readiness, or inferred
  semantics.
- If exact meaning is absent, omit the claim or report a warning. A compiler
  defect must be reported as a system defect, not reclassified as user error.

## Evidence boundary

Interpretation is descriptive evidence. The deterministic adapters still
compile the same frozen Model directly, and the independent Reviewer audits
the exact content-addressed output.
