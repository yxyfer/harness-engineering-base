"""Prerequisite diagnosis: never install, execute gates or rewrite files."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any

from config import ConfigError, validate
from profiles import print_selection, resolve
from readiness import context_status


def module_available(python: str, name: str) -> bool:
    result = subprocess.run(
        [
            python,
            "-c",
            "import importlib.util,sys; "
            "sys.exit(0 if importlib.util.find_spec(sys.argv[1]) else 1)",
            name,
        ],
        capture_output=True,
        timeout=10,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    return result.returncode == 0


def prerequisites(target: Path, config: dict[str, Any], selection):
    rows = []

    def record(name, available, reason):
        rows.append(
            {"name": name, "available": bool(available), "reason": reason}
        )

    profiles = selection["profiles"]
    if "python" in profiles:
        environment = target / ".venv"
        python = (
            str(environment / "bin/python")
            if environment.exists() or environment.is_symlink()
            else (shutil.which("python3") or sys.executable)
        )
        valid_python = Path(python).is_file() and os.access(python, os.X_OK)
        record(
            "python",
            valid_python,
            "target .venv preferred; no environment substitution",
        )
        record(
            "ruff",
            valid_python and module_available(python, "ruff"),
            "python-static formatter/linter in selected interpreter",
        )
        record(
            "pyright",
            shutil.which("pyright")
            or (valid_python and module_available(python, "pyright")),
            "python-static type checker; CLI or selected interpreter module",
        )
        if config["commands"]["test"]:
            record(
                "python-tests",
                True,
                "reviewed native test command; not executed",
            )
        else:
            tool = Path(__file__).with_name("python-tests.py")
            runner = subprocess.run(
                [sys.executable, str(tool), "resolve", str(target)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            name = runner.stdout.strip()
            record(
                "python-tests",
                runner.returncode == 0
                and valid_python
                and (name == "unittest" or module_available(python, "pytest")),
                "declared/conventional test runner in selected interpreter",
            )
    if "typescript" in profiles:
        runner = (
            "pnpm"
            if (target / "pnpm-lock.yaml").is_file()
            else ("yarn" if (target / "yarn.lock").is_file() else "npm")
        )
        for tool in ("node", runner):
            record(
                tool,
                shutil.which(tool),
                "typescript native runtime/package runner",
            )
        for tool in ("prettier", "eslint", "tsc"):
            path = target / "node_modules/.bin" / tool
            record(
                tool,
                path.is_file() and os.access(path, os.X_OK),
                "typescript-static project-local tool; presence is not execution",
            )
        from source_paths import project_file

        package = project_file(target, "package.json")
        scripts = (
            json.loads(package.read_text()).get("scripts", {})
            if package.is_file()
            else {}
        )
        if type(scripts) is not dict:
            raise ValueError("package.json scripts must be an object")
        record(
            "typescript-tests",
            config["commands"]["test"] or scripts.get("test"),
            "reviewed command or project test script; collection not verified",
        )
    if "nextjs" in selection["frameworks"]:
        tool = target / "node_modules/.bin/next"
        record(
            "next",
            tool.is_file() and os.access(tool, os.X_OK),
            "Next.js native prerequisite; framework verification still unsupported",
        )
    for profile, tools in {
        "shell": ("shellcheck", "shfmt"),
        "markdown": ("markdownlint-cli2",),
    }.items():
        if profile in profiles:
            for tool in tools:
                record(
                    tool, shutil.which(tool), f"{profile}-static native tool"
                )
    return rows


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: doctor.py TARGET CONFIG", file=sys.stderr)
        return 2
    try:
        target = Path(sys.argv[1]).resolve()
        config = validate(Path(sys.argv[2]))
        selection = resolve(target, config)
        print_selection(selection)
        blocked = bool(selection["issues"])
        for row in context_status(target, config, selection):
            print(f"doctor: context {row['path']}: {row['state']}")
            blocked |= row["blocking"]
        for row in prerequisites(target, config, selection):
            state = "available" if row["available"] else "missing"
            print(
                f"doctor: prerequisite {row['name']}: {state}; {row['reason']}"
            )
            blocked |= not row["available"]
        print(
            "doctor: blocked; resolve the reported gaps, then rerun"
            if blocked
            else "doctor: ready to run applicable checks; no checks executed"
        )
        return 1 if blocked else 0
    except ConfigError as error:
        print(f"config: {error}", file=sys.stderr)
        return 4
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(f"doctor: unavailable: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
