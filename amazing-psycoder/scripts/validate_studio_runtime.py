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


def experiment_model_errors(model: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    presentation = model.get("presentation", {})
    windows = [item for item in presentation.get("windows", []) if isinstance(item, dict)]
    window_ids = [item.get("id") for item in windows]
    for value in sorted(duplicates(window_ids), key=str):
        errors.append(f"experimentModel.presentation.windows has duplicate id {value!r}")
    known_windows = set(window_ids)

    sequences = [item for item in model.get("sequences", []) if isinstance(item, dict)]
    sequence_ids = [item.get("id") for item in sequences]
    for value in sorted(duplicates(sequence_ids), key=str):
        errors.append(f"experimentModel.sequences has duplicate id {value!r}")
    sequence_orders = [item.get("order") for item in sequences]
    for value in sorted(duplicates(sequence_orders), key=str):
        errors.append(f"experimentModel.sequences has duplicate order {value!r}")
    if sequence_orders and sorted(sequence_orders) != list(range(1, len(sequence_orders) + 1)):
        errors.append("experimentModel.sequences order must be contiguous from 1")

    referenced_windows: set[Any] = set()
    for sequence in sequences:
        references = sequence.get("windowIds", [])
        repeated_references = duplicates(references)
        if repeated_references:
            errors.append(
                f"sequence {sequence.get('id')!r} repeats windows: "
                + ", ".join(map(repr, sorted(repeated_references, key=str)))
            )
        unknown = [item for item in references if item not in known_windows]
        if unknown:
            errors.append(
                f"sequence {sequence.get('id')!r} references unknown windows: "
                + ", ".join(map(repr, unknown))
            )
        referenced_windows.update(references)

    unreachable = sorted(known_windows - referenced_windows, key=str)
    if unreachable:
        errors.append(
            "experimentModel contains unreachable windows: " + ", ".join(map(repr, unreachable))
        )

    tables = [item for item in model.get("conditionTables", []) if isinstance(item, dict)]
    table_ids = [item.get("id") for item in tables]
    for value in sorted(duplicates(table_ids), key=str):
        errors.append(f"experimentModel.conditionTables has duplicate id {value!r}")
    table_by_id = {item.get("id"): item for item in tables}
    columns_by_table: dict[Any, set[Any]] = {}
    for table in tables:
        columns = [item.get("name") for item in table.get("columns", []) if isinstance(item, dict)]
        for value in sorted(duplicates(columns), key=str):
            errors.append(f"conditionTable {table.get('id')!r} has duplicate column {value!r}")
        columns_by_table[table.get("id")] = set(columns)
        declared = set(columns)
        for row_index, row in enumerate(table.get("rows", [])):
            if isinstance(row, dict):
                unknown = sorted(set(row) - declared)
                if unknown:
                    errors.append(
                        f"conditionTable {table.get('id')!r} row {row_index} contains undeclared columns: "
                        + ", ".join(map(repr, unknown))
                    )

    table_for_window: dict[Any, set[Any]] = {window_id: set() for window_id in known_windows}
    for sequence in sequences:
        table_id = sequence.get("conditionTableId")
        if table_id is not None and table_id not in table_by_id:
            errors.append(
                f"sequence {sequence.get('id')!r} references unknown condition table {table_id!r}"
            )
        for window_id in sequence.get("windowIds", []):
            if window_id in table_for_window and table_id is not None:
                table_for_window[window_id].add(table_id)

    for window in windows:
        window_id = window.get("id")
        element_orders: list[Any] = []
        referenced_columns: set[Any] = set()
        for element in window.get("scene", {}).get("elements", []):
            if not isinstance(element, dict):
                continue
            element_orders.append(element.get("order"))
            for binding_name in ("content", "color", "source"):
                binding = element.get(binding_name)
                if isinstance(binding, dict) and binding.get("kind") == "condition_column":
                    referenced_columns.add(binding.get("column"))
        for value in sorted(duplicates(element_orders), key=str):
            errors.append(f"window {window_id!r} has duplicate scene element order {value!r}")
        if element_orders and sorted(element_orders) != list(range(1, len(element_orders) + 1)):
            errors.append(f"window {window_id!r} scene element order must be contiguous from 1")

        timing = window.get("timing", {})
        mode = timing.get("mode")
        if mode == "fixed" and "durationMs" not in timing:
            errors.append(f"window {window_id!r} fixed timing requires durationMs")
        if mode == "condition_column":
            column = timing.get("durationColumn")
            if not column:
                errors.append(
                    f"window {window_id!r} condition_column timing requires durationColumn"
                )
            else:
                referenced_columns.add(column)
        if mode == "manual_continue" and not timing.get("continueKeys"):
            errors.append(f"window {window_id!r} manual_continue timing requires continueKeys")

        response = window.get("response", {})
        if response.get("enabled"):
            if not response.get("allowedKeys"):
                errors.append(f"window {window_id!r} enabled response requires allowedKeys")
            correct = response.get("correctAnswer")
            if isinstance(correct, dict) and correct.get("kind") == "condition_column":
                referenced_columns.add(correct.get("column"))
        elif (
            any(
                response.get(field)
                for field in (
                    "allowedKeys",
                    "responseEndsWindow",
                    "recordResponse",
                    "recordRt",
                    "recordAccuracy",
                )
            )
            or "correctAnswer" in response
        ):
            errors.append(
                f"window {window_id!r} disabled response cannot configure response behavior"
            )
        onset = response.get("rtOnset")
        if isinstance(onset, dict) and onset.get("windowId") not in known_windows:
            errors.append(f"window {window_id!r} has unresolved rtOnset {onset.get('windowId')!r}")

        if referenced_columns:
            bound_tables = table_for_window.get(window_id, set())
            if not bound_tables:
                errors.append(
                    f"window {window_id!r} references condition columns without a bound condition table"
                )
            for table_id in bound_tables:
                missing = sorted(
                    referenced_columns - columns_by_table.get(table_id, set()), key=str
                )
                if missing:
                    errors.append(
                        f"window {window_id!r} references columns missing from condition table {table_id!r}: "
                        + ", ".join(map(repr, missing))
                    )

    data_contract = model.get("dataContract", {})
    participant_fields = [
        item for item in data_contract.get("participantFields", []) if isinstance(item, dict)
    ]
    output_fields = [
        item for item in data_contract.get("outputFields", []) if isinstance(item, dict)
    ]
    for array_name in ("participantFields", "outputFields"):
        names = [
            item.get("name") for item in data_contract.get(array_name, []) if isinstance(item, dict)
        ]
        for value in sorted(duplicates(names), key=str):
            errors.append(f"experimentModel.dataContract.{array_name} has duplicate name {value!r}")

    all_field_names = [item.get("name") for item in participant_fields + output_fields]
    for value in sorted(duplicates(all_field_names), key=str):
        errors.append(f"experimentModel.dataContract has duplicate field name {value!r}")
    for field in participant_fields:
        if field.get("source") != "participant":
            errors.append(f"participant field {field.get('name')!r} must use source 'participant'")
    for field in output_fields:
        if field.get("source") == "participant":
            errors.append(
                f"participant output {field.get('name')!r} must be declared in participantFields"
            )

    variables = [item for item in model.get("variables", []) if isinstance(item, dict)]
    variable_names = [item.get("name") for item in variables]
    for value in sorted(duplicates(variable_names), key=str):
        errors.append(f"experimentModel.variables has duplicate name {value!r}")
    variables_by_name = {item.get("name"): item for item in variables}
    for variable in variables:
        if variable.get("scope") != "experiment":
            errors.append(
                f"variable {variable.get('name')!r} uses unsupported runtime scope "
                f"{variable.get('scope')!r}; current three-platform generation supports experiment scope only"
            )
    advanced_writes_by_window: dict[str, set[str]] = {}
    for logic in model.get("advancedLogic", []):
        if not isinstance(logic, dict):
            continue
        scope = logic.get("scope", {})
        program = logic.get("program")
        if (
            scope.get("kind") != "window"
            or not scope.get("id")
            or logic.get("hook") != "after_window"
            or logic.get("reviewState") != "verified"
            or not isinstance(program, dict)
        ):
            continue
        writes = advanced_writes_by_window.setdefault(scope["id"], set())
        writes.update(
            statement.get("key")
            for statement in program.get("statements", [])
            if isinstance(statement, dict) and isinstance(statement.get("key"), str)
        )

    condition_column_names = set().union(*columns_by_table.values()) if columns_by_table else set()
    for field in output_fields:
        name = field.get("name")
        source = field.get("source")
        if source == "condition":
            if name not in condition_column_names:
                errors.append(
                    f"condition output {name!r} does not map to any real condition-table column"
                )
            if field.get("required") is True:
                for sequence in sequences:
                    table_id = sequence.get("conditionTableId")
                    if table_id is None:
                        continue
                    table = table_by_id.get(table_id)
                    if table is None:
                        continue
                    if name not in columns_by_table.get(table_id, set()):
                        errors.append(
                            f"required condition output {name!r} is missing from condition table "
                            f"{table_id!r}"
                        )
                        continue
                    missing_rows = [
                        index
                        for index, row in enumerate(table.get("rows", []))
                        if not isinstance(row, dict) or row.get(name) is None
                    ]
                    if missing_rows:
                        errors.append(
                            f"required condition output {name!r} is null or absent in condition table "
                            f"{table_id!r} rows {missing_rows!r}"
                        )
        elif source == "advanced_logic":
            variable = variables_by_name.get(name)
            if variable is None or variable.get("source") != "advanced_logic":
                errors.append(
                    f"advanced-logic output {name!r} requires a matching advanced_logic variable"
                )
            elif field.get("required") is True and "initialValue" not in variable:
                errors.append(
                    f"required advanced-logic output {name!r} requires a typed initialValue"
                )
            if not any(name in names for names in advanced_writes_by_window.values()):
                errors.append(
                    f"advanced-logic output {name!r} has no verified after-window logic writer"
                )

    reserved_state_reads = {"response", "rt_ms", "accuracy"}
    for logic in model.get("advancedLogic", []):
        if not isinstance(logic, dict):
            continue
        scope = logic.get("scope", {})
        window_id = scope.get("id") if scope.get("kind") == "window" else None
        for reference in logic.get("writes", []):
            if isinstance(reference, str) and reference.startswith("state."):
                name = reference.removeprefix("state.")
                if name not in variables_by_name:
                    errors.append(
                        f"advanced logic {logic.get('id')!r} writes undeclared state variable {name!r}"
                    )
        for reference in logic.get("reads", []):
            if not isinstance(reference, str) or "." not in reference:
                continue
            source, name = reference.split(".", 1)
            if (
                source == "state"
                and name not in variables_by_name
                and name not in reserved_state_reads
            ):
                errors.append(
                    f"advanced logic {logic.get('id')!r} reads undeclared state variable {name!r}"
                )
            if source == "condition" and window_id is not None:
                bound_tables = table_for_window.get(window_id, set())
                if not bound_tables:
                    errors.append(
                        f"advanced logic {logic.get('id')!r} reads condition column {name!r} "
                        "without a bound condition table"
                    )
                for table_id in bound_tables:
                    if name not in columns_by_table.get(table_id, set()):
                        errors.append(
                            f"advanced logic {logic.get('id')!r} reads missing condition column "
                            f"{name!r} from table {table_id!r}"
                        )

    windows_by_id = {item.get("id"): item for item in windows}

    def window_produces_observation(window: dict[str, Any], sequence: dict[str, Any]) -> bool:
        table = table_by_id.get(sequence.get("conditionTableId"))
        table_columns = columns_by_table.get(sequence.get("conditionTableId"), set())
        response = window.get("response", {})
        for field in output_fields:
            source = field.get("source")
            name = field.get("name")
            if (
                source == "condition"
                and data_contract.get("savePolicy") == "incremental_trial"
                and table is not None
                and name in table_columns
            ):
                return True
            if source == "advanced_logic" and name in advanced_writes_by_window.get(
                window.get("id"), set()
            ):
                return True
            if source == "system" and (
                name == "window_id" or (name == "onset" and response.get("recordOnset") is True)
            ):
                return True
            if source == "response":
                flag = (
                    "recordResponse"
                    if name in {"response", "response_key"}
                    else "recordRt"
                    if name in {"rt", "rt_ms"}
                    else "recordAccuracy"
                    if name in {"accuracy", "correct"}
                    else None
                )
                if flag and response.get(flag) is True:
                    return True
        return False

    if data_contract.get("savePolicy") == "incremental_window" and output_fields:
        has_explicit_writer = any(
            window_produces_observation(window, sequence)
            for sequence in sequences
            for window_id in sequence.get("windowIds", [])
            if (window := windows_by_id.get(window_id)) is not None
        )
        if not has_explicit_writer:
            errors.append(
                "incremental_window requires at least one explicit system, response, "
                "or advanced-logic writer"
            )

    if data_contract.get("savePolicy") == "incremental_trial":

        def has_output(source: str, names: set[str]) -> bool:
            return any(
                item.get("source") == source and item.get("name") in names for item in output_fields
            )

        for sequence in sequences:
            sequence_windows = [
                windows_by_id[window_id]
                for window_id in sequence.get("windowIds", [])
                if window_id in windows_by_id
            ]
            for declared, flag, label in (
                (
                    has_output("response", {"response", "response_key"}),
                    "recordResponse",
                    "response",
                ),
                (has_output("response", {"rt", "rt_ms"}), "recordRt", "RT"),
                (has_output("response", {"accuracy", "correct"}), "recordAccuracy", "accuracy"),
                (has_output("system", {"onset"}), "recordOnset", "onset"),
            ):
                writer_count = sum(
                    1 for window in sequence_windows if window.get("response", {}).get(flag) is True
                )
                if declared and writer_count > 1:
                    errors.append(
                        f"sequence {sequence.get('id')!r} has {writer_count} windows writing {label} "
                        "into one incremental_trial field; use incremental_window or keep one writer"
                    )
                required = any(
                    item.get("source") == ("system" if label == "onset" else "response")
                    and item.get("name")
                    in (
                        {"response", "response_key"}
                        if label == "response"
                        else {"rt", "rt_ms"}
                        if label == "RT"
                        else {"accuracy", "correct"}
                        if label == "accuracy"
                        else {"onset"}
                    )
                    and item.get("required") is True
                    for item in output_fields
                )
                produces_observation = any(
                    window_produces_observation(window, sequence) for window in sequence_windows
                )
                total_writers = sum(
                    1 for window in windows if window.get("response", {}).get(flag) is True
                )
                if required and total_writers == 0:
                    errors.append(f"data contract has no writer for required {label} output")
                elif required and produces_observation and writer_count == 0:
                    errors.append(
                        f"sequence {sequence.get('id')!r} has no writer for required {label} output"
                    )
            if has_output("system", {"window_id"}) and len(sequence_windows) > 1:
                errors.append(
                    f"sequence {sequence.get('id')!r} cannot write one window_id field for "
                    "multiple windows in incremental_trial mode"
                )
    elif data_contract.get("savePolicy") == "incremental_window":
        required_writers = (
            ("response", {"response", "response_key"}, "recordResponse"),
            ("response", {"rt", "rt_ms"}, "recordRt"),
            ("response", {"accuracy", "correct"}, "recordAccuracy"),
            ("system", {"onset"}, "recordOnset"),
        )
        for source, names, flag in required_writers:
            if not any(
                item.get("source") == source
                and item.get("name") in names
                and item.get("required") is True
                for item in output_fields
            ):
                continue
            if not any(window.get("response", {}).get(flag) is True for window in windows):
                errors.append(f"data contract has no writer for required {sorted(names)!r} output")
                continue
            for window in windows:
                sequence_id = next(
                    (
                        item.get("id")
                        for item in sequences
                        if window.get("id") in item.get("windowIds", [])
                    ),
                    None,
                )
                sequence = next((item for item in sequences if item.get("id") == sequence_id), None)
                if (
                    sequence is not None
                    and window_produces_observation(window, sequence)
                    and window.get("response", {}).get(flag) is not True
                ):
                    errors.append(
                        f"window {window.get('id')!r} has no writer for required "
                        f"{sorted(names)!r} incremental-window output"
                    )

    assets = [item for item in model.get("assets", []) if isinstance(item, dict)]
    for field in ("id", "path"):
        repeated = duplicates([item.get(field) for item in assets])
        for value in sorted(repeated, key=str):
            errors.append(f"experimentModel.assets has duplicate {field} {value!r}")
    for index, asset in enumerate(assets):
        if not isinstance(asset.get("sizeBytes"), int) or asset.get("sizeBytes", 0) < 1:
            errors.append(f"experimentModel.assets[{index}].sizeBytes must be a positive integer")

    known_assets = {item.get("id") for item in assets}
    font_asset_id = presentation.get("display", {}).get("fontPolicy", {}).get("assetId")
    if font_asset_id is not None and font_asset_id not in known_assets:
        errors.append(f"presentation.display.fontPolicy references unknown asset {font_asset_id!r}")

    for logic in model.get("advancedLogic", []):
        if not isinstance(logic, dict):
            continue
        unsupported = [
            platform
            for platform in model.get("targets", [])
            if logic.get("support", {}).get(platform) != "supported"
        ]
        if unsupported:
            errors.append(
                f"advanced logic {logic.get('id')!r} is unsupported for targets: "
                + ", ".join(map(str, unsupported))
            )
    return errors


def generation_errors(value: dict[str, Any]) -> list[str]:
    model = value.get("experimentModel", {})
    errors = experiment_model_errors(model)
    target = value.get("target", {}).get("platform")
    if target not in model.get("targets", []):
        errors.append("target.platform must be declared in experimentModel.targets")
    if value.get("projectName") != model.get("metadata", {}).get("name"):
        errors.append("projectName must exactly match experimentModel.metadata.name")
    expected_model_hash = canonical_json_sha256(model)
    if value.get("modelHash") != expected_model_hash:
        errors.append("modelHash does not match canonical ExperimentModel@4 bytes")

    asset_manifest = value.get("assetManifest", [])
    expected_asset_hash = canonical_json_sha256(asset_manifest)
    if value.get("assetSetHash") != expected_asset_hash:
        errors.append("assetSetHash does not match canonical assetManifest bytes")
    manifest_by_id = {item.get("id"): item for item in asset_manifest if isinstance(item, dict)}
    model_assets = {
        item.get("id"): item for item in model.get("assets", []) if isinstance(item, dict)
    }
    if set(manifest_by_id) != set(model_assets):
        errors.append("assetManifest ids must exactly match experimentModel.assets ids")
    for asset_id in sorted(set(manifest_by_id).intersection(model_assets), key=str):
        if manifest_by_id[asset_id] != model_assets[asset_id]:
            errors.append(
                f"assetManifest entry {asset_id!r} must exactly match experimentModel.assets"
            )

    summary = value.get("validationSummary", {})
    expected_total = (
        summary.get("errorCount", 0) + summary.get("warningCount", 0) + summary.get("infoCount", 0)
    )
    if summary.get("totalIssues") != expected_total:
        errors.append(
            "validationSummary.totalIssues must equal errorCount + warningCount + infoCount"
        )
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
        f"{array_name} has duplicate {field_name} {item!r}" for item in sorted(repeated, key=str)
    ]


def artifact_errors(value: dict[str, Any]) -> list[str]:
    errors = unique_field_errors(value, "files", "path")
    paths = {item.get("path") for item in value.get("files", []) if isinstance(item, dict)}
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
        item.get("path") for item in value.get("reviewed_files", []) if isinstance(item, dict)
    }
    missing = sorted(reviewed_paths - reviewed_scope, key=str)
    if missing:
        errors.append(
            "reviewed_files paths missing from scope.reviewed: " + ", ".join(map(repr, missing))
        )
    return errors


def repair_errors(value: dict[str, Any]) -> list[str]:
    errors = unique_field_errors(value, "files", "path")
    repeated = duplicates(value.get("addressed_issue_ids", []))
    for item in sorted(repeated, key=str):
        errors.append(f"addressed_issue_ids has duplicate id {item!r}")
    allowed = MODEL_OWNED_FILES.get(value.get("platform"), set())
    paths = {item.get("path") for item in value.get("files", []) if isinstance(item, dict)}
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
        raise ValueError(
            "cannot derive readiness from an invalid review: " + "; ".join(review_validation)
        )

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
