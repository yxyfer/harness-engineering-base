"""Capture Step 04 command results and the exact local source identity."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]


def identity():
    inventory = json.loads((ROOT / ".harness/release-files.json").read_text())
    names = inventory + [
        ".harness/manifest.json", ".harness/config.toml", "AGENTS.md",
        "README.md", "docs/ARCHITECTURE.md", "docs/QUALITY.md",
        "docs/DECISIONS.md",
    ]
    return {
        "head": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "sha256": {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in names
        },
    }


def run(item):
    command, relative = item
    started = time.monotonic()
    environment = {
        key: value for key, value in os.environ.items()
        if not key.startswith("HARNESS_") and key != "CONFIG_PATH"
    }
    try:
        result = subprocess.run(
            command, cwd=ROOT / relative, env=environment,
            capture_output=True, text=True, timeout=180, check=False,
        )
        record = {
            "command": command, "cwd": relative,
            "exit": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr,
        }
    except FileNotFoundError as error:
        record = {
            "command": command, "cwd": relative, "exit": None,
            "status": "unavailable", "error": str(error),
        }
    record["feedback_seconds"] = round(time.monotonic() - started, 6)
    return record


def main():
    mode = sys.argv[1]
    node = ".harness/tests/fixtures/nextjs-project"
    python = ".harness/tests/fixtures/python-project"
    if mode == "matrix":
        items = [(["./harness", action], ".") for action in
                 ("check", "test", "self-test", "smoke", "inspect")]
        items += [(["./harness", action, fixture], ".")
                  for fixture in (node, python)
                  for action in ("check", "test", "smoke", "inspect")]
        items += [(["python3", ".harness/bin/manifest.py", "verify", "."], "."),
                  (["git", "diff", "--check"], ".")]
    elif mode == "smoke-retry":
        items = [(["./harness", "smoke", fixture], ".")
                 for fixture in (node, python)]
    elif mode == "native":
        items = [(["npm", "run", "--silent", action], node)
                 for action in ("format:check", "lint", "typecheck", "test")]
        items += [(["python3", "-m", "unittest", "discover", "-s", "tests"], python)]
        items += [([str(ROOT / ".venv/bin/python"), "-m", tool, "--version"], ".")
                  for tool in ("pytest", "ruff", "pyright")]
        items += [([tool, "--version"], ".")
                  for tool in ("shellcheck", "shfmt", "markdownlint-cli2")]
    elif mode == "final":
        items = [(["./harness", action], ".")
                 for action in ("check", "inspect")]
        items += [(["python3", ".harness/bin/manifest.py", "verify", "."], "."),
                  (["git", "diff", "--check"], ".")]
    else:
        raise SystemExit("use matrix, native, smoke-retry or final")
    before = identity()
    with ThreadPoolExecutor(max_workers=3) as executor:
        records = list(executor.map(run, items))
    result = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "source": before, "source_unchanged": before == identity(),
        "commands": records,
    }
    content = json.dumps(result, indent=2).replace(str(ROOT), "<repository>")
    print(content)


if __name__ == "__main__":
    main()
