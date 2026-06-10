# Experiment Config Schema

Declarative YAML format for defining an experiment. When all config fields are filled and condition files are provided, the experiment code can be generated without further questions.

> **Related**: [condition-file.md](condition-file.md) · [spec-template.md](spec-template.md)

> ⚠️ **LANGUAGE NOTE**: Example values in this schema (e.g., `"休息一下"`, `"正确"`, `"错误"`, `"非常正性"`, `玫瑰`, `牡丹`) are Chinese-language placeholders showing the CONCEPT. When generating code, use the equivalent text in the user's language as determined by the design workflow. See [Language Consistency (Red Line)](../../psy-exp-coder/SKILL.md#language-consistency-red-line).

## Schema

```yaml
# === Required: Meta ===
name: "Experiment Name"           # human-readable
paradigm: go-nogo                 # from supported paradigm list
platform: psychopy                # psychopy | psychtoolbox | jspsych

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
    rt_onset: self                # "self" = RT from this window; or name of another window (e.g., "Target")
    data: [rt, key, acc]          # columns recorded at this window

  - name: Feedback
    content: "correct_incorrect"  # built-in: correct_incorrect | timeout | none
    duration: 500
    response: none
    show_in: [practice]           # only show in these block types

  - name: ITI
    content: ""                   # empty = blank screen
    duration: [500, 800]          # random uniform between min and max
    response: none

# === Required: Block Structure ===
blocks:
  - name: Practice
    condition_file: "conditions/practice.xlsx"
    type: practice                # practice | formal | rest | debrief
    feedback: true
    repeatable: true              # participant can repeat this block
    instruction_text: "按空格键对X反应，看到O不反应"

  - name: Block_1
    condition_file: "conditions/block_1.xlsx"
    type: formal
    feedback: false

  - name: Rest
    type: rest
    duration: 30000               # ms, or "self-paced"
    instruction_text: "休息一下，按空格键继续"

  - name: Block_2
    condition_file: "conditions/block_2.xlsx"
    type: formal
    feedback: false

# === Required if response collected: Response Rules ===
response_rules:
  correct: "{correct_response}"   # column in condition file, or literal key name
  deadline: 2000                  # global response deadline (ms) — MUST be confirmed with user
  anticipatory_threshold: 100     # RT below this is flagged
  mapping:                        # key → response mapping (REQUIRED for multi-key responses)
    f: red
    j: green
    k: blue

# === Optional: Paradigm-specific Settings ===
paradigm_config:
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

# === Conditionally Required: Font Settings (REQUIRED if experiment uses text stimuli, esp. CJK) ===
font:
  auto_detect: true               # true = auto-detect by OS; false = use path below
  path: "/System/Library/Fonts/PingFang.ttc"  # CJK font (used when auto_detect=false)
  height: 40
  language_style: "LTR"

# === Optional: Data Output ===
output:
  directory: "data/"
  filename_pattern: "sub-{subject_id}_{task_name}_{date}.csv"
  incremental_save: true
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
| `rt_onset` | str | `"self"` or `"Target"` | **Required on response windows**. `"self"` = RT measured from this window's flip. A window name = RT measured from that window's flip. For split patterns (separate stimulus + response windows), both are valid depending on task: Go/No-go typically uses `self` on the response window; Dot-probe/Priming typically uses the stimulus window name. If absent on a response window, ask before code generation |
| `data` | [str] | `[rt, key, acc]` | Columns recorded at this window. Only meaningful on response windows |
| `show_in` | [str] | `[practice]` | Restrict this window to specific block types. If absent, window appears in all blocks. Valid values: `practice`, `formal`, `rest`, `debrief` |

## Supported Paradigms

The `paradigm` field maps to the paradigm filename (without `.md`) in [paradigms/](../paradigms/). **Core paradigms** have full `## Must Confirm` and `## Condition File Columns` for guided design:

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

windows:
  - name: Fixation
    content: "+"
    duration: 500
    response: none
  - name: Stimulus
    content: "{stimulus}"
    duration: 500
    response: none
  - name: Response
    content: "{stimulus}"
    duration: "{deadline}"
    response: [space]
    rt_onset: self
    data: [rt, key, acc]
  - name: ITI
    content: ""
    duration: [500, 800]
    response: none

blocks:
  - name: Practice
    condition_file: "conditions/practice.xlsx"
    type: practice
    feedback: true
  - name: Formal
    condition_file: "conditions/formal.xlsx"
    type: formal
    feedback: false

response_rules:
  correct: "{correct_response}"
  deadline: 2000
```

## Validation Rules

Checks 1-6 must pass before code generation. Checks 7-9 are design-level validations.

1. Every `{column_name}` in `content`, `duration`, `response`, `correct` exists in ALL referenced condition files
2. `stimulus_folder` path exists and contains all stimulus files referenced via `{column}` in condition files
3. All `condition_file` paths exist and are valid xlsx/csv
4. Number of rows in each condition file equals `block.trials` (unless `block.trials` is omitted or trials are auto-generated)
5. At least one window accepts input (response is not `none`)
6. Block types are valid: `practice`, `formal`, `rest`, `debrief`
7. `paradigm` matches one of the known paradigm names
8. Every trial type has a resolvable correct response — including no-go (correct=no response), stop (correct=withhold), catch trials, and timeout. No trial type may have ambiguous accuracy coding
9. Every response-collecting window has `rt_onset` defined (either `"self"` or a valid window name)
