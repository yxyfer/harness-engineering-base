"""Native evidence, conservative identities and bounded-process regressions."""

from __future__ import annotations

import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".harness/bin"))
from evidence_identity import fingerprint  # noqa: E402
from evidence_reports import native_report, result_problem, validate_schema  # noqa: E402
from evidence_runner import execute, LOG_LIMIT, redact  # noqa: E402


class VerifyEvidenceTest(unittest.TestCase):
    def test_smoke_native_evidence_and_missing_report_fail_closed(self):
        config = self.target / ".harness/config.toml"
        original = config.read_text()
        config.write_text(
            original.replace("schema_version = 1", "schema_version = 2")
            .replace('mode = "local"', 'mode = "off"')
            .replace(
                'profiles = ["auto"]',
                'profiles = ["auto"]\nframeworks = []\ncapabilities = ["browser-ui"]\nroots = ["."]',
            )
        )
        _, report, _ = self.run_verify("--only", "smoke")
        row = next(c for c in report["controls"] if c["name"] == "smoke")
        self.assertEqual(row["state"], "unavailable")
        self.assertIn("required browser smoke-evidence", row["reason"])
        config.write_text(original)
        for xml, state in (
            (
                '<testsuite tests="1"><testcase name="journey"/></testsuite>',
                "passed",
            ),
            (
                '<testsuite tests="1"><testcase><failure/></testcase></testsuite>',
                "failed",
            ),
            ('<testsuite tests="0"/>', "failed"),
            ("malformed", "unavailable"),
        ):
            self.write(
                ".harness/smoke-evidence.json",
                json.dumps(
                    {
                        "adapter": "junit",
                        "command": [
                            sys.executable,
                            "-c",
                            "import os;from pathlib import Path;Path(os.environ['HARNESS_TEST_REPORT']).write_text("
                            + repr(xml)
                            + ")",
                        ],
                    }
                ),
            )
            _, report, _ = self.run_verify("--only", "smoke")
            row = next(c for c in report["controls"] if c["name"] == "smoke")
            self.assertEqual(row["state"], state, row)
            self.assertFalse(report["complete"])
        self.write(
            ".harness/smoke-evidence.json",
            json.dumps(
                {"adapter": "junit", "command": [sys.executable, "-c", "pass"]}
            ),
        )
        _, report, _ = self.run_verify("--only", "smoke")
        self.assertEqual(
            next(c for c in report["controls"] if c["name"] == "smoke")[
                "state"
            ],
            "unavailable",
        )
        (self.target / ".harness/smoke-evidence.json").unlink()
        (self.target / ".harness/smoke-evidence.json").symlink_to(
            self.target / "pyproject.toml"
        )
        result = subprocess.run(
            [str(ROOT / "harness"), "verify", str(self.target)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symlink", result.stderr)

    def test_server_capability_never_passes_missing_or_failed_native_evidence(
        self,
    ):
        config_path = self.target / ".harness/config.toml"
        config_path.write_text(
            config_path.read_text()
            .replace("schema_version = 1", "schema_version = 2")
            .replace('mode = "local"', 'mode = "off"')
            .replace(
                'profiles = ["auto"]',
                'profiles = ["auto"]\nframeworks = []\ncapabilities = ["identity"]\nroots = ["."]',
            )
        )
        self.write(
            "package.json",
            '{"scripts":{"test:server":"reviewed-native-suite"}}',
        )
        _, report, _ = self.run_verify("--only", "tests")
        row = next(
            c for c in report["controls"] if c["name"] == "server-boundaries"
        )
        self.assertEqual(row["state"], "unavailable")
        self.assertFalse(report["complete"])
        self.write(
            ".harness/server-evidence.json",
            json.dumps(
                {
                    "adapter": "junit",
                    "command": [
                        sys.executable,
                        "-c",
                        'import os;from pathlib import Path;Path(os.environ[\'HARNESS_TEST_REPORT\']).write_text(\'<testsuite tests="1" failures="1"><testcase name="synthetic-gate"><failure/></testcase></testsuite>\');raise SystemExit(1)',
                    ],
                }
            ),
        )
        _, report, _ = self.run_verify("--only", "tests")
        row = next(
            c for c in report["controls"] if c["name"] == "server-boundaries"
        )
        self.assertEqual(row["state"], "failed", row)
        self.assertEqual(row["counts"]["failures"], 1)
        _, report, _ = self.run_verify("--only", "check")
        row = next(
            c for c in report["controls"] if c["name"] == "server-boundaries"
        )
        self.assertEqual(row["state"], "unavailable")
        self.assertFalse(report["complete"])

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="verify evidence ")
        self.addCleanup(temporary.cleanup)
        self.target = Path(temporary.name)
        self.write(
            ".harness/config.toml",
            (ROOT / ".harness/default-config.toml")
            .read_text()
            .replace('check = ""', 'check = "true"')
            .replace('smoke = ""', 'smoke = "true"')
            .replace('  "documentation",\n', "")
            .replace('  "provenance",\n', "")
            .replace('  "demo-integrity",\n', "")
            .replace('  "standards",\n', ""),
        )
        self.write(
            "pyproject.toml", '[tool.harness.tests]\nrunner = "unittest"\n'
        )
        self.write(
            "tests/test_app.py",
            "import unittest\nclass App(unittest.TestCase):\n    def test_ok(self):\n        self.assertEqual(1, 1)\n",
        )

    def write(self, name, content):
        path = self.target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def run_verify(self, *args, environment=None):
        env = {
            k: v for k, v in os.environ.items() if not k.startswith("HARNESS_")
        }
        env.update(PYTHONDONTWRITEBYTECODE="1")
        env.update(environment or {})
        result = subprocess.run(
            [str(ROOT / "harness"), "verify", str(self.target), *args],
            capture_output=True,
            text=True,
            env=env,
            timeout=30,
        )
        reports = list((self.target / ".harness/reports").glob("*/report.json"))
        path = (
            max(reports, key=lambda p: p.stat().st_mtime_ns)
            if reports
            else None
        )
        self.assertIsNotNone(path, result.stdout + result.stderr)
        assert path is not None
        report = json.loads(path.read_text())
        return result, report, path

    def test_complete_native_success_and_output_identity(self):
        result, report, path = self.run_verify()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(report["complete"])
        self.assertEqual(report["controls"][1]["counts"]["collected"], 1)
        self.assertEqual(
            report["inputs"]["digest"],
            fingerprint(
                self.target,
                ROOT / ".harness",
                self.target / ".harness/config.toml",
            )["digest"],
        )
        check, _, _ = self.run_verify("--validate-report", str(path))
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_declared_nextjs_production_build_failure_is_required(self):
        self.write(
            "package.json",
            json.dumps(
                {
                    "dependencies": {"next": "16.3.8"},
                    "scripts": {"build": "node -e 'process.exit(23)'"},
                }
            ),
        )
        result, report, _ = self.run_verify()
        build = next(
            c for c in report["controls"] if c["name"] == "nextjs-build"
        )
        self.assertEqual(build["state"], "failed")
        self.assertTrue(build["required"])
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(report["complete"])

    def test_nextjs_build_is_omitted_not_passed_in_test_only_scope(self):
        self.write(
            "package.json",
            '{"dependencies":{"next":"16.3.8"},"scripts":{"build":"true"}}',
        )
        _, report, _ = self.run_verify("--only", "tests")
        build = next(
            c for c in report["controls"] if c["name"] == "nextjs-build"
        )
        self.assertEqual(build["state"], "unavailable")
        self.assertIn("omitted", build["reason"])

    def test_failure_and_skip_preserved(self):
        for body, counter in (
            ("self.fail('synthetic failure')", "failures"),
            ("self.skipTest('synthetic skip')", "skipped"),
        ):
            self.write(
                "tests/test_app.py",
                f"import unittest\nclass App(unittest.TestCase):\n    def test_case(self):\n        {body}\n",
            )
            result, report, _ = self.run_verify()
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(report["controls"][1]["counts"][counter], 1)

    def test_zero_required_collection(self):
        self.write("tests/test_app.py", "# no cases\n")
        result, report, _ = self.run_verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotEqual(report["controls"][1]["state"], "passed")

    def test_opaque_success_missing_report_is_unavailable(self):
        self.write(
            ".harness/evidence.json",
            json.dumps(
                {"adapter": "junit", "command": [sys.executable, "-c", "pass"]}
            ),
        )
        result, report, _ = self.run_verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(report["controls"][1]["state"], "unavailable")

    def test_malformed_native_report(self):
        self.write(
            ".harness/evidence.json",
            json.dumps(
                {
                    "adapter": "junit",
                    "command": [
                        sys.executable,
                        "-c",
                        "import os;from pathlib import Path;Path(os.environ['HARNESS_TEST_REPORT']).write_text('broken')",
                    ],
                }
            ),
        )
        result, report, _ = self.run_verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertIsNotNone(report, result.stderr)

    def test_partial_scope_is_not_complete(self):
        result, report, _ = self.run_verify("--only", "tests")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(report["scope"], "partial")
        self.assertFalse(report["complete"])

    def test_untracked_source_config_and_lock_make_evidence_stale(self):
        for name in (
            "new_source.py",
            "package-lock.json",
            ".harness/config.toml",
        ):
            _, _, path = self.run_verify()
            if name.endswith("config.toml"):
                self.write(
                    name,
                    (self.target / name).read_text() + "\n# reviewed edit\n",
                )
            else:
                self.write(name, "{}\n")
            result, _, _ = self.run_verify("--validate-report", str(path))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("stale evidence", result.stderr)

    def test_mid_run_edit_blocks_complete(self):
        self.write(
            "tests/test_app.py",
            'import unittest\nfrom pathlib import Path\nclass App(unittest.TestCase):\n    def test_mutation(self):\n        Path("new_source.py").write_text("# changed during test")\n',
        )
        result, report, _ = self.run_verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(report["stable"])

    def test_missing_executable(self):
        self.write(
            ".harness/evidence.json",
            json.dumps(
                {"adapter": "junit", "command": ["/nonexistent/native-runner"]}
            ),
        )
        result, report, _ = self.run_verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(report["controls"][1]["state"], "unavailable")

    def test_native_junit_retries_fail_and_counts_survive(self):
        path = self.write(
            "retry.xml",
            '<testsuite tests="1"><testcase name="flaky"><flakyFailure>first attempt failed</flakyFailure></testcase></testsuite>',
        )
        counts = native_report(path, "junit")
        self.assertEqual(counts["retries"], 1)
        self.assertTrue(result_problem(counts))

    def test_native_node_direct_cases_and_failure(self):
        counts = native_report(
            self.write(
                "node.xml",
                '<testsuites><testcase name="fails"><failure>synthetic</failure></testcase></testsuites>',
            ),
            "junit",
        )
        self.assertEqual(counts["collected"], 1)
        self.assertEqual(counts["failures"], 1)

    def test_native_flaky_attempts_remain_blocking(self):
        script = """import os,unittest
from pathlib import Path
attempt = 0
class Flaky(unittest.TestCase):
    def test_retry(self):
        global attempt
        attempt += 1
        self.assertGreater(attempt, 1, "first native attempt fails")
first = unittest.TestResult()
Flaky("test_retry").run(first)
second = unittest.TestResult()
Flaky("test_retry").run(second)
assert len(first.failures) == 1 and second.wasSuccessful()
Path(os.environ["HARNESS_TEST_REPORT"]).write_text('<testsuite tests="1"><testcase name="retry"><flakyFailure>first native attempt fails</flakyFailure></testcase></testsuite>')
"""
        self.write("flaky_runner.py", script)
        self.write(
            ".harness/evidence.json",
            json.dumps(
                {
                    "adapter": "junit",
                    "command": [sys.executable, "flaky_runner.py"],
                }
            ),
        )
        result, report, _ = self.run_verify("--only", "tests")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(report["controls"][1]["counts"]["retries"], 1)
        self.assertEqual(report["controls"][1]["state"], "failed")

    def test_timeout_exit_zero_does_not_pass(self):
        self.write(
            ".harness/evidence.json",
            json.dumps(
                {
                    "adapter": "unittest",
                    "command": [
                        sys.executable,
                        "-c",
                        "import signal,time,sys;signal.signal(signal.SIGTERM,lambda *_:sys.exit(0));time.sleep(10)",
                    ],
                }
            ),
        )
        result, report, _ = self.run_verify(
            "--only", "tests", "--timeout", "0.3"
        )
        self.assertNotEqual(result.returncode, 0)
        item = report["controls"][1]
        self.assertEqual(item["exit"], 0)
        self.assertEqual(item["state"], "failed")
        self.assertIn("timeout", item["reason"])

    def test_stale_artifact_is_rejected(self):
        _, report, path = self.run_verify()
        artifact = path.parent / report["controls"][0]["artifacts"][0]["path"]
        artifact.write_text("tampered evidence")
        result, _, _ = self.run_verify("--validate-report", str(path))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("evidence artifact", result.stderr)

    def test_unsupported_capability_cannot_be_complete(self):
        config = (ROOT / ".harness/config-v2.example.toml").read_text()
        config = config.replace(
            "capabilities = []", 'capabilities = ["identity"]'
        )
        self.write(".harness/config.toml", config)
        result, report, _ = self.run_verify("--only", "tests")
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(
            any(
                c["name"] == "identity" and c["state"] == "unavailable"
                for c in report["controls"]
            )
        )

    def test_maintained_symlinks_reject_incomplete_identity(self):
        link = self.target / "linked_source.py"
        link.symlink_to(self.target / "tests/test_app.py")
        with self.assertRaises(ValueError):
            fingerprint(
                self.target,
                ROOT / ".harness",
                self.target / ".harness/config.toml",
            )

    def test_redacts_malformed_native_evidence(self):
        self.write(
            ".harness/evidence.json",
            json.dumps(
                {
                    "adapter": "junit",
                    "command": [
                        sys.executable,
                        "-c",
                        "import os;from pathlib import Path;Path(os.environ['HARNESS_TEST_REPORT']).write_text('token=synthetic-secret')",
                    ],
                }
            ),
        )
        result, report, path = self.run_verify()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(report["controls"][1]["state"], "unavailable")
        self.assertNotIn(
            "synthetic-secret", (path.parent / "tests.native").read_text()
        )

    def test_native_junit_zero_and_inconsistent_counts(self):
        self.assertTrue(
            result_problem(
                native_report(
                    self.write("zero.xml", '<testsuite tests="0"/>'), "junit"
                )
            )
        )
        with self.assertRaises(ValueError):
            native_report(
                self.write(
                    "bad.xml", '<testsuite tests="2"><testcase/></testsuite>'
                ),
                "junit",
            )

    def test_report_schema_rejects_missing_and_wrong_state(self):
        _, report, _ = self.run_verify()
        schema = json.loads(
            (ROOT / ".harness/verification/schema.json").read_text()
        )
        report["controls"][0]["state"] = "pretend"
        with self.assertRaises(ValueError):
            validate_schema(report, schema)
        with self.assertRaises(ValueError):
            validate_schema({}, schema)

    def test_bounded_redacted_logs(self):
        self.assertNotIn(
            "quoted-synthetic-marker", redact('token="quoted-synthetic-marker"')
        )
        path = self.target / "log"
        old = os.environ.get("SYNTHETIC_SECRET")
        os.environ["SYNTHETIC_SECRET"] = "synthetic-sensitive-marker"
        self.addCleanup(
            lambda: os.environ.pop("SYNTHETIC_SECRET", None)
            if old is None
            else os.environ.update(SYNTHETIC_SECRET=old)
        )
        result = execute(
            [
                sys.executable,
                "-c",
                "print('synthetic-sensitive-marker token=second-marker'); print('x'*200000)",
            ],
            self.target,
            path,
            dict(os.environ),
            5,
        )
        self.assertEqual(result["exit"], 0)
        self.assertTrue(result["truncated"])
        self.assertLessEqual(path.stat().st_size, LOG_LIMIT)
        self.assertNotIn("synthetic-sensitive-marker", path.read_text())
        self.assertNotIn("second-marker", path.read_text())

    def test_timeout_terminates_descendants(self):
        pidfile = self.target / "child.pid"
        script = (
            "import subprocess,time,signal,sys; "
            f"p=subprocess.Popen([{sys.executable!r},'-c','import time;time.sleep(60)']);"
            f"open({str(pidfile)!r},'w').write(str(p.pid));"
            "signal.signal(signal.SIGTERM,lambda *_:(p.wait(timeout=2),sys.exit(0)));"
            "time.sleep(60)"
        )
        result = execute(
            [sys.executable, "-c", script],
            self.target,
            self.target / "log",
            dict(os.environ),
            0.4,
        )
        self.assertIn("timeout", result["reason"])
        child = int(pidfile.read_text())
        with self.assertRaises(ProcessLookupError):
            os.kill(child, 0)

    def test_interrupt_writes_incomplete_evidence_and_cleans_child(self):
        self.write(
            ".harness/evidence.json",
            json.dumps(
                {
                    "adapter": "unittest",
                    "command": [
                        sys.executable,
                        "-c",
                        "from pathlib import Path;import os,time;Path('running.pid').write_text(str(os.getpid()));time.sleep(60)",
                    ],
                }
            ),
        )
        env = {
            k: v for k, v in os.environ.items() if not k.startswith("HARNESS_")
        }
        process = subprocess.Popen(
            [str(ROOT / "harness"), "verify", str(self.target)],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        deadline = time.monotonic() + 10
        while (
            not (self.target / "running.pid").exists()
            and time.monotonic() < deadline
        ):
            time.sleep(0.05)
        process.send_signal(signal.SIGINT)
        stdout, stderr = process.communicate(timeout=10)
        self.assertNotEqual(process.returncode, 0)
        paths = list((self.target / ".harness/reports").glob("*/report.json"))
        self.assertTrue(paths, stdout + stderr)
        self.assertFalse(json.loads(paths[0].read_text())["complete"])
        child = int((self.target / "running.pid").read_text())
        with self.assertRaises(ProcessLookupError):
            os.kill(child, 0)
