# Stroop — jsPsych 8.x

> **Parent**: [psy-exp-coder](../../SKILL.md) · [Platform Spec](../spec/README.md)
> **Config reference**: [Stroop design](../../../psy-exp-designer/paradigms/stroop.md)

## Exact Design Boundary

This reference covers only a classic color-word Stroop design in which the
participant classifies ink color. It does not define semantic, emotional,
numerical, bilingual, or other Stroop-family experiments. Those designs require
their own confirmed stimuli, conditions, correctness rules, timing, and data
semantics.

## Candidate Design Pattern

Render the color word and collect the color-classification key in the same
keyboard-response trial. The text comes from the configured word field; the CSS
color comes from the ink-color field. Correctness is determined from the
explicit confirmed mapping for ink color, never from word meaning or key order.

The response trial's RT onset is its own browser presentation onset (`self`).
Use the plugin's recorded `data.rt`; do not create a parallel JavaScript timer.
Keep practice feedback as a separate conditional timeline node and omit it from
formal trials when the config says so. Persist completed trials through the
configured data adapter rather than relying only on a final browser download.

## Required Condition Fields

`word`, `ink_color`, `congruency`, and `correct_key`.

## Implementation Boundary

This file provides candidate checks for the exact classic color-word design only.
The confirmed config remains authoritative for all experiment semantics. Plugin initialization, preloading,
timeline construction, abort handling, and current jsPsych APIs come exclusively
from the platform spec and mapping references. `labjs-stroop.md` is a lab.js
logic reference and must not be used as a jsPsych implementation template.
