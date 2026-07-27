#!/usr/bin/env python3
"""Validate PsyCoder Studio v1.4.0 records beyond JSON Schema structure."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from validate_skills import runtime_schema_validator


SCHEMAS = {
    "generation": "generation-input",
    "artifact": "artifact-output",
    "review": "review-output",
    "repair": "repair-attempt",
    "runtime-evidence": "runtime-evidence",
    "readiness": "readiness-snapshot",
}

MODEL_OWNED_FILES = {
    "psychopy": {"main.py"},
    "jspsych": {"index.html", "experiment.js"},
    "psychtoolbox": {"main.m"},
}


def canonical_json_sha256(value: Any) -> str:
    """Hash the contract's canonical UTF-8 JSON representation."""
    payload = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def schema_errors(root: Path, record_type: str, value: dict[str, Any]) -> list[str]:
    validator = runtime_schema_validator(
        root,
        f"runtime/schemas/{SCHEMAS[record_type]}.schema.json",
    )
    errors: list[str] = []
    for error in sorted(
        validator.iter_errors(value),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    ):
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"{location}: {error.message}")
    return errors


def duplicates(values: list[Any]) -> set[Any]:
    seen: set[Any] = set()
    repeated: set[Any] = set()
    for value in values:
        if value in seen:
            repeated.add(value)
        seen.add(value)
    return repeated


