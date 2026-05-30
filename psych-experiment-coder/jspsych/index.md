# jsPsych — Platform Index

> **状态**: Reference-complete, manual generation | **范式**: 25 | **Demo**: 23 `.js`

## Quick links

| Layer | Path | Content |
|-------|------|---------|
| L1 Spec | [spec/README.md](spec/README.md) | jsPsych 7.x Canonical Skeleton + anti-patterns |
| L2 Mapping | [mapping/README.md](mapping/README.md) | Config→timeline mapping + 7.x/6.1.0/PsychoJS + migration table |
| L3 Paradigms | [paradigms/](paradigms/) | 25 paradigm reference files |
| L4 Demos | [demo/_raw/](demo/_raw/) | 23 Pavlovia-exported `.js` files |

## Mandatory API quick reference

| Category | Use | Never |
|----------|-----|-------|
| Init | `initJsPsych()` + `jsPsych.run()` | `jsPsych.init()` |
| Plugin | class reference: `jsPsychHtmlKeyboardResponse` | string: `'html-keyboard-response'` |
| No keys | `"NO_KEYS"` (string) | `jsPsych.NO_KEYS` |
| RT source | `data.rt` (automatic) | `Date.now()` manual timing |
| Timing | `trial_duration: N` (ms) | `setTimeout`/`setInterval` |
| Data save | `on_finish` + `.localSave('csv', fn)` | trial-internal save |
| Correctness | `jsPsych.pluginAPI.compareKeys()` | `==` manual compare |

## Paradigm quick list

Antisaccade · ANT · BART · Bilingual Stroop · Butterfly Simon · Change Detection · Children Flanker · Choice RT · Climate Reflection · CPT · Corsi Blocks · Cyberball · Drag and Drop · EAST · IAT · lab.js Stroop · Mental Rotation · Multisensory Nature · Multisensory Nature Climate · Numerical Stroop · Phone a Friend · Psychophysics Staircase · Rating to Choice · Sternberg · WCST
