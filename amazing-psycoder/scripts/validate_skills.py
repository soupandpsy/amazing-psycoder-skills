#!/usr/bin/env python3
"""Validate Amazing PsyCoder manifests, links, fences, and system contracts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

try:
    from jsonschema import FormatChecker
    from jsonschema.validators import validator_for
    from referencing import Registry, Resource
except ImportError:  # reported as a validation error with installation guidance
    FormatChecker = None
    Registry = None
    Resource = None
    validator_for = None


SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER = re.compile(r"\bv(\d+\.\d+\.\d+)\b")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
FRONTMATTER_KEY = re.compile(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$")
QUOTED_FIELD = re.compile(r'^\s{2}(display_name|short_description|default_prompt):\s+(["\'])(.*)\2\s*$')
FORBIDDEN_CONTRACTS = (
    (re.compile(r"Time-to-event\s*\(Stop-signal\)", re.IGNORECASE), "SSRT must not be routed to ordinary survival analysis"),
    (re.compile(r"(?:Cox[^\n]{0,80}(?:examine|predict|model)[^\n]{0,80}(?:SSRT|stop-signal reaction time)|Log-?Rank[^\n]{0,80}(?:compare|test)[^\n]{0,80}(?:SSRT|stop-signal))", re.IGNORECASE), "SSRT must not be presented as an ordinary Cox/Log-Rank outcome"),
    (re.compile(r"statsmodels\.Logit\(\)\s*/\s*pymer4", re.IGNORECASE), "plain Logit must not be presented as a GLMM implementation"),
    (re.compile(r"config YAML \(internal artifact, not shown", re.IGNORECASE), "configs must be saved and their paths reported"),
    (re.compile(r"config YAML is never shown", re.IGNORECASE), "configs must remain inspectable by the user"),
    (re.compile(r"default to PsychoPy", re.IGNORECASE), "ambiguous platforms must not be silently assumed"),
    (re.compile(r"(?:backend|keyboard)[^\n]{0,100}\b50\s*[-–]\s*70\s*ms\b|\b50\s*[-–]\s*70\s*ms\b[^\n]{0,100}(?:backend|keyboard)", re.IGNORECASE), "fixed backend latency claims require context-specific evidence"),
    (re.compile(r"(?:waitRelease|key[- ]release)[^\n]{0,100}\b100\s*[-–]\s*200\s*ms\b|\b100\s*[-–]\s*200\s*ms\b[^\n]{0,100}(?:waitRelease|key[- ]release)", re.IGNORECASE), "fixed key-release delay claims require context-specific evidence"),
    (re.compile(r"ratio error\s*>\s*(?:10|20)", re.IGNORECASE), "severity must be impact-based, not an arbitrary percentage"),
    (re.compile(r"\b(?:acc|accuracy)\s*=\s*-1\b", re.IGNORECASE), "missing or timeout accuracy must not use a numeric sentinel"),
    (re.compile(r"system guarantees code quality", re.IGNORECASE), "the system must report evidence limits rather than guarantee correctness"),
    (re.compile(r"globals\s*\(\s*\)[^\n]{0,80}(?:recommended|推荐)|(?:recommended|推荐)[^\n]{0,80}globals\s*\(\s*\)", re.IGNORECASE), "namespace injection must not be recommended"),
    (re.compile(r"every test must output effect size via pingouin", re.IGNORECASE), "effect estimates must follow the estimand; no single package is universally required"),
    (re.compile(r"default[^\n]{0,80}correction\s*=\s*Bonferroni", re.IGNORECASE), "multiplicity handling must follow a declared claim family, not a universal default"),
    (re.compile(r"anticipatory responses[^\n]{0,80}RT\s*<\s*100\s*ms", re.IGNORECASE), "anticipation thresholds must be task/device-derived rather than universal"),
    (re.compile(r"every string in generated experiment code must use the language", re.IGNORECASE), "scientific stimuli and machine-readable tokens must not be auto-translated"),
    (re.compile(r"Windows[^\n]{0,120}(?:±|\+/-)\s*10\s*[-–]\s*15\s*ms\s+jitter", re.IGNORECASE), "fixed platform jitter claims require current target-hardware evidence"),
    (re.compile(r"Little'?s?[^\n]{0,120}(?:not significant|non-?significant)[^\n]{0,120}(?:consistent with|supports?)[^\n]{0,40}MAR", re.IGNORECASE), "a non-significant MCAR test does not establish MAR"),
    (re.compile(r"conventional threshold for (?:a )?medium effect size", re.IGNORECASE), "predictive metrics require domain/decision interpretation, not universal magnitude cutoffs"),
    (re.compile(r'"ready_for_execution"\s*:\s*errors\s*==\s*0\s*,', re.IGNORECASE), "config-only validation must not imply execution readiness"),
    (re.compile(r"\b(?:RANDOM_SEED|randomSeed)\s*=\s*42\b"), "generation references must resolve seeds from the confirmed scope rather than copy a universal seed"),
    (re.compile(r"Levene[^\n]{0,120}p\s*>\s*0?\.0?5[^\n]{0,120}(?:Student|ANOVA)|Levene[^\n]{0,120}p\s*<\s*0?\.0?5[^\n]{0,120}Welch", re.IGNORECASE), "Levene p-values must not mechanically select the variance model"),
    (re.compile(r"library\s*\(\s*retimes\s*\)|\bretimes::", re.IGNORECASE), "the archived retimes package must not be a maintained generation dependency"),
    (re.compile(r'"smoke_test_evidence"\s*:\s*\[\s*"', re.IGNORECASE), "runtime readiness requires structured per-test evidence, not a summary string"),
)
REQUIRED_CONTRACTS = {
    "SKILL.md": ("## Evidence State Model", "## Execution Profiles", "STANDALONE.md", "scripts/validate_analysis.py"),
    "STANDALONE.md": ("## Capability Boundary", "user workspace", "runtime/capabilities.json"),
    "PSYCODER_STUDIO.md": ("machine-readable `runtime/`", "Reviewer never returns rewritten files", "scripts/validate_studio_runtime.py"),
    "psy-ana-designer/SKILL.md": ("estimand", "selected_method", "scripts/validate_analysis.py", "exact language version"),
    "psy-ana-coder/SKILL.md": ("ready_for_execution", "scripts/validate_analysis.py", "Authoritative-source boundary", "dependency_file"),
    "psy-ana-coder/python/demo/README.md": ("not generation templates", "Do not load, copy, validate, or adapt"),
    "psy-ana-coder/r/demo/README.md": ("not generation templates", "Do not load, copy, validate, or adapt"),
    "psy-ana-designer/methods/USAGE.md": ("candidate reminders", "never override"),
    "psy-ana-designer/plots/USAGE.md": ("visual-design reminders", "not publication evidence"),
    "psy-ana-reviewer/SKILL.md": ("result-audit", "ready_for_publication", "ready_for_execution"),
    "psy-exp-designer/SKILL.md": ("scripts/validate_experiment.py", "Decision Registry"),
    "psy-exp-coder/SKILL.md": ("generate", "modify", "debug"),
    "psy-exp-reviewer/SKILL.md": ("smoke test", "ready_for_collection", "RuntimeEvidence"),
    "psy-exp-designer/references/config-schema.md": ("runtime:", "framework_version", "response_event", "seed_scope", "record_resolved_seed", "{run_id}"),
    "psy-ana-designer/references/config-schema.md": ('version: "1.2"', "runtime:", "language_version", "dependency_strategy", "dependency_file", "loader_options", "model_formula", "dependence_structure"),
    "psy-exp-designer/references/data-recording.md": ("response status", "linked event table", "never encode missing RT"),
    "scripts/validate_experiment.py": ("ready_for_collection\": False", "pre_code_ready", "ENV001", "WIN007", "WIN010", "WIN011", "RND004", "OUT005"),
    "scripts/validate_analysis.py": ("ready_for_publication\": False", "analysis_plan_ready", "Q007", "CODE005", "CODE010", "CODE011", "CODE013", "ENV002", "ENV005", "ENV009", "DATA009"),
    "psy-exp-reviewer/references/review-report-schema.md": ("RuntimeEvidence", "FileObject", "launch_exit", "incremental_recovery", "evidence_paths", "sha256"),
    "psy-exp-coder/jspsych/spec/README.md": ("jspsych@8.2.3", "evaluateTimelineVariable", "abortExperiment"),
}

RUNTIME_FILES = (
    "runtime/manifest.json",
    "runtime/profiles.json",
    "runtime/capabilities.json",
    "runtime/paradigm-aliases.json",
    "runtime/routing.json",
    "runtime/primitives.json",
    "runtime/artifacts/psychopy.json",
    "runtime/artifacts/jspsych.json",
    "runtime/artifacts/psychtoolbox.json",
    "runtime/schemas/designer-output.schema.json",
    "runtime/schemas/generation-input.schema.json",
    "runtime/schemas/interpreter-output.schema.json",
    "runtime/schemas/execution-plan.schema.json",
    "runtime/schemas/artifact-output.schema.json",
    "runtime/schemas/review-output.schema.json",
    "runtime/schemas/repair-attempt.schema.json",
    "runtime/schemas/runtime-evidence.schema.json",
    "runtime/schemas/readiness-snapshot.schema.json",
)

CONTRACT_VERSION_FILES = (
    "runtime/manifest.json",
    "runtime/profiles.json",
    "runtime/capabilities.json",
    "runtime/routing.json",
    "runtime/primitives.json",
)

MODEL_ARTIFACTS = {
    "psychopy": {"main.py"},
    "jspsych": {"index.html", "experiment.js"},
    "psychtoolbox": {"main.m"},
}


def runtime_schema_validator(root: Path, relative: str):
    """Return a Draft 2020-12 validator with every local runtime schema registered."""
    if validator_for is None or Registry is None or Resource is None or FormatChecker is None:
        raise RuntimeError("jsonschema is required: python -m pip install jsonschema")

    schemas: dict[str, dict] = {}
    registry = Registry()
    for schema_path in sorted((root / "runtime" / "schemas").glob("*.schema.json")):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str) or not schema_id:
            raise ValueError(f"{schema_path}: schema requires a non-empty $id")
        schemas[str(schema_path.relative_to(root))] = schema
        registry = registry.with_resource(schema_id, Resource.from_contents(schema))

    schema = schemas[relative]
    validator_class = validator_for(schema)
    validator_class.check_schema(schema)
    return validator_class(schema, registry=registry, format_checker=FormatChecker())


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("SKILL.md must start with ---")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("frontmatter is missing its closing ---") from exc

    raw = lines[1:end]
    values: dict[str, str] = {}
    current: str | None = None
    for line in raw:
        match = FRONTMATTER_KEY.match(line)
        if match and not line.startswith((" ", "\t")):
            current = match.group(1)
            value = (match.group(2) or "").strip()
            values[current] = "" if value in {">", ">-", "|", "|-"} else value.strip('"\'')
        elif current and line.startswith((" ", "\t")):
            values[current] = f"{values[current]} {line.strip()}".strip()
        elif line.strip():
            raise ValueError(f"unsupported frontmatter syntax: {line}")
    return values, lines[end + 1 :]


def parse_openai_yaml(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "interface:":
        raise ValueError("agents/openai.yaml must start with interface:")
    for line in lines[1:]:
        if not line.strip():
            continue
        match = QUOTED_FIELD.match(line)
        if not match:
            raise ValueError(f"unsupported or unquoted interface field: {line}")
        values[match.group(1)] = match.group(3)
    return values


def direct_link_errors(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for match in MARKDOWN_LINK.finditer(text):
        raw = match.group(1).strip()
        if not raw or raw.startswith(("#", "http://", "https://", "mailto:", "data:")):
            continue
        target = raw.split("#", 1)[0].strip("<>")
        if not target:
            continue
        destination = (path.parent / unquote(target)).resolve()
        if not destination.exists():
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"{path}:{line}: broken local link {raw}")
    return errors


def fence_errors(path: Path) -> list[str]:
    markers = sum(
        1
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines()
        if line.lstrip().startswith("```")
    )
    if markers % 2:
        return [f"{path}: unbalanced fenced-code markers ({markers})"]
    return []


def headings_inside_fences(path: Path) -> list[str]:
    """Reject the review-gate failure mode where a rule heading enters a code block."""
    errors: list[str] = []
    inside = False
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if line.lstrip().startswith("```"):
            inside = not inside
        elif inside and re.match(r"^#{1,6}\s+Rule\b", line):
            errors.append(f"{path}:{number}: review rule heading is inside a fenced code block")
    return errors


def semantic_contract_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for relative, markers in REQUIRED_CONTRACTS.items():
        path = root / relative
        try:
            content = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{path}: {exc}")
            continue
        for marker in markers:
            if marker not in content:
                errors.append(f"{path}: missing required system contract marker {marker!r}")

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".py", ".yaml", ".yml"}:
            continue
        relative_parts = path.relative_to(root).parts
        if "_raw" in relative_parts or "demo" in relative_parts or "tests" in relative_parts or ".pytest_cache" in relative_parts or path == Path(__file__).resolve():
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        for pattern, message in FORBIDDEN_CONTRACTS:
            match = pattern.search(content)
            if match:
                line = content.count("\n", 0, match.start()) + 1
                errors.append(f"{path}:{line}: {message}")

    gate = root / "psy-exp-reviewer" / "references" / "review-gate.md"
    if gate.exists():
        errors.extend(headings_inside_fences(gate))
        gate_text = gate.read_text(encoding="utf-8")
        positions = [gate_text.find(f"### Rule {number}:") for number in range(1, 6)]
        if any(position < 0 for position in positions) or positions != sorted(positions):
            errors.append(f"{gate}: Rule 1..5 headings must exist in order")
    return errors


def runtime_contract_errors(root: Path, *, require_jsonschema: bool = True) -> list[str]:
    errors: list[str] = []
    values: dict[str, dict] = {}
    for relative in RUNTIME_FILES:
        path = root / relative
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{path}: top-level JSON value must be an object")
            continue
        values[relative] = value

    manifest = values.get("runtime/manifest.json", {})
    profiles = values.get("runtime/profiles.json", {})
    capabilities = values.get("runtime/capabilities.json", {})
    root_skill = (root / "SKILL.md").read_text(encoding="utf-8", errors="replace")

    skill_version = manifest.get("skillVersion")
    if not isinstance(skill_version, str) or f"v{skill_version}" not in root_skill:
        errors.append(f"{root / 'runtime/manifest.json'}: skillVersion must match the root SKILL.md version")
    if skill_version != "1.4.0":
        errors.append(f"{root / 'runtime/manifest.json'}: unified skillVersion must be 1.4.0")

    for skill_file in [root / "SKILL.md", *sorted(root.glob("*/SKILL.md"))]:
        match = SEMVER.search(skill_file.read_text(encoding="utf-8", errors="replace"))
        if not match or match.group(1) != skill_version:
            errors.append(f"{skill_file}: skill version must match manifest skillVersion v{skill_version}")

    contract_version = manifest.get("contractVersion")
    if contract_version != "1.4.0":
        errors.append(f"{root / 'runtime/manifest.json'}: unified contractVersion must be 1.4.0")
    for relative in CONTRACT_VERSION_FILES:
        value = values.get(relative, {})
        if value.get("contractVersion") != contract_version:
            errors.append(f"{root / relative}: contractVersion must match manifest contractVersion {contract_version!r}")

    serialization = manifest.get("serialization", {})
    if not isinstance(serialization, dict) or serialization.get("executionModel") != "ExecutionPlan@2.0":
        errors.append(f"{root / 'runtime/manifest.json'}: executionModel must be ExecutionPlan@2.0")

    contracts = manifest.get("contracts", {})
    if not isinstance(contracts, dict):
        errors.append(f"{root / 'runtime/manifest.json'}: contracts must map record names to schemas")
    else:
        for name, relative in contracts.items():
            if not isinstance(relative, str) or relative not in values:
                errors.append(f"{root / 'runtime/manifest.json'}: invalid contract path for {name!r}: {relative!r}")

    schema_files = tuple(item for item in RUNTIME_FILES if "/schemas/" in item)
    schema_backend_available = all(
        item is not None for item in (validator_for, Registry, Resource, FormatChecker)
    )
    if schema_backend_available:
        for relative in schema_files:
            try:
                runtime_schema_validator(root, relative)
            except Exception as exc:
                errors.append(f"{root / relative}: invalid or unresolved JSON Schema: {exc}")
    elif require_jsonschema:
        errors.append(
            f"{root / 'runtime/schemas'}: full JSON Schema graph validation requires "
            "jsonschema and referencing; install the development requirements or "
            "use --portable for installation-only checks"
        )
    else:
        # Installation must remain possible in a plain Python environment. This
        # fallback verifies JSON parsing and schema identity only; release/CI
        # validation still uses the full jsonschema graph above.
        for relative in schema_files:
            schema = values.get(relative, {})
            if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
                errors.append(f"{root / relative}: portable check requires JSON Schema draft 2020-12")
            if not isinstance(schema.get("$id"), str) or not schema.get("$id"):
                errors.append(f"{root / relative}: portable check requires a non-empty $id")

    execution_schema = values.get("runtime/schemas/execution-plan.schema.json", {})
    schema_version = execution_schema.get("properties", {}).get("schemaVersion", {}).get("const")
    if schema_version != "2.0":
        errors.append(f"{root / 'runtime/schemas/execution-plan.schema.json'}: schemaVersion must be 2.0")

    generation_schema = values.get("runtime/schemas/generation-input.schema.json", {})
    valid_contract = generation_schema.get("properties", {}).get("validationSummary", {}).get("properties", {})
    if valid_contract.get("valid", {}).get("const") is not True or valid_contract.get("errorCount", {}).get("const") != 0:
        errors.append(f"{root / 'runtime/schemas/generation-input.schema.json'}: generation requires valid=true and errorCount=0")

    review_properties = values.get("runtime/schemas/review-output.schema.json", {}).get("properties", {})
    forbidden_review_fields = {
        "repairs_applied",
        "issues_before_repair",
        "issues_after_repair",
        "static_review_passed",
        "smoke_test_status",
        "ready_for_packaging",
        "ready_for_collection",
    }
    leaked = sorted(forbidden_review_fields.intersection(review_properties))
    if leaked:
        errors.append(f"{root / 'runtime/schemas/review-output.schema.json'}: read-only review leaks derived/mutation fields: {', '.join(leaked)}")
    if manifest.get("profilesPath") != "runtime/profiles.json":
        errors.append(f"{root / 'runtime/manifest.json'}: profilesPath must point to runtime/profiles.json")
    migration_guide = manifest.get("migrationGuide")
    if not isinstance(migration_guide, str) or not (root / migration_guide).is_file():
        errors.append(f"{root / 'runtime/manifest.json'}: migrationGuide must point to a readable file")
    if profiles.get("defaultProfile") != "standalone":
        errors.append(f"{root / 'runtime/profiles.json'}: standalone must be the default profile")
    declared_profiles = profiles.get("profiles")
    if not isinstance(declared_profiles, dict) or not {"standalone", "studio"}.issubset(declared_profiles):
        errors.append(f"{root / 'runtime/profiles.json'}: standalone and studio profiles are required")
    if capabilities.get("scope") != "psycoder_studio_deployment":
        errors.append(f"{root / 'runtime/capabilities.json'}: capability scope must be explicit")

    if capabilities.get("capabilityModel") != "platform_adapter":
        errors.append(f"{root / 'runtime/capabilities.json'}: capabilityModel must be platform_adapter")
    for platform in capabilities.get("platforms", []):
        if not isinstance(platform, dict):
            errors.append(f"{root / 'runtime/capabilities.json'}: every platform must be an object")
            continue
        artifact = platform.get("artifactContract")
        if not isinstance(artifact, str) or artifact not in values:
            errors.append(f"{root / 'runtime/capabilities.json'}: invalid artifactContract {artifact!r}")
    for profile in capabilities.get("verifiedGenerationProfiles", []):
        if not isinstance(profile, dict) or not isinstance(profile.get("id"), str):
            errors.append(f"{root / 'runtime/capabilities.json'}: every generation profile needs an id")
            continue
        artifact = profile.get("artifactContract")
        if not isinstance(artifact, str) or artifact not in values:
            errors.append(f"{root / 'runtime/capabilities.json'}: invalid profile artifactContract {artifact!r}")

    for platform, expected_model_paths in MODEL_ARTIFACTS.items():
        relative = f"runtime/artifacts/{platform}.json"
        contract = values.get(relative, {})
        files = contract.get("files", [])
        if not isinstance(files, list):
            errors.append(f"{root / relative}: files must be an array")
            continue
        paths = [item.get("path") for item in files if isinstance(item, dict)]
        if len(paths) != len(set(paths)):
            errors.append(f"{root / relative}: artifact paths must be unique")
        priorities = [item.get("priority") for item in files if isinstance(item, dict)]
        if len(priorities) != len(set(priorities)):
            errors.append(f"{root / relative}: artifact priorities must be unique")
        invalid_owners = sorted(
            {
                item.get("owner")
                for item in files
                if isinstance(item, dict) and item.get("owner") not in {"model", "compiler"}
            },
            key=str,
        )
        if invalid_owners:
            errors.append(f"{root / relative}: invalid artifact owners: {invalid_owners}")
        model_paths = {
            item.get("path")
            for item in files
            if isinstance(item, dict) and item.get("owner") == "model"
        }
        if model_paths != expected_model_paths:
            errors.append(
                f"{root / relative}: model-owned paths must be {sorted(expected_model_paths)!r}, "
                f"got {sorted(model_paths)!r}"
            )
        audit = next(
            (item for item in files if isinstance(item, dict) and item.get("path") == "audit_report.md"),
            None,
        )
        if not audit or audit.get("owner") != "compiler":
            errors.append(f"{root / relative}: audit_report.md must be compiler-rendered")

    routing = values.get("runtime/routing.json", {}).get("stages", {})
    if isinstance(routing, dict):
        substitutions = {
            "platform": "psychopy",
            "designerParadigm": "stroop",
            "coderParadigm": "stroop",
        }
        for stage in ("interpreter", "code_generator", "reviewer"):
            templates = routing.get(stage)
            if not isinstance(templates, list):
                errors.append(f"{root / 'runtime/routing.json'}: missing stage {stage}")
                continue
            for template in templates:
                try:
                    relative = str(template).format(**substitutions)
                except (KeyError, ValueError) as exc:
                    errors.append(f"{root / 'runtime/routing.json'}: invalid route {template!r}: {exc}")
                    continue
                if not (root / relative).is_file():
                    errors.append(f"{root / 'runtime/routing.json'}: routed file does not exist: {relative}")
    else:
        errors.append(f"{root / 'runtime/routing.json'}: stages must be an object")
    return errors


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    try:
        frontmatter, body = parse_frontmatter(skill_file)
    except (OSError, ValueError) as exc:
        return [f"{skill_file}: {exc}"]

    unexpected = sorted(set(frontmatter) - {"name", "description"})
    if unexpected:
        errors.append(f"{skill_file}: unexpected frontmatter keys: {', '.join(unexpected)}")

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if name != skill_dir.name:
        errors.append(f"{skill_file}: name {name!r} does not match directory {skill_dir.name!r}")
    if not SKILL_NAME.fullmatch(name):
        errors.append(f"{skill_file}: invalid skill name {name!r}")
    if not 1 <= len(description) <= 1024:
        errors.append(f"{skill_file}: description length must be 1..1024, got {len(description)}")
    if len(body) >= 500:
        errors.append(f"{skill_file}: body must be under 500 lines, got {len(body)}")

    metadata_file = skill_dir / "agents" / "openai.yaml"
    try:
        metadata = parse_openai_yaml(metadata_file)
    except (OSError, ValueError) as exc:
        errors.append(f"{metadata_file}: {exc}")
    else:
        required = {"display_name", "short_description", "default_prompt"}
        missing = sorted(required - set(metadata))
        if missing:
            errors.append(f"{metadata_file}: missing fields: {', '.join(missing)}")
        short = metadata.get("short_description", "")
        if short and not 25 <= len(short) <= 64:
            errors.append(f"{metadata_file}: short_description must be 25..64 characters, got {len(short)}")
        prompt = metadata.get("default_prompt", "")
        if prompt and f"${name}" not in prompt:
            errors.append(f"{metadata_file}: default_prompt must mention ${name}")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate Amazing PsyCoder skills and system contracts."
    )
    parser.add_argument(
        "--portable",
        action="store_true",
        help=(
            "run installation-safe checks without requiring third-party Python packages; "
            "release validation must omit this flag"
        ),
    )
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parents[1]
    skill_dirs = [root, *sorted(path.parent for path in root.glob("*/SKILL.md"))]
    errors: list[str] = []
    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir))
    for markdown_file in root.rglob("*.md"):
        errors.extend(direct_link_errors(markdown_file))
        errors.extend(fence_errors(markdown_file))
    errors.extend(semantic_contract_errors(root))
    errors.extend(runtime_contract_errors(root, require_jsonschema=not args.portable))

    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    mode = "portable installation contracts" if args.portable else "full schema and system contracts"
    print(f"Validated {len(skill_dirs)} skills: manifests, metadata, links, fences, and {mode}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
