"""Policy scope and single project resolution in disposable installations."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import unittest
import venv


ROOT = Path(__file__).resolve().parents[2]
CLAIM = "live " + "integration\n"
RECORDER = """#!/usr/bin/env python3
import json
from pathlib import Path
import sys
with Path('.calls.jsonl').open('a') as stream:
    stream.write(json.dumps([Path(sys.argv[0]).name, *sys.argv[1:]]) + '\\n')
"""


class CheckContractTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="check contract ")
        self.addCleanup(temporary.cleanup)
        self.target = Path(temporary.name)
        manifest = json.loads((ROOT / ".harness/manifest.json").read_text())
        for name in [*manifest["managed_files"], ".harness/manifest.json"]:
            destination = self.target / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, destination)
        self.config = (ROOT / ".harness/default-config.toml").read_text()
        self.write(".harness/config.toml", self.config)
        for tool in ("shellcheck", "shfmt", "markdownlint-cli2"):
            self.write(f"tool bin/{tool}", RECORDER, executable=True)

    def write(self, name, content, executable=False):
        path = self.target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        if executable:
            path.chmod(0o755)

    def run_check(self, *arguments, environment=None):
        clean = {
            key: value for key, value in os.environ.items()
            if not key.startswith("HARNESS_") and key != "CONFIG_PATH"
        }
        trace = clean.pop("QH_TEST_TRACE", None)
        clean["PATH"] = str(self.target / "tool bin") + ":" + clean["PATH"]
        clean["PYTHONDONTWRITEBYTECODE"] = "1"
        command = [str(self.target / "harness"), "check", *arguments,
                   str(self.target)]
        started = time.monotonic()
        result = subprocess.run(
            command, cwd=self.target, env={**clean, **(environment or {})},
            text=True, capture_output=True, check=False, timeout=45,
        )
        if trace:
            record = {
                "case": self.id(), "command": command,
                "exit": result.returncode,
                "feedback_seconds": round(time.monotonic() - started, 6),
                "stdout": result.stdout, "stderr": result.stderr,
            }
            serialized = json.dumps(record).replace(
                str(self.target), "<temporary>"
            ).replace(str(ROOT), "<repository>")
            with Path(trace).open("a") as stream:
                stream.write(serialized + "\n")
        return result

    def calls(self):
        path = self.target / ".calls.jsonl"
        return [json.loads(line) for line in path.read_text().splitlines()]

    def syntax_environment(self):
        # Isolate the degraded fallback even when host tools are installed.
        venv.EnvBuilder(with_pip=False).create(self.target / ".venv")

    def test_python_shebangs_avoid_shell_and_get_python_size_analysis(self):
        self.write(
            "python worker", "#!/usr/bin/env -S python3 -u\n" +
            "value = 1\n" * 400, executable=True,
        )
        self.write("shell worker", "#!/bin/sh\nexit 0\n", executable=True)
        result = self.run_check("--command", "true")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("python worker has 401 lines", result.stdout)
        for call in self.calls():
            if call[0] in {"shellcheck", "shfmt"}:
                self.assertIn("shell worker", call)
                self.assertNotIn("python worker", call)
                self.assertNotIn(".harness/checks/standards/check", call)

    def test_nested_exclusions_apply_to_all_tree_checks(self):
        self.syntax_environment()
        self.write(".harness/config.toml", self.config.replace(
            '"generated",', '"src/generated",'
        ))
        self.write("pyproject.toml", "[project]\nname = 'synthetic'\n")
        self.write("src/generated/bad.py", "def broken(:\n" * 400)
        self.write("src/generated/README.md", "[broken](missing.md)\n")
        self.write("src/generated/claim.txt", CLAIM)
        self.write("src/generated/bad shell", "#!/bin/sh\n", True)
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("bad.py has", result.stdout)
        self.assertNotIn("src/generated/bad shell", str(self.calls()))

    def test_component_exclusion_applies_at_any_depth(self):
        for name in ("generated", "src/nested/generated"):
            self.write(f"{name}/README.md", "[broken](missing.md)\n")
            self.write(f"{name}/claim.txt", CLAIM)
        result = self.run_check("--command", "true")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_similarly_named_and_non_root_directories_remain_checked(self):
        self.write(".harness/config.toml", self.config.replace(
            '"generated",', '"src/generated",'
        ))
        for name in ("src/generated-copy", "other/src/generated"):
            with self.subTest(name=name):
                self.write(f"{name}/README.md", "[broken](missing.md)\n")
                result = self.run_check("--command", "true")
                self.assertEqual(result.returncode, 1)
                self.assertIn(name, result.stderr)
                (self.target / name / "README.md").unlink()

    def test_extensionless_python_syntax_error_is_a_failure(self):
        self.syntax_environment()
        self.write("pyproject.toml", "[project]\nname = 'synthetic'\n")
        self.write("broken worker", "#!/usr/bin/env python3\ndef broken(:\n",
                   executable=True)
        result = self.run_check()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("broken worker", result.stderr)
        self.assertIn("syntax", result.stderr.lower())

    def test_symlink_sources_are_not_read_or_sent_to_tools(self):
        self.syntax_environment()
        outside = tempfile.TemporaryDirectory(prefix="outside check ")
        self.addCleanup(outside.cleanup)
        base = Path(outside.name)
        for name, content in {
            "bad.py": "def broken(:\n" * 400,
            "README.md": "[broken](missing.md)\n",
            "claim.txt": CLAIM,
            "bad.sh": "#!/bin/sh\n",
        }.items():
            (base / name).write_text(content)
            (self.target / name).symlink_to(base / name)
        (self.target / "outside tree").symlink_to(base)
        (self.target / "cycle").symlink_to(self.target)
        self.write("pyproject.toml", "[project]\nname = 'synthetic'\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("bad.py has", result.stdout)
        self.assertNotIn("bad.sh", str(self.calls()))

    def test_canonical_policy_document_symlink_is_rejected(self):
        self.write("AGENTS.md", "# Synthetic\n")
        for name in ("PRODUCT", "ARCHITECTURE", "DESIGN", "DATA", "QUALITY",
                     "SECURITY", "DECISIONS"):
            self.write(f"docs/{name}.md", "# Synthetic\n")
        self.write("outside-context.txt", "## System shape\n## Boundaries\n"
                   "## External systems\n")
        (self.target / "docs/ARCHITECTURE.md").unlink()
        (self.target / "docs/ARCHITECTURE.md").symlink_to(
            self.target / "outside-context.txt"
        )
        result = self.run_check("--command", "touch project-ran")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("symlink", result.stderr)
        self.assertFalse((self.target / "project-ran").exists())

    def test_overrides_preserve_precedence_and_run_once_without_python(self):
        self.write("pyproject.toml", "[project]\nname = 'synthetic'\n")
        self.write("bad.py", "def broken(:\n")
        self.write(".harness/config.toml", self.config.replace(
            'check = ""', 'check = "echo config >> selected.txt"'
        ))
        for arguments, environment, expected in (
            (("--command", "echo cli >> selected.txt"),
             {"HARNESS_CHECK_COMMAND": "echo env >> selected.txt"}, "cli"),
            ((), {"HARNESS_CHECK_COMMAND": "echo env >> selected.txt"}, "env"),
            ((), {}, "config"),
        ):
            with self.subTest(expected=expected):
                result = self.run_check(*arguments, environment=environment)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(
                    (self.target / "selected.txt").read_text(), expected + "\n"
                )
                self.assertNotIn("parsing Python", result.stdout)
                (self.target / "selected.txt").unlink()

    def test_policy_failure_blocks_override(self):
        self.write("README.md", "[broken](missing.md)\n")
        result = self.run_check("--command", "echo ran >> selected.txt")
        self.assertEqual(result.returncode, 1)
        self.assertIn("policy check 'documentation' failed", result.stderr)
        self.assertFalse((self.target / "selected.txt").exists())

    def test_angle_bracket_markdown_links_support_spaces(self):
        self.write("notes with spaces.md", "# Synthetic notes\n")
        self.write("README.md", "[notes](<notes with spaces.md>)\n")
        result = self.run_check("--command", "true")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_failing_standards_tool_blocks_override(self):
        self.write("tool bin/shellcheck", "#!/bin/sh\nexit 9\n", True)
        result = self.run_check("--command", "touch project-ran")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("policy check 'standards' failed", result.stderr)
        self.assertFalse((self.target / "project-ran").exists())

    def test_override_failure_is_not_hidden(self):
        result = self.run_check("--command", "echo once >> selected.txt; exit 7")
        self.assertEqual(result.returncode, 1)
        self.assertIn("project command failed with exit 7", result.stderr)
        self.assertEqual((self.target / "selected.txt").read_text(), "once\n")

    def test_package_check_is_one_implementation_without_auto_python(self):
        self.write("pyproject.toml", "[project]\nname = 'synthetic'\n")
        self.write("bad.py", "def broken(:\n")
        self.write("package.json", json.dumps({"scripts": {
            "check": "echo check >> selected.txt",
            "lint": "echo lint >> selected.txt",
            "typecheck": "echo typecheck >> selected.txt",
        }}))
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.target / "selected.txt").read_text(), "check\n")

    def test_package_lint_and_typecheck_fallback_each_run_once(self):
        self.write("pyproject.toml", "[project]\nname = 'synthetic'\n")
        self.write("bad.py", "def broken(:\n")
        self.write("package.json", json.dumps({"scripts": {
            "lint": "echo lint >> selected.txt",
            "typecheck": "echo typecheck >> selected.txt",
        }}))
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.target / "selected.txt").read_text(),
                         "lint\ntypecheck\n")

    def test_native_tools_own_their_scope(self):
        self.syntax_environment()
        self.write("pyproject.toml", "[project]\nname = 'synthetic'\n")
        self.write("generated/native.py", "value = 1\n")
        self.write("generated/README.md", "# Synthetic\n")
        self.write("ruff/__main__.py", RECORDER.replace(
            "Path(sys.argv[0]).name", "'ruff'"
        ) + "if sys.argv[1:2] == ['check']:\n"
          "    assert Path('generated/native.py').exists()\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(["ruff", "format", "--check", "."], self.calls())
        self.assertIn(["ruff", "check", "."], self.calls())
        self.assertIn(["markdownlint-cli2", "**/*.md"], self.calls())


if __name__ == "__main__":
    unittest.main()
