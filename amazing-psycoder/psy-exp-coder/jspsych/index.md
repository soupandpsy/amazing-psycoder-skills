# jsPsych — Platform Index

> **状态**: Reference-complete, config-driven generation | **范式**: 26 | **Demo**: 23 `.js`

## Quick links

| Layer | Path | Content |
|-------|------|---------|
| L1 Spec | [spec/README.md](spec/README.md) | pinned jsPsych 8.x Canonical Skeleton + anti-patterns |
| L2 Mapping | [mapping/README.md](mapping/README.md) | Config→timeline mapping + legacy/PsychoJS migration notes |
| L3 Paradigms | [paradigms/](paradigms/) | 26 logic-only legacy references; code is quarantined |
| L4 Demos | [demo/_raw/](demo/_raw/) | 23 Pavlovia-exported `.js` files |

## Mandatory API quick reference

| Category | Use | Never |
|----------|-----|-------|
| Init | `initJsPsych()` + `jsPsych.run()` | `jsPsych.init()` |
| Plugin | class reference: `jsPsychHtmlKeyboardResponse` | string: `'html-keyboard-response'` |
| No keys | `"NO_KEYS"` (string) | `jsPsych.NO_KEYS` |
| RT source | `data.rt` (automatic) | `Date.now()` manual timing |
| Timing | `trial_duration: N` (ms) | `setTimeout`/`setInterval` |
| Data save | `on_data_update` durable checkpoint + final `.localSave('csv', fn)` | end-only/in-memory save |
| Correctness | `jsPsych.pluginAPI.compareKeys()` | `==` manual compare |

## Paradigm quick list

Antisaccade · ANT · BART · Bilingual Stroop · Butterfly Simon · Change Detection · Children Flanker · Choice RT · Climate Reflection · CPT · Corsi Blocks · Cyberball · Drag and Drop · EAST · IAT · lab.js Stroop · Mental Rotation · Multisensory Nature · Multisensory Nature Climate · Numerical Stroop · Phone a Friend · Psychophysics Staircase · Rating to Choice · Sternberg · WCST
