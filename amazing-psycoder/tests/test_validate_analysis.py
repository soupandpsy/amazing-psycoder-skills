from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_analysis.py"
FIXTURE = ROOT / "tests" / "fixtures" / "valid-analysis" / "config.yaml"
SPEC = importlib.util.spec_from_file_location("validate_analysis", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


class AnalysisConfigTests(unittest.TestCase):
    def validate_copy(self, old: str, new: str):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.yaml"
            path.write_text(FIXTURE.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")
            return validator.validate_config(path)

    def test_valid_config_is_plan_ready_but_not_execution_ready(self) -> None:
        _, findings = validator.validate_config(FIXTURE)
        self.assertEqual([], [item for item in findings if item.level == "error"])
        report = validator.serialize(FIXTURE, None, "python", findings)
        self.assertTrue(report["static_gate_passed"])
        self.assertTrue(report["analysis_plan_ready"])
        self.assertIsNone(report["code_static_gate_passed"])
        self.assertFalse(report["ready_for_execution"])
        self.assertFalse(report["ready_for_publication"])

    def test_previous_schema_version_is_rejected(self) -> None:
        _, findings = self.validate_copy('version: "1.2"', 'version: "1.1"')
        self.assertIn("ANA004", {item.code for item in findings})

    def test_code_scope_can_be_execution_ready_but_not_publication_ready(self) -> None:
        code_path = FIXTURE.with_name("analysis.py")
        config, config_findings = validator.validate_config(FIXTURE)
        findings = [*config_findings, *validator.validate_code(code_path, "python", config)]
        self.assertEqual([], [item for item in findings if item.level == "error"])
        report = validator.serialize(FIXTURE, code_path, "python", findings)
        self.assertFalse(report["analysis_plan_ready"])
        self.assertTrue(report["code_static_gate_passed"])
        self.assertTrue(report["ready_for_execution"])
        self.assertFalse(report["ready_for_publication"])

    def test_code_scope_requires_generated_dependency_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config_path = root / "config.yaml"
            code_path = root / "analysis.py"
            config_path.write_text(FIXTURE.read_text(encoding="utf-8"), encoding="utf-8")
            code_path.write_text(FIXTURE.with_name("analysis.py").read_text(encoding="utf-8"), encoding="utf-8")
            config, config_findings = validator.validate_config(config_path)
            findings = [*config_findings, *validator.validate_code(code_path, "python", config, root)]
        self.assertIn("CODE010", {item.code for item in findings})

    def test_stochastic_analysis_requires_seed(self) -> None:
        _, findings = self.validate_copy("stochastic: false", "stochastic: true")
        self.assertIn("MOD002", {item.code for item in findings})

    def test_repeated_data_requires_subject_clustering(self) -> None:
        _, findings = self.validate_copy("clustering: [subject_id, stimulus]", "clustering: [stimulus]")
        self.assertIn("DES006", {item.code for item in findings})

    def test_between_subject_trial_rows_still_require_subject_clustering(self) -> None:
        config_text = FIXTURE.read_text(encoding="utf-8").replace("design_type: within", "design_type: between").replace(
            "clustering: [subject_id, stimulus]", "clustering: [stimulus]"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.yaml"
            path.write_text(config_text, encoding="utf-8")
            _, findings = validator.validate_config(path)
        self.assertIn("DES006", {item.code for item in findings})

    def test_declared_item_identifier_requires_item_clustering(self) -> None:
        _, findings = self.validate_copy("clustering: [subject_id, stimulus]", "clustering: [subject_id]")
        self.assertIn("DES016", {item.code for item in findings})

    def test_non_clustering_identifier_requires_explicit_justification(self) -> None:
        config_text = FIXTURE.read_text(encoding="utf-8").replace(
            "  clustering: [subject_id, stimulus]",
            "  clustering: [subject_id]\n  non_clustering_justifications:\n    item: All fixed stimuli are exhaustively sampled; inference is conditional on this set.",
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.yaml"
            path.write_text(config_text, encoding="utf-8")
            _, findings = validator.validate_config(path)
        self.assertNotIn("DES016", {item.code for item in findings})

    def test_categorical_levels_must_be_nonempty_and_unique(self) -> None:
        _, findings = self.validate_copy("levels: [congruent, incongruent]", "levels: [congruent, congruent]")
        self.assertIn("DES017", {item.code for item in findings})

    def test_runtime_must_be_exact_and_pinned(self) -> None:
        _, findings = self.validate_copy('language_version: "3.12.4"', 'language_version: "3.12"')
        self.assertIn("ENV002", {item.code for item in findings})

    def test_dependency_artifact_is_required_and_language_appropriate(self) -> None:
        _, missing = self.validate_copy("  dependency_file: requirements.lock\n", "")
        self.assertIn("ENV005", {item.code for item in missing})
        _, wrong_language = self.validate_copy("dependency_file: requirements.lock", "dependency_file: renv.lock")
        self.assertIn("ENV007", {item.code for item in wrong_language})

    def test_r_runtime_requires_renv_lock_strategy(self) -> None:
        config_text = (
            FIXTURE.read_text(encoding="utf-8")
            .replace("language: python", "language: r")
            .replace('language_version: "3.12.4"', 'language_version: "4.4.1"')
            .replace("dependency_strategy: lockfile", "dependency_strategy: pinned")
            .replace("dependency_file: requirements.lock", "dependency_file: renv.lock")
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.yaml"
            path.write_text(config_text, encoding="utf-8")
            _, findings = validator.validate_config(path)
        self.assertIn("ENV009", {item.code for item in findings})

    def test_dependency_and_output_paths_cannot_escape_project(self) -> None:
        _, dependency = self.validate_copy("dependency_file: requirements.lock", "dependency_file: ../requirements.lock")
        self.assertIn("ENV006", {item.code for item in dependency})
        _, output = self.validate_copy("save_path: output/", "save_path: ../output/")
        self.assertIn("OUT005", {item.code for item in output})

    def test_remote_uri_is_not_misclassified_as_a_local_project_path(self) -> None:
        _, findings = self.validate_copy("data_path: data/", "data_path: https://example.org/data/")
        self.assertIn("DATA005", {item.code for item in findings})

    def test_multifile_pattern_and_paths_are_portable(self) -> None:
        config_text = FIXTURE.read_text(encoding="utf-8").replace(
            "data_path: data/", "data_path: /Users/example/stroop.csv"
        ).replace("sub-{subject_id}_stroop.csv", "stroop.csv")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.yaml"
            path.write_text(config_text, encoding="utf-8")
            _, findings = validator.validate_config(path)
        codes = {item.code for item in findings}
        self.assertIn("DATA005", codes)
        self.assertIn("DATA006", codes)

    def test_multifile_data_path_must_be_a_directory(self) -> None:
        _, findings = self.validate_copy("data_path: data/", "data_path: data/stroop.csv")
        self.assertIn("DATA008", {item.code for item in findings})

    def test_format_specific_loader_options_are_explicit(self) -> None:
        config_text = FIXTURE.read_text(encoding="utf-8").replace("file_format: csv", "file_format: xlsx")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.yaml"
            path.write_text(config_text, encoding="utf-8")
            _, findings = validator.validate_config(path)
        self.assertIn("DATA012", {item.code for item in findings})

    def test_execution_log_cannot_escape_output_directory(self) -> None:
        _, findings = self.validate_copy("execution_log: analysis-run.json", "execution_log: ../analysis-run.json")
        self.assertIn("OUT006", {item.code for item in findings})

    def test_question_requires_model_formula(self) -> None:
        _, findings = self.validate_copy(
            "    model_formula: rt ~ condition + (1 + condition | subject_id) + (1 | stimulus)\n",
            "",
        )
        self.assertIn("Q005", {item.code for item in findings})

    def test_ssrt_survival_routing_is_blocked(self) -> None:
        config_text = FIXTURE.read_text(encoding="utf-8").replace(
            "Does incongruency increase reaction time?", "What is SSRT?"
        ).replace("linear_mixed_model", "cox_regression")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.yaml"
            path.write_text(config_text, encoding="utf-8")
            _, findings = validator.validate_config(path)
        self.assertIn("Q007", {item.code for item in findings})

    def test_plain_logit_is_blocked_for_repeated_binary_data(self) -> None:
        source = """import importlib.metadata
import yaml
config = yaml.safe_load(open('analysis_config.yaml'))
source_row = []
exclusion_log = []
model = smf.logit('accuracy ~ condition', data).fit()
Path('out').write_text(str(model))
environment = importlib.metadata.version('pandas')
"""
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "config.yaml"
            config_text = FIXTURE.read_text(encoding="utf-8").replace("name: rt", "name: accuracy").replace("type: continuous", "type: binary")
            config_path.write_text(config_text, encoding="utf-8")
            config, _ = validator.validate_config(config_path)
            code_path = Path(directory) / "analysis.py"
            code_path.write_text(source, encoding="utf-8")
            findings = validator.validate_code(code_path, "python", config)
        self.assertIn("CODE005", {item.code for item in findings})

    def test_requirements_artifact_rejects_unpinned_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "requirements.lock").write_text("pandas>=2\n", encoding="utf-8")
            code_path = root / "analysis.py"
            code_path.write_text(FIXTURE.with_name("analysis.py").read_text(encoding="utf-8"), encoding="utf-8")
            config, _ = validator.validate_config(FIXTURE)
            findings = validator.validate_code(code_path, "python", config, root)
        self.assertIn("CODE011", {item.code for item in findings})

    def test_success_only_execution_manifest_is_rejected(self) -> None:
        source = FIXTURE.with_name("analysis.py").read_text(encoding="utf-8").replace(
            "sys.excepthook = record_unhandled_failure", "success_only_manifest = True"
        )
        source = source.replace("def record_unhandled_failure(exc_type, exc_value, exc_traceback):", "def ordinary_helper(exc_type, exc_value, exc_traceback):")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copy(FIXTURE.with_name("requirements.lock"), root / "requirements.lock")
            code_path = root / "analysis.py"
            code_path.write_text(source, encoding="utf-8")
            config, _ = validator.validate_config(FIXTURE)
            findings = validator.validate_code(code_path, "python", config, root)
        self.assertIn("CODE013", {item.code for item in findings})

    def test_r_code_scope_passes_static_and_parse_contract(self) -> None:
        config_text = (
            FIXTURE.read_text(encoding="utf-8")
            .replace("language: python", "language: r")
            .replace('language_version: "3.12.4"', 'language_version: "4.4.1"')
            .replace("dependency_file: requirements.lock", "dependency_file: renv.lock")
        )
        source = """config <- yaml::read_yaml("config.yaml")
language_version <- config$runtime$language_version; current_version <- paste(R.version$major, R.version$minor, sep = ".")
dependency_file <- config$runtime$dependency_file
execution_log <- file.path(config$output$save_path, "analysis-run.json")
tryCatch({
  data <- readr::read_csv("data/input.csv")
  data$source_row <- seq_len(nrow(data))
  exclusion_log <- data.frame()
  model <- stats::lm(rt ~ condition, data = data)
  confidence <- stats::confint(model)
  residual_diagnostics <- stats::resid(model)
  environment <- utils::sessionInfo()
  readr::write_csv(data, "output/result.csv")
}, error = function(e) {
  writeLines(conditionMessage(e), execution_log)
})
"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config_path = root / "config.yaml"
            code_path = root / "analysis.R"
            config_path.write_text(config_text, encoding="utf-8")
            code_path.write_text(source, encoding="utf-8")
            (root / "renv.lock").write_text(
                '{"R":{"Version":"4.4.1"},"Packages":{"yaml":{"Version":"2.3.10"},"readr":{"Version":"2.1.5"}}}',
                encoding="utf-8",
            )
            config, config_findings = validator.validate_config(config_path)
            findings = [*config_findings, *validator.validate_code(code_path, "r", config, root)]
        self.assertEqual([], [item for item in findings if item.level == "error"])

    def test_r_syntax_failure_is_not_downgraded_to_runtime_warning(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".R", encoding="utf-8", delete=False) as handle:
            handle.write("x <-\n")
            code_path = Path(handle.name)
        failed_parse = subprocess.CompletedProcess(
            args=["Rscript"],
            returncode=1,
            stdout="",
            stderr="Error in parse(file = path) : unexpected end of input",
        )
        try:
            with mock.patch.object(validator.shutil, "which", return_value="/fake/Rscript"):
                with mock.patch.object(validator.subprocess, "run", return_value=failed_parse):
                    findings = validator.validate_code(code_path, "r", {})
        finally:
            code_path.unlink(missing_ok=True)
        self.assertIn("CODE006", {item.code for item in findings if item.level == "error"})

    def test_broken_r_runtime_is_reported_as_environment_warning(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".R", encoding="utf-8", delete=False) as handle:
            handle.write("x <- 1\n")
            code_path = Path(handle.name)
        runtime_failure = subprocess.CompletedProcess(
            args=["Rscript"],
            returncode=134,
            stdout="",
            stderr="dyld: Library not loaded: libR.dylib; library load denied by system policy",
        )
        try:
            with mock.patch.object(validator.shutil, "which", return_value="/fake/Rscript"):
                with mock.patch.object(validator.subprocess, "run", return_value=runtime_failure):
                    findings = validator.validate_code(code_path, "r", {})
        finally:
            code_path.unlink(missing_ok=True)
        self.assertNotIn("CODE006", {item.code for item in findings})
        self.assertIn("CODE007", {item.code for item in findings if item.level == "warning"})


if __name__ == "__main__":
    unittest.main()
