"""Application/suite boundaries exercised through disposable installations."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
import venv


ROOT = Path(__file__).resolve().parents[2]
FAILING_APP = (
    "import unittest\nclass App(unittest.TestCase):\n"
    "    def test_app(self):\n"
    "        print('application-case-collected')\n"
    "        self.assertEqual(1, 2, 'application broken')\n"
)
PASSING_APP = FAILING_APP.replace("assertEqual(1, 2", "assertEqual(2, 2")


class RunnerContractTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="runner contract ")
        self.addCleanup(temporary.cleanup)
        self.target = Path(temporary.name)

    def write(self, name: str, content: str) -> None:
        path = self.target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def declare(self, runner: str) -> None:
        self.write(
            "pyproject.toml", f'[tool.harness.tests]\nrunner = "{runner}"\n'
        )

    def install(self) -> None:
        manifest = json.loads((ROOT / ".harness/manifest.json").read_text())
        for name in [*manifest["managed_files"], ".harness/manifest.json"]:
            destination = self.target / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, destination)
        config = (ROOT / ".harness/config.toml").read_text()
        config = re.sub(r'(?m)^test = .*$', 'test = ""', config)
        self.write(".harness/config.toml", config)

    def run_harness(
        self, action: str = "test", *arguments: str,
        environment: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        executable = self.target / "harness"
        if not executable.exists():
            executable = ROOT / "harness"
        clean = {
            key: value for key, value in os.environ.items()
            if not key.startswith("HARNESS_") and key != "CONFIG_PATH"
        }
        clean["PYTHONDONTWRITEBYTECODE"] = "1"
        trace = clean.pop("QH_TEST_TRACE", None)
        command = [str(executable), action, *arguments, str(self.target)]
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
            with Path(trace).open("a", encoding="utf-8") as stream:
                stream.write(serialized + "\n")
        return result

    def require_real_pytest(self) -> None:
        self.assertIsNotNone(
            importlib.util.find_spec("pytest"),
            "Install .harness/tests/requirements.txt in the kit environment; "
            "real pytest collection is required, not skipped.",
        )

    def test_installed_application_failure_and_healthy_control(self) -> None:
        self.install()
        self.declare("unittest")
        self.write("tests/test_app.py", FAILING_APP)
        failing = self.run_harness()
        self.assertEqual(failing.returncode, 1, failing.stdout + failing.stderr)
        self.assertIn("application broken", failing.stderr)
        self.assertIn("application-case-collected", failing.stdout)
        self.assertNotIn("running harness contract tests", failing.stdout)
        self.write("tests/test_app.py", PASSING_APP)
        healthy = self.run_harness()
        self.assertEqual(healthy.returncode, 0, healthy.stderr)
        self.assertIn("application-case-collected", healthy.stdout)
        self.assertIn("Ran 1 test", healthy.stderr)

    def test_missing_pytest_cannot_drop_mixed_suite(self) -> None:
        self.declare("pytest")
        venv.EnvBuilder(with_pip=False).create(self.target / ".venv")
        self.write("tests/test_legacy.py", PASSING_APP)
        self.write(
            "tests/test_function.py", "def test_function():\n    assert False\n"
        )
        result = self.run_harness()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("pytest", result.stderr)
        self.assertIn("required", result.stderr)
        self.assertIn("install", result.stderr.lower())
        self.assertNotIn("unittest discovery", result.stdout)

    def test_missing_local_runner_does_not_use_host_pytest(self) -> None:
        self.require_real_pytest()
        self.install()
        self.declare("pytest")
        venv.EnvBuilder(with_pip=False).create(self.target / ".venv")
        self.write(
            "tests/test_function.py", "def test_function():\n    assert True\n"
        )
        result = self.run_harness()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(str(self.target / ".venv/bin/python"), result.stderr)

    def test_real_local_pytest_collects_both_styles(self) -> None:
        self.require_real_pytest()
        self.install()
        self.declare("pytest")
        (self.target / ".venv").symlink_to(sys.prefix, target_is_directory=True)
        self.write("tests/test_legacy.py", PASSING_APP)
        self.write(
            "tests/test_function.py", "def test_function():\n    assert False\n"
        )
        failing = self.run_harness()
        self.assertEqual(failing.returncode, 1, failing.stdout + failing.stderr)
        self.assertIn("1 failed, 1 passed", failing.stdout)
        self.write(
            "tests/test_function.py", "def test_function():\n    assert True\n"
        )
        healthy = self.run_harness()
        self.assertEqual(healthy.returncode, 0, healthy.stderr)
        self.assertIn("2 passed", healthy.stdout)

    def test_zero_pytest_cases_fail(self) -> None:
        self.require_real_pytest()
        self.install()
        self.declare("pytest")
        (self.target / ".venv").symlink_to(sys.prefix, target_is_directory=True)
        self.write("tests/test_empty.py", "value = 1\n")
        result = self.run_harness()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("no tests ran", result.stdout.lower())
        self.assertIn("exit 5", result.stderr)

    def test_declared_unittest_needs_no_pytest_and_uses_local_env(self) -> None:
        self.install()
        self.declare("unittest")
        venv.EnvBuilder(with_pip=False).create(self.target / ".venv")
        self.write(
            "tests/test_local.py",
            "import sys\nimport unittest\nfrom pathlib import Path\n"
            "class Local(unittest.TestCase):\n"
            "    def test_prefix(self):\n"
            "        self.assertEqual(\n"
            "            Path(sys.prefix), Path('.venv').resolve()\n"
            "        )\n",
        )
        result = self.run_harness()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Ran 1 test", result.stderr)

    def test_zero_unittest_cases_fail(self) -> None:
        self.install()
        self.declare("unittest")
        self.write("tests/test_empty.py", "value = 1\n")
        result = self.run_harness()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("zero", result.stderr.lower())

    def test_native_override_uses_local_python(self) -> None:
        venv.EnvBuilder(with_pip=False).create(self.target / ".venv")
        self.write("record.py", "import sys\nprint(sys.prefix)\n")
        result = self.run_harness("test", "--command", "python record.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(self.target / ".venv"), result.stdout)

    def test_self_test_is_independent_and_rejects_empty_suite(self) -> None:
        self.install()
        # Replace this disposable suite to avoid recursive installation tests.
        for path in (self.target / ".harness/tests").glob("test_*.py"):
            path.unlink()
        self.write(".harness/tests/test_contract.py", PASSING_APP)
        self.write("tests/test_app.py", FAILING_APP)
        self.declare("unittest")
        self.write("package.json", '{"scripts":{"test":"exit 17"}}')
        venv.EnvBuilder(with_pip=False).create(self.target / ".venv")
        app = self.run_harness()
        contract = self.run_harness(
            "self-test", environment={"HARNESS_TEST_COMMAND": "exit 19"}
        )
        self.assertEqual(app.returncode, 1, app.stdout + app.stderr)
        self.assertIn("exit 17", app.stderr)
        self.assertEqual(contract.returncode, 0, contract.stderr)
        self.assertIn("Ran 1 test", contract.stderr)
        self.write(".harness/tests/test_contract.py", FAILING_APP)
        self.assertEqual(self.run_harness("self-test").returncode, 1)
        self.write(".harness/tests/test_contract.py", "value = 1\n")
        empty = self.run_harness("self-test")
        self.assertEqual(empty.returncode, 1, empty.stdout + empty.stderr)
        self.assertIn("zero", empty.stderr.lower())

    def test_self_test_cannot_be_redirected_by_cli(self) -> None:
        result = self.run_harness("self-test", "--command", "true")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("--command", result.stderr)

    def test_invalid_runner_declaration_fails_without_traceback(self) -> None:
        for declaration in ('runner = "unknown"', 'runner = ["pytest"]'):
            with self.subTest(declaration=declaration):
                self.write(
                    "pyproject.toml", f"[tool.harness.tests]\n{declaration}\n"
                )
                self.write("tests/test_app.py", PASSING_APP)
                result = self.run_harness()
                self.assertEqual(result.returncode, 1)
                self.assertIn("runner", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_default_python_convention_does_not_fallback(self) -> None:
        venv.EnvBuilder(with_pip=False).create(self.target / ".venv")
        self.write("tests/test_app.py", PASSING_APP)
        result = self.run_harness()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("pytest", result.stderr)
        self.assertNotIn("unittest discovery", result.stdout)

    def test_installed_harness_does_not_supply_app_tests(self) -> None:
        self.install()
        result = self.run_harness()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("no tests detected", result.stderr)

    def test_broken_local_environment_is_reported(self) -> None:
        (self.target / ".venv").mkdir()
        self.declare("unittest")
        self.write("tests/test_app.py", PASSING_APP)
        result = self.run_harness()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(".venv", result.stderr)


if __name__ == "__main__":
    unittest.main()
