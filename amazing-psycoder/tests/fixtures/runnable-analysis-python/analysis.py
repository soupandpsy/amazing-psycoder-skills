"""Runnable paired-analysis fixture with success and failure evidence."""

from __future__ import annotations

import hashlib
import importlib.metadata as metadata
import json
import platform
import sys
import traceback
import warnings
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from scipy import stats


PROJECT = Path(__file__).resolve().parent
CONFIG_PATH = PROJECT / "config.yaml"
config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
started_at = datetime.now(timezone.utc).isoformat()


def project_path(value: str) -> Path:
    candidate = (PROJECT / value).resolve()
    candidate.relative_to(PROJECT)
    return candidate


output_dir = project_path(config["output"]["save_path"])
output_dir.mkdir(parents=True, exist_ok=True)
execution_log = output_dir / config["output"]["execution_log"]
dependency_file = project_path(config["runtime"]["dependency_file"])
input_files: list[Path] = []


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record_unhandled_failure(exc_type, exc_value, exc_traceback) -> None:
    failure = {
        "command": f"{sys.executable} {Path(__file__).name}",
        "started_at": started_at,
        "ended_at": datetime.now(timezone.utc).isoformat(),
        "exit_status": 1,
        "config_sha256": file_hash(CONFIG_PATH),
        "code_sha256": file_hash(Path(__file__)),
        "dependency_sha256": file_hash(dependency_file) if dependency_file.is_file() else None,
        "input_sha256": {str(path.relative_to(PROJECT)): file_hash(path) for path in input_files if path.is_file()},
        "outputs_sha256": {},
        "warnings": [],
        "environment": {
            "python": platform.python_version(),
            "dependency_file": str(dependency_file.relative_to(PROJECT)),
        },
        "error": "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)),
    }
    execution_log.write_text(json.dumps(failure, indent=2, ensure_ascii=False), encoding="utf-8")
    sys.__excepthook__(exc_type, exc_value, exc_traceback)


sys.excepthook = record_unhandled_failure

if platform.python_version() != str(config["runtime"]["language_version"]):
    raise RuntimeError("running Python version does not match config.runtime.language_version")
if not dependency_file.is_file():
    raise FileNotFoundError("declared dependency artifact is missing")

pins = {}
for raw_line in dependency_file.read_text(encoding="utf-8").splitlines():
    line = raw_line.strip()
    if line and not line.startswith("#"):
        package, version = line.split("==", 1)
        pins[package.lower()] = version
used_distributions = {"numpy": "numpy", "pandas": "pandas", "pyyaml": "PyYAML", "scipy": "scipy"}
for normalized, distribution in used_distributions.items():
    if pins.get(normalized) != metadata.version(distribution):
        raise RuntimeError(f"installed {distribution} does not match requirements.lock")

data_path = project_path(config["experiment"]["data_path"])
input_files = [data_path]
data_raw = pd.read_csv(data_path)
required_columns = {"subject_id", "condition", "rt"}
missing_columns = required_columns - set(data_raw.columns)
if missing_columns:
    raise ValueError(f"missing required columns: {sorted(missing_columns)}")
if set(data_raw["condition"].dropna().unique()) != {"control", "experimental"}:
    raise ValueError("condition levels do not match the confirmed config")

data = data_raw.assign(source_row=np.arange(1, len(data_raw) + 1))
reasons = pd.Series(pd.NA, index=data.index, dtype="string")
reasons = reasons.mask(data["rt"].isna(), "missing_rt")
reasons = reasons.mask(data["rt"].notna() & (data["rt"] < config["cleaning"]["rt_lower"]), "rt_below_confirmed_bound")
reasons = reasons.mask(data["rt"].notna() & (data["rt"] > config["cleaning"]["rt_upper"]), "rt_above_confirmed_bound")
exclusion_log = data.loc[reasons.notna(), ["source_row", "subject_id", "condition", "rt"]].copy()
exclusion_log["reason"] = reasons.dropna()
analysis_data = data.loc[reasons.isna()].copy()

paired = analysis_data.pivot(index="subject_id", columns="condition", values="rt").dropna()
if paired.empty or set(paired.columns) != {"control", "experimental"}:
    raise ValueError("no complete subject pairs remain")
differences = paired["experimental"] - paired["control"]

with warnings.catch_warnings(record=True) as captured_warnings:
    warnings.simplefilter("always")
    test = stats.ttest_rel(paired["experimental"], paired["control"])

n_pairs = int(differences.size)
estimate = float(differences.mean())
std_error = float(differences.std(ddof=1) / np.sqrt(n_pairs))
critical = float(stats.t.ppf(0.975, df=n_pairs - 1))
ci_low = estimate - critical * std_error
ci_high = estimate + critical * std_error
result = pd.DataFrame(
    [{"n_pairs": n_pairs, "estimate": estimate, "std_error": std_error, "ci_low": ci_low, "ci_high": ci_high, "t": float(test.statistic), "p_value": float(test.pvalue)}]
)
descriptive = analysis_data.groupby("condition", as_index=False)["rt"].agg(n="count", mean="mean", sd="std", median="median")
diagnostics = {
    "n_pairs": n_pairs,
    "all_finite": bool(np.isfinite(differences).all()),
    "difference_sd": float(differences.std(ddof=1)),
}
environment = {
    "python": platform.python_version(),
    "python_build": sys.version,
    "platform": platform.platform(),
    "dependency_file": str(dependency_file.relative_to(PROJECT)),
    "packages": {distribution: metadata.version(distribution) for distribution in used_distributions.values()},
}

result.to_csv(output_dir / "paired-contrast.csv", index=False)
descriptive.to_csv(output_dir / "descriptive-statistics.csv", index=False)
exclusion_log.to_csv(output_dir / "exclusion-log.csv", index=False)
(output_dir / "model-diagnostics.json").write_text(json.dumps(diagnostics, indent=2), encoding="utf-8")
(output_dir / "environment.json").write_text(json.dumps(environment, indent=2), encoding="utf-8")
notebook = {
    "cells": [{"cell_type": "markdown", "metadata": {}, "source": ["# Paired RT analysis\n", "See the hashed CSV and JSON outputs produced by `analysis.py`.\n"]}],
    "metadata": {"language_info": {"name": "python", "version": platform.python_version()}},
    "nbformat": 4,
    "nbformat_minor": 5,
}
(output_dir / "report.ipynb").write_text(json.dumps(notebook, indent=2), encoding="utf-8")

output_names = [
    "paired-contrast.csv",
    "descriptive-statistics.csv",
    "exclusion-log.csv",
    "model-diagnostics.json",
    "environment.json",
    "report.ipynb",
]
success = {
    "command": f"{sys.executable} {Path(__file__).name}",
    "started_at": started_at,
    "ended_at": datetime.now(timezone.utc).isoformat(),
    "exit_status": 0,
    "config_sha256": file_hash(CONFIG_PATH),
    "code_sha256": file_hash(Path(__file__)),
    "dependency_sha256": file_hash(dependency_file),
    "input_sha256": {str(path.relative_to(PROJECT)): file_hash(path) for path in input_files},
    "outputs_sha256": {name: file_hash(output_dir / name) for name in output_names},
    "warnings": [str(item.message) for item in captured_warnings],
    "environment": environment,
    "error": None,
}
execution_log.write_text(json.dumps(success, indent=2, ensure_ascii=False), encoding="utf-8")
