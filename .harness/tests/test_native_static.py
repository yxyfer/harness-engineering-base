"""Thin native delegation and missing-control regressions."""

import os
import hashlib
import json
import shutil
from pathlib import Path
import subprocess
import tempfile
import unittest
import venv

from test_phase2_contract import VALID_CONFIG

ROOT = Path(__file__).resolve().parents[2]


class NativeStaticTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="native static ")
        self.addCleanup(temporary.cleanup)
        self.target = Path(temporary.name).resolve()
        self.write(".harness/config.toml", VALID_CONFIG)

    def write(self, name, content):
        path = self.target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def run_harness(self, action, *arguments):
        environment = {
            k: v
            for k, v in os.environ.items()
            if not k.startswith("HARNESS_") and k != "CONFIG_PATH"
        }
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        environment["PATH"] = (
            str(self.target / "tool-bin") + ":" + environment["PATH"]
        )
        result = subprocess.run(
            [str(ROOT / "harness"), action, *arguments, str(self.target)],
            env=environment,
            capture_output=True,
            text=True,
            timeout=30,
        )
        trace = os.environ.get("QH_TEST_TRACE")
        if trace:
            with Path(trace).open("a") as stream:
                stream.write(
                    json.dumps(
                        {
                            "case": self.id(),
                            "action": action,
                            "exit": result.returncode,
                            "stdout": result.stdout,
                            "stderr": result.stderr,
                        }
                    )
                    + "\n"
                )
        return result

    def test_missing_python_static_tools_fail_without_syntax_success(self):
        self.write("pyproject.toml", "[project]\nname='synthetic'\n")
        self.write("main.py", "value = 1\n")
        venv.EnvBuilder(with_pip=False).create(self.target / ".venv")
        result = self.run_harness("check")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("ruff", result.stderr.lower())
        self.assertNotIn("degraded", result.stderr)

    def test_format_delegates_explicit_command_once(self):
        result = self.run_harness(
            "format", "--command", "printf formatted > selected.txt"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            (self.target / "selected.txt").read_text(), "formatted"
        )

    def test_typescript_missing_local_tools_cannot_pass(self):
        self.write("package.json", '{"private":true}')
        self.write("main.ts", "export const value = 1;\n")
        result = self.run_harness("check")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("project-local", result.stderr)

    def test_legacy_config_accepts_optional_format_without_replacement(self):
        config = self.target / ".harness/config.toml"
        config.write_text(
            VALID_CONFIG.replace(
                'check = ""',
                'check = ""\nformat = "printf configured > selected.txt"',
            )
        )
        before = config.read_bytes()
        result = self.run_harness("format")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(config.read_bytes(), before)
        self.assertEqual(
            (self.target / "selected.txt").read_text(), "configured"
        )

    def template(self, language):
        source = ROOT / ".harness/templates" / language
        shutil.copytree(
            source,
            self.target,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns(
                ".venv",
                "node_modules",
                "__pycache__",
                ".ruff_cache",
                ".pytest_cache",
                ".mypy_cache",
            ),
        )
        dependency = ".venv" if language == "python" else "node_modules"
        if not (source / dependency).is_dir():
            self.fail(
                f"locked native test setup missing: {source / dependency}"
            )
        (self.target / dependency).symlink_to(
            source / dependency, target_is_directory=True
        )

    def fingerprint(self):
        sys_path = str(ROOT / ".harness/bin")
        import sys

        sys.path.insert(0, sys_path)
        from source_paths import walk_files

        return {
            str(p.relative_to(self.target)): hashlib.sha256(
                p.read_bytes()
            ).hexdigest()
            for p in walk_files(
                self.target,
                [".venv", "node_modules", "__pycache__", ".ruff_cache"],
            )
        }

    def assert_native_failure(self, marker):
        formatted = self.run_harness("format")
        self.assertEqual(
            formatted.returncode, 0, formatted.stdout + formatted.stderr
        )
        before = self.fingerprint()
        result = self.run_harness("check")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(marker, result.stdout + result.stderr)
        self.assertEqual(self.fingerprint(), before)

    def test_native_format_is_idempotent_and_check_preserves_bytes(self):
        for language, name, source in (
            (
                "python",
                "src/example_app/domain.py",
                "def label(value: object)->str:\n return str(value)\n",
            ),
            (
                "typescript",
                "src/domain/label.ts",
                "export const label=(value:unknown):string=>String(value)\n",
            ),
        ):
            with self.subTest(language=language):
                # Each language gets its own independent package root.
                with tempfile.TemporaryDirectory(
                    prefix="format native "
                ) as temporary:
                    previous = self.target
                    self.target = Path(temporary).resolve()
                    try:
                        self.write(".harness/config.toml", VALID_CONFIG)
                        self.template(language)
                        self.write(name, source)
                        before = self.fingerprint()
                        first = self.run_harness("format")
                        self.assertEqual(first.returncode, 0, first.stderr)
                        once = self.fingerprint()
                        self.assertNotEqual(before, once)
                        second = self.run_harness("format")
                        self.assertEqual(second.returncode, 0, second.stderr)
                        self.assertEqual(self.fingerprint(), once)
                        checked = self.run_harness("check")
                        self.assertEqual(
                            checked.returncode,
                            0,
                            checked.stdout + checked.stderr,
                        )
                        self.assertEqual(self.fingerprint(), once)
                    finally:
                        self.target = previous

    def test_typescript_strict_type_error_is_checked(self):
        self.template("typescript")
        self.write(
            "src/domain/broken.ts", "export const broken: string = 123;\n"
        )
        self.assert_native_failure("TS2322")

    def test_typescript_untrusted_any_and_floating_promise_fail_lint(self):
        self.template("typescript")
        self.write(
            "src/domain/broken.ts",
            "export function decode(value: any): string { return value; }\nPromise.resolve(1);\n",
        )
        self.assert_native_failure("no-explicit-any")
        result = self.run_harness("check")
        self.assertIn("no-floating-promises", result.stdout + result.stderr)

    def test_typescript_domain_cannot_import_io(self):
        self.template("typescript")
        self.write("src/io/write.ts", "export const value = 1;\n")
        self.write(
            "src/domain/broken.ts",
            "import { value } from '../io/write.js';\nexport const decision = value;\n",
        )
        self.assert_native_failure("no-restricted-imports")

    def test_typescript_client_cannot_import_server(self):
        self.template("typescript")
        self.write(
            "src/server/secret.ts", "export const secret = 'synthetic';\n"
        )
        self.write(
            "src/client/main.ts",
            "import { secret } from '../server/secret.js';\nexport const leaked = secret;\n",
        )
        self.assert_native_failure("Client modules")

    def test_python_strict_return_error_is_checked(self):
        self.template("python")
        self.write(
            "src/example_app/broken.py", "def broken() -> str:\n    return 1\n"
        )
        self.assert_native_failure("reportReturnType")

    def test_python_broad_runtime_exception_fails_lint(self):
        self.template("python")
        self.write(
            "src/example_app/broken.py",
            "try:\n    int('invalid')\nexcept Exception:\n    pass\n",
        )
        self.assert_native_failure("BLE001")

    def test_python_domain_cannot_import_adapter(self):
        self.template("python")
        self.write("src/example_app/io.py", "value = 1\n")
        self.write(
            "src/example_app/domain.py",
            "from example_app.io import value\n\ndef decision() -> int:\n    return value\n",
        )
        self.assert_native_failure("TID251")

    def test_check_does_not_fix_bad_formatting(self):
        self.template("python")
        self.write("src/example_app/domain.py", "value=  1\n")
        before = self.fingerprint()
        result = self.run_harness("check")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("Would reformat", result.stdout + result.stderr)
        self.assertEqual(self.fingerprint(), before)

    def test_split_scripts_require_all_static_controls(self):
        self.write(
            "package.json", '{"scripts":{"lint":"true","typecheck":"true"}}'
        )
        result = self.run_harness("check")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("format:check", result.stderr)

    def test_direct_typescript_defaults_use_local_tools(self):
        self.template("typescript")
        package = self.target / "package.json"
        content = json.loads(package.read_text())
        content["scripts"] = {}
        package.write_text(json.dumps(content, indent=2) + "\n")
        formatted = self.run_harness("format")
        self.assertEqual(formatted.returncode, 0, formatted.stderr)
        before = self.fingerprint()
        checked = self.run_harness("check")
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertIn("node_modules/.bin/tsc", checked.stdout)
        self.assertEqual(before, self.fingerprint())

    def test_existing_package_managers_and_equivalent_formatter_are_preserved(
        self,
    ):
        self.write(
            "package.json", '{"scripts":{"format":"existing formatter"}}'
        )
        for manager, lock in (
            ("pnpm", "pnpm-lock.yaml"),
            ("yarn", "yarn.lock"),
        ):
            with self.subTest(manager=manager):
                self.write(
                    lock, "# Synthetic routing lock; not used for installs\n"
                )
                executable = self.write(
                    f"tool-bin/{manager}",
                    f'#!/bin/sh\n[ "$1" = run ] && [ "$2" = format ] || exit 2\nprintf {manager} > selected.txt\n',
                )
                executable.chmod(0o755)
                result = self.run_harness("format")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(
                    (self.target / "selected.txt").read_text(), manager
                )
                (self.target / lock).unlink()

    def test_missing_pyright_does_not_pass_after_ruff(self):
        venv.EnvBuilder(with_pip=False).create(self.target / ".venv")
        self.write("ruff/__main__.py", "# Synthetic routing probe only\n")
        self.write("main.py", "value = 1\n")
        checked = self.run_harness("check")
        self.assertEqual(checked.returncode, 1, checked.stdout + checked.stderr)
        self.assertIn("pyright", checked.stderr)

    def test_malformed_command_table_has_config_error_not_traceback(self):
        config = self.target / ".harness/config.toml"
        config.write_text(
            VALID_CONFIG.replace(
                "[project]", "commands = 42\n\n[project]"
            ).replace(
                '[commands]\nsetup = ""\nstart = ""\ncheck = ""\ntest = ""\nsmoke = ""\n',
                "",
            )
        )
        result = self.run_harness("format")
        self.assertEqual(result.returncode, 4, result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_generated_cache_does_not_select_application_markdown(self):
        import sys

        sys.path.insert(0, str(ROOT / ".harness/bin"))
        from config import validate
        from profiles import resolve

        self.write("main.py", "value = 1\n")
        self.write(".pytest_cache/README.md", "# Generated runtime cache\n")
        selection = resolve(
            self.target, validate(self.target / ".harness/config.toml")
        )
        self.assertEqual(selection["profiles"], ["python"])

    def test_native_checks_exclude_runtime_but_include_default_source(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "native_ci", ROOT / ".harness/ci/run.py"
        )
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        files = module.sources("python")
        self.assertTrue(
            any(
                "templates/python/src/example_app/domain.py" in name
                for name in files
            )
        )
        self.assertFalse(
            any(
                ".venv" in Path(name).parts
                or "node_modules" in Path(name).parts
                for name in files
            )
        )

    def test_installed_defaults_do_not_format_managed_kit(self):
        for language in ("python", "typescript"):
            with self.subTest(language=language):
                with tempfile.TemporaryDirectory(
                    prefix="installed native "
                ) as temporary:
                    previous = self.target
                    self.target = Path(temporary).resolve()
                    try:
                        self.template(language)
                        manifest = json.loads(
                            (ROOT / ".harness/manifest.json").read_text()
                        )
                        for name in [
                            *manifest["managed_files"],
                            ".harness/manifest.json",
                        ]:
                            destination = self.target / name
                            destination.parent.mkdir(
                                parents=True, exist_ok=True
                            )
                            shutil.copy2(ROOT / name, destination)
                        self.write(".harness/config.toml", VALID_CONFIG)
                        managed_before = {
                            name: (self.target / name).read_bytes()
                            for name in manifest["managed_files"]
                        }
                        formatted = self.run_harness("format")
                        self.assertEqual(
                            formatted.returncode,
                            0,
                            formatted.stdout + formatted.stderr,
                        )
                        self.assertEqual(
                            managed_before,
                            {
                                name: (self.target / name).read_bytes()
                                for name in manifest["managed_files"]
                            },
                        )
                        checked = self.run_harness("check")
                        self.assertEqual(
                            checked.returncode,
                            0,
                            checked.stdout + checked.stderr,
                        )
                    finally:
                        self.target = previous


if __name__ == "__main__":
    unittest.main()
