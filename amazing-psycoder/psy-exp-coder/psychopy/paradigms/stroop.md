# Classic Color-Word Stroop — PsychoPy Reference

> **Parent**: [psy-exp-coder](../../SKILL.md) · [PsychoPy contract](../spec/README.md)
> **Design reference**: [classic color-word Stroop](../../../psy-exp-designer/paradigms/stroop.md)

## Scope

Use this document only when the confirmed specification describes a classic
color-word Stroop task: the participant classifies ink color while ignoring a
color word. This document is reference evidence, not an executable template.
The confirmed specification remains the only source of timing, response,
condition, randomization, feedback, data, runtime, and output semantics.

Semantic, emotional, bilingual, numerical, picture, spatial, and other
Stroop-family experiments are separate designs. Flanker and Simon are separate
paradigms. Never inherit logic between them because they share an interference
label or historical lineage.

## Required Confirmed Semantics

Before generation, the specification must explicitly define:

- the exact stimulus set and ink-color set;
- the task-relevant dimension and participant instruction;
- the response device, allowed responses, and complete ink-color mapping;
- the condition fields and how every trial resolves its correct response;
- congruent, incongruent, neutral, or other conditions and their requested counts;
- every sequence, window, timing mode, deadline, and RT onset;
- practice/formal structure, feedback policy, randomization, and seed policy;
- required participant, condition, response, timing, accuracy, and system data;
- the pinned PsychoPy/runtime contract and target collection environment.

If any required semantic is missing or conflicting, stop at validation. Do not
fill it from this file.

## Neutral Window Mapping

PsyCoder Studio windows have no role or type. Map each confirmed window by its
capabilities:

| Capability | PsychoPy implementation concern |
| --- | --- |
| `stimulus.displayMode` and content bindings | Construct the matching visual/audio object from the confirmed content or condition field. |
| `timing.mode` and duration | End from the declared clock/deadline rule; do not infer a universal fixation, stimulus, feedback, or ITI duration. |
| `response.enabled` | Initialize the confirmed input device and collect only declared responses. |
| `response.rtOnset` | Reset the response clock on the flip that first presents the declared onset window. |
| `feedback.enabled` | Resolve correct/incorrect/timeout text from the recorded trial result and declared feedback policy. |
| `data.*` | Persist the exact declared fields with stable trial/block indices and timestamps. |
| Builder sequence execution | Preserve top-to-bottom row order, left-to-right window order, and the declared practice/formal/once/between-block execution. |

Names such as `Fixation`, `Instructions`, or `Feedback` are user labels only.
They never select implementation behavior.

## PsychoPy Invariants

1. Generate against the exact pinned PsychoPy version and verified API contract.
2. Create stimulus objects from the declared display mode and bindings; never
   execute condition column names as Python code.
3. Synchronize visual onset and the response clock with the same screen flip.
4. Clear stale input before scored response collection begins.
5. Derive correctness from the confirmed condition field, fixed key, or mapping;
   the ink color is task-relevant only because the specification says so.
6. Record omissions and timeouts distinctly from incorrect responses.
7. Save incrementally according to the output contract and perform durable save
   plus window/device cleanup on normal completion and abort.
8. Keep practice feedback, formal feedback, breaks, and end screens controlled by
   sequence/window settings rather than paradigm defaults.

## Condition Contract

Column names are project-defined. A common classic design may contain fields
equivalent to stimulus text, ink color, condition label, and correct response,
but generation must use the names and mappings present in the confirmed spec.
Validate that:

- every bound field exists in every applicable trial row;
- every ink-color value resolves to one declared response;
- every correct-response value is allowed by the response window;
- requested condition counts and balance constraints are mathematically feasible;
- randomization preserves any declared item, repetition, transition, or block constraints.

## Rejected Legacy Shortcuts

- Do not copy historical PsychoPy Builder exports or their imports/API calls.
- Do not use a bundled fixed key mapping, color list, trial count, or 50/50 ratio.
- Do not assume a merged stimulus-response routine, a 500 ms fixation, a 2 s
  deadline, or practice-only feedback.
- Do not route numerical Stroop, Flanker, or Simon through this reference.
- Do not treat a project/paradigm label as proof that the design is complete.

## Review Checklist

- The exact design matches classic color-word Stroop.
- Every executable behavior is traceable to the confirmed spec.
- Window labels do not drive branches.
- RT onset is synchronized to the declared visible event.
- Condition rows, response mapping, and correctness rules agree.
- Practice/formal feedback behavior is represented by sequence/window settings.
- Generated data is sufficient to reproduce exclusions and the planned Stroop comparison.
- Runtime, dependency, output, abort, and cleanup contracts are explicit.
