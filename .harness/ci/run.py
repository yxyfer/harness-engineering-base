#!/usr/bin/env python3
"""Bounded native CI phases; no remote services or model-based grading."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".harness/bin"))
# The shared module lives in the managed bin directory, not an installed package.
from source_paths import profile_for, walk_files  # noqa: E402

LOGS = ROOT / os.environ.get("HARNESS_CI_LOGS", ".harness/tmp/ci-logs")
NODE = ROOT / ".harness/tests/fixtures/nextjs-project"
PYTHON = ROOT / ".harness/tests/fixtures/python-project"


def run(name: str, command: list[str], cwd: Path = ROOT, *, negative=False):
    LOGS.mkdir(parents=True, exist_ok=True)
    print(f"{name}: {command!r} (cwd={cwd})", flush=True)
    started = time.monotonic()
    result = subprocess.run(
        command, cwd=cwd, capture_output=True, text=True, timeout=180
    )
    output = result.stdout + result.stderr
    log = LOGS / f"{name}-{time.time_ns()}.log"
    log.write_text(output)
    print(output, end="", flush=True)
    record = {
        "name": name,
        "command": command,
        "cwd": str(cwd),
        "exit": result.returncode,
        "seconds": time.monotonic() - started,
        "expected_failure": negative,
        "output_log": str(log.relative_to(ROOT)),
    }
    with (LOGS / "results.jsonl").open("a") as stream:
        stream.write(json.dumps(record) + "\n")
    if result.returncode < 0 or (result.returncode == 0) == negative:
        raise RuntimeError(f"{name}: unexpected exit {result.returncode}")
    return output


def sources(profile: str) -> list[str]:
    # Runtime directories are pruned before enumeration; fixtures are explicit.
    paths = walk_files(
        ROOT / ".harness",
        [
            "tmp",
            "node_modules",
            "fixtures",
            ".venv",
            "__pycache__",
            ".ruff_cache",
        ],
    )
    return [str(p) for p in paths if profile_for(p) == profile]


def static(*, policy=True):
    for tool in ("shellcheck", "shfmt", "markdownlint-cli2", "pyright"):
        if shutil.which(tool) is None:
            raise RuntimeError(f"required CI tool missing: {tool}")
        run(f"version-{tool}", [tool, "--version"])
    shell = [str(ROOT / "harness"), *sources("shell")]
    run("shellcheck", ["shellcheck", *shell])
    run("shfmt", ["shfmt", "-d", "-i", "2", *shell])
    run("markdown", ["markdownlint-cli2", "**/*.md"])
    python = sources("python")
    config = str(ROOT / ".harness/ci/ruff.toml")
    run(
        "ruff-format",
        [
            sys.executable,
            "-m",
            "ruff",
            "format",
            "--check",
            "--config",
            config,
            *python,
        ],
    )
    run(
        "ruff-lint",
        [sys.executable, "-m", "ruff", "check", "--config", config, *python],
    )
    run("pyright", ["pyright", "--project", "pyrightconfig.json"])
    if policy:
        run("policy", ["./harness", "check"])


def format_source():
    config = str(ROOT / ".harness/ci/ruff.toml")
    run(
        "ruff-format-write",
        [
            sys.executable,
            "-m",
            "ruff",
            "format",
            "--config",
            config,
            *sources("python"),
        ],
    )
    run(
        "shfmt-write",
        ["shfmt", "-w", "-i", "2", str(ROOT / "harness"), *sources("shell")],
    )


def contracts():
    run("harness-test", ["./harness", "test"])
    run("harness-self-test", ["./harness", "self-test"])


def fixtures():
    run("node-check", ["npm", "run", "check"], NODE)
    run(
        "python-format",
        [sys.executable, "-m", "ruff", "format", "--check", "."],
        PYTHON,
    )
    run("python-lint", [sys.executable, "-m", "ruff", "check", "."], PYTHON)
    run("python-types", ["pyright", "--project", "pyproject.toml"], PYTHON)
    for kind, path in (("node", NODE), ("python", PYTHON)):
        for action in ("check", "test", "smoke"):
            run(
                f"{kind}-harness-{action}",
                [str(ROOT / "harness"), action, str(path)],
            )


def negatives():
    # Fingerprint maintained inputs, including project-owned context. Mutations
    # are only in TemporaryDirectory; dependencies are reused, not reinstalled.
    def fingerprint():
        return {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in walk_files(
                ROOT,
                [
                    ".git",
                    ".venv",
                    "node_modules",
                    "tmp",
                    "__pycache__",
                    ".ruff_cache",
                ],
            )
        }

    before = fingerprint()
    with tempfile.TemporaryDirectory(
        prefix="harness-ci-negatives-"
    ) as directory:
        target = Path(directory)
        shell = target / "bad.sh"
        shell.write_text('#!/bin/sh\nprintf "%s\\n" $1\n')
        output = run(
            "negative-shell", ["shellcheck", str(shell)], negative=True
        )
        assert "SC2086" in output
        markdown = target / "bad.md"
        markdown.write_text("# Heading\n### Skipped level\n")
        output = run(
            "negative-markdown",
            ["markdownlint-cli2", str(markdown)],
            negative=True,
        )
        assert "MD001" in output
        python = target / "bad.py"
        python.write_text("print(missing_name)\n")
        output = run(
            "negative-python",
            [sys.executable, "-m", "ruff", "check", str(python)],
            negative=True,
        )
        assert "F821" in output
        typescript = target / "bad.ts"
        typescript.write_text('const value: number = "wrong";\n')
        tsc = NODE / "node_modules/.bin/tsc"
        output = run(
            "negative-typescript",
            [str(tsc), "--noEmit", "--strict", str(typescript)],
            negative=True,
        )
        assert "TS2322" in output
        fixture = target / "python-fixture"
        shutil.copytree(
            PYTHON,
            fixture,
            ignore=shutil.ignore_patterns(
                ".venv", "__pycache__", ".ruff_cache"
            ),
        )
        (fixture / "tests/test_negative.py").write_text(
            "import unittest\n"
            "class Negative(unittest.TestCase):\n"
            "    def test_failure(self):\n"
            "        self.fail('deliberate application failure')\n"
        )
        output = run(
            "negative-test",
            [str(ROOT / "harness"), "test", str(fixture)],
            negative=True,
        )
        assert "deliberate application failure" in output
        (fixture / "src/example_app/message.py").write_text(
            'def page_html() -> bytes:\n    return b"broken content"\n'
        )
        output = run(
            "negative-smoke",
            [str(ROOT / "harness"), "smoke", str(fixture)],
            negative=True,
        )
        assert "golden-path content was not returned" in output
    if fingerprint() != before:
        raise RuntimeError("negative controls changed maintained source")
    print("negative controls: all rejected; maintained source unchanged")


if __name__ == "__main__":
    phases = {
        "static": static,
        "native": lambda: static(policy=False),
        "format": format_source,
        "contracts": contracts,
        "fixtures": fixtures,
        "negatives": negatives,
    }
    if len(sys.argv) != 2 or sys.argv[1] not in phases:
        raise SystemExit("usage: run.py static|contracts|fixtures|negatives")
    phases[sys.argv[1]]()
