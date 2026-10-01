import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).parents[2]
STANDARDS_CHECK = (
    REPOSITORY_ROOT / ".harness" / "checks" / "standards" / "check"
)
DEFAULT_CONFIG = REPOSITORY_ROOT / ".harness" / "config.toml"


class StandardsContractTest(unittest.TestCase):
    def run_check(
        self, target: Path, config: Path = DEFAULT_CONFIG
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(STANDARDS_CHECK), str(target)],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "CONFIG_PATH": str(config)},
        )

    def test_auto_detection_selects_only_present_profiles(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            (target / "module.py").write_text("value = 1\n", encoding="utf-8")
            (target / "README.md").write_text("# Example\n", encoding="utf-8")
            result = self.run_check(target)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('profiles=["markdown","python"]', result.stdout)
        self.assertNotIn('"typescript"', result.stdout)

    def test_explicit_profiles_cannot_remove_detected_requirements(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            config = target / "config.toml"
            content = DEFAULT_CONFIG.read_text(encoding="utf-8").replace(
                'profiles = ["auto"]', 'profiles = ["markdown"]'
            )
            config.write_text(content, encoding="utf-8")
            (target / "module.py").write_text("value = 1\n", encoding="utf-8")
            result = self.run_check(target, config)

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('profiles=["markdown","python"]', result.stdout)
        self.assertIn("contradiction", result.stdout)

    def test_size_warnings_name_threshold_and_rationale_route(self) -> None:
        function_body = "\n".join("    value += 1" for _ in range(51))
        source = (
            "def oversized():\n"
            "    value = 0\n"
            f"{function_body}\n"
            "    return value\n"
        )
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            (target / "module.py").write_text(source, encoding="utf-8")
            result = self.run_check(target)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("threshold 50", result.stdout)
        self.assertIn("scoped rationale", result.stdout)

    def test_explicit_noise_paths_are_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            generated = target / "generated"
            generated.mkdir()
            (generated / "large.py").write_text(
                "value = 1\n" * 400, encoding="utf-8"
            )
            result = self.run_check(target)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("large.py has", result.stdout)

    def test_fixture_tool_configuration_uses_shared_line_width(self) -> None:
        python_config = (
            REPOSITORY_ROOT
            / ".harness/tests/fixtures/python-project/pyproject.toml"
        ).read_text(encoding="utf-8")
        prettier_path = (
            REPOSITORY_ROOT
            / ".harness/tests/fixtures/nextjs-project/prettier.config.mjs"
        )
        prettier_config = prettier_path.read_text(encoding="utf-8")
        configured_width = subprocess.run(
            [
                sys.executable,
                str(REPOSITORY_ROOT / ".harness/bin/config.py"),
                "get",
                str(DEFAULT_CONFIG),
                "standards.line_length",
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

        self.assertEqual(configured_width, "80")
        self.assertIn("line-length = 80", python_config)
        self.assertIn("printWidth: 80", prettier_config)

    def test_required_standards_documents_are_present(self) -> None:
        standards = REPOSITORY_ROOT / ".harness" / "standards"
        expected = {
            "BASE.md",
            "NAMING.md",
            "TESTING.md",
            "ARCHITECTURE.md",
        }
        languages = {"python.md", "typescript.md", "shell.md", "markdown.md"}

        self.assertEqual(
            {path.name for path in standards.glob("*.md")}, expected
        )
        self.assertEqual(
            {path.name for path in (standards / "languages").glob("*.md")},
            languages,
        )


if __name__ == "__main__":
    unittest.main()
