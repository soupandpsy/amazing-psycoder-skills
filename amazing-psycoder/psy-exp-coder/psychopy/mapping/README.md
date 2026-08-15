# ExperimentModel 4.0 to PsychoPy mapping

This document maps the frozen PsyCoder Studio `ExperimentModel@4.0` directly
to the pinned PsychoPy runtime. The Model and exact asset manifest are the only
semantic inputs. No plan, IR, preset task, default condition table, response
key, feedback text, data field, or hidden template may supply behavior.

## Input authority

- `presentation.display` defines the shared 1280x720 reference space,
  `contain` scale, center-pixel/Y-up coordinates, background, and font policy.
- `presentation.windows[]` defines each ordered text/image scene, timing,
  response, correctness, and recording behavior.
- `sequences[]` defines top-to-bottom execution, left-to-right window order,
  repetitions, ordering policy, and an optional real `conditionTableId`.
- `conditionTables[]` contains only user-imported or explicitly
  agent-confirmed rows and columns.
- `assets[]`, `dataContract`, `runtime`, and verified `advancedLogic`
  are explicit dependencies.

Every binding is resolved and validated before code emission. A fixed-content
sequence needs no condition table.

## Display and scene mapping

Use PsychoPy pixel units. For target client size `W x H`:

```text
scale = min(W / 1280, H / 720)
offsetX = (W - 1280 * scale) / 2
offsetY = (H - 720 * scale) / 2
```

The model origin already matches PsychoPy's centered Y-up pixel convention.
Scale every reference position and dimension uniformly. Leave unused margins
in the Model background color. Do not stretch.

- `scene.elements: []` draws only the cleared background.
- A text element maps to one precreated `visual.TextStim`; resolve its content
  and color binding from the current row or response state.
- An image element maps to a preloaded `visual.ImageStim`; its source must be
  an existing model asset or real asset-path column.
- Element `order` is draw order. Convert the declared anchor without changing
  geometry.
- Font metrics are strictly comparable only when the same font asset is bound;
  otherwise retain the explicit target-machine warning.

Create and load stimuli before timed loops when practical. Never perform disk
I/O in the measured presentation path.

## Timing and response mapping

| Model semantics | PsychoPy behavior |
| --- | --- |
| `fixed` | flip once, use a non-blocking frame loop until `durationMs` |
| `condition_column` | validate the real row value as milliseconds, then use the fixed loop |
| `manual_continue` | poll the explicit `continueKeys`; no inferred key |
| `until_response` | poll explicit `allowedKeys` until a response ends the window |
| response enabled + `responseEndsWindow=false` | record the first allowed response without shortening fixed timing |
| response enabled + `responseEndsWindow=true` | record first allowed response and end according to the declared mode |

Reset the response clock on the first visible flip for `rtOnset=self`, or use
the explicitly referenced window onset. When a key is both a response and
continue key, record it first, then end the window. Abort handling is separate
from scientific choices and remains reachable on every frame.

Correctness uses only the declared fixed key or the declared real condition
column. Disabled responses have no keys, correctness, RT, or response code.

## Sequence and condition mapping

- Preserve `sequence.order` and `windowIds[]` exactly.
- No `conditionTableId`: execute the window chain once per repetition using an
  in-memory empty row context.
- Bound table: traverse every exact row once per repetition.
- `table_order`: preserve bytes/row order.
- `fixed_random`: resolve and record the declared seed, then reproduce the
  same permutation.
- `fully_random`: realize and record each permutation according to Model
  semantics.
- An unresolved table, column, asset, invalid duration, or unsupported advanced
  logic blocks generation.

An ITI is an explicit blank window. Never synthesize a global ITI.

## Source units and project structure

Window units contain only that window's draw, timing, response, and data
fragment. Sequence units compose window units and own row/repetition order.
The complete entry point owns imports, participant input, the single PsychoPy
window, preload, data output, sequence assembly, and cleanup exactly once.

Emit a compilation manifest and source map back to Model JSON Pointers. The
test-only conformance trace must cover scene elements, transformed coordinates,
timing, keys, correctness, condition row, data writes, resources, and advanced
logic.

## Fail closed

Reject missing references, unsupported element kinds, unbound columns, missing
assets/fonts required for strict metrics, invalid termination, semantic drift,
or trace mismatch. Never replace a rejected design with an example experiment,
placeholder, old adapter, or best-effort default.
