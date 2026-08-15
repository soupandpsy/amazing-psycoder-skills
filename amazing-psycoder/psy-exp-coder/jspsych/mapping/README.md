# ExperimentModel 4.0 to jsPsych mapping

This document maps the frozen PsyCoder Studio `ExperimentModel@4.0` directly
to pinned jsPsych 8. The same scene resolver serves static Canvas rendering and
real interactive sequence preview; preview output never becomes experiment
authority.

## Input authority

The exact frozen Model and asset manifest define display, windows, sequences,
optional condition tables, responses, data, resources, and verified advanced
logic. No plan, IR, paradigm label, default table, conventional column, key,
feedback string, or placeholder may add semantics.

## Shared descriptor

`buildJsPsychWindowDescriptor` is a pure function of Model, sequence ID,
window ID, current condition row, and response state. It resolves:

- ordered text/image scene elements;
- literal, real condition-column, and explicit response-feedback bindings;
- reference-space geometry and anchors;
- timing, continue keys, response keys, correctness, and data flags;
- required assets and validation diagnostics.

It returns plugin parameters plus a pure visual representation. It does not
start jsPsych, install a timer/listener, or write state.

## Display and scene mapping

Render an absolute 1280x720 internal stage, then apply one `contain` transform
into the available target rectangle:

```text
scale = min(W / 1280, H / 720)
offsetX = (W - 1280 * scale) / 2
offsetY = (H - 720 * scale) / 2
```

Convert Model Y-up to DOM Y-down while preserving anchors and uniform scale.
Use absolute CSS/Canvas pixels. An empty element list renders only the declared
background. Static cards use ordinary React/DOM nodes and never create a
jsPsych instance.

Text is escaped and image URLs resolve only from the frozen asset set or a real
asset-path column. Preload dynamic-preview images before running. Strict font
metrics require the same bound font file; otherwise retain the target-machine
warning.

## Dynamic timeline and timing

The sequence preview dynamically imports jsPsych and required plugins, creates
one isolated instance, and runs only the selected condition row's single
window chain. It does not execute the whole table or formal repetitions.

| Model semantics | jsPsych behavior |
| --- | --- |
| `fixed` | explicit `trial_duration`; response does not shorten it unless `responseEndsWindow=true` |
| `condition_column` | validated row milliseconds become `trial_duration` |
| `manual_continue` | choices are the union of continue and response keys; only continue or explicit response-end closes |
| `until_response` | explicit response choices end the trial |
| disabled response | no scientific response choices or correctness code |

When one key is both response and continue, record it before ending. Opening the
dialog focuses its target. Restart, condition-row change, close, and abort must
terminate the old jsPsych instance and remove every timer and listener.

Preview data remains in memory and is never appended to formal experiment data.

## Sequence and condition mapping

- Preserve sequence and window order exactly.
- Unbound sequences use one in-memory empty row context; they do not create a
  condition table.
- Bound sequences use only the exact declared table rows and real columns.
- `repetitions` means whole-table traversal count.
- `table_order`, `fixed_random`, and `fully_random` implement the declared
  order and record seed/realized order where applicable.
- An ITI is an explicit blank window.

## Source units and full runtime

Window units are timeline-node fragments with no `initJsPsych`, imports, or
global exit. Sequence units compose nodes and row/repetition policy. The
complete experiment owns pinned dependencies, one `initJsPsych`, preload,
participant input, timeline assembly, incremental checkpointing, export, and
abort/cleanup once.

Emit compilation manifest, Model-pointer source map, and a test-only
conformance trace. Playwright must exercise the complete runtime; static syntax
alone is insufficient.

## Fail closed

Reject unresolved tables, columns, assets, timing, keys, feedback state,
advanced logic, plugin support, focus/cleanup defects, semantic drift, or trace
mismatch. Never substitute a sample timeline, hidden default, or legacy API.
