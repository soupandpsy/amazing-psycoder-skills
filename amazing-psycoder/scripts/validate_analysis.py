#!/usr/bin/env python3
"""Deterministically validate Amazing PsyCoder analysis artifacts.

Static success means ready for execution testing at most. Publication readiness
requires a successful clean run and review of the generated results.
"""

from __future__ import annotations

import argparse
import ast
import io
import json
import re
import shutil
import subprocess
import sys
import tokenize
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


MISSING = re.compile(r"\[(?:MISSING|TODO|TBD|ASSUMED)\]", re.IGNORECASE)
ABSOLUTE_PATH = re.compile(r"(?:/Users/|/home/|[A-Za-z]:[\\/])")
WINDOWS_ABSOLUTE = re.compile(r"^[A-Za-z]:[\\/]")
URI_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://")
ANALYSIS_MODES = {"confirmatory", "exploratory", "mixed"}
DESIGN_TYPES = {"within", "between", "mixed"}
OBSERVATION_LEVELS = {"trial", "subject-summary", "event"}
ROLES = {"primary", "secondary", "exploratory", "manipulation-check", "descriptive"}
FORMATS = {"csv", "tsv", "txt", "xlsx", "parquet", "json"}
LANGUAGES = {"r", "python"}
DEPENDENCY_STRATEGIES = {"pinned", "lockfile"}
EXACT_LANGUAGE_VERSION = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
DEPENDENCY_FILES = {
    "python": {
        "pinned": {"requirements.txt"},
        "lockfile": {"requirements.lock", "uv.lock", "poetry.lock", "pdm.lock", "conda-lock.yml", "conda-lock.yaml"},
    },
    "r": {"pinned": {"renv.lock"}, "lockfile": {"renv.lock"}},
}
LOADER_OPTIONS = {"delimiter", "sheet", "encoding", "json_orient"}
IV_TYPES = {"categorical", "continuous", "ordinal", "binary"}
DV_TYPES = {"continuous", "binary", "count", "ordinal", "categorical", "proportion", "time-to-event"}


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    message: str
    location: str = ""


def add(findings: list[Finding], level: str, code: str, message: str, location: str = "") -> None:
    findings.append(Finding(level, code, message, location))


