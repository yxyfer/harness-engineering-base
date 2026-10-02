"""Thin fixed control coordination; native commands remain authoritative."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import sys
import tempfile
import time
import uuid

from config import validate
from evidence_identity import digest, fingerprint
from evidence_reports import native_report, result_problem, validate_evidence
from evidence_runner import execute, redact, tools
from profiles import resolve
from isolation import command as isolate, environment as synthetic_environment
from security import enabled as security_enabled, run as security_controls

KIT = Path(__file__).resolve().parents[1]
ROOT = KIT.parent


def test_command(
    target: Path, config: dict, report: Path
) -> tuple[list[str], str]:
    evidence = target / ".harness/evidence.json"
    if evidence.exists():
        if evidence.is_symlink():
            raise ValueError("evidence configuration must not be a symlink")
        settings = json.loads(evidence.read_text())
        if set(settings) != {"adapter", "command"} or settings[
            "adapter"
        ] not in {
            "junit",
            "unittest",
        }:
            raise ValueError(
                "evidence.json requires adapter (junit/unittest) and command"
            )
        command = settings["command"]
        if (
            type(command) is not list
            or not command
            or any(type(c) is not str or not c for c in command)
        ):
            raise ValueError("evidence command must be a non-empty argv list")
        return [
            part.replace("{report}", str(report)) for part in command
        ], settings["adapter"]
    if (
        config["commands"]["test"]
        or os.environ.get("HARNESS_TEST_COMMAND")
        or (target / "package.json").exists()
    ):
        raise ValueError(
            "opaque test command requires reviewed .harness/evidence.json native adapter"
        )
    spec = importlib.util.spec_from_file_location(
        "python_tests", KIT / "bin/python-tests.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    runner = module.resolve_runner(target)
    python = (
        str(target / ".venv/bin/python")
        if (target / ".venv").exists()
        else shutil.which("python3")
    )
    if not python:
        raise ValueError("required Python unavailable")
    if runner == "pytest":
        return [python, "-m", "pytest", f"--junitxml={report}"], "junit"
    return [
        python,
        str(KIT / "bin/python-tests.py"),
        "unittest",
        "tests",
    ], "unittest"


def control(name: str, reason: str) -> dict:
    return {
        "name": name,
        "required": True,
        "state": "unavailable",
        "reason": reason,
        "command": [],
        "exit": None,
        "seconds": 0.0,
        "counts": None,
        "artifacts": [],
        "truncated": False,
    }


def run_control(
    item: dict,
    command: list[str],
    target: Path,
    directory: Path,
    env: dict,
    timeout: float,
    adapter: str | None = None,
) -> None:
    log = directory / (item["name"] + ".log")
    item["command"] = [redact(part) for part in command]
    try:
        outcome = execute(command, target, log, env, timeout)
        item.update(outcome)
        item["state"] = (
            "passed"
            if item["exit"] == 0
            and item["reason"] == "native command completed"
            else "failed"
        )
        if adapter and not item["reason"].startswith(
            ("interrupted", "timeout")
        ):
            path = Path(env["HARNESS_TEST_REPORT"])
            counts = native_report(path, adapter)
            item["counts"] = counts
            problem = result_problem(counts)
            if problem:
                item.update(state="failed", reason=problem)
    except (OSError, ValueError, KeyError, TypeError) as error:
        item.update(state="unavailable", reason=redact(str(error)))
    if adapter:
        path = Path(env["HARNESS_TEST_REPORT"])
        if path.is_file() and not path.is_symlink():
            with path.open("rb") as stream:
                raw = stream.read(4 * 1024 * 1024)
            path.write_text(redact(raw.decode(errors="replace")))
            item["artifacts"].append(
                {"path": path.name, "sha256": digest(path.read_bytes())}
            )
    if log.exists():
        item["artifacts"].append(
            {"path": log.name, "sha256": digest(log.read_bytes())}
        )


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default=".")
    parser.add_argument("--config")
    parser.add_argument(
        "--only", nargs="+", choices=["check", "tests", "smoke", "self-test"]
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--validate-report", type=Path)
    return parser.parse_args()


def main() -> int:
    args = arguments()
    target = Path(args.target).resolve()
    config_path = Path(
        args.config
        or os.environ.get("HARNESS_CONFIG")
        or (
            target / ".harness/config.toml"
            if (target / ".harness/config.toml").exists()
            else KIT / "default-config.toml"
        )
    ).resolve()
    config = validate(config_path)
    schema = json.loads((KIT / "verification/schema.json").read_text())
    if args.validate_report:
        report = json.loads(args.validate_report.read_text())
        validate_evidence(report, schema)
        current = fingerprint(target, KIT, config_path)
        if report["inputs"]["digest"] != current["digest"]:
            raise ValueError("stale evidence: input identity changed")
        for item in report["controls"]:
            for artifact in item["artifacts"]:
                path = args.validate_report.parent / artifact["path"]
                if (
                    path.parent != args.validate_report.parent
                    or path.is_symlink()
                    or digest(path.read_bytes()) != artifact["sha256"]
                ):
                    raise ValueError("stale or unsafe evidence artifact")
        print("verify: schema, inputs and retained artifacts valid")
        return 0 if report["complete"] else 1
    if not 0 < args.timeout <= 1800:
        raise ValueError("timeout must be > 0 and <= 1800 seconds")
    # Fixed outputs: never exclude arbitrary user source via an output option.
    output = target / ".harness/reports"
    if any(p.is_symlink() for p in (target / ".harness", output)):
        raise ValueError("report directory must not contain symlinks")
    output.mkdir(parents=True, exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="verify-", dir=output))
    before = fingerprint(target, KIT, config_path)
    selection = resolve(target, config)
    started = time.monotonic()
    env = dict(
        os.environ, PYTHONDONTWRITEBYTECODE="1", HARNESS_CONFIG=str(config_path)
    )
    env.pop("HARNESS_CLI_COMMAND", None)
    if (target / ".venv/bin").is_dir():
        env["PATH"] = str(target / ".venv/bin") + os.pathsep + env["PATH"]
    selected = set(
        args.only
        or [
            "check",
            "tests",
            "smoke",
            *(["self-test"] if args.self_test else []),
        ]
    )
    controls = []
    interrupted = False
    secured = security_enabled(target, config)
    isolation_ok = False
    isolated_env = {}
    if secured:
        item = control(
            "test-isolation", "external macOS sandbox direct-egress preflight"
        )
        controls.append(item)
        isolated_env = synthetic_environment(target, directory)
        try:
            run_control(
                item,
                isolate([sys.executable, str(KIT / "bin/isolation_probe.py")]),
                target,
                directory,
                isolated_env,
                min(args.timeout, 10),
            )
        except ValueError:
            item["reason"] = "external macOS isolation unavailable; no fallback"
        isolation_ok = item["state"] == "passed"
        interrupted |= item["reason"].startswith("interrupted")
        if not args.only and not interrupted:
            controls.extend(
                security_controls(target, config_path, config, directory)
            )
            interrupted |= any(
                c["reason"].startswith("interrupted") for c in controls
            )
        else:
            controls.append(
                control(
                    "security-baseline",
                    "not run after interruption"
                    if interrupted
                    else "required security omitted by partial scope",
                )
            )
    static = control("check", "shared applicable static and policy controls")
    tests = control("tests", "shared application test controls")
    smoke = control("smoke", "required application golden-path smoke")
    if "nextjs" in selection["frameworks"]:
        item = control("nextjs-build", "real native production build")
        controls.append(item)
        if interrupted or (secured and not isolation_ok):
            item["reason"] = (
                "production build not run after isolation/interruption gap"
            )
        elif "check" not in selected:
            item["reason"] = (
                "required production build omitted by partial scope"
            )
        else:
            manager = (
                "pnpm"
                if (target / "pnpm-lock.yaml").exists()
                else "yarn"
                if (target / "yarn.lock").exists()
                else "npm"
            )
            argv = [manager, "run", "build"]
            run_control(
                item,
                isolate(argv) if secured else argv,
                target,
                directory,
                isolated_env if secured else env,
                args.timeout,
            )
            interrupted |= item["reason"].startswith("interrupted")
    test_required = any(
        c["name"].endswith("-tests") for c in selection["controls"]
    ) or bool(
        config["commands"]["test"]
        or os.environ.get("HARNESS_TEST_COMMAND")
        or (target / ".harness/evidence.json").exists()
    )
    for item in (static, tests, smoke):
        controls.append(item)
        if item is tests and not test_required:
            item.update(
                required=False,
                state="not-applicable",
                reason="no application test profile or reviewed test command",
            )
        elif interrupted:
            item["reason"] = "not run after interruption"
        elif secured and not isolation_ok:
            item["reason"] = (
                "required external isolation unavailable; application not executed"
            )
        elif item["name"] not in selected:
            item["reason"] = "required control omitted by partial scope"
        else:
            report_path = directory / "tests.native"
            run_env = dict(env, HARNESS_TEST_REPORT=str(report_path))
            if secured:
                run_env = dict(
                    isolated_env,
                    HARNESS_CONFIG=str(config_path),
                    HARNESS_TEST_REPORT=str(report_path),
                )
            try:
                command, adapter = (
                    test_command(target, config, report_path)
                    if item is tests
                    else (
                        [str(ROOT / "harness"), item["name"], str(target)],
                        None,
                    )
                )
                run_control(
                    item,
                    isolate(command) if secured else command,
                    target,
                    directory,
                    run_env,
                    args.timeout,
                    adapter,
                )
            except (OSError, ValueError, TypeError) as error:
                item.update(state="unavailable", reason=redact(str(error)))
            interrupted |= "interrupted;" in item["reason"]
    if args.self_test or "self-test" in selected:
        item = control("self-test", "explicit harness-change contract suite")
        controls.append(item)
        if (
            not interrupted
            and "self-test" in selected
            and (not secured or isolation_ok)
        ):
            run_control(
                item,
                isolate([str(ROOT / "harness"), "self-test", str(target)])
                if secured
                else [str(ROOT / "harness"), "self-test", str(target)],
                target,
                directory,
                dict(
                    isolated_env if secured else env,
                    HARNESS_CONFIG=str(config_path),
                    HARNESS_TEST_REPORT=str(directory / "self-test.native"),
                ),
                args.timeout,
                "unittest",
            )
            interrupted |= item["reason"].startswith("interrupted")
    for unsupported in selection["controls"]:
        if unsupported["status"] == "unsupported":
            controls.append(control(unsupported["name"], unsupported["reason"]))
    if selection["issues"]:
        controls.append(
            control("applicability", "; ".join(selection["issues"]))
        )
    versions = {} if interrupted else tools(target, directory, env)
    if "interrupted" in versions:
        controls.append(control("version-probe", versions.pop("interrupted")))
    after = fingerprint(target, KIT, config_path)
    stable = before["digest"] == after["digest"]
    if not stable:
        controls.append(
            control("input-stability", "inputs changed during verification")
        )
    partial = bool(args.only)
    report = {
        "schema_version": 1,
        "run_id": str(uuid.uuid4()),
        "inputs": before,
        "end_digest": after["digest"],
        "stable": stable,
        "scope": "partial" if partial else "full",
        "selection": selection,
        "controls": controls,
        "tools": versions,
        "seconds": time.monotonic() - started,
        "complete": stable
        and not partial
        and all(not c["required"] or c["state"] == "passed" for c in controls),
    }
    validate_evidence(report, schema)
    path = directory / "report.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    # Assert writing output (including native/version logs) cannot alter identity.
    if fingerprint(target, KIT, config_path)["digest"] != after["digest"]:
        report.update(stable=False, complete=False)
        report["controls"].append(
            control(
                "input-stability-final", "inputs changed while writing evidence"
            )
        )
        validate_evidence(report, schema)
        path.write_text(json.dumps(report, indent=2) + "\n")
    for item in controls:
        print(f"verify: {item['name']}: {item['state']}: {item['reason']}")
    print(
        f"verify: {'complete' if report['complete'] else 'incomplete'} {report['scope']}; {path}"
    )
    return 0 if report["complete"] else 1


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal.default_int_handler)
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"verify: unavailable: {redact(str(error))}", file=sys.stderr)
        raise SystemExit(1)
