import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest


REPOSITORY_ROOT = Path(__file__).parents[2]
HARNESS = REPOSITORY_ROOT / "harness"
CONFIG_TOOL = REPOSITORY_ROOT / ".harness" / "bin" / "config.py"
MANIFEST_TOOL = REPOSITORY_ROOT / ".harness" / "bin" / "manifest.py"


VALID_CONFIG = textwrap.dedent(
    """\
    schema_version = 1

    [project]
    profiles = ["auto"]

    [commands]
    setup = ""
    start = ""
    check = ""
    test = ""
    smoke = ""

    [checks]
    required = ["architecture", "documentation", "provenance", "demo-integrity"]

    [standards]
    line_length = 100
    file_lines_warning = 350
    function_lines_warning = 50

    [readiness]
    required_documents = ["PRODUCT.md", "ARCHITECTURE.md"]
    fail_on_needs_input = false

    [security]
    mode = "local"

    [analysis]
    exclude = ["node_modules", ".venv", "dist", "build"]
    """
)


class ConfigContractTest(unittest.TestCase):
    def run_config(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CONFIG_TOOL), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )

    def write_config(self, directory: Path, content: str = VALID_CONFIG) -> Path:
        path = directory / "config.toml"
        path.write_text(content, encoding="utf-8")
        return path

    def test_valid_configuration_supports_value_lookup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = self.write_config(Path(temporary))
            validation = self.run_config("validate", str(path))
            lookup = self.run_config("get", str(path), "standards.line_length")

        self.assertEqual(validation.returncode, 0, validation.stderr)
        self.assertEqual(lookup.returncode, 0, lookup.stderr)
        self.assertEqual(lookup.stdout.strip(), "100")

    def test_unknown_key_reports_file_key_and_expected_keys(self) -> None:
        invalid = VALID_CONFIG.replace(
            'profiles = ["auto"]', 'profiles = ["auto"]\nmystery = true'
        )
        with tempfile.TemporaryDirectory() as temporary:
            path = self.write_config(Path(temporary), invalid)
            result = self.run_config("validate", str(path))

        self.assertEqual(result.returncode, 4)
        self.assertIn(str(path), result.stderr)
        self.assertIn("project.mystery", result.stderr)
        self.assertIn("expected one of", result.stderr)

    def test_invalid_value_reports_expected_type_or_range(self) -> None:
        invalid = VALID_CONFIG.replace("line_length = 100", "line_length = 0")
        with tempfile.TemporaryDirectory() as temporary:
            path = self.write_config(Path(temporary), invalid)
            result = self.run_config("validate", str(path))

        self.assertEqual(result.returncode, 4)
        self.assertIn("standards.line_length", result.stderr)
        self.assertIn("positive integer", result.stderr)

    def test_invalid_enum_type_returns_config_error_without_traceback(self) -> None:
        invalid = VALID_CONFIG.replace('mode = "local"', 'mode = ["local"]')
        with tempfile.TemporaryDirectory() as temporary:
            path = self.write_config(Path(temporary), invalid)
            result = self.run_config("validate", str(path))

        self.assertEqual(result.returncode, 4)
        self.assertIn("security.mode", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


class ManifestContractTest(unittest.TestCase):
    def run_manifest(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(MANIFEST_TOOL), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_manifest_verification_detects_modified_managed_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            harness_dir = root / ".harness"
            harness_dir.mkdir()
            managed = root / "harness"
            managed.write_text("original\n", encoding="utf-8")
            version_path = harness_dir / "VERSION"
            version_path.write_text("0.1.0\n", encoding="utf-8")
            managed_digest = hashlib.sha256(managed.read_bytes()).hexdigest()
            version_digest = hashlib.sha256(version_path.read_bytes()).hexdigest()
            manifest = {
                "schema_version": 1,
                "harness_version": "0.1.0",
                "installed_at": "2026-09-08T00:00:00Z",
                "managed_files": {
                    ".harness/VERSION": f"sha256:{version_digest}",
                    "harness": f"sha256:{managed_digest}",
                },
            }
            (harness_dir / "manifest.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )

            valid = self.run_manifest("verify", str(root))
            managed.write_text("changed\n", encoding="utf-8")
            modified = self.run_manifest("verify", str(root))

        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertEqual(modified.returncode, 5)
        self.assertIn("harness", modified.stderr)
        self.assertIn("checksum mismatch", modified.stderr)

    def test_installed_manifest_is_valid_and_contains_relative_paths(self) -> None:
        result = self.run_manifest("verify", str(REPOSITORY_ROOT))
        self.assertEqual(result.returncode, 0, result.stderr)

        manifest = json.loads(
            (REPOSITORY_ROOT / ".harness" / "manifest.json").read_text()
        )
        for path in manifest["managed_files"]:
            self.assertFalse(Path(path).is_absolute(), path)
            self.assertNotIn("..", Path(path).parts)
        self.assertNotIn(".harness/config.toml", manifest["managed_files"])


class PublicContractTest(unittest.TestCase):
    def run_harness(
        self,
        *arguments: str,
        environment: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        import os

        return subprocess.run(
            [str(HARNESS), *arguments],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, **(environment or {})},
        )

    def configured_test_command(self, command: str) -> str:
        return VALID_CONFIG.replace('test = ""', f'test = "{command}"')

    def test_command_precedence_is_cli_then_environment_then_config(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            config = target / "config.toml"
            config.write_text(
                self.configured_test_command("printf config > source.txt"),
                encoding="utf-8",
            )

            configured = self.run_harness("test", "--config", str(config), str(target))
            self.assertEqual(configured.returncode, 0, configured.stderr)
            self.assertEqual((target / "source.txt").read_text(), "config")

            environment = self.run_harness(
                "test",
                "--config",
                str(config),
                str(target),
                environment={"HARNESS_TEST_COMMAND": "printf environment > source.txt"},
            )
            self.assertEqual(environment.returncode, 0, environment.stderr)
            self.assertEqual((target / "source.txt").read_text(), "environment")

            cli = self.run_harness(
                "test",
                "--config",
                str(config),
                "--command",
                "printf cli > source.txt",
                str(target),
                environment={"HARNESS_TEST_COMMAND": "printf environment > source.txt"},
            )
            self.assertEqual(cli.returncode, 0, cli.stderr)
            self.assertEqual((target / "source.txt").read_text(), "cli")

    def test_public_exit_codes_are_stable(self) -> None:
        usage = self.run_harness("inspect", "--unknown")
        self.assertEqual(usage.returncode, 2)

        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            invalid_config = target / "invalid.toml"
            invalid_config.write_text("schema_version = 99\n", encoding="utf-8")
            invalid = self.run_harness(
                "inspect", "--config", str(invalid_config), str(target)
            )
            self.assertEqual(invalid.returncode, 4)

            delegated = self.run_harness(
                "test", "--command", "exit 17", str(target)
            )
            self.assertEqual(delegated.returncode, 1)
            self.assertIn("project command failed with exit 17", delegated.stderr)

            isolated = target / "isolated"
            isolated.mkdir()
            isolated_harness = isolated / "harness"
            isolated_harness.write_bytes(HARNESS.read_bytes())
            isolated_harness.chmod(0o755)
            broken = subprocess.run(
                [str(isolated_harness), "test"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(broken.returncode, 5)
            self.assertIn("installation error", broken.stderr)


if __name__ == "__main__":
    unittest.main()
