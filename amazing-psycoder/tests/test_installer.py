from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "install.sh"
SKILL_NAMES = (
    "amazing-psycoder",
    "psy-exp-designer",
    "psy-exp-coder",
    "psy-exp-reviewer",
    "psy-ana-designer",
    "psy-ana-coder",
    "psy-ana-reviewer",
)


class InstallerTransactionTests(unittest.TestCase):
    def run_installer(self, arguments: list[str], environment: dict[str, str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(INSTALLER), *arguments],
            cwd=ROOT.parent,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_mid_batch_failure_restores_every_previous_skill(self) -> None:
        real_mv = shutil.which("mv")
        self.assertIsNotNone(real_mv)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "skills"
            fake_bin = root / "bin"
            target.mkdir()
            fake_bin.mkdir()
            for name in SKILL_NAMES:
                (target / name / "old-marker").mkdir(parents=True)

            fake_mv = fake_bin / "mv"
            fake_mv.write_text(
                "#!/bin/bash\n"
                "case \"${1:-}\" in\n"
                "  */stage/psy-ana-designer) exit 97 ;;\n"
                "esac\n"
                f"exec {real_mv} \"$@\"\n",
                encoding="utf-8",
            )
            fake_mv.chmod(0o755)
            environment = os.environ.copy()
            environment["PATH"] = f"{fake_bin}{os.pathsep}{environment['PATH']}"

            result = subprocess.run(
                ["bash", str(INSTALLER), str(target)],
                cwd=ROOT.parent,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(0, result.returncode)
            for name in SKILL_NAMES:
                self.assertTrue((target / name / "old-marker").is_dir(), name)
            self.assertEqual([], list(target.glob(".amazing-psycoder.transaction.*")))

    def test_codex_user_scope_uses_official_personal_agents_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment = os.environ.copy()
            environment["HOME"] = str(root / "home")
            result = self.run_installer(["codex"], environment)
            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            self.assertTrue((root / "home" / ".agents" / "skills" / "amazing-psycoder" / "SKILL.md").is_file())
            check = self.run_installer(["--check", "codex"], environment)
            self.assertEqual(0, check.returncode, check.stderr + check.stdout)

    def test_claude_user_scope_respects_claude_config_dir(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment = os.environ.copy()
            environment["CLAUDE_CONFIG_DIR"] = str(root / "claude-config")
            result = self.run_installer(["claude"], environment)
            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            self.assertTrue((root / "claude-config" / "skills" / "amazing-psycoder" / "SKILL.md").is_file())

    def test_hermes_user_scope_respects_home(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment = os.environ.copy()
            environment["HOME"] = str(root / "home")
            result = self.run_installer(["hermes"], environment)
            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            self.assertTrue((root / "home" / ".hermes" / "skills" / "amazing-psycoder" / "SKILL.md").is_file())
            check = self.run_installer(["--check", "hermes"], environment)
            self.assertEqual(0, check.returncode, check.stderr + check.stdout)

    def test_openclaw_user_scope_respects_home(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            environment = os.environ.copy()
            environment["HOME"] = str(root / "home")
            result = self.run_installer(["openclaw"], environment)
            self.assertEqual(0, result.returncode, result.stderr + result.stdout)
            self.assertTrue(
                (
                    root
                    / "home"
                    / ".openclaw"
                    / "skills"
                    / "amazing-psycoder"
                    / "SKILL.md"
                ).is_file()
            )
            check = self.run_installer(["--check", "openclaw"], environment)
            self.assertEqual(0, check.returncode, check.stderr + check.stdout)

    def test_project_scopes_use_host_specific_directories(self) -> None:
        for platform, relative in (
            ("claude", ".claude/skills"),
            ("codex", ".agents/skills"),
            ("openclaw", ".agents/skills"),
        ):
            with self.subTest(platform=platform), tempfile.TemporaryDirectory() as directory:
                project = Path(directory) / "project"
                project.mkdir()
                result = self.run_installer(
                    ["--scope", "project", "--project-dir", str(project), platform],
                    os.environ.copy(),
                )
                self.assertEqual(0, result.returncode, result.stderr + result.stdout)
                self.assertTrue((project / relative / "amazing-psycoder" / "SKILL.md").is_file())

    def test_project_scope_rejects_hosts_without_a_canonical_project_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            project.mkdir()
            result = self.run_installer(
                ["--scope", "project", "--project-dir", str(project), "hermes"],
                os.environ.copy(),
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("暂不支持 --scope project", result.stdout + result.stderr)

    def test_help_lists_every_supported_host(self) -> None:
        result = self.run_installer(["--help"], os.environ.copy())
        self.assertEqual(0, result.returncode)
        for platform in ("claude", "codex", "hermes", "openclaw"):
            self.assertIn(platform, result.stdout)

    def test_auto_detection_rejects_ambiguous_hosts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fake_bin = root / "bin"
            fake_bin.mkdir()
            fake_codex = fake_bin / "codex"
            fake_codex.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            fake_codex.chmod(0o755)
            environment = os.environ.copy()
            environment["CLAUDE_CODE"] = "1"
            environment["HOME"] = str(root / "home")
            environment["PATH"] = f"{fake_bin}{os.pathsep}/usr/bin:/bin"
            result = self.run_installer([], environment)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("多个宿主", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
