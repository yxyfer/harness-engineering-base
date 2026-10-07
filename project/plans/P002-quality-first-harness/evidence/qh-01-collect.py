"""Collect Step 01 evidence without changing runtime or installing tools.

Run from the repository root. Records process exits and command-to-completion
feedback time, including failures. This is an audit collector, not a gate.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
NODE_FIXTURE = Path(".harness/tests/fixtures/nextjs-project")
PYTHON_FIXTURE = Path(".harness/tests/fixtures/python-project")
REMOVED_KEYS = sorted(
    key for key in os.environ
    if key.startswith("HARNESS_") or key == "CONFIG_PATH"
)
ENVIRONMENT = {
    key: value for key, value in os.environ.items() if key not in REMOVED_KEYS
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def run(command: list[str], cwd: Path = ROOT) -> dict:
    started_at = timestamp()
    started = time.monotonic()
    try:
        result = subprocess.run(
            command, cwd=cwd, env=ENVIRONMENT, capture_output=True,
            text=True, check=False, timeout=120,
        )
        record = {
            "exit": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr,
            "status": "passed" if result.returncode == 0 else "failed",
        }
    except (OSError, subprocess.TimeoutExpired) as error:
        record = {
            "exit": None, "status": "unavailable",
            "error": str(error),
        }
    record.update({
        "command": command, "cwd": str(cwd), "started_at": started_at,
        "feedback_seconds": round(time.monotonic() - started, 6),
        "feedback_method": "monotonic elapsed command-to-completion",
    })
    print(
        f"{command}: exit={record['exit']} "
        f"elapsed={record['feedback_seconds']}s", flush=True,
    )
    return record


def identity() -> dict:
    def git(*arguments: str) -> bytes:
        return subprocess.check_output(["git", *arguments], cwd=ROOT)

    names = git("ls-files", "-co", "--exclude-standard", "-z")
    files = {}
    for name in sorted(set(names.decode().split("\0")) - {""}):
        path = ROOT / name
        if path.is_file():
            files[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "head": git("rev-parse", "HEAD").decode().strip(),
        "branch": git("branch", "--show-current").decode().strip(),
        "status": git("status", "--short").decode(),
        "diff_sha256": hashlib.sha256(git("diff", "--binary")).hexdigest(),
        "files_sha256": files,
    }


def tools() -> dict:
    records = {
        "python": run([sys.executable, "--version"]),
        "node": run(["node", "--version"]),
        "npm": run(["npm", "--version"]),
    }
    for name in ("shellcheck", "shfmt", "markdownlint-cli2"):
        executable = shutil.which(name, path=ENVIRONMENT.get("PATH"))
        records[name] = (
            run([name, "--version"]) if executable else
            {"status": "unavailable", "exit": None, "reason": "not on PATH"}
        )
    local_python = ROOT / PYTHON_FIXTURE / ".venv/bin/python"
    python = str(local_python) if local_python.exists() else sys.executable
    for name in ("ruff", "pyright", "pytest"):
        record = run([python, "-m", name, "--version"], ROOT / PYTHON_FIXTURE)
        if record["exit"] != 0:
            record["status"] = "unavailable"
        records[name] = record
    for name in ("prettier", "eslint", "typescript", "@types/node"):
        package = ROOT / NODE_FIXTURE / "node_modules" / name / "package.json"
        records[name] = (
            {"version": json.loads(package.read_text())["version"],
             "status": "installed", "evidence": str(package)}
            if package.is_file() else {"status": "unavailable"}
        )
    return records


def matrix(final: bool, smoke_only: bool) -> list[dict]:
    if smoke_only:
        return [
            run(["./harness", "smoke", str(fixture)])
            for fixture in (NODE_FIXTURE, PYTHON_FIXTURE)
        ]
    commands = [["./harness", "check"], ["./harness", "test"]]
    if not final:
        commands.insert(0, ["./harness", "inspect"])
        for fixture in (NODE_FIXTURE, PYTHON_FIXTURE):
            for action in ("check", "test", "smoke"):
                commands.append(["./harness", action, str(fixture)])
        commands.append(["./harness", "smoke"])
    commands.append(["git", "diff", "--check"])
    return [run(command) for command in commands]


def native() -> list[dict]:
    records = [
        run(["npm", "run", "--silent", script], ROOT / NODE_FIXTURE)
        for script in ("format:check", "lint", "typecheck", "test")
    ]
    local_python = ROOT / PYTHON_FIXTURE / ".venv/bin/python"
    python = str(local_python) if local_python.exists() else sys.executable
    records.append(run(
        [python, "-m", "unittest", "discover", "-s", "tests"],
        ROOT / PYTHON_FIXTURE,
    ))
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--initial", type=Path)
    parser.add_argument("--final", action="store_true")
    parser.add_argument("--smoke-only", action="store_true")
    args = parser.parse_args()
    evidence = {
        "started_at": timestamp(), "before": identity(),
        "environment": {
            "os": platform.platform(), "machine": platform.machine(),
            "python": sys.version, "timezone_for_reporting": "Europe/Paris",
            "removed_override_keys": REMOVED_KEYS, "cache_state": "unknown",
            "data": "synthetic; disposable local projects/services",
            "downloads": "none", "mode": "current config; local",
        },
        "commands": matrix(args.final, args.smoke_only),
    }
    if not args.final and not args.smoke_only:
        evidence["tools"] = tools()
        evidence["native"] = native()
        evidence["probes"] = run([
            sys.executable, "verification/audit-2026-10-01-probes.py",
        ])
    if args.initial:
        evidence["initial"] = json.loads(args.initial.read_text())
    evidence["after"] = identity()
    evidence["completed_at"] = timestamp()
    serialized = json.dumps(evidence, indent=2).replace(str(ROOT), "<repository>")
    args.output.write_text(serialized + "\n", encoding="utf-8")
    print(f"Evidence saved: {args.output}")


if __name__ == "__main__":
    main()
