from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_experiment.py"
FIXTURE = ROOT / "tests" / "fixtures" / "valid-stroop"
SPEC = importlib.util.spec_from_file_location("validate_experiment", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


class ConfigValidationTests(unittest.TestCase):
    def test_valid_stroop_fixture_passes(self) -> None:
        config, tables, findings = validator.validate_config(FIXTURE / "config.yaml")
        self.assertEqual(1, len(tables))
        self.assertEqual([], [finding for finding in findings if finding.level == "error"])
        report = validator.serialize(FIXTURE / "config.yaml", None, config, tables, findings)
        self.assertTrue(report["static_gate_passed"])
        self.assertTrue(report["pre_code_ready"])
        self.assertIsNone(report["code_static_gate_passed"])
        self.assertFalse(report["ready_for_collection"])
        self.assertTrue(report["runtime_smoke_test_required"])

    def test_missing_rt_onset_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "fixture"
            shutil.copytree(FIXTURE, target)
            config = target / "config.yaml"
            config.write_text(config.read_text().replace("    rt_onset: self\n", ""), encoding="utf-8")
            _, _, findings = validator.validate_config(config)
        self.assertIn("WIN004", {finding.code for finding in findings})

    def test_rt_measurement_contract_requires_rationale_and_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "fixture"
            shutil.copytree(FIXTURE, target)
            config = target / "config.yaml"
            text = config.read_text(encoding="utf-8")
            text = text.replace(
                '    rt_rationale: "RT starts at the verified display onset of the scored color word"\n',
                "",
            ).replace("    rt_contract_status: confirmed\n", "")
            config.write_text(text, encoding="utf-8")
            _, _, findings = validator.validate_config(config)
        codes = {finding.code for finding in findings}
        self.assertIn("WIN010", codes)
        self.assertIn("WIN011", codes)

    def test_missing_condition_column_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "fixture"
            shutil.copytree(FIXTURE, target)
            conditions = target / "conditions" / "formal.csv"
            conditions.write_text(conditions.read_text().replace("word,", "label,"), encoding="utf-8")
            _, _, findings = validator.validate_config(target / "config.yaml")
        self.assertIn("COND003", {finding.code for finding in findings})

    def test_empty_correct_response_is_not_silently_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "fixture"
            shutil.copytree(FIXTURE, target)
            conditions = target / "conditions" / "formal.csv"
            conditions.write_text(conditions.read_text().replace("1,RED,red,congruent,congruent,f", "1,RED,red,congruent,congruent,"), encoding="utf-8")
            _, _, findings = validator.validate_config(target / "config.yaml")
        self.assertIn("COND009", {finding.code for finding in findings})

    def test_stroop_key_must_come_from_ink_color(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "fixture"
            shutil.copytree(FIXTURE, target)
            conditions = target / "conditions" / "formal.csv"
            conditions.write_text(conditions.read_text().replace("4,RED,green,incongruent,incongruent,j", "4,RED,green,incongruent,incongruent,f"), encoding="utf-8")
            _, _, findings = validator.validate_config(target / "config.yaml")
        self.assertIn("FID004", {finding.code for finding in findings})

    def test_declared_ratio_uses_only_attainable_rounding_counts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "fixture"
            shutil.copytree(FIXTURE, target)
            conditions = target / "conditions" / "formal.csv"
            conditions.write_text(
                conditions.read_text().replace(
                    "2,GREEN,green,congruent,congruent,j",
                    "2,GREEN,green,incongruent,incongruent,j",
                ),
                encoding="utf-8",
            )
            _, _, findings = validator.validate_config(target / "config.yaml")
        self.assertIn("FID002", {finding.code for finding in findings})

    def test_filename_requires_collision_resistant_run_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "fixture"
            shutil.copytree(FIXTURE, target)
            config = target / "config.yaml"
            config.write_text(config.read_text().replace("{run_id}", "{date}"), encoding="utf-8")
            _, _, findings = validator.validate_config(config)
        self.assertIn("OUT005", {finding.code for finding in findings})

    def test_malformed_structural_sections_fail_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "fixture"
            shutil.copytree(FIXTURE, target)
            config = target / "config.yaml"
            config.write_text(config.read_text().replace("response_rules:\n", "response_rules: invalid\nlegacy_response_rules:\n", 1), encoding="utf-8")
            _, _, findings = validator.validate_config(config)
        self.assertIn("RSP001", {finding.code for finding in findings})

    def test_response_event_and_duration_are_semantically_validated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "fixture"
            shutil.copytree(FIXTURE, target)
            config = target / "config.yaml"
            text = config.read_text().replace("duration: 1500", "duration: -1", 1).replace("response_event: key_down", "response_event: vague_event")
            config.write_text(text, encoding="utf-8")
            _, _, findings = validator.validate_config(config)
        codes = {finding.code for finding in findings}
        self.assertIn("WIN008", codes)
        self.assertIn("WIN009", codes)

    def test_condition_path_cannot_escape_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "fixture"
            shutil.copytree(FIXTURE, target)
            config = target / "config.yaml"
            config.write_text(config.read_text().replace("conditions/formal.csv", "../formal.csv"), encoding="utf-8")
            _, _, findings = validator.validate_config(config)
        self.assertIn("COND008", {finding.code for finding in findings})

    def test_output_uri_is_not_misclassified_as_a_local_project_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "fixture"
            shutil.copytree(FIXTURE, target)
            config = target / "config.yaml"
            config.write_text(
                config.read_text(encoding="utf-8").replace("directory: data/", "directory: https://example.org/data/"),
                encoding="utf-8",
            )
            _, _, findings = validator.validate_config(config)
        self.assertIn("OUT006", {finding.code for finding in findings})


class CodeValidationTests(unittest.TestCase):
    def validate_text(self, suffix: str, platform: str, source: str):
        with tempfile.NamedTemporaryFile("w", suffix=suffix, encoding="utf-8", delete=False) as handle:
            handle.write(source)
            path = Path(handle.name)
        try:
            return validator.validate_code(path, platform)
        finally:
            path.unlink(missing_ok=True)

    def test_psychopy_contract_passes(self) -> None:
        source = """import random
from psychopy import visual
from psychopy.hardware import keyboard
BASE_COLUMNS = ['subject_id', 'block', 'trial', 'condition', 'stimulus', 'correct_response', 'response', 'rt', 'accuracy', 'timestamp']
random.seed(42)
kb = keyboard.Keyboard(backend='ptb')
data_file = open('data.csv', 'a')
try:
    win.callOnFlip(kb.clock.reset)
    win.callOnFlip(kb.clearEvents)
    keys = kb.getKeys(keyList=['f', 'escape'], waitRelease=False)
    if keys:
        rt = keys[0].rt
    data_file.flush()
finally:
    data_file.flush()
    data_file.close()
"""
        findings = self.validate_text(".py", "psychopy", source)
        self.assertEqual([], [finding for finding in findings if finding.level == "error"])

    def test_psychopy_legacy_timing_fails(self) -> None:
        findings = self.validate_text(".py", "psychopy", "import time\ntime.sleep(1)\n")
        self.assertIn("CODE200", {finding.code for finding in findings})

    def test_psychopy_namespace_injection_fails(self) -> None:
        findings = self.validate_text(".py", "psychopy", "globals()['condition'] = trial['condition']\n")
        self.assertIn("CODE200", {finding.code for finding in findings})

    def test_cjk_comments_and_docstrings_do_not_imply_display_font_usage(self) -> None:
        source = '''"""中文模块说明。"""
# 中文注释不等于屏幕刺激
import random
from psychopy.hardware import keyboard
BASE_COLUMNS = ['subject_id', 'block', 'trial', 'condition', 'stimulus', 'correct_response', 'response', 'rt', 'accuracy', 'timestamp']
random.seed(42)
kb = keyboard.Keyboard(backend='ptb')
try:
    win.callOnFlip(kb.clock.reset)
    win.callOnFlip(kb.clearEvents)
    key = kb.getKeys(keyList=['f', 'escape'], waitRelease=False)[0]
    rt = key.rt
    data_file.flush()
finally:
    data_file.close()
'''
        findings = self.validate_text(".py", "psychopy", source)
        self.assertNotIn("CODE007", {finding.code for finding in findings})

    def test_key_release_requires_release_timestamp_semantics(self) -> None:
        source = """from psychopy import visual
from psychopy.hardware import keyboard
BASE_COLUMNS = ['subject_id', 'block', 'trial', 'condition', 'stimulus', 'correct_response', 'response', 'rt', 'accuracy', 'timestamp']
kb = keyboard.Keyboard(backend='ptb')
try:
    win.callOnFlip(kb.clock.reset)
    win.callOnFlip(kb.clearEvents)
    keys = kb.getKeys(keyList=['f', 'escape'], waitRelease=True)
    rt = keys[0].rt
    data_file.flush()
finally:
    data_file.close()
"""
        config = {
            "windows": [{"response": ["f"], "response_event": "key_release", "rt_onset": "self"}],
            "response_rules": {"correct": "f"},
            "randomization": {"method": "fixed"},
        }
        with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8", delete=False) as handle:
            handle.write(source)
            path = Path(handle.name)
        try:
            findings = validator.validate_code(path, "psychopy", config)
        finally:
            path.unlink(missing_ok=True)
        self.assertIn("CODE103", {finding.code for finding in findings})

    def test_missing_base_data_columns_fails(self) -> None:
        source = """import random
from psychopy.hardware import keyboard
random.seed(42)
kb = keyboard.Keyboard(backend='ptb')
try:
    win.callOnFlip(kb.clock.reset)
    win.callOnFlip(kb.clearEvents)
    key = kb.getKeys(keyList=['escape'], waitRelease=False)[0]
    rt = key.rt
    data_file.flush()
finally:
    data_file.close()
"""
        findings = self.validate_text(".py", "psychopy", source)
        self.assertIn("CODE101", {finding.code for finding in findings})

    def test_jspsych_contract_passes(self) -> None:
        source = """const baseColumns = ['subject_id', 'block', 'trial', 'condition', 'stimulus', 'correct_response', 'response', 'rt', 'accuracy', 'timestamp'];
function handleEmergencyAbort(event) {
  if (event.key === 'Escape') jsPsych.abortExperiment('Safe abort', {abort_reason: 'escape'});
}
const jsPsych = initJsPsych({
  on_data_update: function(data) { localStorage.setItem('checkpoint', JSON.stringify(data)); },
  on_finish: function() {
    document.removeEventListener('keydown', handleEmergencyAbort, true);
    jsPsych.data.get().localSave('csv', 'data.csv');
  }
});
document.addEventListener('keydown', handleEmergencyAbort, true);
jsPsych.randomization.setSeed('42');
const preload = {type: jsPsychPreload, auto_preload: true};
function score(data) { const rt = data.rt; return jsPsych.pluginAPI.compareKeys(data.response, 'f'); }
const timeline = [preload];
jsPsych.run(timeline);
"""
        findings = self.validate_text(".js", "jspsych", source)
        self.assertEqual([], [finding for finding in findings if finding.level == "error"])

    def test_jspsych_escape_cannot_be_a_scored_choice(self) -> None:
        source = """const baseColumns = ['subject_id', 'block', 'trial', 'condition', 'stimulus', 'correct_response', 'response', 'rt', 'accuracy', 'timestamp'];
function handleEmergencyAbort(event) {
  if (event.key === 'Escape') jsPsych.abortExperiment('Safe abort', {abort_reason: 'escape'});
}
const jsPsych = initJsPsych({
  on_data_update: function(data) { localStorage.setItem('checkpoint', JSON.stringify(data)); },
  on_finish: function() {
    document.removeEventListener('keydown', handleEmergencyAbort, true);
    jsPsych.data.get().localSave('csv', 'data.csv');
  }
});
document.addEventListener('keydown', handleEmergencyAbort, true);
jsPsych.randomization.setSeed('42');
const preload = {type: jsPsychPreload, auto_preload: true};
const scored = {type: jsPsychHtmlKeyboardResponse, choices: ['f', 'escape']};
function score(data) { const rt = data.rt; return jsPsych.pluginAPI.compareKeys(data.response, 'f'); }
jsPsych.run([preload, scored]);
"""
        findings = self.validate_text(".js", "jspsych", source)
        self.assertIn("CODE200", {finding.code for finding in findings})

    def test_jspsych_math_random_requires_semantic_seed_order_review(self) -> None:
        source = """const baseColumns = ['subject_id', 'block', 'trial', 'condition', 'stimulus', 'correct_response', 'response', 'rt', 'accuracy', 'timestamp'];
function handleEmergencyAbort(event) {
  if (event.key === 'Escape') jsPsych.abortExperiment('Safe abort', {abort_reason: 'escape'});
}
const jsPsych = initJsPsych({
  on_data_update: function(data) { localStorage.setItem('checkpoint', JSON.stringify(data)); },
  on_finish: function() {
    document.removeEventListener('keydown', handleEmergencyAbort, true);
    jsPsych.data.get().localSave('csv', 'data.csv');
  }
});
document.addEventListener('keydown', handleEmergencyAbort, true);
jsPsych.randomization.setSeed('42');
const preload = {type: jsPsychPreload, auto_preload: true};
const iti = Math.random() * 1000 + 1000;
function score(data) { const rt = data.rt; return jsPsych.pluginAPI.compareKeys(data.response, 'f'); }
jsPsych.run([preload]);
"""
        findings = self.validate_text(".js", "jspsych", source)
        self.assertNotIn("CODE200", {finding.code for finding in findings})
        self.assertIn("CODE300", {finding.code for finding in findings if finding.level == "warning"})

    def test_psychtoolbox_contract_is_static_pass_with_warning(self) -> None:
        source = """headers = {'subject_id', 'block', 'trial', 'condition', 'stimulus', 'correct_response', 'response', 'rt', 'accuracy', 'timestamp'};
Screen('Preference', 'SkipSyncTests', 0);
rng(42, 'twister');
PsychImaging('OpenWindow', 0);
try
  KbQueueCreate; KbQueueStart; KbQueueFlush;
  stimOnset = Screen('Flip', window, when);
  [pressed, firstPress] = KbQueueCheck;
  rt = firstPress(1) - stimOnset;
  fid = fopen('data.csv', 'a'); fprintf(fid, '%f', rt); fclose(fid);
  Priority(0); ShowCursor;
catch ME
  sca; Priority(0); ShowCursor;
end
"""
        findings = self.validate_text(".m", "psychtoolbox", source)
        self.assertEqual([], [finding for finding in findings if finding.level == "error"])
        self.assertIn("CODE006", {finding.code for finding in findings})


class ReferenceTemplateTests(unittest.TestCase):
    BASE_COLUMNS = (
        "subject_id", "block", "trial", "condition", "stimulus",
        "correct_response", "response", "rt", "accuracy", "timestamp",
    )

    def validate_reference_code(self, reference: Path, heading: str, fence: str, suffix: str, platform: str):
        section = reference.read_text(encoding="utf-8").split(heading, 1)[1]
        source = section.split(f"```{fence}", 1)[1].split("```", 1)[0]
        with tempfile.NamedTemporaryFile("w", suffix=suffix, encoding="utf-8", delete=False) as handle:
            handle.write(source)
            path = Path(handle.name)
        try:
            return validator.validate_code(path, platform)
        finally:
            path.unlink(missing_ok=True)

    def test_psychopy_canonical_skeleton_passes_static_contract(self) -> None:
        reference = ROOT / "psy-exp-coder" / "psychopy" / "spec" / "README.md"
        findings = self.validate_reference_code(reference, "### 1.9 Canonical Code Skeleton", "python", ".py", "psychopy")
        self.assertEqual([], [finding for finding in findings if finding.level == "error"])

    def test_psychtoolbox_canonical_skeleton_passes_static_contract(self) -> None:
        reference = ROOT / "psy-exp-coder" / "psychtoolbox" / "spec" / "README.md"
        findings = self.validate_reference_code(reference, "### 1.1 Canonical Code Skeleton", "matlab", ".m", "psychtoolbox")
        self.assertEqual([], [finding for finding in findings if finding.level == "error"])

    def test_all_canonical_skeletons_expose_base_data_columns(self) -> None:
        cases = (
            (ROOT / "psy-exp-coder" / "psychopy" / "spec" / "README.md", "### 1.9 Canonical Code Skeleton", "python"),
            (ROOT / "psy-exp-coder" / "jspsych" / "spec" / "README.md", "## 8. Canonical Code Skeleton", "html"),
            (ROOT / "psy-exp-coder" / "psychtoolbox" / "spec" / "README.md", "### 1.1 Canonical Code Skeleton", "matlab"),
        )
        for reference, heading, fence in cases:
            section = reference.read_text(encoding="utf-8").split(heading, 1)[1]
            source = section.split(f"```{fence}", 1)[1].split("```", 1)[0]
            for column in self.BASE_COLUMNS:
                self.assertIn(column, source, f"{reference} is missing {column}")

    def test_generation_references_avoid_unseeded_randomization(self) -> None:
        ptb_paradigms = ROOT / "psy-exp-coder" / "psychtoolbox" / "paradigms"
        for reference in ptb_paradigms.glob("*.md"):
            self.assertNotIn("rng('shuffle')", reference.read_text(encoding="utf-8"), str(reference))

        js_mapping = ROOT / "psy-exp-coder" / "jspsych" / "mapping" / "README.md"
        self.assertNotIn("Math.random()", js_mapping.read_text(encoding="utf-8"))
        js_spec = ROOT / "psy-exp-coder" / "jspsych" / "spec" / "README.md"
        self.assertNotIn("Math.random()", js_spec.read_text(encoding="utf-8"))

    def test_jspsych_canonical_skeleton_passes_static_contract(self) -> None:
        reference = ROOT / "psy-exp-coder" / "jspsych" / "spec" / "README.md"
        section = reference.read_text(encoding="utf-8").split("## 8. Canonical Code Skeleton", 1)[1]
        source = section.split("```html", 1)[1].split("```", 1)[0]
        with tempfile.NamedTemporaryFile("w", suffix=".html", encoding="utf-8", delete=False) as handle:
            handle.write(source)
            path = Path(handle.name)
        try:
            findings = validator.validate_code(path, "jspsych")
        finally:
            path.unlink(missing_ok=True)
        self.assertEqual([], [finding for finding in findings if finding.level == "error"])

    def test_condition_generator_template_executes(self) -> None:
        reference = ROOT / "psy-exp-designer" / "references" / "condition-file-generation.md"
        section = reference.read_text(encoding="utf-8").split("## Standalone Generation Script Template", 1)[1]
        source = section.split("```python", 1)[1].split("```", 1)[0]
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, "-c", source, "--seed", "12345"],
                cwd=directory,
                capture_output=True,
                text=True,
                check=False,
            )
            generated = sorted((Path(directory) / "conditions").glob("*.xlsx"))
            manifest = json.loads((Path(directory) / "conditions" / "generation-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(3, len(generated))
        self.assertEqual(12345, manifest["resolved_seed"])
        self.assertEqual(3, len(manifest["files_sha256"]))


if __name__ == "__main__":
    unittest.main()
