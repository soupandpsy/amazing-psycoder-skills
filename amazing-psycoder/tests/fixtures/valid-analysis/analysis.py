"""Static-contract fixture for the v1.2 analysis config.

This file is parsed and audited in CI; publication readiness still requires an
actual clean run against real data and review of the generated artifacts.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import re
import sys
import traceback
import warnings
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf
import yaml


CONFIG_PATH = Path(__file__).with_name("config.yaml")
config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
project_dir = CONFIG_PATH.parent
dependency_file = (project_dir / config["runtime"]["dependency_file"]).resolve()
data_path = (project_dir / config["experiment"]["data_path"]).resolve()
output_dir = (project_dir / config["output"]["save_path"]).resolve()
output_dir.mkdir(parents=True, exist_ok=True)
started_at = datetime.now(timezone.utc).isoformat()


def record_unhandled_failure(exc_type, exc_value, exc_traceback):
    failure_log = {
        "command": f"{sys.executable} {Path(__file__).name}",
        "started_at": started_at,
        "ended_at": datetime.now(timezone.utc).isoformat(),
        "exit_status": 1,
        "config_sha256": hashlib.sha256(CONFIG_PATH.read_bytes()).hexdigest(),
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "dependency_sha256": hashlib.sha256(dependency_file.read_bytes()).hexdigest() if dependency_file.is_file() else None,
        "error": "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)),
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
    }
    (output_dir / config["output"]["execution_log"]).write_text(
        json.dumps(failure_log, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    sys.__excepthook__(exc_type, exc_value, exc_traceback)


sys.excepthook = record_unhandled_failure

if platform.python_version() != config["runtime"]["language_version"]:
    raise RuntimeError("running Python version does not match config.runtime.language_version")
if not dependency_file.is_file():
    raise FileNotFoundError("declared dependency_file is missing")

pattern = re.sub(r"\{[A-Za-z_][A-Za-z0-9_]*\}", "*", config["experiment"]["file_pattern"])
input_files = sorted(data_path.glob(pattern))
if not input_files:
    raise FileNotFoundError("no files matched the configured multi-file pattern")
frames = []
for input_file in input_files:
    frame = pd.read_csv(input_file)
    frame["source_file"] = str(input_file.relative_to(project_dir))
    frame["source_file_row"] = range(1, len(frame) + 1)
    frames.append(frame)
data = pd.concat(frames, ignore_index=True)
required_columns = {"subject_id", "stimulus", "condition", "rt"}
missing_columns = required_columns - set(data.columns)
if missing_columns:
    raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

data = data.copy()
data["source_row"] = range(1, len(data) + 1)
missing_rt = data["rt"].isna()
exclusion_log = data.loc[missing_rt, ["source_row", "subject_id"]].assign(reason="missing_rt")
analysis_data = data.loc[~missing_rt].copy()

with warnings.catch_warnings(record=True) as captured_warnings:
    warnings.simplefilter("always")
    model = smf.mixedlm(
        "rt ~ C(condition, Sum)",
        analysis_data,
        groups=analysis_data["subject_id"],
        re_formula="~C(condition, Sum)",
        vc_formula={"stimulus": "0 + C(stimulus)"},
    )
    result = model.fit(method="lbfgs")

confidence = result.conf_int()
estimates = pd.DataFrame(
    {
        "term": result.params.index,
        "estimate": result.params.values,
        "std_error": result.bse.reindex(result.params.index).values,
        "ci_low": confidence.reindex(result.params.index)[0].values,
        "ci_high": confidence.reindex(result.params.index)[1].values,
    }
)
estimates.to_csv(output_dir / "model-estimates.csv", index=False)
exclusion_log.to_csv(output_dir / "exclusion-log.csv", index=False)
diagnostics = {"converged": bool(result.converged)}
(output_dir / "model-diagnostics.json").write_text(
    json.dumps(diagnostics, indent=2), encoding="utf-8"
)

environment = {
    package: importlib.metadata.version(package)
    for package in ("pandas", "statsmodels", "PyYAML")
}
output_names = ["model-estimates.csv", "exclusion-log.csv", "model-diagnostics.json"]
execution_log = {
    "command": f"{sys.executable} {Path(__file__).name}",
    "started_at": started_at,
    "ended_at": datetime.now(timezone.utc).isoformat(),
    "exit_status": 0,
    "config_sha256": hashlib.sha256(CONFIG_PATH.read_bytes()).hexdigest(),
    "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "dependency_sha256": hashlib.sha256(dependency_file.read_bytes()).hexdigest(),
    "input_paths": [str(path.relative_to(project_dir)) for path in input_files],
    "input_sha256": {str(path.relative_to(project_dir)): hashlib.sha256(path.read_bytes()).hexdigest() for path in input_files},
    "warnings": [str(item.message) for item in captured_warnings],
    "outputs_sha256": {name: hashlib.sha256((output_dir / name).read_bytes()).hexdigest() for name in output_names},
    "environment": {"python": platform.python_version(), "dependency_file": str(dependency_file.relative_to(project_dir)), **environment},
}
(output_dir / config["output"]["execution_log"]).write_text(
    json.dumps(execution_log, indent=2, ensure_ascii=False), encoding="utf-8"
)
