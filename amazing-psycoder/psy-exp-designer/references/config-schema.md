# Standalone Experiment Config Schema

Declarative YAML format for defining an experiment. When all config fields are filled and condition files are provided, the experiment code can be generated without further questions.

> This YAML document is the editable handoff for standalone Claude Code/Codex
> use. PsyCoder Studio does not submit this YAML to its Worker: the website
> stores `ExperimentModel@4.0` JSON and compiles it directly for the selected
> platform. Keep the semantics equivalent, but never serialize this
> standalone shape as a Studio Canvas or any retired experiment document.

> **Related**: [condition-file.md](condition-file.md) · [spec-template.md](spec-template.md) · deterministic validator: `../../scripts/validate_experiment.py`

> ⚠️ **LANGUAGE NOTE**: Instruction/feedback examples are placeholders and must be adapted to the confirmed participant language. Scientific stimuli (words, images, audio), response keys, condition codes, and data fields are not auto-translated; they follow the confirmed design exactly. See [Language Consistency (Red Line)](../../psy-exp-coder/SKILL.md#language-consistency-red-line).

## Schema

```yaml
# === Required: Meta ===
name: "Experiment Name"           # human-readable
paradigm: go-nogo                 # exact design/variant identifier; custom values allowed
paradigm_family: inhibition       # optional research lineage; metadata only
variant: letter-go-nogo           # optional exact variant; metadata only
platform: psychopy                # psychopy | psychtoolbox | jspsych
runtime:
  framework_version: "2024.2.4"  # exact confirmed target; never silently use "latest"
  dependency_strategy: pinned     # pinned | lockfile
  target_environment: "lab workstation profile A"

# === Optional: Stimulus Folder (global) ===
stimulus_folder: "stimuli/"     # prepended to all {column} image references. One global path for all windows

# === Required: Window Sequence ===
# Each window = one screen event in the trial
# Order defines the timeline.
windows:

  - name: Fixation                # unique name for this window
    content: "+"                  # literal string, or {column_name} from condition file
    duration: 500                 # ms; integer = fixed, [min, max] = random uniform
    response: none                # none | key_list | mouse | any

  - name: Stimulus
    content: "{stimulus}"         # {stimulus} is substituted from condition file column
    duration: 500
    response: none
  - name: Response
    content: "{stimulus}"
    duration: 2000                # response deadline
    response: [f, j]              # allowed keys
    response_event: key_down      # key_down | key_release | click | submit | touch | voice | gaze_event | custom
    rt_onset: self                # "self" = RT from this window; or name of another window (e.g., "Target")
    rt_rationale: "RT starts when this scored stimulus is actually displayed"
    rt_contract_status: confirmed # proposed | confirmed; generation requires confirmed
    data: [rt, key, acc]          # columns recorded at this window

  - name: Feedback
    content: "correct_incorrect"  # built-in: correct_incorrect | timeout | none
    duration: 500
    response: none
    show_in: [practice]           # only show in these contexts (practice/formal/rest/debrief)

  - name: ITI
    content: ""                   # empty = blank screen
    duration: [500, 800]          # random uniform between min and max
    response: none

# === Required: Sequence Structure (Primary Format) ===
# Each sequence = one horizontal row of windows on the canvas.
# Sequences execute top-to-bottom; windows within a sequence run left-to-right.
trial_sources:
  practice_table: "conditions/practice.xlsx"
  formal_table: "conditions/formal.xlsx"

sequences:
  - name: Trial
    order: 1
    window_ids: [Fixation, Stimulus, Response, Feedback, ITI]
    trial_source_id: formal_table      # optional; one source per sequence
    execution:
      repetitions: 1                  # positive cycle count; 1 already means once
      order_mode: fixed_random        # table_order | fixed_random | fully_random
      seed: "{subject_id}"            # required for fixed_random
      reshuffle_each_cycle: false      # reuse the same fixed order across cycles

  - name: Feedback                  # only shown when feedback is active
    order: 2
    window_ids: [Feedback, ITI]
    execution:
      repetitions: 1
      order_mode: table_order
    show_in: [practice]             # optional; restrict to specific contexts

  - name: Rest
    order: 3
    window_ids: [Rest]
    execution:
      repetitions: 1
      order_mode: table_order
    duration: 30000                 # ms, or "self-paced"

# === Required: Randomization Contract ===
randomization:
  method: pseudorandom            # random | pseudorandom | blocked | counterbalanced | fixed
  seed_scope: per_subject         # per_session | per_subject | fixed
  seed: "{subject_id}"            # integer/string/template; resolve before randomization
  record_resolved_seed: true      # save the resolved seed or complete realized order
  max_consecutive_same_condition: 3

# === Required if response collected: Response Rules ===
response_rules:
  correct: "{correct_response}"   # column in condition file, or literal key name
  deadline: 2000                  # global response deadline (ms) — MUST be confirmed with user
  anticipatory_threshold: 100     # illustrative only; must be task/device/protocol-derived and confirmed
  mapping:                        # key → response mapping (REQUIRED for multi-key responses)
    f: red
    j: green
    k: blue

# === Optional: Explicit Custom/Variant Logic ===
paradigm_config:
  # These fields are executable only because they are explicitly confirmed in
  # this config. They are never inherited from paradigm or paradigm_family.
  # Go/No-go
  go_ratio: 0.8
  max_consecutive_nogo: 2

  # Stop-signal
  stop_probability: 0.25
  initial_ssd: 250
  ssd_step: 50
  ssd_bounds: [50, 800]
  stop_signal:
    type: auditory                # auditory | visual
    stimulus: "750Hz_tone.wav"
    duration: 100

  # Stroop
  target_dimension: ink_color    # which dimension to respond to
  distractor_dimension: word     # which dimension to ignore
  congruency_ratio: 0.5          # proportion congruent (vs incongruent)

  # Eriksen Flanker
  flanker_type: arrow            # arrow | letter | fish
  n_flankers: 4                  # per side (2 left, 2 right typical)
  spacing: 1.0                   # center-to-flanker spacing in degrees
  congruency_ratio: 0.5          # proportion congruent (vs incongruent)

  # Simon
  compatibility_type: spatial    # spatial stimulus-response compatibility
  stimulus_modality: visual      # visual | auditory
  response_modality: manual      # manual | vocal
  congruency_ratio: 0.5          # proportion congruent (vs incongruent)

  # Navon
  attended_level: global         # global | local | cued
  target_letters: [H, S]         # which letters appear
  response_mapping:              # key → letter for global task
    f: H
    j: S

  # Priming
  prime_duration: 40             # ms
  soa: 60                        # stimulus onset asynchrony (ms)
  mask_type: forward             # forward | backward | both | none
  mask_duration: 500             # ms, only if mask_type is set
  prime_visibility_check: false  # include prime detection catch trials?

  # Rating
  scale_type: likert             # likert | vas
  n_points: 9                    # number of scale points (Likert only)
  anchors:                       # scale endpoint labels
    low: "非常负性"
    high: "非常正性"
  dimensions:                    # rating dimension(s)
    - name: valence
      anchor_low: "非常负性"
      anchor_high: "非常正性"
    - name: arousal
      anchor_low: "非常平静"
      anchor_high: "非常激动"

  # IAT
  block_structure: standard       # standard (7-block) | custom
  error_correction: forced        # forced | feedback_only
  counterbalance_order: true      # compatible-first vs incompatible-first across subjects

  # EAST
  attribute_words:
    positive: [健康, 快乐, 美好]
    negative: [邪恶, 吝啬, 卑鄙]
  target_categories:
    a: [玫瑰, 牡丹]
    b: [空气, 土地]
    c: [蟑螂, 蚊子]
  color_positive: blue
  color_negative: green
  repetitions: 2

  # N-back
  n_levels: [1, 2, 3]
  match_ratio: 0.33
  lure_type: none                 # none | n-1 | n+1 | both

  # Dot-probe
  soa: 500
  stimulus_pair_config: pairs.csv # file defining emotional/neutral pairings

  # Visual Search
  set_sizes: [4, 8, 12]          # number of items per display
  target_present_ratio: 0.5       # proportion target-present trials
  search_type: conjunction        # feature | conjunction
  display_layout: circle          # circle | grid | random

  # Task Switching
  tasks:                          # task definitions
    - name: parity
      cue: "红色边框"
      rule: "odd_even"
    - name: magnitude
      cue: "蓝色边框"
      rule: "greater_less_5"
  csi: 300                        # cue-stimulus interval (ms)
  rci: 1000                       # response-cue interval (ms)
  switch_ratio: 0.5               # proportion switch trials

# === Optional: Window Timing Overrides (per paradigm) ===
timing:
  fixation: 500
  feedback: 500
  iti: [500, 800]

# === Optional: Display Settings ===
display:
  fullscreen: true
  background: [-0.5, -0.5, -0.5]  # PsychoPy normalized units
  units: deg                      # deg | pix | norm

# === Conditionally Required: Font Settings (required for CJK/font-sensitive stimuli) ===
font:
  auto_detect: true               # true = auto-detect by OS; false = use path below
  path: "/System/Library/Fonts/PingFang.ttc"  # CJK font (used when auto_detect=false)
  height: 40
  language_style: "LTR"

# === Required: Data Output ===
output:
  directory: "data/"
  filename_pattern: "sub-{subject_id}_{task_name}_{run_id}.csv"  # collision-resistant per launch
  incremental_save: true
  trial_summary: true              # one analyzable summary row per trial
  event_file: null                 # optional linked table for repeated within-trial events
```

## Content Value Types

| Type | Syntax | Example | Description |
|------|--------|---------|-------------|
| Literal text | `"+"` | `"+"` | Fixed text displayed as-is |
| Column reference | `"{column_name}"` | `"{stimulus}"` | Substituted from condition file column |
| Image file | `"{stimulus}"` + `stimulus_folder` | `"stimuli/{stimulus}"` | Global `stimulus_folder` prepended to column value |
| Built-in feedback | `"correct_incorrect"` | `"correct_incorrect"` | Automatic 正确/错误 text |
| Empty | `""` | `""` | Blank screen |

## Duration Value Types

| Type | Syntax | Example | Description |
|------|--------|---------|-------------|
| Fixed | integer | `500` | Exact ms |
| Random uniform | `[min, max]` | `[500, 800]` | Random from uniform distribution |
| Column reference | `"{column_name}"` | `"{deadline}"` | Per-trial value from condition file column |
| Until response | `"until_key"` | `"until_key"` | Waits for keypress (uses `response` field) |
| Self-paced | `"self_paced"` | `"self_paced"` | Waits for any input |

## Response Value Types

| Type | Syntax | Example | Description |
|------|--------|---------|-------------|
| No response | `none` | `none` | No input expected |
| Key list | `[f, j]` | `[f, j]` | Specific allowed keys |
| Single key | `space` | `space` | One allowed key |
| Mouse | `mouse` | `mouse` | Mouse click |
| Any key | `any` | `any` | Any keyboard input |

## Window Metadata Fields

In addition to `content`, `duration`, and `response`, each window can have these optional metadata fields:

| Field | Type | Example | Description |
|-------|------|---------|-------------|
| `name` | str | `"Fixation"` | Unique window name (required) |
| `rt_onset` | str | `"self"` or `"Target"` | **Required on response windows**. `"self"` = RT measured from this window's verified presentation timestamp. A window name = RT measured from that named window's verified presentation timestamp. Never choose it solely from a paradigm label |
| `rt_rationale` | str | `"RT starts at target display"` | Scientific meaning of the response-event/anchor pairing |
| `rt_contract_status` | str | `confirmed` | `proposed` or `confirmed`; code generation requires explicit confirmation |
| `data` | [str] | `[rt, key, acc]` | Columns recorded at this window. Only meaningful on response windows |
| `show_in` | [str] | `[practice]` | Restrict this window to specific contexts. If absent, window appears in all sequences. Valid values: `practice`, `formal`, `rest`, `debrief` |

## Paradigm References

When an exact match exists, the `paradigm` field may map to a reference filename
(without `.md`) in [paradigms/](../paradigms/). These files improve guided
design; they are not a whitelist, templates, or executable contracts. Custom
identifiers are valid when the config explicitly defines complete windows,
conditions, correctness, randomization, and output semantics. A family label
never imports another variant's rules.

**Core references** have full `## Must Confirm` and `## Condition File Columns` for guided design:

```
go-nogo, navon, priming, stroop, eriksen-flanker, simon,
rating, stop-signal, iat, n-back, dot-probe, visual-search,
task-switching, east
```

**Extended paradigms** have reference descriptions (experiment logic + literature). When using these, ask paradigm-specific questions manually during design:

```
antisaccade, attention-network-task, bart, bilingual-stroop,
change-detection, children-flanker-task, choice-reaction-time,
climate-reflection-task, continuous-performance-test, corsi-blocks,
cyberball, delay-discounting, drag-and-drop,
mental-rotation, multisensory-nature, numerical-stroop,
phone-a-friend, posner-cuing, psychophysics-staircase,
rating-to-choice, sternberg, ultimatum-game,
wisconsin-card-sorting, writing-distraction
```

## Minimal Config Example

The shortest valid config for a Go/No-go task:

```yaml
name: "Letter Go/No-go"
paradigm: go-nogo
platform: psychopy
runtime:
  framework_version: "2024.2.4"
  dependency_strategy: pinned
  target_environment: "lab workstation profile A"

windows:
  - name: Fixation
    content: "+"
    duration: 500
    response: none
  - name: StimulusResponse
    content: "{stimulus}"
    duration: "{deadline}"
    response: [space]
    response_event: key_down
    rt_onset: self
    rt_rationale: "RT starts at the verified display onset of the scored stimulus"
    rt_contract_status: confirmed
    data: [rt, key, acc]
  - name: ITI
    content: ""
    duration: [500, 800]
    response: none

sequences:
  - name: Practice
    order: 1
    window_ids: [Fixation, StimulusResponse, Feedback, ITI]
    trial_source_id: practice_table
    execution:
      repetitions: 1
      order_mode: fixed_random
      seed: "{subject_id}"
      reshuffle_each_cycle: false
    show_in: [practice]

  - name: Formal
    order: 2
    window_ids: [Fixation, StimulusResponse, ITI]
    trial_source_id: formal_table
    execution:
      repetitions: 1
      order_mode: fixed_random
      seed: "{subject_id}"
      reshuffle_each_cycle: false

trial_sources:
  practice_table: "conditions/practice.xlsx"
  formal_table: "conditions/formal.xlsx"

response_rules:
  correct: "{correct_response}"
  deadline: 2000

randomization:
  method: pseudorandom
  seed_scope: per_subject
  seed: "{subject_id}"
  record_resolved_seed: true

output:
  directory: "data/"
  filename_pattern: "sub-{subject_id}_go-nogo_{run_id}.csv"
  incremental_save: true
  trial_summary: true
```

## Validation Rules

All checks must pass before code generation. Checks 1-8 are deterministic artifact checks; checks 9-11 verify design semantics.

1. `runtime` records an exact framework version, pinned/lockfile dependency strategy, and target environment; every `{column_name}` in `content`, `duration`, `response`, `correct` exists in ALL referenced condition files
2. `stimulus_folder` path exists and contains all stimulus files referenced via `{column}` in condition files
3. All `condition_file` paths exist and are valid xlsx/csv
4. Every sequence has `execution.repetitions` ≥ 1 and ≤ 10,000 and `order_mode` in `table_order`, `fixed_random`, `fully_random`; `fixed_random` has a non-empty seed; every `window_ids` entry references an existing window; every `trial_source_id` references `trial_sources`
5. At least one window accepts input (response is not `none`)
6. Sequence `show_in` values (if present) are valid: `practice`, `formal`, `rest`, `debrief`. The configuration must not contain the retired `blocks` field.
7. `randomization` defines a valid method; every stochastic method declares `seed_scope`, a resolvable seed, and `record_resolved_seed: true`. A fixed seed across sessions needs a stated justification
8. `output` defines directory; a collision-resistant filename containing `{subject_id}` plus `{session_id}`, `{run_id}`, or `{timestamp}`; `incremental_save: true`; and one trial-summary row per trial. A date alone is not unique enough. Designs with repeated within-trial observations also define a linked event-level output rather than collapsing events into one cell
9. `paradigm` is a stable exact design identifier. If an exact reference exists it may be consulted; otherwise validation continues as a custom design. `paradigm_family` and `variant` are metadata and never fill missing semantics
10. Every trial type has a resolvable correct response — including no-go (correct=no response), stop (correct=withhold), catch trials, and timeout. No trial type may have ambiguous accuracy coding
11. Every response-collecting window declares the scored `response_event`, a resolvable `rt_onset` (`"self"` or a valid window name), an `rt_rationale`, and `rt_contract_status: confirmed`. A structurally valid anchor is not evidence that the scientific operational definition is correct
12. (sequences) Condition variation: at least two distinct condition values must exist across all condition rows. A design where every row is identical passes structure checks but represents a degenerate experiment
13. (sequences) ITI precedence: if `itiMs` is set as a timing override AND an ITI window exists in the trial sequence, the ITI window takes precedence (the timing override is ignored). Only one ITI mechanism should be active
14. (sequences) Key-platform compatibility: response key names must match the target platform convention. PsychoPy/jsPsych: lowercase characters (`f`, `j`, `space`). PTB: `KbName()` values (`LeftArrow`, `RightArrow`). Key names that don't exist on the target platform are rejected before code generation
