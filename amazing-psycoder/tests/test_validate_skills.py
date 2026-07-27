from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_skills.py"
SPEC = importlib.util.spec_from_file_location("validate_skills", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)

RUNTIME_SCRIPT = ROOT / "scripts" / "validate_studio_runtime.py"
RUNTIME_SPEC = importlib.util.spec_from_file_location("validate_studio_runtime", RUNTIME_SCRIPT)
assert RUNTIME_SPEC and RUNTIME_SPEC.loader
runtime_validator = importlib.util.module_from_spec(RUNTIME_SPEC)
sys.modules[RUNTIME_SPEC.name] = runtime_validator
RUNTIME_SPEC.loader.exec_module(runtime_validator)


class SemanticContractTests(unittest.TestCase):
    def test_repository_contracts_pass(self) -> None:
        self.assertEqual([], validator.semantic_contract_errors(ROOT))

    def test_multilingual_readmes_share_user_facing_v1_4_content(self) -> None:
        repository = ROOT.parent
        readmes = [
            repository / "README.md",
            repository / "docs" / "README_EN.md",
            repository / "docs" / "README_ZH-HANT.md",
            repository / "docs" / "README_JA.md",
            repository / "docs" / "README_DE.md",
            repository / "docs" / "README_FR.md",
        ]
        markers = (
            "v1.4.0",
            "PsychoPy",
            "jsPsych",
            "Psychtoolbox",
            "ready_for_collection",
            "ready_for_publication",
            "ready_for_execution",
            "PSYCODER_STUDIO.md",
            "requirements-dev.txt",
            "./install.sh claude",
            "./install.sh codex",
            "./install.sh hermes",
            "./install.sh openclaw",
            "~/.agents/skills",
            "~/.hermes/skills",
            "~/.openclaw/skills",
            "38 × 3",
        )
        for readme in readmes:
            content = readme.read_text(encoding="utf-8")
            for marker in markers:
                self.assertIn(marker, content, f"{readme} is missing {marker}")
            self.assertIsNone(
                re.search(r"\b(?:PsychoPy|jsPsych|Psychtoolbox)\s+v?\d", content),
                f"{readme} should not show versions beside experiment platform names",
            )
            self.assertEqual([], validator.direct_link_errors(readme))
            self.assertEqual([], validator.fence_errors(readme))

    def test_documented_reference_inventory_matches_repository(self) -> None:
        repository = ROOT.parent
        inventories = (
            (
                ROOT / "psy-exp-designer" / "paradigms",
                {"README.md"},
                38,
                "38",
            ),
            (
                ROOT / "psy-ana-designer" / "methods",
                {"README.md", "USAGE.md"},
                60,
                "60",
            ),
            (
                ROOT / "psy-ana-designer" / "plots",
                {"README.md", "USAGE.md"},
                48,
                "48",
            ),
        )
        readmes = [
            repository / "README.md",
            *sorted((repository / "docs").glob("README_*.md")),
        ]
        for directory, excluded, expected, documented in inventories:
            actual = len(
                [
                    path
                    for path in directory.glob("*.md")
                    if path.name not in excluded
                ]
            )
            self.assertEqual(expected, actual, f"unexpected inventory count in {directory}")
            for readme in readmes:
                self.assertIn(documented, readme.read_text(encoding="utf-8"))

    def test_primary_readme_preserves_original_user_journey_safely(self) -> None:
        repository = ROOT.parent
        primary = (repository / "README.md").read_text(encoding="utf-8")
        original_structure = (
            "> 让心理学研究者更专注于研究问题，而不是代码。",
            "## 📖 为什么做这个项目",
            "## 👥 适合这些人",
            "## ⚡ 安装",
            "## 🚀 快速开始",
            "## 🧪 实验编程",
            "### 🎬 Demo：做一个 Stroop 实验",
            "## 📊 数据分析",
            "### 🎬 Demo：分析一组 Stroop 数据",
            "## 📂 文件结构",
        )
        for marker in original_structure:
            self.assertIn(marker, primary)

        for plain_language_marker in (
            "心理学研究从设计到分析的常见困难",
            "研究进行中的两类主要困难",
            "四个 AI Agent",
            "### 实验设计参考",
            "分析方案既可以在数据收集前规划",
            "### 分析语言与环境",
            "在正式电脑上试跑",
            "不等于 38 × 3",
            "还不能直接开始收数据",
            "还不能说结果已经适合写入论文",
            "同一组 60 个颜色词组合会被所有被试看到",
            "rt ~ condition + (1 + condition | subject_id) + (1 | stimulus)",
            "不做固定 RT 上下限或 ±SD 剔除",
            "环境：R 4.4.1 + renv.lock",
        ):
            self.assertIn(plain_language_marker, primary)

        stale_or_unsafe_claims = (
            "让心理学研究的代码门槛彻底消失",
            "最终拿到的代码打开就能跑",
            "分析结果期刊审稿人也挑不出毛病",
            "审计通过 · 就绪标签：ready_for_collection",
            "审计通过 · 就绪标签：ready_for_publication",
            "RT 150-2000ms · 正确试次",
            "https://www.jspsych.org/v7/",
            "clawhub install amazing-psycoder",
            "hermes skills install https://github.com/soupandpsy/amazing-psycoder-skills",
            "反应时也有重复试次，同一刺激会被多人看到。",
            "当前 PsyCoder Studio 已验证的自动生成",
            "当前心理学研究面临的痛点",
            "实验推进落地的两大门槛",
            "你只需要描述实验想法或现有数据",
            "希望实验代码有质量保障",
            "### 范式覆盖",
            "数据收回来后，同样分三步",
            "回答粒度不同",
            "由宿主匹配 Skill",
            "各宿主",
            "实验编程与数据分析中的两类主要困难",
            "## ✅ 正式使用前必须知道",
            "[✅ 使用边界](#-正式使用前必须知道)",
        )
        for claim in stale_or_unsafe_claims:
            self.assertNotIn(claim, primary)

        translated_readmes = sorted((repository / "docs").glob("README_*.md"))
        synchronized_slogans = {
            "README_EN.md": "> Helping psychology researchers focus more on research questions, not code.",
            "README_ZH-HANT.md": "> 讓心理學研究者更專注於研究問題，而不是程式碼。",
            "README_JA.md": "> 心理学研究者がコードではなく、研究上の問いにより集中できるように。",
            "README_DE.md": "> Damit sich psychologische Forschende stärker auf ihre Forschungsfragen konzentrieren können – statt auf Code.",
            "README_FR.md": "> Pour que les chercheurs en psychologie se concentrent davantage sur leurs questions de recherche que sur le code.",
        }
        synchronized_language_markers = {
            "README_EN.md": (
                "Common Challenges from Study Design to Data Analysis",
                "Two Main Challenges in Conducting Research",
                "four AI agents",
                "### Experiment Design References",
                "### Analysis Languages and Environments",
            ),
            "README_ZH-HANT.md": (
                "心理學研究從設計到分析的常見困難",
                "研究進行中的兩類主要困難",
                "四個 AI Agent",
                "### 實驗設計參考",
                "### 分析語言與環境",
            ),
            "README_JA.md": (
                "研究設計からデータ分析までに生じる一般的な課題",
                "研究を進める上での二つの主要課題",
                "4 つの AI エージェント",
                "### 実験設計リファレンス",
                "### 分析言語と実行環境",
            ),
            "README_DE.md": (
                "Häufige Herausforderungen von der Studienplanung bis zur Datenanalyse",
                "Zwei zentrale Schwierigkeiten bei der Durchführung von Forschung",
                "vier KI-Agenten",
                "### Referenzen für Experimentdesigns",
                "### Analysesprachen und Laufzeitumgebungen",
            ),
            "README_FR.md": (
                "Difficultés courantes de la conception de l'étude à l'analyse des données",
                "Deux difficultés principales dans la conduite d’une recherche",
                "quatre agents IA",
                "### Références de conception expérimentale",
                "### Langages et environnements d'analyse",
            ),
        }
        for readme in translated_readmes:
            translated = readme.read_text(encoding="utf-8")
            self.assertIn(
                synchronized_slogans[readme.name],
                translated,
                f"{readme} has a stale or unsynchronized slogan",
            )
            self.assertGreaterEqual(
                len(translated.splitlines()),
                350,
                f"{readme} should preserve the original long-form user journey",
            )
            for marker in (
                "## 📖",
                "## 👥",
                "## ⚡",
                "## 🚀",
                "## 🧪",
                "## 📊",
                "## 🎬",
                "## 📂",
                "PsychoPy",
                "Stroop",
                "analysis.R",
                "R 4.4.1",
                "rt ~ condition + (1 + condition | subject_id) + (1 | stimulus)",
            ):
                self.assertIn(marker, translated, f"{readme} is missing {marker}")
            for marker in synchronized_language_markers[readme.name]:
                self.assertIn(
                    marker,
                    translated,
                    f"{readme} is missing synchronized academic/plain-language marker {marker}",
                )
            for claim in (
                "https://www.jspsych.org/v7/",
                "clawhub install amazing-psycoder",
                "hermes skills install https://github.com/soupandpsy/amazing-psycoder-skills",
                "RT 150-2000ms",
                "TR 150-2000ms",
                "What you get runs right out of the box",
                "最終拿到的程式碼打開就能跑",
                "最終的に届くコードはそのまま実行でき",
                "Was du am Ende in den Händen hältst, läuft auf Anhieb",
                "Le code que vous obtenez est prêt à lancer",
                "Making the coding barrier in psychology research disappear completely",
                "讓心理學研究的程式碼門檻徹底消失",
                "心理学研究におけるコーディングの壁を完全になくす",
                "Lass die Hürde des Programmierens in der Psychologieforschung komplett verschwinden",
                "Faites disparaître complètement la barrière du code dans la recherche en psychologie",
                "9-item quality gate",
                "9 項品質門",
                "9 項目の品質ゲート",
                "9-Punkte-Qualitätstor",
                "9 portes qualité",
                "Every method choice goes through 12-dimension comparison",
                "每個方法選擇經過 12 維度對比",
                "各手法の選択は 12 次元の比較に基づきます",
                "Jede Methodenentscheidung durchläuft einen 12-Dimensionen-Vergleich",
                "Chaque méthode est évaluée sur 12 dimensions",
                "The last checkpoint before publication",
                "發表前最後一關",
                "発表前の最終チェック",
                "Die letzte Prüfung vor der Publikation",
                "Dernière vérification avant publication",
                "Current Pain Points in Psychology Research",
                "Two Major Barriers to Getting Experiments Done",
                "You just answer its questions",
                "After installation, type `/amazing-psycoder`",
                "each host",
                "let the host match the skill",
                "Paradigm Coverage",
                "Once data is collected",
                "當前心理學研究面臨的痛點",
                "實驗推進落地的兩大門檻",
                "你只需要描述實驗想法或現有資料",
                "你只需要回答它提出的問題",
                "讓宿主匹配 Skill",
                "各宿主",
                "範式覆蓋",
                "資料收回來後",
                "現在の心理学研究が直面する課題",
                "実験を進める上での二つの大きな壁",
                "あなたは質問に答えるだけです",
                "ホストに Skill",
                "パラダイムカバレッジ",
                "データを集めた後も",
                "Aktuelle Schmerzpunkte in der psychologischen Forschung",
                "Die zwei großen Hürden bei der Umsetzung von Experimenten",
                "Du musst nur die Fragen beantworten",
                "der Host ordnet den Skill zu",
                "Paradigmen-Abdeckung",
                "Sind die Daten erst einmal da",
                "publikationsreifen Analyse",
                "Points de friction dans la recherche en psychologie",
                "Les deux grands obstacles à la réalisation d'une expérience",
                "Vous n'avez qu'à répondre",
                "l'hôte associer le Skill",
                "Paradigmes couverts",
                "Une fois les données collectées",
                "Two Main Challenges: Experiment Programming and Data Analysis",
                "實驗編程與資料分析中的兩類主要困難",
                "実験プログラミングとデータ分析における二つの主要課題",
                "Zwei Hauptaufgaben: Experiment-Programmierung und Datenanalyse",
                "Deux difficultés principales : programmer l'expérience et analyser les données",
                "## ✅ Before Real Use",
                "## ✅ 正式使用前必須知道",
                "## ✅ 本番利用の前に",
                "## ✅ Vor dem echten Einsatz",
                "## ✅ Avant l'utilisation réelle",
            ):
                self.assertNotIn(claim, translated, f"{readme} still contains {claim}")

    def test_readme_platform_claims_match_runtime_capabilities(self) -> None:
        capabilities = json.loads(
            (ROOT / "runtime" / "capabilities.json").read_text(encoding="utf-8")
        )
        platforms = {item["platform"] for item in capabilities["platforms"]}
        self.assertEqual({"psychopy", "jspsych", "psychtoolbox"}, platforms)
        self.assertEqual("1.4.0", capabilities["contractVersion"])
        self.assertIn("live PsyCoder Studio deployment", capabilities["evidenceBoundary"])
        self.assertTrue(capabilities["verifiedGenerationProfiles"])
        for profile in capabilities["verifiedGenerationProfiles"]:
            self.assertIn(profile["platform"], platforms)
            self.assertTrue(profile["limitations"])

        studio_contract = (ROOT / "PSYCODER_STUDIO.md").read_text(encoding="utf-8")
        orchestrator = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("The current Studio deployment has", studio_contract)
        self.assertIn("does not prove", studio_contract)
        self.assertNotIn("The Studio uses a Skill Reference Engine", orchestrator)
        self.assertIn("does not prove a live Studio deployment", orchestrator)

    def test_portable_validator_runs_without_site_packages(self) -> None:
        result = subprocess.run(
            [sys.executable, "-S", str(SCRIPT), "--portable"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr + result.stdout)
        self.assertIn("portable installation contracts", result.stdout)

    def test_review_rule_inside_fence_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "gate.md"
            path.write_text("```\n### Rule 5: Runtime\n```\n", encoding="utf-8")
            self.assertTrue(validator.headings_inside_fences(path))

    def test_stale_fixed_latency_claim_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative, markers in validator.REQUIRED_CONTRACTS.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("\n".join(markers), encoding="utf-8")
            stale = root / "reference.md"
            stale.write_text("The keyboard backend always causes a 50-70ms RT error.", encoding="utf-8")
            errors = validator.semantic_contract_errors(root)
        self.assertTrue(any("fixed backend latency" in error for error in errors))

    def test_universal_method_and_threshold_claims_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative, markers in validator.REQUIRED_CONTRACTS.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("\n".join(markers), encoding="utf-8")
            stale = root / "reference.md"
            stale.write_text(
                "Every test must output effect size via pingouin.\n"
                "Anticipatory responses (RT < 100ms) are always invalid.\n",
                encoding="utf-8",
            )
            errors = validator.semantic_contract_errors(root)
        self.assertTrue(any("no single package" in error for error in errors))
        self.assertTrue(any("task/device-derived" in error for error in errors))

    def test_ssrt_survival_example_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative, markers in validator.REQUIRED_CONTRACTS.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("\n".join(markers), encoding="utf-8")
            stale = root / "method.md"
            stale.write_text(
                "A Cox model was used to examine condition effects on SSRT.",
                encoding="utf-8",
            )
            errors = validator.semantic_contract_errors(root)
        self.assertTrue(any("Cox/Log-Rank" in error for error in errors))

    def test_stale_seed_and_variance_switch_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative, markers in validator.REQUIRED_CONTRACTS.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("\n".join(markers), encoding="utf-8")
            stale = root / "method.md"
            stale.write_text(
                "RANDOM_SEED = 42\nLevene p > 0.05 means use Student ANOVA.\n",
                encoding="utf-8",
            )
            errors = validator.semantic_contract_errors(root)
        self.assertTrue(any("confirmed scope" in error for error in errors))
        self.assertTrue(any("mechanically select" in error for error in errors))

    def test_summary_string_cannot_stand_in_for_runtime_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative, markers in validator.REQUIRED_CONTRACTS.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("\n".join(markers), encoding="utf-8")
            stale = root / "review.json.md"
            stale.write_text('"smoke_test_evidence": ["all tests passed"]', encoding="utf-8")
            errors = validator.semantic_contract_errors(root)
        self.assertTrue(any("structured per-test evidence" in error for error in errors))


class RuntimeSchemaTests(unittest.TestCase):
    HASH = "a" * 64

    @classmethod
    def execution_plan(cls) -> dict:
        return {
            "schemaVersion": "2.0",
            "projectName": "Schema fixture",
            "project": {
                "id": "project-1",
                "name": "Schema fixture",
                "paradigm": "custom",
                "paradigmFamily": None,
                "variant": None,
            },
            "target": {"platform": "psychopy"},
            "generationProfile": None,
            "sequences": [
                {
                    "id": "sequence-1",
                    "name": "Trial",
                    "order": 1,
                    "windowIds": ["response-1"],
                    "execution": {"mode": "once"},
                }
            ],
            "windows": [
                {
                    "id": "response-1",
                    "label": "Response",
                    "order": 1,
                    "durationMs": 1000,
                    "stimulus": {
                        "type": "text",
                        "displayMode": "text",
                        "staticText": "X",
                    },
                    "response": {
                        "enabled": True,
                        "allowedKeys": ["f"],
                        "event": "key_down",
                        "correctKeyMode": "fixed",
                        "correctKey": "f",
                        "rtOnset": "response-1",
                        "recordRt": True,
                        "recordAccuracy": True,
                    },
                    "timing": {"mode": "fixed"},
                    "data": {
                        "recordResponse": True,
                        "recordRt": True,
                        "recordAccuracy": True,
                        "recordOnset": True,
                        "recordTrialFields": True,
                    },
                }
            ],
            "trialSource": {
                "mode": "generated",
                "factors": [{"name": "condition", "levels": ["a"], "balance": "equal"}],
                "randomization": {"seed": "participant-session"},
            },
            "conditions": {"mode": "generated", "fields": [], "rules": []},
            "responses": {
                "id": "response-rule-1",
                "allowedKeys": ["f"],
                "correctKeySource": "fixed",
                "correctKey": "f",
                "rtOnset": "response-1",
                "responseEvent": "key_down",
                "recordRT": True,
                "recordAccuracy": True,
            },
            "dataSchema": [],
            "assets": [],
            "itiMs": 0,
        }

    @classmethod
    def generation_envelope(cls) -> dict:
        return {
            "schemaVersion": "2.0",
            "projectName": "Schema fixture",
            "target": {"platform": "psychopy"},
            "experimentSpec": {
                "schemaVersion": "2.4",
                "meta": {},
                "flow": [{}],
                "trialRoutines": [{}],
                "windows": [{}],
                "conditions": {},
                "responses": {},
                "dataSchema": [{}],
                "assets": [],
                "builderState": {},
                "designLifecycle": {
                    "status": "confirmed",
                    "confirmedAt": "2026-07-23T10:00:00+08:00",
                },
            },
            "executionPlan": cls.execution_plan(),
            "executionPlanHash": cls.HASH,
            "validationSummary": {
                "valid": True,
                "errorCount": 0,
                "warningCount": 0,
                "infoCount": 0,
                "totalIssues": 0,
                "topIssueCodes": [],
            },
            "aiMode": "authenticated",
            "requestedAt": "2026-07-23T10:00:00+08:00",
        }

    def validator(self, name: str):
        return validator.runtime_schema_validator(ROOT, f"runtime/schemas/{name}.schema.json")

    def test_runtime_contracts_and_schema_graph_pass(self) -> None:
        self.assertEqual([], validator.runtime_contract_errors(ROOT))

    def test_generation_rejects_failed_validation_summary(self) -> None:
        envelope = self.generation_envelope()
        self.assertTrue(self.validator("generation-input").is_valid(envelope))
        envelope["validationSummary"]["valid"] = False
        self.assertFalse(self.validator("generation-input").is_valid(envelope))

    def test_generation_semantics_verify_hash_references_and_totals(self) -> None:
        envelope = self.generation_envelope()
        envelope["executionPlanHash"] = runtime_validator.canonical_json_sha256(
            envelope["executionPlan"]
        )
        self.assertEqual([], runtime_validator.validate_record(ROOT, "generation", envelope))

        envelope["validationSummary"]["totalIssues"] = 1
        errors = runtime_validator.validate_record(ROOT, "generation", envelope)
        self.assertTrue(any("totalIssues must equal" in error for error in errors))

        envelope["validationSummary"]["totalIssues"] = 0
        envelope["executionPlan"]["sequences"][0]["windowIds"] = ["missing-window"]
        envelope["executionPlanHash"] = runtime_validator.canonical_json_sha256(
            envelope["executionPlan"]
        )
        errors = runtime_validator.validate_record(ROOT, "generation", envelope)
        self.assertTrue(any("unknown windows" in error for error in errors))
        self.assertTrue(any("unreachable windows" in error for error in errors))

    def test_artifact_output_rejects_path_traversal(self) -> None:
        output = {
            "platform": "psychopy",
            "executionPlanHash": self.HASH,
            "files": [
                {
                    "path": "../escape.py",
                    "content": "print('unsafe')",
                    "mediaType": "text/x-python",
                    "language": "python",
                    "ownership": "model",
                }
            ],
            "warnings": [],
            "assumptions": [],
        }
        self.assertFalse(self.validator("artifact-output").is_valid(output))
        output["files"][0]["path"] = "main.py"
        self.assertTrue(self.validator("artifact-output").is_valid(output))

    def test_artifact_semantics_reject_duplicate_paths(self) -> None:
        output = {
            "platform": "psychopy",
            "executionPlanHash": self.HASH,
            "files": [
                {
                    "path": "main.py",
                    "content": "print(1)",
                    "mediaType": "text/x-python",
                    "ownership": "model",
                },
                {
                    "path": "main.py",
                    "content": "print(2)",
                    "mediaType": "text/x-python",
                    "ownership": "model",
                },
            ],
            "warnings": [],
            "assumptions": [],
        }
        errors = runtime_validator.validate_record(ROOT, "artifact", output)
        self.assertTrue(any("duplicate path" in error for error in errors))

    def test_reviewer_cannot_repair_or_self_certify(self) -> None:
        report = {
            "review_id": "review-1",
            "artifact_set_hash": self.HASH,
            "execution_plan_hash": self.HASH,
            "mode": "code-audit",
            "scope": {"reviewed": ["main.py"], "not_reviewed": ["target timing"]},
            "issues": [],
            "reviewed_files": [{"path": "main.py", "sha256": self.HASH}],
            "summary": "No static findings.",
            "reviewed_at": "2026-07-23T10:00:00+08:00",
        }
        schema = self.validator("review-output")
        self.assertTrue(schema.is_valid(report))
        report["repairs_applied"] = ["changed main.py"]
        report["ready_for_collection"] = True
        self.assertFalse(schema.is_valid(report))

    def test_review_scope_must_cover_hashed_files(self) -> None:
        report = {
            "review_id": "review-1",
            "artifact_set_hash": self.HASH,
            "execution_plan_hash": self.HASH,
            "mode": "code-audit",
            "scope": {"reviewed": ["README.md"], "not_reviewed": []},
            "issues": [],
            "reviewed_files": [{"path": "main.py", "sha256": self.HASH}],
            "summary": "Scope mismatch fixture.",
            "reviewed_at": "2026-07-23T10:00:00+08:00",
        }
        errors = runtime_validator.validate_record(ROOT, "review", report)
        self.assertTrue(any("missing from scope.reviewed" in error for error in errors))

    def test_repair_attempt_rejects_protected_pipeline_path(self) -> None:
        repair = {
            "attempt": 1,
            "platform": "psychopy",
            "source_review_id": "review-1",
            "input_artifact_set_hash": self.HASH,
            "execution_plan_hash": self.HASH,
            "addressed_issue_ids": ["REV-001"],
            "files": [
                {
                    "path": "_pipeline/execution_plan.json",
                    "content": "{}",
                    "ownership": "model",
                }
            ],
            "summary": "Attempted protected rewrite.",
        }
        self.assertFalse(self.validator("repair-attempt").is_valid(repair))
        repair["files"][0]["path"] = "main.py"
        self.assertTrue(self.validator("repair-attempt").is_valid(repair))

    def test_readiness_rejects_contradictory_state(self) -> None:
        snapshot = {
            "artifact_set_hash": self.HASH,
            "review_id": "review-1",
            "static_review_passed": False,
            "smoke_test_status": "passed",
            "ready_for_packaging": True,
            "ready_for_collection": True,
            "blockers": [],
            "derived_at": "2026-07-23T10:00:00+08:00",
        }
        schema = self.validator("readiness-snapshot")
        self.assertFalse(schema.is_valid(snapshot))
        snapshot.update(
            {
                "static_review_passed": True,
                "ready_for_packaging": True,
                "ready_for_collection": True,
            }
        )
        self.assertTrue(schema.is_valid(snapshot))

    def test_readiness_is_derived_from_review_artifacts_and_runtime_evidence(self) -> None:
        report = {
            "review_id": "review-1",
            "artifact_set_hash": self.HASH,
            "execution_plan_hash": self.HASH,
            "mode": "code-audit",
            "scope": {"reviewed": ["main.py"], "not_reviewed": []},
            "issues": [],
            "reviewed_files": [{"path": "main.py", "sha256": self.HASH}],
            "summary": "No static findings.",
            "reviewed_at": "2026-07-23T10:00:00+08:00",
        }
        missing = runtime_validator.derive_readiness(
            ROOT,
            report,
            artifact_contract_passed=True,
            runtime_evidence=None,
            derived_at="2026-07-23T10:30:00+08:00",
        )
        self.assertTrue(missing["ready_for_packaging"])
        self.assertFalse(missing["ready_for_collection"])
        self.assertEqual("missing", missing["smoke_test_status"])

        evidence = {
            "evidence_id": "evidence-1",
            "artifact_set_hash": self.HASH,
            "target": {
                "platform": "psychopy",
                "os": "macOS test target",
                "runtime_version": "PsychoPy 2024.2.4",
                "hardware": "lab keyboard and display",
            },
            "tests": [
                {
                    "id": test_id,
                    "result": "passed",
                    "procedure": f"Observed {test_id}",
                    "evidence_paths": [f"smoke/{test_id}.md"],
                }
                for test_id in (
                    "launch_exit",
                    "full_short_session",
                    "data_integrity",
                    "incremental_recovery",
                )
            ],
            "started_at": "2026-07-23T10:00:00+08:00",
            "completed_at": "2026-07-23T10:20:00+08:00",
            "recorded_by": "lab operator",
        }
        passed = runtime_validator.derive_readiness(
            ROOT,
            report,
            artifact_contract_passed=True,
            runtime_evidence=evidence,
            derived_at="2026-07-23T10:30:00+08:00",
        )
        self.assertTrue(passed["ready_for_packaging"])
        self.assertTrue(passed["ready_for_collection"])
        self.assertEqual([], passed["blockers"])

        artifact_blocked = runtime_validator.derive_readiness(
            ROOT,
            report,
            artifact_contract_passed=False,
            runtime_evidence=evidence,
            derived_at="2026-07-23T10:30:00+08:00",
        )
        self.assertEqual("passed", artifact_blocked["smoke_test_status"])
        self.assertFalse(artifact_blocked["ready_for_packaging"])
        self.assertFalse(artifact_blocked["ready_for_collection"])


if __name__ == "__main__":
    unittest.main()
