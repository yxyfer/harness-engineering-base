"""Native security findings and unavailable evidence must remain distinct."""

import importlib
from datetime import datetime, timedelta, timezone
import json
import os
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest
import venv
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".harness/bin"))


class SecurityContractTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="security synthetic ")
        self.addCleanup(temporary.cleanup)
        self.target = Path(temporary.name).resolve()
        self.work = self.target / ".harness/reports/native"
        self.work.mkdir(parents=True)
        self.reports = importlib.import_module("security_reports")
        self.advisories = importlib.import_module("security_advisories")
        self.security = importlib.import_module("security")
        self.isolation = importlib.import_module("isolation")

    def write(self, name, contents):
        path = self.target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents)
        return path

    def test_native_clean_and_malformed_dependency_data(self):
        self.assertEqual(
            self.reports.dependencies({"dependencies": []}, "python", "r.lock"),
            [],
        )
        for native in (
            {},
            {"dependencies": [{"name": "x", "skip_reason": "not found"}]},
        ):
            with self.assertRaises(ValueError):
                self.reports.dependencies(native, "python", "r.lock")
        npm = {
            "auditReportVersion": 2,
            "vulnerabilities": {},
            "metadata": {"dependencies": {}},
        }
        self.assertEqual(
            self.reports.dependencies(npm, "npm", "package-lock.json"), []
        )
        npm["error"] = {"code": "ENOAUDIT"}
        with self.assertRaises(ValueError):
            self.reports.dependencies(npm, "npm", "package-lock.json")

    def test_native_npm_severities(self):
        npm = {
            "auditReportVersion": 2,
            "metadata": {"dependencies": {}},
            "vulnerabilities": {
                "synthetic": {
                    "range": "<2",
                    "via": [{"source": 123, "severity": "high"}],
                }
            },
        }
        rows = self.reports.dependencies(npm, "npm", "package-lock.json")
        self.assertTrue(self.reports.apply_policy(rows, [])[0]["blocking"])
        npm["vulnerabilities"]["synthetic"]["via"][0]["severity"] = "low"
        rows = self.reports.dependencies(npm, "npm", "package-lock.json")
        self.assertFalse(self.reports.apply_policy(rows, [])[0]["blocking"])

    def test_expired_broad_duplicate_and_secret_exceptions_rejected(self):
        row = self.reports.finding(
            "source-python", "S307", "main.py", "high", line=1
        )
        tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
        exception = {
            "fingerprint": row["fingerprint"],
            "owner": "repository owner",
            "reason": "synthetic approved fixture",
            "expires": tomorrow,
        }
        self.assertTrue(
            self.reports.apply_policy([row], [exception])[0]["excepted"]
        )
        self.assertFalse(row["blocking"])
        for changes in (
            {"expires": "2000-01-01T00:00:00Z"},
            {"fingerprint": "*"},
            {"owner": ""},
            {
                "expires": (
                    datetime.now(timezone.utc) + timedelta(days=91)
                ).isoformat()
            },
        ):
            with self.assertRaises(ValueError):
                self.reports.validate_exceptions([{**exception, **changes}])
        with self.assertRaises(ValueError):
            self.reports.validate_exceptions([exception, exception])
        secret = self.reports.finding(
            "secrets", "github-pat", "env", "critical", line=1
        )
        with self.assertRaises(ValueError):
            self.reports.apply_policy(
                [secret], [{**exception, "fingerprint": secret["fingerprint"]}]
            )

    def test_offline_missing_malformed_expired_lock_changed_and_failed_capture(
        self,
    ):
        lock = {"path": "requirements.lock", "ecosystem": "python"}
        self.write(lock["path"], "synthetic==1.0\n")
        path = self.advisories.cache_path(self.target, lock)
        with self.assertRaises(ValueError):
            self.advisories.offline(self.target, lock)
        path.parent.mkdir(parents=True, exist_ok=True)
        saved = {
            "source": self.advisories.SOURCES["python"],
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "tool": self.advisories.VERSIONS["python"],
            "lock_digest": self.advisories.lock_id(self.target, lock),
            "exit": 0,
            "report": {
                "dependencies": [
                    {"name": "synthetic", "version": "1.0", "vulns": []}
                ]
            },
        }
        path.write_text(json.dumps(saved))
        self.assertEqual(self.advisories.offline(self.target, lock)[0], [])
        for changes in (
            {"fetched_at": "2000-01-01T00:00:00Z"},
            {"lock_digest": "changed"},
            {"exit": 42},
            {"report": {}},
            {"exit": 1},
            {"source": "unreviewed"},
        ):
            path.write_text(json.dumps({**saved, **changes}))
            with self.assertRaises((ValueError, KeyError)):
                self.advisories.offline(self.target, lock)
        path.write_text("malformed")
        with self.assertRaises(ValueError):
            self.advisories.offline(self.target, lock)

    def test_unsafe_policy_paths_symlinks_and_missing_root_lock(self):
        settings = {
            "schema_version": 1,
            "dependency_scope": "synthetic stdlib fixture",
            "locks": [],
            "exceptions": [],
        }
        policy = self.write(".harness/security.json", json.dumps(settings))
        self.assertEqual(self.reports.policy(self.target)["locks"], [])
        for path in ("../outside", "/tmp/no", "a//b", "a\\b"):
            policy.write_text(
                json.dumps(
                    {
                        **settings,
                        "locks": [{"path": path, "ecosystem": "python"}],
                    }
                )
            )
            with self.assertRaises(ValueError):
                self.reports.policy(self.target)
        self.write("requirements.lock", "synthetic==1\n")
        (self.target / "linked.lock").symlink_to(
            self.target / "requirements.lock"
        )
        policy.write_text(
            json.dumps(
                {
                    **settings,
                    "locks": [{"path": "linked.lock", "ecosystem": "python"}],
                }
            )
        )
        with self.assertRaises(ValueError):
            self.reports.policy(self.target)
        policy.write_text(json.dumps(settings))
        self.write("package.json", "{}")
        with self.assertRaises(ValueError):
            self.reports.policy(self.target)

    def test_synthetic_environment_does_not_inherit_credentials_or_hooks(self):
        with patch.dict(
            os.environ,
            {
                "OPENAI_API_KEY": "synthetic-inherited-secret",
                "AWS_SECRET_ACCESS_KEY": "synthetic-aws",
                "NODE_OPTIONS": "--require=untrusted",
                "HARNESS_TEST_COMMAND": "bad",
                "PYTHONPATH": "/untrusted",
            },
        ):
            env = self.isolation.environment(self.target, self.work)
        self.assertNotIn("OPENAI_API_KEY", env)
        self.assertNotIn("AWS_SECRET_ACCESS_KEY", env)
        self.assertNotIn("NODE_OPTIONS", env)
        self.assertNotIn("HARNESS_TEST_COMMAND", env)
        self.assertNotIn("PYTHONPATH", env)
        self.assertEqual(env["HARNESS_ENVIRONMENT"], "synthetic")

    def test_actual_native_secret_finding_safe_case_and_no_disclosure(self):
        from evidence_identity import digest

        secret = "ghp_" + digest(b"synthetic security test only")[:36]
        self.write(".env", "GITHUB_TOKEN=" + secret + "\n")
        env = self.isolation.environment(self.target, self.work)
        rows = self.security.secrets(
            self.target, self.work, env, {"files": {".env": "synthetic"}}
        )
        self.assertTrue(rows)
        self.assertEqual(rows[0]["control"], "secrets")
        for path in self.work.rglob("*"):
            if path.is_file():
                self.assertNotIn(secret, path.read_text())
        self.write(".env", "ENVIRONMENT=synthetic\n")
        self.assertEqual(
            self.security.secrets(
                self.target, self.work, env, {"files": {".env": "synthetic"}}
            ),
            [],
        )

    def test_native_source_security_positive_and_safe_python(self):
        from evidence_identity import digest

        (self.target / ".venv").symlink_to(ROOT / ".venv")
        source = self.write("main.py", "result = eval(input())\n")
        env = self.isolation.environment(self.target, self.work)
        rows = self.security.source(self.target, self.work, env, {}, "python")
        self.assertEqual(rows[0]["id"], "S307")
        self.assertNotIn(
            "eval(input())", (self.work / "source.native").read_text()
        )
        source.write_text("result = 1\n")
        self.assertEqual(
            self.security.source(self.target, self.work, env, {}, "python"), []
        )
        self.assertTrue(digest(source.read_bytes()))

    def test_native_javascript_security_and_missing_required_tool(self):
        fixture = ROOT / ".harness/tests/fixtures/nextjs-project"
        (self.target / "node_modules").symlink_to(fixture / "node_modules")
        self.write(
            "eslint.config.mjs", (fixture / "eslint.config.mjs").read_text()
        )
        source = self.write("main.mjs", "eval('1');\n")
        env = self.isolation.environment(self.target, self.work)
        rows = self.security.source(
            self.target, self.work, env, {}, "typescript"
        )
        self.assertTrue(any(row["id"] == "no-eval" for row in rows))
        source.write_text("export const value = 1;\n")
        self.assertEqual(
            self.security.source(self.target, self.work, env, {}, "typescript"),
            [],
        )
        with patch.object(
            self.security,
            "node_tool",
            side_effect=ValueError("required tool missing"),
        ):
            with self.assertRaises(ValueError):
                self.security.source(
                    self.target, self.work, env, {}, "typescript"
                )

    def test_native_scanner_failure_missing_report_and_contradictory_exit(self):
        env = self.isolation.environment(self.target, self.work)
        report = self.work / "native.json"
        cases = [
            "import sys;sys.exit(42)",
            "pass",
            "from pathlib import Path;Path("
            + repr(str(report))
            + ").write_text('[]');raise SystemExit(1)",
        ]
        for code in cases:
            with self.assertRaises(ValueError):
                self.security.scanner(
                    [sys.executable, "-c", code],
                    self.target,
                    self.work,
                    env,
                    report,
                    lambda x: x,
                )

    def test_actual_external_egress_child_http_and_loopback(self):
        from evidence_runner import execute

        env = self.isolation.environment(self.target, self.work)
        command = self.isolation.command(
            [sys.executable, str(ROOT / ".harness/bin/isolation_probe.py")]
        )
        log = self.work / "isolation.log"
        result = execute(command, self.target, log, env, 10)
        self.assertEqual(result["exit"], 0, log.read_text())
        self.assertEqual(json.loads(log.read_text())["direct_egress"], "denied")

    def test_unavailable_external_isolation_has_no_fallback(self):
        with patch.object(self.isolation.sys, "platform", "unsupported"):
            with self.assertRaises(ValueError):
                self.isolation.command([sys.executable, "-c", "pass"])

    def test_real_no_pip_environment_does_not_remove_source_control(self):
        venv.EnvBuilder(with_pip=False).create(self.target / ".venv")
        self.write("main.py", "value = 1\n")
        env = self.isolation.environment(self.target, self.work)
        with self.assertRaisesRegex(ValueError, "ruff missing"):
            self.security.source(self.target, self.work, env, {}, "python")

    def test_security_interruption_keeps_all_required_gaps_visible(self):
        self.write(
            ".harness/security.json",
            json.dumps(
                {
                    "schema_version": 1,
                    "dependency_scope": "synthetic stdlib",
                    "locks": [],
                    "exceptions": [],
                }
            ),
        )
        config_path = self.write(
            ".harness/config.toml",
            (ROOT / ".harness/default-config.toml").read_text(),
        )
        config = importlib.import_module("config").validate(config_path)
        with patch.object(
            self.security, "secrets", side_effect=KeyboardInterrupt
        ):
            rows = self.security.run(
                self.target, config_path, config, self.work
            )
        self.assertTrue(all(r["state"] == "unavailable" for r in rows))
        self.assertTrue(
            all(r["reason"].startswith("interrupted") for r in rows)
        )

    def test_secured_verify_actual_native_success_and_missing_policy(self):
        # Use the shipped fallback shape with only architecture for this
        # coordinator fixture; native security, runner and isolation still run.
        configured = (
            (ROOT / ".harness/default-config.toml")
            .read_text()
            .replace('check = ""', 'check = "true"')
            .replace('smoke = ""', 'smoke = "true"')
        )
        for policy_name in (
            "documentation",
            "provenance",
            "demo-integrity",
            "standards",
        ):
            configured = configured.replace(f'  "{policy_name}",\n', "")
        self.write(".harness/config.toml", configured)
        self.write(
            ".harness/security.json",
            json.dumps(
                {
                    "schema_version": 1,
                    "dependency_scope": "Synthetic stdlib-only coordinator fixture",
                    "locks": [],
                    "exceptions": [],
                }
            ),
        )
        (self.target / ".venv").symlink_to(ROOT / ".venv")
        self.write(
            "tests/test_app.py",
            "import unittest\nclass App(unittest.TestCase):\n    def test_synthetic(self):\n        self.assertEqual(2 + 2, 4)\n",
        )
        argv = [
            sys.executable,
            str(ROOT / ".harness/bin/python-tests.py"),
            "unittest",
            "tests",
        ]
        self.write(
            ".harness/evidence.json",
            json.dumps({"adapter": "unittest", "command": argv}),
        )
        env = {
            k: v for k, v in os.environ.items() if not k.startswith("HARNESS_")
        }
        result = subprocess.run(
            [str(ROOT / "harness"), "verify", str(self.target)],
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report_path = next(
            (self.target / ".harness/reports").glob("verify-*/report.json")
        )
        report = json.loads(report_path.read_text())
        self.assertTrue(report["complete"])
        self.assertTrue(report["stable"])
        tests = next(c for c in report["controls"] if c["name"] == "tests")
        self.assertEqual(tests["counts"]["collected"], 1)
        self.assertIn("sandbox-exec", tests["command"][0])
        # Reviewed security remains applicable without its required data.
        self.write(".harness/security.json", "{}")
        failed = subprocess.run(
            [str(ROOT / "harness"), "verify", str(self.target)],
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn(
            "security policy missing, invalid or expired", failed.stdout
        )

    def test_advisory_capture_changes_identity_but_report_writes_do_not(self):
        from evidence_identity import fingerprint

        config = self.write(
            ".harness/config.toml",
            (ROOT / ".harness/default-config.toml").read_text(),
        )
        lock = {"path": "requirements.lock", "ecosystem": "python"}
        self.write(lock["path"], "synthetic==1\n")
        self.write(".harness/security.json", json.dumps({"locks": [lock]}))
        first = fingerprint(self.target, ROOT / ".harness", config)["digest"]
        cache = self.advisories.cache_path(self.target, lock)
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text("synthetic capture bytes")
        second = fingerprint(self.target, ROOT / ".harness", config)["digest"]
        self.assertNotEqual(first, second)
        self.write(".harness/reports/generated.json", "generated report")
        self.assertEqual(
            second,
            fingerprint(self.target, ROOT / ".harness", config)["digest"],
        )

    def test_native_dependency_findings_not_success(self):
        security = importlib.import_module("security_reports")
        report = {
            "dependencies": [
                {
                    "name": "synthetic",
                    "version": "1.0",
                    "vulns": [{"id": "SYNTHETIC-001", "fix_versions": ["2.0"]}],
                }
            ],
            "fixes": [],
        }
        findings = security.dependencies(report, "python", "requirements.lock")
        self.assertEqual(findings[0]["id"], "SYNTHETIC-001")
        self.assertEqual(findings[0]["severity"], "unknown")

    def test_missing_native_data_is_not_clean(self):
        security = importlib.import_module("security_reports")
        with self.assertRaises(ValueError):
            security.dependencies({}, "python", "requirements.lock")


if __name__ == "__main__":
    unittest.main()