def load_config(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    if yaml is not None:
        value = yaml.safe_load(text)
    else:
        try:
            value = json.loads(text)
        except json.JSONDecodeError as exc:
            raise RuntimeError("PyYAML is required for YAML configs: pip install pyyaml") from exc
    if not isinstance(value, dict):
        raise ValueError("config root must be a mapping")
    return value


def walk(value: Any, location: str = "config") -> Iterable[tuple[str, Any]]:
    yield location, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{location}[{index}]")


def text(value: Any) -> str:
    return str(value if value is not None else "").strip()


def absolute_local_path(value: Any) -> bool:
    raw = text(value)
    return Path(raw).is_absolute() or bool(WINDOWS_ABSOLUTE.match(raw))


def escapes_project(value: Any) -> bool:
    """Return true for absolute paths or explicit parent traversal."""
    raw = text(value).replace("\\", "/")
    return absolute_local_path(raw) or bool(URI_SCHEME.match(raw)) or ".." in Path(raw).parts


def require_mapping(config: dict[str, Any], key: str, findings: list[Finding]) -> dict[str, Any]:
    value = config.get(key)
    if not isinstance(value, dict):
        add(findings, "error", "ANA002", f"{key} must be a mapping", f"config.{key}")
        return {}
    return value


def require_list(config: dict[str, Any], key: str, findings: list[Finding]) -> list[Any]:
    value = config.get(key)
    if not isinstance(value, list) or not value:
        add(findings, "error", "ANA003", f"{key} must be a non-empty list", f"config.{key}")
        return []
    return value


def validate_config(path: Path) -> tuple[dict[str, Any], list[Finding]]:
    findings: list[Finding] = []
    try:
        config = load_config(path)
    except (OSError, RuntimeError, ValueError) as exc:
        return {}, [Finding("error", "ANA000", str(exc), str(path))]

    for location, value in walk(config):
        if isinstance(value, str) and MISSING.search(value):
            add(findings, "error", "ANA001", "unresolved marker in confirmed config", location)

    if text(config.get("version")) != "1.2":
        add(findings, "error", "ANA004", "analysis config version must be 1.2", "config.version")
    mode = text(config.get("analysis_mode")).lower()
    if mode not in ANALYSIS_MODES:
        add(findings, "error", "ANA005", f"analysis_mode must be one of {sorted(ANALYSIS_MODES)}", "config.analysis_mode")

    runtime = require_mapping(config, "runtime", findings)
    runtime_language = text(runtime.get("language")).lower()
    if runtime_language not in LANGUAGES:
        add(findings, "error", "ENV001", f"runtime.language must be one of {sorted(LANGUAGES)}", "config.runtime.language")
    language_version = text(runtime.get("language_version")).lower()
    if not EXACT_LANGUAGE_VERSION.fullmatch(language_version):
        add(findings, "error", "ENV002", "runtime.language_version must be an exact patch-level target such as 3.12.4 or 4.4.1", "config.runtime.language_version")
    dependency_strategy = text(runtime.get("dependency_strategy")).lower()
    if dependency_strategy not in DEPENDENCY_STRATEGIES:
        add(findings, "error", "ENV003", f"runtime.dependency_strategy must be one of {sorted(DEPENDENCY_STRATEGIES)}", "config.runtime.dependency_strategy")
    if runtime_language == "r" and dependency_strategy == "pinned":
        add(findings, "error", "ENV009", "R projects must use dependency_strategy: lockfile with renv.lock", "config.runtime.dependency_strategy")
    if not text(runtime.get("target_environment")):
        add(findings, "error", "ENV004", "runtime.target_environment is required", "config.runtime.target_environment")
    dependency_file = text(runtime.get("dependency_file"))
    if not dependency_file:
        add(findings, "error", "ENV005", "runtime.dependency_file is required and must name the generated pin/lock artifact", "config.runtime.dependency_file")
    elif escapes_project(dependency_file):
        add(findings, "error", "ENV006", "runtime.dependency_file must stay inside the project", "config.runtime.dependency_file")
    elif runtime_language in DEPENDENCY_FILES and dependency_strategy in DEPENDENCY_STRATEGIES:
        allowed = DEPENDENCY_FILES[runtime_language][dependency_strategy]
        if Path(dependency_file).name.lower() not in allowed:
            add(findings, "error", "ENV007", f"runtime.dependency_file does not match the {runtime_language} {dependency_strategy} strategy; use one of {sorted(allowed)}", "config.runtime.dependency_file")

    prereg = require_mapping(config, "preregistration", findings)
    if mode in {"confirmatory", "mixed"}:
        alpha = prereg.get("alpha")
        if not isinstance(alpha, (int, float)) or not 0 < float(alpha) < 1:
            add(findings, "error", "ANA006", "confirmatory/mixed analysis requires alpha in (0,1)", "config.preregistration.alpha")

    experiment = require_mapping(config, "experiment", findings)
    data_path = text(experiment.get("data_path"))
    if not data_path:
        add(findings, "error", "DATA001", "experiment.data_path is required", "config.experiment.data_path")
    elif escapes_project(data_path):
        add(findings, "error", "DATA005", "experiment.data_path must stay inside the project", "config.experiment.data_path")
    file_format = text(experiment.get("file_format")).lower()
    if file_format not in FORMATS:
        add(findings, "error", "DATA002", f"file_format must be one of {sorted(FORMATS)}", "config.experiment.file_format")
    loader_options = experiment.get("loader_options", {})
    if not isinstance(loader_options, dict):
        add(findings, "error", "DATA009", "experiment.loader_options must be a mapping", "config.experiment.loader_options")
        loader_options = {}
    unknown_loader_options = set(loader_options) - LOADER_OPTIONS
    if unknown_loader_options:
        add(findings, "error", "DATA010", f"unsupported loader_options: {sorted(unknown_loader_options)}", "config.experiment.loader_options")
    if file_format == "txt" and not text(loader_options.get("delimiter")):
        add(findings, "error", "DATA011", "txt input requires loader_options.delimiter", "config.experiment.loader_options.delimiter")
    if file_format == "xlsx" and not text(loader_options.get("sheet")):
        add(findings, "error", "DATA012", "xlsx input requires an explicit loader_options.sheet", "config.experiment.loader_options.sheet")
    if file_format == "json" and text(loader_options.get("json_orient")).lower() not in {"records", "columns"}:
        add(findings, "error", "DATA013", "json input requires loader_options.json_orient: records or columns", "config.experiment.loader_options.json_orient")
    if not isinstance(experiment.get("multi_file"), bool):
        add(findings, "error", "DATA003", "multi_file must be boolean", "config.experiment.multi_file")
    elif experiment.get("multi_file"):
        pattern = text(experiment.get("file_pattern"))
        if not pattern or "{subject_id}" not in pattern:
            add(findings, "error", "DATA006", "multi_file data requires file_pattern containing {subject_id}", "config.experiment.file_pattern")
        elif escapes_project(pattern) or Path(pattern).name != pattern:
            add(findings, "error", "DATA007", "file_pattern must be a filename template inside experiment.data_path", "config.experiment.file_pattern")
        expected_suffixes = {"txt": {".txt", ".tsv"}, "xlsx": {".xlsx", ".xls"}}
        suffixes = expected_suffixes.get(file_format, {f".{file_format}"})
        if Path(data_path).suffix.lower() in suffixes:
            add(findings, "error", "DATA008", "multi_file experiment.data_path must identify a directory; file_pattern identifies the files", "config.experiment.data_path")
    ids = experiment.get("id_columns")
    if not isinstance(ids, dict) or not text(ids.get("subject")):
        add(findings, "error", "DATA004", "id_columns.subject is required", "config.experiment.id_columns.subject")

    design = require_mapping(config, "design", findings)
    design_type = text(design.get("design_type")).lower()
    if design_type not in DESIGN_TYPES:
        add(findings, "error", "DES001", f"design_type must be one of {sorted(DESIGN_TYPES)}", "config.design.design_type")
    level = text(design.get("observation_level")).lower()
    if level not in OBSERVATION_LEVELS:
        add(findings, "error", "DES002", f"observation_level must be one of {sorted(OBSERVATION_LEVELS)}", "config.design.observation_level")
    ivs = design.get("ivs")
    dvs = design.get("dvs")
    if not isinstance(ivs, list):
        add(findings, "error", "DES003", "design.ivs must be a list", "config.design.ivs")
        ivs = []
    if not isinstance(dvs, list) or not dvs:
        add(findings, "error", "DES004", "design.dvs must be a non-empty list", "config.design.dvs")
        dvs = []
    iv_names: set[str] = set()
    for index, item in enumerate(ivs):
        location = f"config.design.ivs[{index}]"
        if not isinstance(item, dict):
            add(findings, "error", "DES007", "IV must be a mapping", location)
            continue
        name = text(item.get("name"))
        kind = text(item.get("type")).lower()
        if not name or name in iv_names:
            add(findings, "error", "DES008", "IV name must be non-empty and unique", f"{location}.name")
        iv_names.add(name)
        if kind not in IV_TYPES:
            add(findings, "error", "DES009", f"IV type must be one of {sorted(IV_TYPES)}", f"{location}.type")
        if kind in {"categorical", "ordinal", "binary"}:
            levels = item.get("levels")
            if not isinstance(levels, list) or not levels:
                add(findings, "error", "DES010", "categorical/ordinal/binary IV requires a non-empty explicit levels list", f"{location}.levels")
            elif len({text(value) for value in levels}) != len(levels) or any(not text(value) for value in levels):
                add(findings, "error", "DES017", "IV levels must be non-empty and unique", f"{location}.levels")

    dv_types: dict[str, str] = {}
    for index, item in enumerate(dvs):
        location = f"config.design.dvs[{index}]"
        if not isinstance(item, dict):
            add(findings, "error", "DES011", "DV must be a mapping", location)
            continue
        name = text(item.get("name"))
        kind = text(item.get("type")).lower()
        if not name or name in dv_types:
            add(findings, "error", "DES012", "DV name must be non-empty and unique", f"{location}.name")
        if kind not in DV_TYPES:
            add(findings, "error", "DES013", f"DV type must be one of {sorted(DV_TYPES)}", f"{location}.type")
        if not text(item.get("unit")):
            add(findings, "error", "DES014", "DV unit/encoding is required", f"{location}.unit")
        if name:
            dv_types[name] = kind
    clustering = design.get("clustering")
    if not isinstance(clustering, list):
        add(findings, "error", "DES005", "design.clustering must be a list", "config.design.clustering")
        clustering = []
    elif len({text(value) for value in clustering}) != len(clustering) or any(not text(value) for value in clustering):
        add(findings, "error", "DES015", "design.clustering units must be non-empty and unique", "config.design.clustering")
    subject_col = text(ids.get("subject")) if isinstance(ids, dict) else ""
    declared_clusters = {text(value) for value in clustering}
    non_clustering = design.get("non_clustering_justifications")
    if non_clustering is not None and not isinstance(non_clustering, dict):
        add(findings, "error", "DES018", "design.non_clustering_justifications must be a mapping when provided", "config.design.non_clustering_justifications")
        non_clustering = {}
    non_clustering = non_clustering if isinstance(non_clustering, dict) else {}
    if level in {"trial", "event"} and subject_col not in declared_clusters:
        add(findings, "error", "DES006", "trial/event data must declare subject clustering, including between-subject designs with repeated rows", "config.design.clustering")
    if isinstance(ids, dict) and level in {"trial", "event"}:
        for key in ("item", "session"):
            identifier = text(ids.get(key))
            justification = text(non_clustering.get(key) or non_clustering.get(identifier))
            if identifier and identifier not in declared_clusters and not justification:
                add(findings, "error", "DES016", f"declared {key} identifier {identifier!r} must appear in clustering or have an explicit non-clustering justification", "config.design.clustering")

    questions = require_list(config, "questions", findings)
    seen: set[str] = set()
    primary = 0
    for index, question in enumerate(questions):
        location = f"config.questions[{index}]"
        if not isinstance(question, dict):
            add(findings, "error", "Q001", "question must be a mapping", location)
            continue
        qid = text(question.get("id"))
        if not qid or qid in seen:
            add(findings, "error", "Q002", "question id must be non-empty and unique", f"{location}.id")
        seen.add(qid)
        dv = text(question.get("dv"))
        if dv not in dv_types:
            add(findings, "error", "Q003", f"question dv {dv!r} is not declared in design.dvs", f"{location}.dv")
        role = text(question.get("role")).lower()
        if role not in ROLES:
            add(findings, "error", "Q004", f"role must be one of {sorted(ROLES)}", f"{location}.role")
        primary += role == "primary"
        for field in ("question", "estimand", "hypothesis", "selected_method", "rationale", "model_formula", "dependence_structure"):
            if not text(question.get(field)):
                add(findings, "error", "Q005", f"{field} is required", f"{location}.{field}")
        alternatives = question.get("alternatives_considered")
        if not isinstance(alternatives, list):
            add(findings, "error", "Q006", "alternatives_considered must be a list", f"{location}.alternatives_considered")

        method = text(question.get("selected_method")).lower().replace("-", "_")
        qtext = f"{text(question.get('question'))} {text(question.get('estimand'))}".lower()
        if "ssrt" in qtext and any(token in method for token in ("cox", "logrank", "survival")):
            add(findings, "error", "Q007", "SSRT must not be routed to ordinary survival analysis", f"{location}.selected_method")
        if dv_types.get(dv) == "binary" and method in {"anova", "lmer", "linear_model", "ols"}:
            add(findings, "error", "Q008", "binary outcome requires a compatible binomial/ordinal model", f"{location}.selected_method")

    if mode in {"confirmatory", "mixed"} and primary == 0:
        add(findings, "error", "Q009", "confirmatory/mixed analysis requires at least one primary question", "config.questions")

    cleaning = require_mapping(config, "cleaning", findings)
    if not text(cleaning.get("missing_policy")):
        add(findings, "error", "CLN001", "missing_policy with level/rationale is required", "config.cleaning.missing_policy")
    if not isinstance(cleaning.get("sensitivity_rules"), list):
        add(findings, "error", "CLN002", "sensitivity_rules must be a list", "config.cleaning.sensitivity_rules")

    model = require_mapping(config, "model", findings)
    stochastic = model.get("stochastic")
    if not isinstance(stochastic, bool):
        add(findings, "error", "MOD001", "model.stochastic must be boolean", "config.model.stochastic")
    if stochastic and not isinstance(model.get("seed"), int):
        add(findings, "error", "MOD002", "stochastic analysis requires integer model.seed", "config.model.seed")
    if not isinstance(model.get("diagnostics"), list) or not model.get("diagnostics"):
        add(findings, "error", "MOD003", "model.diagnostics must be a non-empty list", "config.model.diagnostics")
    if not text(model.get("contrast")):
        add(findings, "error", "MOD004", "model.contrast must be explicit; use not_applicable with rationale when no factor coding is involved", "config.model.contrast")
    if not text(model.get("correction")):
        add(findings, "error", "MOD005", "model.correction/multiplicity strategy must be explicit; use none/not_applicable with rationale when appropriate", "config.model.correction")

    output = require_mapping(config, "output", findings)
    for field in ("save_path", "report_format", "execution_log"):
        if not output.get(field):
            add(findings, "error", "OUT001", f"output.{field} is required", f"config.output.{field}")
    if not isinstance(output.get("figures"), list):
        add(findings, "error", "OUT002", "output.figures must be a list", "config.output.figures")
    if not isinstance(output.get("effect_sizes"), list) or not output.get("effect_sizes"):
        add(findings, "error", "OUT004", "output.effect_sizes must be a non-empty list of claim-appropriate estimates/uncertainty", "config.output.effect_sizes")
    if output.get("environment_capture") is not True:
        add(findings, "error", "OUT003", "output.environment_capture must be true", "config.output.environment_capture")
    if escapes_project(output.get("save_path")):
        add(findings, "error", "OUT005", "output.save_path must stay inside the project", "config.output.save_path")
    execution_log = text(output.get("execution_log"))
    if execution_log and (escapes_project(execution_log) or Path(execution_log).name != execution_log):
        add(findings, "error", "OUT006", "output.execution_log must be a filename written inside output.save_path", "config.output.execution_log")
    return config, findings


def validate_code(path: Path, language: str, config: dict[str, Any], project_root: Path | None = None) -> list[Finding]:
    findings: list[Finding] = []
    try:
        source = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        return [Finding("error", "CODE000", str(exc), str(path))]
    if MISSING.search(source):
        add(findings, "error", "CODE001", "analysis code contains unresolved marker", str(path))
    if ABSOLUTE_PATH.search(source):
        add(findings, "error", "CODE002", "analysis code contains a user-specific absolute path", str(path))

    root = (project_root or path.parent).resolve()
    dependency_file = text((config.get("runtime") or {}).get("dependency_file"))
    if dependency_file:
        dependency_path = (root / dependency_file).resolve()
        try:
            dependency_path.relative_to(root)
        except ValueError:
            dependency_path = Path("")
        if not dependency_path.is_file():
            add(findings, "error", "CODE010", "declared dependency artifact is missing from the generated project", str(root / dependency_file))
        elif dependency_path.name.lower() in {"requirements.txt", "requirements.lock"}:
            requirement_lines = []
            invalid_lines = []
            for raw_line in dependency_path.read_text(encoding="utf-8").splitlines():
                line = raw_line.strip()
                if not line or line.startswith(("#", "--hash=", "\\")):
                    continue
                if line.startswith("--"):
                    continue
                requirement_lines.append(line)
                if not re.match(r"^[A-Za-z0-9][A-Za-z0-9_.-]*(?:\[[^]]+\])?==[^\s;\\]+(?:\s*;\s*.+)?(?:\s*\\)?$", line):
                    invalid_lines.append(line)
            if not requirement_lines or invalid_lines:
                add(findings, "error", "CODE011", "requirements dependency artifact must contain only exact package==version pins (plus comments/options/hashes)", str(dependency_path))
        elif dependency_path.name.lower() == "renv.lock":
            try:
                lock = json.loads(dependency_path.read_text(encoding="utf-8"))
                lock_r = text((lock.get("R") or {}).get("Version"))
                packages = lock.get("Packages")
                package_versions_complete = isinstance(packages, dict) and bool(packages) and all(
                    isinstance(item, dict) and text(item.get("Version")) for item in packages.values()
                )
            except (OSError, json.JSONDecodeError, AttributeError):
                lock_r = ""
                package_versions_complete = False
            expected_r = text((config.get("runtime") or {}).get("language_version"))
            if lock_r != expected_r or not package_versions_complete:
                add(findings, "error", "CODE012", "renv.lock must match runtime.language_version and contain versioned package records", str(dependency_path))

    if language == "python":
        if path.suffix.lower() != ".py":
            add(findings, "error", "CODE003", "Python analysis artifact must use .py", str(path))
        tree: ast.AST | None = None
        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            add(findings, "error", "CODE004", f"Python syntax error: {exc.msg}", f"{path}:{exc.lineno}")
        if tree is not None:
            has_failure_manifest_guard = any(
                (isinstance(node, ast.Try) and bool(node.finalbody))
                or (
                    isinstance(node, (ast.Assign, ast.AnnAssign))
                    and any(
                        isinstance(target, ast.Attribute)
                        and isinstance(target.value, ast.Name)
                        and target.value.id == "sys"
                        and target.attr == "excepthook"
                        for target in (node.targets if isinstance(node, ast.Assign) else [node.target])
                    )
                )
                or (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "atexit"
                    and node.func.attr == "register"
                )
                for node in ast.walk(tree)
            )
            if not has_failure_manifest_guard:
                add(findings, "error", "CODE013", "analysis code must preserve a machine-readable execution manifest on unhandled failure", str(path))
        try:
            semantic_source = tokenize.untokenize(
                token._replace(string="") if token.type == tokenize.COMMENT else token
                for token in tokenize.generate_tokens(io.StringIO(source).readline)
            )
        except (tokenize.TokenError, IndentationError):
            semantic_source = source
        required = {
            "config ingestion": r"analysis_config|yaml\.safe_load",
            "exact runtime check": r"platform\.python_version\s*\(.*language_version|language_version.*platform\.python_version\s*\(",
            "dependency artifact guard": r"dependency_file",
            "data ingestion": r"read_csv|read_excel|read_parquet|read_json|read_table",
            "source-row/exclusion provenance": r"source_row|exclusion_log|excluded_rows|exclusion_reason|provenance",
            "claim uncertainty interval": r"conf_int\s*\(|confidence|credible|\bci(?:95)?_(?:low|high|lo|hi)\b",
            "model diagnostics": r"converged|singular|resid|diagnostic|rhat|posterior_predict",
            "environment capture": r"importlib\.metadata|pip\s+freeze|session_info|platform\.platform|sys\.version|environment",
            "execution manifest": r"analysis-run|execution_log",
            "saved output": r"write_text|to_csv|savefig|to_json",
        }
        repeated_binary = any(
            isinstance(dv, dict) and text(dv.get("type")).lower() == "binary"
            for dv in (config.get("design", {}).get("dvs") or [])
        ) and text(config.get("design", {}).get("observation_level")).lower() in {"trial", "event"}
        if repeated_binary and re.search(r"\b(?:smf\.)?logit\s*\(", source, re.IGNORECASE):
            add(findings, "error", "CODE005", "plain Logit cannot implement repeated binary random effects", str(path))
    else:
        semantic_source = "\n".join(line.split("#", 1)[0] for line in source.splitlines())
        if path.suffix.lower() not in {".r", ".rmd", ".qmd"}:
            add(findings, "error", "CODE003", "R analysis artifact must use .R/.Rmd/.qmd", str(path))
        required = {
            "config ingestion": r"read_yaml|yaml\.load_file",
            "exact runtime check": r"R\.version.*language_version|language_version.*R\.version",
            "dependency artifact guard": r"dependency_file",
            "data ingestion": r"read_csv|read_tsv|read_excel|read_parquet|fromJSON",
            "source-row/exclusion provenance": r"source_row|exclusion_log|excluded_rows|exclusion_reason|provenance",
            "claim uncertainty interval": r"confint\s*\(|confidence|credible|\bCI_(?:low|high)\b",
            "model diagnostics": r"convergence|singular|resid|diagnostic|rhat|posterior_predict",
            "environment capture": r"sessionInfo\s*\(",
            "execution manifest": r"analysis-run|execution_log",
            "failure-safe execution manifest": r"tryCatch\s*\(|on\.exit\s*\(",
            "saved output": r"write_|ggsave|saveRDS|render",
        }
        if shutil.which("Rscript") and path.suffix.lower() == ".r":
            try:
                result = subprocess.run(
                    ["Rscript", "--vanilla", "-e", f"parse(file={json.dumps(str(path))})"],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=30,
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                add(findings, "warning", "CODE007", f"Rscript unavailable for parse validation: {exc}", str(path))
            else:
                if result.returncode:
                    detail = (result.stderr or result.stdout).strip()
                    runtime_failure = re.search(
                        r"dyld|library not loaded|not valid for use in process|library load denied|"
                        r"cannot open shared object|failed to map segment|bad cpu type",
                        detail,
                        re.IGNORECASE,
                    )
                    if runtime_failure:
                        summary = next((line.strip() for line in detail.splitlines() if line.strip()), "Rscript could not start")
                        add(findings, "warning", "CODE007", f"Rscript is installed but unusable: {summary}", str(path))
                    else:
                        summary = next((line.strip() for line in reversed(detail.splitlines()) if line.strip()), "unknown parse error")
                        add(findings, "error", "CODE006", f"R parse check failed: {summary}", str(path))
        elif not shutil.which("Rscript"):
            add(findings, "warning", "CODE007", "Rscript unavailable; R syntax/runtime not checked", str(path))

    for description, pattern in required.items():
        if not re.search(pattern, semantic_source, re.IGNORECASE):
            add(findings, "error", "CODE100", f"missing required pattern: {description}", str(path))
    return findings


def serialize(config_path: Path, code_path: Path | None, language: str | None, findings: list[Finding]) -> dict[str, Any]:
    errors = sum(finding.level == "error" for finding in findings)
    warnings = sum(finding.level == "warning" for finding in findings)
    return {
        "config": str(config_path),
        "code": str(code_path) if code_path else None,
        "language": language,
        "static_gate_passed": errors == 0,
        "analysis_plan_ready": errors == 0 and code_path is None,
        "code_static_gate_passed": errors == 0 if code_path is not None else None,
        "ready_for_execution": errors == 0 and code_path is not None,
        "ready_for_publication": False,
        "execution_and_result_review_required": True,
        "errors": errors,
        "warnings": warnings,
        "findings": [asdict(finding) for finding in findings],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path)
    parser.add_argument("--code", type=Path)
    parser.add_argument("--language", choices=("r", "python"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    config_path = args.config.resolve()
    config, findings = validate_config(config_path)
    configured_language = text((config.get("runtime") or {}).get("language")).lower() if isinstance(config.get("runtime"), dict) else ""
    language = args.language or (configured_language if configured_language in LANGUAGES else None)
    if args.code:
        suffix = args.code.suffix.lower()
        inferred_language = "python" if suffix == ".py" else "r" if suffix in {".r", ".rmd", ".qmd"} else None
        if args.language and configured_language in LANGUAGES and args.language != configured_language:
            add(findings, "error", "ENV008", "--language conflicts with config.runtime.language", str(args.code))
        if inferred_language and language and inferred_language != language:
            add(findings, "error", "CODE009", "code suffix conflicts with config/runtime language", str(args.code))
        if language:
            findings.extend(validate_code(args.code.resolve(), language, config, config_path.parent))
        else:
            add(findings, "error", "CODE008", "cannot infer analysis language; pass --language", str(args.code))
    report = serialize(config_path, args.code.resolve() if args.code else None, language, findings)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        for finding in findings:
            location = f" ({finding.location})" if finding.location else ""
            print(f"{finding.level.upper()} {finding.code}: {finding.message}{location}")
        print(f"Static analysis validation: {'PASS' if report['static_gate_passed'] else 'FAIL'} ({report['errors']} errors, {report['warnings']} warnings)")
        if report["analysis_plan_ready"]:
            print("The validated config is analysis-plan-ready; no code was reviewed, so it is not ready for execution.")
        elif report["ready_for_execution"]:
            print("The provided config and code passed deterministic static checks and are ready for execution testing.")
        print("Publication readiness requires successful execution and result review.")
    return 0 if report["static_gate_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
