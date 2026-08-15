# ExperimentModel 4.0 to Psychtoolbox mapping

This document maps the frozen PsyCoder Studio `ExperimentModel@4.0` directly
to pinned MATLAB and Psychtoolbox. Only the Model and exact asset manifest may
affect the generated task. There is no plan, IR, preset experiment, default
condition table, paradigm-selected template, key, feedback, or data field.

## Input authority

Use `presentation.display`, `presentation.windows[]`, `sequences[]`,
optional `conditionTables[]`, `assets[]`, `dataContract`, `runtime`, and
verified `advancedLogic` exactly as frozen. Every ID, binding, column, asset,
and supported target behavior is validated before source emission.

## Display and scene mapping

Open one Psychtoolbox window and compute:

```text
scale = min(W / 1280, H / 720)
offsetX = (W - 1280 * scale) / 2
offsetY = (H - 720 * scale) / 2
```

Model coordinates are center-pixel/Y-up. Convert them to Psychtoolbox's screen
pixel coordinates by applying the uniform scale, adding the centered viewport
origin, and inverting Y. Preserve the declared anchor. Fill margins/background
with the Model color; never stretch.

- Empty scenes clear and flip only.
- Text elements draw declared content/color/font size in element order.
- Image elements use preloaded textures from exact assets or real asset-path
  columns.
- Resource creation occurs outside measured presentation loops and is released
  during guaranteed cleanup.
- Strict font metrics require the same bound font asset; otherwise keep the
  target-machine warning.

## Timing and response mapping

Use flip timestamps and non-blocking queue/polling loops.

| Model semantics | Psychtoolbox behavior |
| --- | --- |
| `fixed` | flip once; draw/poll until the absolute deadline |
| `condition_column` | validate the real row milliseconds before the loop |
| `manual_continue` | poll only explicit continue/response keys and apply declared end rules |
| `until_response` | explicit allowed response ends the window |
| `responseEndsWindow=false` | record first allowed key without shortening fixed timing |

A shared response/continue key is recorded first, then ends the window. RT is
anchored to the declared visible flip or explicit referenced onset. Abort is
separate and reachable. Do not use blocking waits or `KbCheck` as an RT
measurement implementation.

Correctness reads only a declared fixed key or real table column. Disabled
response behavior emits no keys, correctness, RT, or response functions.

## Sequence and condition mapping

Preserve sequence/window order. An unbound sequence runs once per repetition
with an in-memory empty row context. A bound sequence traverses exact rows.
Implement `table_order`, declared-seed `fixed_random`, and recorded
`fully_random` directly. An ITI is an explicit blank window.

Never synthesize MATLAB tables or conventional field names. Missing table
references, columns, assets, durations, or unsupported advanced logic block
formal generation.

Condition rows, participant values, in-progress records, and checkpoint rows
must use key-preserving containers rather than MATLAB struct fields. This keeps
the user's exact imported headers, including Unicode and spaces, through the
runtime and final table. The primary function name must match its emitted
`main.m` filename.

## Source units and project structure

Window units contain only the relevant draw/input/data fragment. Sequence units
compose windows and own table/repetition ordering. The complete MATLAB entry
point owns environment validation, `PsychDefaultSetup`, key unification,
display setup, cleanup protection, preload, participant data, sequence
assembly, incremental checkpointing, and final close once.

Emit a compilation manifest, Model-pointer source map, and test-only
conformance trace. MATLAB `checkcode`, mock trace, and target
MATLAB/Psychtoolbox smoke evidence are all required; static inspection cannot
establish collection readiness.

## Fail closed

Reject unresolved references, missing fields/assets, invalid termination,
unsupported interactions or hardware requirements, semantic drift, or trace
mismatch. Never replace a rejected design with example Stroop/Posner code, an
old template, or hidden defaults.
