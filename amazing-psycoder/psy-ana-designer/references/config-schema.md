# Analysis Config Schema

Use this YAML as the single source of truth passed from `psy-ana-designer` to `psy-ana-coder`.

```yaml
version: "1.2"
analysis_mode: confirmatory       # confirmatory / exploratory / mixed
runtime:
  language: python                # python / r; confirmed before handoff
  language_version: "3.12.4"      # exact patch-level target, never latest/current
  dependency_strategy: lockfile   # Python: pinned / lockfile; R: lockfile
  dependency_file: requirements.lock # Python: supported pin/lock file; R: renv.lock
  target_environment: "local workstation or CI description"
preregistration:
  reference: null                 # URL/DOI/path when available
  alpha: 0.05

experiment:
  config_path:        # Experiment config, when available
  data_path:          # Project-relative file, or directory when multi_file=true
  file_pattern:       # e.g. "sub-{subject_id}_stroop.csv"
  file_format:        # csv / tsv / txt / xlsx / parquet / json
  loader_options: {}  # normalized: delimiter, sheet, encoding, json_orient
  multi_file:         # true / false
  n_subjects:
  id_columns:
    subject: subject_id
    item: stimulus               # null when items are not sampled/repeated
    session: null

design:
  ivs:                # name, type, levels
  dvs:                # name, type, unit
  design_type:        # within / between / mixed
  observation_level:  # trial / subject-summary / event
  clustering:         # e.g. [subject_id, stimulus, session]
  non_clustering_justifications: {} # optional: item/session identifiers intentionally not modeled as dependence units

questions:
  - id: Q1
    question:         # Natural-language scientific question
    dv:
    role:             # primary / secondary / exploratory / manipulation-check
    estimand:         # exact population quantity/contrast being estimated
    hypothesis:       # directional / non-directional / descriptive
    selected_method:
    alternatives_considered: []
    rationale:        # Why method matches estimand + hierarchy
    model_formula:
    dependence_structure:  # random/correlation/groups/aggregation strategy for subject/item/session/site

cleaning:
  rt_lower:
  rt_upper:
  accuracy_min:
  trial_exclusion:
  missing_policy:     # rule + level + rationale; not just a percentage threshold
  sensitivity_rules: []

model:
  stochastic:         # true / false
  seed:               # required only when stochastic=true
  contrast:           # treatment / sum / helmert
  correction:         # declared claim family + Holm/Bonferroni/FDR/Tukey/planned/hierarchical/none/not_applicable
  diagnostics: []

output:
  save_path:
  report_format:      # RMarkdown / Quarto / notebook
  figures:
  effect_sizes:
  environment_capture: true
  execution_log: analysis-run.json
```

## Completion rules

- Require `analysis_mode`, an estimand/role, and a selected method for every analyzed outcome; recorded QC/logging variables need no inferential question.
- Require a confirmed analysis language, exact language version, dependency strategy, concrete project-relative dependency file, and target environment; Coder must not silently change ecosystems.
- Require observation level and all dependence/clustering units that affect the model (subjects, items, sessions, sites).
- For multi-file input, `data_path` names a directory and `file_pattern` names files within it. Require explicit delimiter/sheet/JSON orientation where the format would otherwise be ambiguous.
- Require alpha/preregistration provenance for confirmatory questions and label post-data decisions as exploratory.
- Require a seed only when `model.stochastic` is true; environment capture is always required.
- Record the source of each decision in the Analysis Decision Registry.
- Mark defaults and inferences as `[ASSUMED]` until Gate 5 confirmation.
- Do not pass unresolved fields to `psy-ana-coder`.
- Save it as `analysis_config.yaml` after Gate 5, report its path, and show its contents on request.
