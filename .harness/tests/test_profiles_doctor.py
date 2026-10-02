"""Read-only applicability and prerequisite boundaries in temporary projects."""

import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import venv

from test_phase2_contract import VALID_CONFIG

ROOT = Path(__file__).resolve().parents[2]
V2 = (
    VALID_CONFIG.replace("schema_version = 1", "schema_version = 2")
    .replace(
        'profiles = ["auto"]',
        'profiles = ["auto"]\nframeworks = ["auto"]\ncapabilities = []\nroots = ["."]',
    )
    .replace('mode = "local"', 'mode = "off"')
    .replace(
        'required_documents = ["PRODUCT.md", "ARCHITECTURE.md"]',
        'required_documents = ["auto"]',
    )
)


class ProfilesDoctorTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="profile doctor ")
        self.addCleanup(temporary.cleanup)
        self.target = Path(temporary.name)
        self.config = self.write(".harness/config.toml", V2)

    def write(self, name, text):
        path = self.target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def resolve(self):
        sys.path.insert(0, str(ROOT / ".harness/bin"))
        module = importlib.import_module("profiles")
        config = importlib.import_module("config").validate(self.config)
        return module.resolve(self.target, config)

    def command(self, action="doctor"):
        environment = {
            k: v
            for k, v in os.environ.items()
            if not k.startswith("HARNESS_") and k != "CONFIG_PATH"
        }
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        environment["PATH"] = (
            str(ROOT / ".harness/ci/node_modules/.bin")
            + ":"
            + environment["PATH"]
        )
        result = subprocess.run(
            [str(ROOT / "harness"), action, str(self.target)],
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

    def test_plain_python_has_no_browser_design_or_data_requirement(self):
        self.write("main.py", "print('synthetic')\n")
        selection = self.resolve()
        self.assertEqual(selection["profiles"], ["python"])
        self.assertEqual(selection["frameworks"], [])
        self.assertEqual(selection["capabilities"], [])
        self.assertNotIn("DESIGN.md", selection["documents"])
        self.assertNotIn("DATA.md", selection["documents"])
        self.assertTrue(
            any(c["name"] == "python-static" for c in selection["controls"])
        )

    def test_nextjs_initial_contract_requires_native_build_tests_and_smoke(
        self,
    ):
        self.write(
            "package.json",
            json.dumps(
                {
                    "dependencies": {"next": "16.3.8"},
                    "scripts": {
                        "build": "next build",
                        "test": "vitest run",
                        "smoke": "playwright test",
                    },
                }
            ),
        )
        self.write(
            ".harness/evidence.json",
            json.dumps(
                {
                    "adapter": "junit",
                    "command": ["node", "local-runner", "{report}"],
                }
            ),
        )
        selection = self.resolve()
        initial = [
            c
            for c in selection["controls"]
            if c["name"] in {"nextjs", "browser-ui"}
        ]
        self.assertTrue(all(c["status"] == "implemented" for c in initial))
        self.assertFalse(selection["issues"])
        self.write(
            "package.json", json.dumps({"dependencies": {"next": "16.3.8"}})
        )
        self.assertTrue(self.resolve()["issues"])

    def test_nextjs_native_contract_does_not_establish_other_capabilities(self):
        self.write(
            "package.json",
            json.dumps(
                {
                    "dependencies": {"next": "16.3.8"},
                    "scripts": {
                        "build": "next build",
                        "test": "vitest run",
                        "smoke": "playwright test",
                    },
                }
            ),
        )
        self.write(
            ".harness/evidence.json",
            '{"adapter":"junit","command":["node","runner"]}',
        )
        self.config.write_text(
            V2.replace("capabilities = []", 'capabilities = ["identity"]')
        )
        self.assertTrue(
            any("identity" in issue for issue in self.resolve()["issues"])
        )

    def test_typescript_selects_native_controls(self):
        self.write("src/main.ts", "export const value = 1;\n")
        selection = self.resolve()
        self.assertEqual(selection["profiles"], ["typescript"])
        self.assertTrue(
            any(c["name"] == "typescript-static" for c in selection["controls"])
        )

    def test_next_dependency_selects_framework_even_without_source(self):
        self.write("package.json", json.dumps({"dependencies": {"next": "1"}}))
        selection = self.resolve()
        self.assertIn("typescript", selection["profiles"])
        self.assertEqual(selection["frameworks"], ["nextjs"])
        self.assertIn("browser-ui", selection["capabilities"])
        self.assertIn("DESIGN.md", selection["documents"])
        self.assertIn("unsupported", " ".join(selection["issues"]))
        self.assertIn("dependencies.next", str(selection["reasons"]))

    def test_fixture_name_does_not_establish_nextjs(self):
        self.write("package.json", '{"name":"nextjs-project"}')
        self.write("app/page.jsx", "export default null;\n")
        self.assertEqual(self.resolve()["frameworks"], [])

    def test_reviewed_profiles_survive_absent_detection(self):
        self.config.write_text(
            V2.replace('profiles = ["auto"]', 'profiles = ["python"]')
        )
        selection = self.resolve()
        self.assertIn("python", selection["profiles"])
        self.assertIn("reviewed", str(selection["reasons"]))

    def test_contradiction_retains_detected_and_reviewed_controls(self):
        self.config.write_text(
            V2.replace('profiles = ["auto"]', 'profiles = ["typescript"]')
        )
        self.write("main.py", "value = 1\n")
        before = self.config.read_bytes()
        selection = self.resolve()
        self.assertEqual(selection["profiles"], ["python", "typescript"])
        self.assertIn("contradiction", " ".join(selection["issues"]))
        self.assertEqual(self.config.read_bytes(), before)

    def test_reviewed_framework_cannot_be_removed_by_detection(self):
        self.config.write_text(
            V2.replace('frameworks = ["auto"]', 'frameworks = ["nextjs"]')
        )
        self.assertEqual(self.resolve()["frameworks"], ["nextjs"])

    def test_explicit_framework_absence_cannot_hide_next_dependency(self):
        self.config.write_text(
            V2.replace('frameworks = ["auto"]', "frameworks = []")
        )
        self.write("package.json", '{"dependencies":{"next":"1"}}')
        selection = self.resolve()
        self.assertIn("nextjs", selection["frameworks"])
        self.assertIn("contradiction", " ".join(selection["issues"]))

    def test_unsupported_capability_remains_a_required_visible_gap(self):
        self.config.write_text(
            V2.replace("capabilities = []", 'capabilities = ["identity"]')
        )
        selection = self.resolve()
        self.assertIn("identity", selection["capabilities"])
        self.assertIn("SECURITY.md", selection["documents"])
        self.assertIn("unsupported", " ".join(selection["issues"]))

    def test_unknown_capability_cannot_disappear(self):
        self.config.write_text(
            V2.replace(
                "capabilities = []", 'capabilities = ["quantum-storage"]'
            )
        )
        self.assertIn("quantum-storage", " ".join(self.resolve()["issues"]))

    def test_nested_mixed_packages_require_explicit_handling(self):
        self.write("api/pyproject.toml", '[project]\nname = "synthetic"\n')
        self.write("web/package.json", '{"dependencies":{"next":"1"}}')
        selection = self.resolve()
        self.assertIn("python", selection["profiles"])
        self.assertIn("typescript", selection["profiles"])
        self.assertIn("multi-package", " ".join(selection["issues"]))

    def test_workspaces_are_not_silently_one_package(self):
        self.write("package.json", '{"workspaces":["packages/*"]}')
        self.assertIn("multi-package", " ".join(self.resolve()["issues"]))

    def test_declared_multiple_roots_are_explicitly_unsupported(self):
        self.config.write_text(
            V2.replace('roots = ["."]', 'roots = ["api", "web"]')
        )
        (self.target / "api").mkdir()
        (self.target / "web").mkdir()
        self.assertIn("multi-package", " ".join(self.resolve()["issues"]))

    def test_unsafe_or_symlink_root_is_rejected(self):
        for root in ("../outside", "/tmp", "api//nested"):
            self.config.write_text(
                V2.replace('roots = ["."]', f'roots = ["{root}"]')
            )
            result = self.command()
            self.assertEqual(
                result.returncode, 4, result.stdout + result.stderr
            )
        self.config.write_text(V2.replace('roots = ["."]', 'roots = ["link"]'))
        (self.target / "link").symlink_to(self.target)
        self.assertIn("symlink", " ".join(self.resolve()["issues"]))

    def test_missing_tool_does_not_remove_python_control(self):
        self.write("main.py", "value = 1\n")
        venv.EnvBuilder(with_pip=False).create(self.target / ".venv")
        before = self.config.read_bytes()
        result = self.command()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("python-static", result.stdout)
        self.assertIn("ruff", result.stdout.lower())
        self.assertIn("missing", result.stdout.lower())
        self.assertEqual(self.config.read_bytes(), before)

    def test_readiness_flag_changes_documentation_exit(self):
        self.config.write_text(
            VALID_CONFIG.replace(
                "fail_on_needs_input = false", "fail_on_needs_input = true"
            )
        )
        self.write("AGENTS.md", "# Synthetic project\n")
        self.write(
            "docs/PRODUCT.md", "# Product\n\nStatus: needs-project-input\n"
        )
        self.write("docs/ARCHITECTURE.md", "# Architecture\n")
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / ".harness/checks/documentation/check"),
                str(self.target),
            ],
            capture_output=True,
            text=True,
            env={**os.environ, "CONFIG_PATH": str(self.config)},
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_legacy_config_keeps_explicit_documents_and_warns_security(self):
        self.config.write_text(VALID_CONFIG)
        before = self.config.read_bytes()
        selection = self.resolve()
        self.assertEqual(
            selection["documents"], ["ARCHITECTURE.md", "PRODUCT.md"]
        )
        self.assertIn("deprecated", " ".join(selection["warnings"]))
        self.assertEqual(self.config.read_bytes(), before)

    def test_v2_requested_security_mode_selects_required_controls(self):
        self.config.write_text(V2.replace('mode = "off"', 'mode = "ci"'))
        selection = self.resolve()
        self.assertTrue(
            any(c["name"] == "security-baseline" for c in selection["controls"])
        )
        self.assertTrue(
            any(c["name"] == "test-isolation" for c in selection["controls"])
        )
        self.assertIn("SECURITY.md", selection["documents"])

    def test_v2_required_context_cannot_be_excluded(self):
        self.config.write_text(
            V2.replace(
                'exclude = ["node_modules", ".venv", "dist", "build"]',
                'exclude = ["docs"]',
            )
        )
        result = self.command()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("docs/PRODUCT.md: missing", result.stdout)

    def test_readiness_only_gates_required_unfinished_context(self):
        self.write("AGENTS.md", "# Synthetic\n")
        for name in ("PRODUCT", "ARCHITECTURE", "QUALITY", "DECISIONS"):
            self.write(f"docs/{name}.md", f"# {name}\n")
        self.write(
            "docs/DESIGN.md", "# Design\n\nStatus: needs-project-input\n"
        )
        sys.path.insert(0, str(ROOT / ".harness/bin"))
        config = importlib.import_module("config").validate(self.config)
        module = importlib.import_module("readiness")
        self.assertFalse(
            any(
                r["blocking"]
                for r in module.context_status(
                    self.target, config, self.resolve()
                )
            )
        )
        self.write(
            "docs/PRODUCT.md", "# Product\n\nStatus: needs-project-input\n"
        )
        self.config.write_text(
            V2.replace(
                "fail_on_needs_input = false", "fail_on_needs_input = true"
            )
        )
        config = importlib.import_module("config").validate(self.config)
        self.assertTrue(
            any(
                r["blocking"]
                for r in module.context_status(
                    self.target, config, self.resolve()
                )
            )
        )

    def test_schema_validation_rejects_malformed_selection_without_traceback(
        self,
    ):
        for old, new in (
            ("capabilities = []", "capabilities = [42]"),
            ('frameworks = ["auto"]', 'frameworks = ["auto", "nextjs"]'),
            ('roots = ["."]', 'roots = ["API", "api"]'),
        ):
            self.config.write_text(V2.replace(old, new))
            result = self.command()
            self.assertEqual(result.returncode, 4, result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_next_metadata_symlink_is_not_followed(self):
        other = self.write("other.json", '{"dependencies":{"next":"1"}}')
        (self.target / "package.json").symlink_to(other)
        selection = self.resolve()
        self.assertIn("symlink", " ".join(selection["issues"]))
        self.assertEqual(selection["frameworks"], [])

    def test_shipped_machinery_is_not_an_application_language(self):
        self.write(".harness/bin/internal.py", "value = 1\n")
        self.write(".harness/ci/package.json", "{}")
        self.write("main.ts", "export const value = 1;\n")
        selection = self.resolve()
        self.assertEqual(selection["profiles"], ["typescript"])
        self.assertFalse(selection["issues"])

    def test_check_contradiction_blocks_project_override(self):
        self.config.write_text(
            V2.replace(
                'profiles = ["auto"]', 'profiles = ["typescript"]'
            ).replace('check = ""', 'check = "touch project-ran"')
        )
        self.write("main.py", "value = 1\n")
        result = self.command("check")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("contradiction", result.stdout)
        self.assertFalse((self.target / "project-ran").exists())

    def test_doctor_is_read_only_and_does_not_execute_controls(self):
        self.write("main.ts", "export const value = 1;\n")
        self.write("package.json", '{"scripts":{"test":"touch control-ran"}}')
        for name in ("PRODUCT", "ARCHITECTURE", "QUALITY", "DECISIONS"):
            self.write(f"docs/{name}.md", f"# Synthetic {name}\n")
        self.write("AGENTS.md", "# Synthetic\n")
        for name in ("prettier", "eslint", "tsc"):
            path = self.write(
                f"node_modules/.bin/{name}",
                "#!/bin/sh\ntouch control-ran\nexit 42\n",
            )
            path.chmod(0o755)
        before = self.config.read_bytes()
        result = self.command()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("no checks executed", result.stdout)
        self.assertFalse((self.target / "control-ran").exists())
        self.assertEqual(before, self.config.read_bytes())
