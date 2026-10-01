"""Release ownership exercised against full disposable installations."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
import venv


ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ".harness/release-files.json"


class ReleaseOwnershipTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="release ownership ")
        self.addCleanup(temporary.cleanup)
        self.target = Path(temporary.name).resolve()
        self.manifest = json.loads(
            (ROOT / ".harness/manifest.json").read_text()
        )
        for name in [*self.manifest["managed_files"], ".harness/manifest.json"]:
            path = self.target / name
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, path)
        shutil.copy2(
            ROOT / ".harness/default-config.toml",
            self.target / ".harness/config.toml",
        )
        self.original_manifest = (
            self.target / ".harness/manifest.json"
        ).read_bytes()

    def write(self, name, content):
        path = self.target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def command(self, command):
        environment = {
            key: value
            for key, value in os.environ.items()
            if not key.startswith("HARNESS_") and key != "CONFIG_PATH"
        }
        trace = environment.pop("QH_TEST_TRACE", None)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        started = time.monotonic()
        result = subprocess.run(
            command,
            cwd=self.target,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=45,
        )
        if trace:
            record = {
                "case": self.id(),
                "command": command,
                "exit": result.returncode,
                "feedback_seconds": round(time.monotonic() - started, 6),
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
            serialized = (
                json.dumps(record)
                .replace(str(self.target), "<temporary>")
                .replace(str(ROOT), "<repository>")
            )
            with Path(trace).open("a") as stream:
                stream.write(serialized + "\n")
        return result

    def tool(self, action="verify", *arguments):
        # The trusted verifier can inspect damaged consumer destinations safely.
        return self.command(
            [
                sys.executable,
                str(ROOT / ".harness/bin/manifest.py"),
                action,
                str(self.target),
                *arguments,
            ]
        )

    def assert_failure(self, result, message):
        self.assertEqual(result.returncode, 5, result.stdout + result.stderr)
        self.assertIn(message, result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def add_project_state(self):
        files = {
            ".agents/skills/project-specific/SKILL.md": "# Project workflow\n",
            ".agents/skills/implement-feature/project-notes.md": "Project notes\n",
            ".harness/local.env": "SYNTHETIC_VALUE=not-a-credential\n",
            ".harness/local-notes.txt": "Customer content\n",
            "AGENTS.md": "# Project instructions\n",
            "docs/PRODUCT.md": "# Project product\n",
        }
        for name, content in files.items():
            self.write(name, content)
        for directory in (
            ".harness/tests/__pycache__",
            ".harness/tests/.pytest_cache",
            ".harness/.ruff_cache",
            ".harness/tests/fixtures/.next",
            ".harness/tests/fixtures/node_modules",
            ".harness/build",
        ):
            self.write(f"{directory}/state.txt", "Generated local state\n")
        return files

    def test_full_installation_allows_project_skills_runtime_and_caches(self):
        self.assertEqual(self.tool().returncode, 0)
        files = self.add_project_state()
        environment = (
            self.target / ".harness/tests/fixtures/python-project/.venv"
        )
        venv.EnvBuilder(with_pip=False).create(environment)
        runtime = self.command(
            [
                str(environment / "bin/python"),
                "-c",
                "import importlib.util, sys; "
                "assert importlib.util.find_spec('pip') is None; print(sys.prefix)",
            ]
        )
        self.assertEqual(runtime.returncode, 0, runtime.stderr)
        verification = self.tool()
        inspection = self.command([str(self.target / "harness"), "inspect"])
        self.assertEqual(verification.returncode, 0, verification.stderr)
        self.assertEqual(inspection.returncode, 0, inspection.stderr)
        self.assertEqual(
            (self.target / ".harness/manifest.json").read_bytes(),
            self.original_manifest,
        )
        for name, content in files.items():
            self.assertEqual((self.target / name).read_text(), content)

    def test_release_output_is_exact_deterministic_and_ignores_local_state(
        self,
    ):
        files = self.add_project_state()
        venv.EnvBuilder(with_pip=False).create(
            self.target / ".harness/tests/fixtures/python-project/.venv"
        )
        (self.target / ".harness/local-link").symlink_to(ROOT)
        first = self.tool("generate-release", self.manifest["installed_at"])
        second = self.tool("generate-release", self.manifest["installed_at"])
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(json.loads(first.stdout), self.manifest)
        self.assertEqual(
            set(json.loads(first.stdout)["managed_files"]),
            set(self.manifest["managed_files"]),
        )
        for name, content in files.items():
            self.assertEqual((self.target / name).read_text(), content)
        self.assertEqual(
            (self.target / ".harness/manifest.json").read_bytes(),
            self.original_manifest,
        )

    def test_modified_and_missing_shipped_files_still_fail(self):
        for name in (
            "harness",
            ".harness/bin/common.sh",
            ".agents/skills/implement-feature/SKILL.md",
            ".harness/tests/fixtures/python-project/app.py",
        ):
            with self.subTest(name=name):
                path = self.target / name
                original = path.read_bytes()
                mode = path.stat().st_mode
                path.write_bytes(original + b"\nlocal edit\n")
                self.assert_failure(self.tool(), "checksum mismatch")
                self.assertEqual(
                    path.read_bytes(), original + b"\nlocal edit\n"
                )
                path.unlink()
                self.assert_failure(self.tool(), "missing")
                path.write_bytes(original)
                path.chmod(mode)
        self.assertEqual(self.tool().returncode, 0)
        self.assertEqual(
            (self.target / ".harness/manifest.json").read_bytes(),
            self.original_manifest,
        )

    def test_legacy_generation_cannot_repair_a_consumer_conflict(self):
        path = self.write(".harness/bin/common.sh", "# Local change\n")
        self.assert_failure(self.tool(), "checksum mismatch")
        legacy = self.tool("generate")
        self.assertEqual(legacy.returncode, 2, legacy.stdout + legacy.stderr)
        self.assertIn("generate-release", legacy.stderr)
        self.assert_failure(self.tool(), "checksum mismatch")
        self.assertEqual(path.read_text(), "# Local change\n")
        self.assertEqual(
            (self.target / ".harness/manifest.json").read_bytes(),
            self.original_manifest,
        )

    def test_release_generation_requires_every_shipped_input(self):
        (self.target / ".harness/checks/standards/README.md").unlink()
        self.assert_failure(self.tool("generate-release"), "missing")
        self.assertEqual(
            (self.target / ".harness/manifest.json").read_bytes(),
            self.original_manifest,
        )

    def test_unsafe_manifest_paths_are_rejected(self):
        for name in (
            "../outside",
            "/tmp/outside",
            "./harness",
            "harness/",
            ".harness//VERSION",
            ".harness/./VERSION",
            ".",
            "",
            "C:/outside",
            "C:\\outside",
            "bad\x00name",
            "bad\nname",
            ".harness/config.toml",
            "AGENTS.md",
        ):
            with self.subTest(name=name):
                candidate = json.loads(self.original_manifest)
                candidate["managed_files"][name] = "sha256:" + "0" * 64
                self.write(".harness/manifest.json", json.dumps(candidate))
                self.assert_failure(self.tool(), "invalid managed file")

    def test_manifest_inventory_cannot_drop_or_absorb_paths(self):
        candidate = json.loads(self.original_manifest)
        candidate["managed_files"].pop("harness")
        self.write(".harness/manifest.json", json.dumps(candidate))
        self.assert_failure(self.tool(), "inventory mismatch")
        path = self.write(
            ".agents/skills/project-specific/SKILL.md", "# Project\n"
        )
        candidate = json.loads(self.original_manifest)
        candidate["managed_files"][str(path.relative_to(self.target))] = (
            "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        )
        self.write(".harness/manifest.json", json.dumps(candidate))
        self.assert_failure(self.tool(), "inventory mismatch")

    def test_duplicate_manifest_json_keys_are_rejected(self):
        text = self.original_manifest.decode()
        repeated = '"schema_version": 1, "schema_version": 1'
        self.write(
            ".harness/manifest.json",
            text.replace('"schema_version": 1', repeated),
        )
        self.assert_failure(self.tool(), "duplicate JSON key")

    def test_release_inventory_is_required_and_checksum_protected(self):
        path = self.target / INVENTORY
        self.assertTrue(path.is_file(), "release inventory must be shipped")
        original = path.read_bytes()
        path.write_bytes(original + b"\n")
        self.assert_failure(self.tool(), "checksum mismatch")
        path.unlink()
        self.assert_failure(self.tool(), "release inventory missing")

    def test_invalid_release_inventory_entries_fail(self):
        for paths in (
            [],
            ["harness", "harness"],
            ["../outside"],
            ["./harness"],
            {"harness": "not a list"},
            [None],
            [42],
            [".harness/config.toml"],
            ["docs/PRODUCT.md"],
            [".harness/tests/.venv/local"],
            [".harness/manifest.json"],
        ):
            with self.subTest(paths=paths):
                self.write(INVENTORY, json.dumps(paths))
                self.assert_failure(
                    self.tool("generate-release"), "release inventory"
                )

    def test_shipped_symlinks_rejected_even_with_matching_content(self):
        original = (self.target / ".harness/bin/common.sh").read_bytes()
        for destination in (
            self.target / "internal-copy",
            ROOT / ".harness/bin/common.sh",
        ):
            with self.subTest(destination=str(destination)):
                if destination.parent == self.target:
                    destination.write_bytes(original)
                path = self.target / ".harness/bin/common.sh"
                path.unlink()
                path.symlink_to(destination)
                self.assert_failure(self.tool(), "symlink")
                self.assert_failure(self.tool("generate-release"), "symlink")
                path.unlink()
                path.write_bytes(original)

    def test_shipped_directory_symlink_is_rejected(self):
        path = self.target / ".harness/standards"
        destination = self.target / "internal standards"
        path.rename(destination)
        path.symlink_to(destination, target_is_directory=True)
        self.assert_failure(self.tool(), "symlink")
        self.assert_failure(self.tool("generate-release"), "symlink")

    def test_metadata_symlinks_are_rejected(self):
        for name in (".harness/manifest.json", ".harness/VERSION", INVENTORY):
            with self.subTest(name=name):
                path = self.target / name
                self.assertTrue(path.is_file())
                original = path.read_bytes()
                destination = self.target / "metadata copy"
                destination.write_bytes(original)
                path.unlink()
                path.symlink_to(destination)
                self.assert_failure(self.tool(), "symlink")
                path.unlink()
                path.write_bytes(original)

    def test_manifest_values_and_nested_duplicates_are_rejected(self):
        for key, value in (
            ("installed_at", "invalidZ"),
            ("schema_version", True),
            ("managed_files", []),
        ):
            with self.subTest(key=key):
                candidate = json.loads(self.original_manifest)
                candidate[key] = value
                self.write(".harness/manifest.json", json.dumps(candidate))
                result = self.tool()
                self.assertEqual(result.returncode, 5, result.stderr)
                self.assertNotIn("Traceback", result.stderr)
        candidate = self.original_manifest.decode().replace(
            '"managed_files": {',
            '"managed_files": {"harness": "duplicate",',
        )
        self.write(".harness/manifest.json", candidate)
        self.assert_failure(self.tool(), "duplicate JSON key")

    def test_metadata_parent_and_root_links_are_rejected(self):
        parent = self.target / ".harness"
        moved = self.target / "kit"
        parent.rename(moved)
        parent.symlink_to(moved, target_is_directory=True)
        self.assert_failure(self.tool(), "symlink")
        self.assert_failure(self.tool("generate-release"), "symlink")
        parent.unlink()
        moved.rename(parent)
        link = self.target / "installation-link"
        link.symlink_to(self.target, target_is_directory=True)
        result = self.command(
            [
                sys.executable,
                str(ROOT / ".harness/bin/manifest.py"),
                "verify",
                str(link),
            ]
        )
        self.assert_failure(result, "symlink")


if __name__ == "__main__":
    unittest.main()
