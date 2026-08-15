# Python Analysis Platform Contract

Use this reference only after analysis config v1.2 passes validation. Preserve the confirmed estimand and hierarchy; do not assume Python APIs are equivalent to R APIs.

## Canonical Structure

1. Read config and record input/config hashes.
2. Import only required packages and capture versions.
3. Configure seeds/backends only for declared stochastic steps.
4. Load data through `pathlib`, validate project boundaries, schema, types, levels, IDs, and denominators.
5. Apply only confirmed cleaning/missingness rules; retain immutable source-row IDs and a reason-coded exclusion table.
6. Produce sample-flow/descriptive summaries at declared observation and clustering levels.
7. Fit `questions[].selected_method`; block if the required estimator is unavailable or the formula ignores declared dependence.
8. Run estimator-appropriate diagnostics and prespecified sensitivity/fallback rules.
9. Save focal estimates with uncertainty plus claim-supporting tables/figures.
10. Save environment and execution manifests.

## Core Guard Pattern

```python
from __future__ import annotations

import importlib.metadata as metadata
import json
import platform
import re
import sys
from pathlib import Path

import pandas as pd
import yaml

PROJECT = Path(__file__).resolve().parent
config_path = PROJECT / "analysis_config.yaml"
config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
if config.get("version") != "1.2":
    raise ValueError("analysis config v1.2 is required")
if platform.python_version() != str(config["runtime"]["language_version"]):
    raise RuntimeError(
        f"Python {config['runtime']['language_version']} required; "
        f"running {platform.python_version()}"
    )


def project_path(value: str) -> Path:
    candidate = (PROJECT / value).resolve()
    try:
        candidate.relative_to(PROJECT)
    except ValueError as exc:
        raise ValueError(f"Path escapes project root: {value}") from exc
    return candidate


def read_one(path: Path, file_format: str, options: dict) -> pd.DataFrame:
    encoding = options.get("encoding")
    if file_format == "csv":
        return pd.read_csv(path, encoding=encoding)
    if file_format == "tsv":
        return pd.read_csv(path, sep="\t", encoding=encoding)
    if file_format == "txt":
        return pd.read_csv(path, sep=options["delimiter"], encoding=encoding)
    if file_format == "xlsx":
        return pd.read_excel(path, sheet_name=options["sheet"])
    if file_format == "parquet":
        return pd.read_parquet(path)
    if file_format == "json":
        return pd.read_json(path, orient=options["json_orient"], encoding=encoding)
    raise ValueError(f"Unsupported file format: {file_format}")

if config["model"]["stochastic"] and config["model"].get("seed") is None:
    raise ValueError("stochastic analysis requires model.seed")

dependency_path = project_path(config["runtime"]["dependency_file"])
if not dependency_path.is_file():
    raise FileNotFoundError(f"Declared dependency artifact is missing: {dependency_path}")

experiment = config["experiment"]
data_path = project_path(experiment["data_path"])
file_format = experiment["file_format"].lower()
loader_options = dict(experiment.get("loader_options") or {})
if experiment["multi_file"]:
    glob_pattern = re.sub(r"\{[A-Za-z_][A-Za-z0-9_]*\}", "*", experiment["file_pattern"])
    input_files = sorted(path for path in data_path.glob(glob_pattern) if path.is_file())
else:
    input_files = [data_path]
if not input_files:
    raise FileNotFoundError("No input files matched the confirmed analysis config")

frames = []
for input_file in input_files:
    frame = read_one(input_file, file_format, loader_options)
    frame["_source_file"] = str(input_file.relative_to(PROJECT))
    frame["_source_file_row"] = range(1, len(frame) + 1)
    frames.append(frame)
data_raw = pd.concat(frames, ignore_index=True)

required = {value for value in config["experiment"]["id_columns"].values() if value}
required.update(config["design"]["clustering"])
required.update(iv["name"] for iv in config["design"]["ivs"])
required.update(dv["name"] for dv in config["design"]["dvs"])
missing = required - set(data_raw.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

data_work = data_raw.assign(_source_row=range(1, len(data_raw) + 1))
exclusion_log = pd.DataFrame(columns=["_source_row", "rule", "reason"])
# Apply only config['cleaning'] rules; never insert generic cutoffs.
# Fit the exact selected method and save estimates, uncertainty, and diagnostics.

# Generate this list from distributions actually imported by the completed script.
USED_DISTRIBUTIONS = ["pandas", "PyYAML"]
environment = {
    "python": platform.python_version(),
    "python_build": sys.version,
    "platform": platform.platform(),
    "packages": {name: metadata.version(name) for name in USED_DISTRIBUTIONS},
    "dependency_file": str(dependency_path.relative_to(PROJECT)),
}
output_dir = project_path(config["output"]["save_path"])
output_dir.mkdir(parents=True, exist_ok=True)
(output_dir / "environment.json").write_text(
    json.dumps(environment, indent=2), encoding="utf-8"
)
```

Treat this as the setup core, not a complete deliverable. Wrap execution so an unhandled failure writes valid JSON with timestamps, non-zero exit status, available artifact/input hashes, environment, and traceback. On success, hash every generated output and run `validate_analysis.py ... --execution-log <configured-log>`; do not hand-write a success-only manifest.

Resolve imports against the declared dependency artifact before execution. The generated lock/pin artifact must cover every third-party distribution imported by the completed script; a syntactically pinned but incomplete file blocks delivery.

## Method/API Guidance

| Need | Validated direction |
|------|---------------------|
| Paired/Welch contrast | `scipy.stats.ttest_rel`; `ttest_ind(..., equal_var=False)` |
| Repeated-measures ANOVA | `pingouin.rm_anova()` when its assumptions/data shape fit |
| Gaussian mixed model | `statsmodels.MixedLM`; verify grouping/variance-component limits |
| Repeated binary/count outcome | Bambi multilevel model, `statsmodels` Bayesian mixed GLM within documented limits, or GEE for a population-average estimand |
| Plain logistic regression | `statsmodels.Logit/GLM` only for independent observations or an explicitly justified covariance strategy; never label it GLMM |
| Bayesian diagnostics | Bambi/PyMC convergence and posterior-predictive checks |
| Environment | exact runtime check + actual imported-distribution snapshot + declared dependency artifact |

## Blocking Anti-Patterns

- Silently selecting a model, threshold, missingness policy, contrast, or multiplicity rule.
- Using plain `Logit()` as a random-effects logistic model.
- Modeling repeated observations with independent `ttest_ind`, `f_oneway`, OLS, or correlation.
- Requiring `random_state` for deterministic tests, or omitting it from actually stochastic steps.
- Treating per-condition Shapiro tests as a universal model gate.
- Losing source-row identity/exclusion reasons or overwriting raw data.
- Ignoring declared item/session/site dependence.
- Hardcoded user paths, suppressed pandas warnings, unsaved declared figures, or missing environment evidence.
- Treating `multi_file` as a single file, silently choosing the first spreadsheet sheet, or ignoring the declared loader format/options.
- Listing template packages that the generated script never imports, or declaring a lock strategy without generating the configured dependency artifact.
- Comparing sensitivity analyses only by p-value threshold crossing.

## Delivery Evidence

Static generation yields `ready_for_execution` at most. When dependencies/data are available, run in a clean process and write `analysis-run.json` on both success and failure (wrapper, `try/finally`, or exception hook), containing command/timestamps/exit status, config/code/dependency/input SHA-256 values available at that point, warnings/traceback, environment, and generated artifact inventory with hashes. A later result audit must reject artifacts whose hashes no longer match the reviewed run.