def execution_plan_errors(plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    project = plan.get("project", {})
    if plan.get("projectName") != project.get("name"):
        errors.append("executionPlan.projectName must equal executionPlan.project.name")

    windows = [item for item in plan.get("windows", []) if isinstance(item, dict)]
    window_ids = [item.get("id") for item in windows]
    for value in sorted(duplicates(window_ids), key=str):
        errors.append(f"executionPlan.windows has duplicate id {value!r}")
    known_windows = set(window_ids)

    sequences = [item for item in plan.get("sequences", []) if isinstance(item, dict)]
    sequence_ids = [item.get("id") for item in sequences]
    for value in sorted(duplicates(sequence_ids), key=str):
        errors.append(f"executionPlan.sequences has duplicate id {value!r}")
    sequence_orders = [item.get("order") for item in sequences]
    for value in sorted(duplicates(sequence_orders), key=str):
        errors.append(f"executionPlan.sequences has duplicate order {value!r}")
    if sequence_orders and sorted(sequence_orders) != list(range(1, len(sequence_orders) + 1)):
        errors.append("executionPlan.sequences order must be contiguous from 1")

    referenced_windows: set[Any] = set()
    order_by_window = {item.get("id"): item.get("order") for item in windows}
    for sequence in sequences:
        references = sequence.get("windowIds", [])
        unknown = [item for item in references if item not in known_windows]
        if unknown:
            errors.append(
                f"sequence {sequence.get('id')!r} references unknown windows: "
                + ", ".join(map(repr, unknown))
            )
        referenced_windows.update(references)
        known_references = [item for item in references if item in order_by_window]
        declared_orders = [order_by_window[item] for item in known_references]
        if declared_orders != sorted(declared_orders):
            errors.append(f"sequence {sequence.get('id')!r} windowIds conflict with window order")

    unreachable = sorted(known_windows - referenced_windows, key=str)
    if unreachable:
        errors.append("executionPlan contains unreachable windows: " + ", ".join(map(repr, unreachable)))

    global_response = plan.get("responses", {})
    global_keys = set(global_response.get("allowedKeys", []))
    for window in windows:
        response = window.get("response")
        if not isinstance(response, dict) or response.get("enabled") is not True:
            continue
        window_keys = set(response.get("allowedKeys", []))
        if not window_keys.issubset(global_keys):
            errors.append(
                f"window {window.get('id')!r} allows keys absent from responses.allowedKeys"
            )
        onset = response.get("rtOnset")
        if onset != "self" and onset not in known_windows:
            errors.append(f"window {window.get('id')!r} has unresolved rtOnset {onset!r}")

    global_onset = global_response.get("rtOnset")
    if global_onset != "self" and global_onset not in known_windows:
        errors.append(f"executionPlan.responses has unresolved rtOnset {global_onset!r}")

    conditions = plan.get("conditions", {})
    field_names = [
        item.get("name")
        for item in conditions.get("fields", [])
        if isinstance(item, dict)
    ]
    for value in sorted(duplicates(field_names), key=str):
        errors.append(f"executionPlan.conditions.fields has duplicate name {value!r}")

    data_names = [
        item.get("name")
        for item in plan.get("dataSchema", [])
        if isinstance(item, dict)
    ]
    for value in sorted(duplicates(data_names), key=str):
        errors.append(f"executionPlan.dataSchema has duplicate name {value!r}")

    assets = [item for item in plan.get("assets", []) if isinstance(item, dict)]
    for field in ("id", "fileName"):
        repeated = duplicates([item.get(field) for item in assets])
        for value in sorted(repeated, key=str):
            errors.append(f"executionPlan.assets has duplicate {field} {value!r}")
    return errors


def generation_errors(value: dict[str, Any]) -> list[str]:
    errors = execution_plan_errors(value.get("executionPlan", {}))
    plan = value.get("executionPlan", {})
    if value.get("target") != plan.get("target"):
        errors.append("target must exactly match executionPlan.target")
    if value.get("projectName") != plan.get("projectName"):
        errors.append("projectName must exactly match executionPlan.projectName")
    expected_hash = canonical_json_sha256(plan)
    if value.get("executionPlanHash") != expected_hash:
        errors.append("executionPlanHash does not match canonical ExecutionPlan bytes")

    summary = value.get("validationSummary", {})
    expected_total = summary.get("errorCount", 0) + summary.get("warningCount", 0) + summary.get("infoCount", 0)
    if summary.get("totalIssues") != expected_total:
        errors.append("validationSummary.totalIssues must equal errorCount + warningCount + infoCount")
    issue_codes = summary.get("topIssueCodes", [])
    if expected_total == 0 and issue_codes:
        errors.append("validationSummary.topIssueCodes must be empty when totalIssues is zero")
    if len(issue_codes) > expected_total:
        errors.append("validationSummary.topIssueCodes cannot exceed totalIssues")
    return errors


def unique_field_errors(
    value: dict[str, Any],
    array_name: str,
    field_name: str,
) -> list[str]:
    items = [item for item in value.get(array_name, []) if isinstance(item, dict)]
    repeated = duplicates([item.get(field_name) for item in items])
    return [
        f"{array_name} has duplicate {field_name} {item!r}"
        for item in sorted(repeated, key=str)
    ]


def artifact_errors(value: dict[str, Any]) -> list[str]:
    errors = unique_field_errors(value, "files", "path")
    paths = {
        item.get("path")
        for item in value.get("files", [])
        if isinstance(item, dict)
    }
    expected = MODEL_OWNED_FILES.get(value.get("platform"), set())
    missing = sorted(expected - paths)
    unexpected = sorted(paths - expected)
    if missing:
        errors.append("missing required model-owned files: " + ", ".join(missing))
    if unexpected:
        errors.append("non-allowlisted model-owned files: " + ", ".join(unexpected))
    return errors


def review_errors(value: dict[str, Any]) -> list[str]:
    errors = unique_field_errors(value, "issues", "id")
    errors.extend(unique_field_errors(value, "reviewed_files", "path"))
    scope = value.get("scope", {})
    reviewed_scope = set(scope.get("reviewed", [])) if isinstance(scope, dict) else set()
    reviewed_paths = {
        item.get("path")
        for item in value.get("reviewed_files", [])
        if isinstance(item, dict)
    }
    missing = sorted(reviewed_paths - reviewed_scope, key=str)
    if missing:
        errors.append("reviewed_files paths missing from scope.reviewed: " + ", ".join(map(repr, missing)))
    return errors


def repair_errors(value: dict[str, Any]) -> list[str]:
    errors = unique_field_errors(value, "files", "path")
    repeated = duplicates(value.get("addressed_issue_ids", []))
    for item in sorted(repeated, key=str):
        errors.append(f"addressed_issue_ids has duplicate id {item!r}")
    allowed = MODEL_OWNED_FILES.get(value.get("platform"), set())
    paths = {
        item.get("path")
        for item in value.get("files", [])
        if isinstance(item, dict)
    }
    unexpected = sorted(paths - allowed)
    if unexpected:
        errors.append("repair contains non-allowlisted files: " + ", ".join(unexpected))
    return errors


def runtime_evidence_errors(value: dict[str, Any]) -> list[str]:
    errors = unique_field_errors(value, "tests", "id")
    try:
        started = datetime.fromisoformat(value.get("started_at", ""))
        completed = datetime.fromisoformat(value.get("completed_at", ""))
        if completed < started:
            errors.append("completed_at must not precede started_at")
    except (TypeError, ValueError):
        pass
    return errors


def derive_readiness(
    root: Path,
    review: dict[str, Any],
    artifact_contract_passed: bool,
    runtime_evidence: dict[str, Any] | None,
    derived_at: str,
    require_timing_device_check: bool = False,
) -> dict[str, Any]:
    """Derive the backend-owned readiness snapshot from validated primitive facts."""
    review_validation = validate_record(root, "review", review)
    if review_validation:
        raise ValueError("cannot derive readiness from an invalid review: " + "; ".join(review_validation))

    critical = sum(
        issue.get("severity") == "critical"
        for issue in review.get("issues", [])
        if isinstance(issue, dict)
    )
    major = sum(
        issue.get("severity") == "major"
        for issue in review.get("issues", [])
        if isinstance(issue, dict)
    )
    static_passed = critical == 0 and major == 0
    packaging = static_passed and artifact_contract_passed
    blockers: list[str] = []
    if critical:
        blockers.append(f"{critical} critical review finding(s)")
    if major:
        blockers.append(f"{major} major review finding(s)")
    if not artifact_contract_passed:
        blockers.append("artifact contract, ownership, path, or hash gate failed")

    required = {
        "launch_exit",
        "full_short_session",
        "data_integrity",
        "incremental_recovery",
    }
    if require_timing_device_check:
        required.add("timing_device_check")

    smoke_status = "missing"
    if runtime_evidence is None:
        blockers.append("required target-machine runtime evidence is missing")
    else:
        evidence_validation = validate_record(root, "runtime-evidence", runtime_evidence)
        if evidence_validation:
            smoke_status = "blocked"
            blockers.append("runtime evidence is malformed or semantically inconsistent")
        elif runtime_evidence.get("artifact_set_hash") != review.get("artifact_set_hash"):
            smoke_status = "blocked"
            blockers.append("runtime evidence does not match the reviewed artifact set")
        else:
            outcomes = {
                item.get("id"): item.get("result")
                for item in runtime_evidence.get("tests", [])
                if isinstance(item, dict)
            }
            missing = sorted(required - set(outcomes))
            required_outcomes = [outcomes[item] for item in required if item in outcomes]
            if missing:
                smoke_status = "missing"
                blockers.append("missing runtime checks: " + ", ".join(missing))
            elif "failed" in required_outcomes:
                smoke_status = "failed"
                blockers.append("one or more required runtime checks failed")
            elif "blocked" in required_outcomes:
                smoke_status = "blocked"
                blockers.append("one or more required runtime checks were blocked")
            else:
                smoke_status = "passed"

    collection = packaging and smoke_status == "passed"
    snapshot = {
        "artifact_set_hash": review["artifact_set_hash"],
        "review_id": review["review_id"],
        "static_review_passed": static_passed,
        "smoke_test_status": smoke_status,
        "ready_for_packaging": packaging,
        "ready_for_collection": collection,
        "blockers": blockers,
        "derived_at": derived_at,
    }
    readiness_errors = validate_record(root, "readiness", snapshot)
    if readiness_errors:
        raise ValueError("derived readiness violates its schema: " + "; ".join(readiness_errors))
    return snapshot


def validate_record(root: Path, record_type: str, value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["<root>: record must be a JSON object"]
    errors = schema_errors(root, record_type, value)
    if errors:
        return errors
    semantic_validators = {
        "generation": generation_errors,
        "artifact": artifact_errors,
        "review": review_errors,
        "repair": repair_errors,
        "runtime-evidence": runtime_evidence_errors,
        "readiness": lambda _: [],
    }
    return semantic_validators[record_type](value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record_type", choices=sorted(SCHEMAS))
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    try:
        value = json.loads(args.path.read_text(encoding="utf-8"))
        errors = validate_record(root, args.record_type, value)
    except (OSError, json.JSONDecodeError, RuntimeError, ValueError) as exc:
        errors = [str(exc)]

    report = {
        "record_type": args.record_type,
        "path": str(args.path.resolve()),
        "valid": not errors,
        "errors": errors,
    }
    if args.json_output:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif errors:
        print(f"{args.record_type} validation failed:")
        for error in errors:
            print(f"- {error}")
    else:
        print(f"{args.record_type} record is valid.")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
