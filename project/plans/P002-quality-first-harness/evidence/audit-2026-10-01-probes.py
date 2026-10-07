"""Reproduce audit findings using disposable projects and no downloads.

These are diagnostic probes, not passing regression tests for desired behaviour.
Run from any directory; JSON output includes actual commands and exit statuses.
The only source access is read-only. All synthetic projects are temporary.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import venv


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "harness"
CONFIG = (ROOT / ".harness/config.toml").read_text()
RESULTS: dict = {}


def run(arguments: list[str], cwd: Path) -> dict:
    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith("HARNESS_") and key != "CONFIG_PATH"
    }
    result = subprocess.run(
        arguments,
        cwd=cwd,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
        timeout=45,
    )
    return {
        "command": arguments,
        "cwd": str(cwd),
        "exit": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def write(target: Path, name: str, content: str) -> Path:
    path = target / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path


def copy_installation(target: Path) -> None:
    manifest = json.loads((ROOT / ".harness/manifest.json").read_text())
    names = [
        *manifest["managed_files"],
        ".harness/manifest.json",
        ".harness/config.toml",
    ]
    for name in names:
        destination = target / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, destination)


def test_selection(base: Path) -> None:
    target = base / "pytest without dependency"
    target.mkdir()
    venv.EnvBuilder(with_pip=False).create(target / ".venv")
    test_file = write(
        target, "tests/test_failure.py", "def test_failure():\n    assert False\n"
    )
    RESULTS["pytest_fallback"] = {
        "harness": run([str(HARNESS), "test", str(target)], target),
        "direct_assertion": run(
            [
                str(target / ".venv/bin/python"),
                "-c",
                "import runpy; "
                f"runpy.run_path({str(test_file)!r})['test_failure']()",
            ],
            target,
        ),
    }
    write(
        target,
        "tests/test_legacy.py",
        "import unittest\nclass Legacy(unittest.TestCase):\n"
        "    def test_ok(self):\n        self.assertTrue(True)\n",
    )
    RESULTS["mixed_suite_skips_pytest_failure"] = run(
        [str(HARNESS), "test", str(target)], target
    )

    target = base / "adopted Python project"
    target.mkdir()
    copy_installation(target)
    write(
        target,
        "tests/test_app.py",
        "import unittest\nclass Application(unittest.TestCase):\n"
        "    def test_failure(self):\n        self.fail('application broken')\n",
    )
    RESULTS["internal_tests_shadow_project"] = {
        "harness": run([str(target / "harness"), "test"], target),
        "direct_project_tests": run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
            target,
        ),
    }


def standards_and_exclusions(base: Path) -> None:
    standards = runpy.run_path(str(ROOT / ".harness/checks/standards/check"))
    RESULTS["extensionless_profiles"] = {
        str(path.relative_to(ROOT)): {
            "shebang": path.read_text().splitlines()[0],
            "classified_as": standards["profile_for"](path),
        }
        for path in sorted((ROOT / ".harness/checks").glob("*/check"))
    }

    target = base / "nested exclusion"
    write(target, "src/generated/large.py", "value = 1\n" * 400)
    config = write(
        target,
        "config.toml",
        CONFIG.replace('"generated",', '"src/generated",'),
    )
    RESULTS["nested_exclusion"] = run(
        [str(HARNESS), "check", "--config", str(config), str(target)], target
    )

    target = base / "excluded broken markdown"
    write(target, "generated/README.md", "[missing](not-present.md)\n")
    RESULTS["documentation_ignores_exclusion"] = run(
        [str(HARNESS), "check", str(target)], target
    )


def override_and_future_config(base: Path) -> None:
    target = base / "explicit Python check"
    write(target, "pyproject.toml", "[project]\nname = 'probe'\n")
    write(target, "bad.py", "def broken(:\n")
    RESULTS["override_still_runs_auto_python"] = run(
        [str(HARNESS), "check", "--command", "true", str(target)], target
    )

    target = base / "readiness flag"
    target.mkdir()
    shutil.copy2(ROOT / "AGENTS.md", target / "AGENTS.md")
    shutil.copytree(ROOT / "docs", target / "docs")
    config = write(
        target,
        "config.toml",
        CONFIG.replace("fail_on_needs_input = false", "fail_on_needs_input = true")
        .replace('mode = "local"', 'mode = "ci"')
        .replace('"DECISIONS.md",', '"DECISIONS.md",\n  "EXTRA.md",'),
    )
    RESULTS["future_configuration_inert"] = run(
        [str(HARNESS), "check", "--config", str(config), str(target)], target
    )


def project_skills(base: Path) -> None:
    target = base / "custom project skill"
    copy_installation(target)
    tool = ROOT / ".harness/bin/manifest.py"
    baseline = run([sys.executable, str(tool), "verify", str(target)], target)
    fixture_venv = target / ".harness/tests/fixtures/python-project/.venv"
    venv.EnvBuilder(with_pip=False).create(fixture_venv)
    RESULTS["fixture_venv_becomes_managed"] = run(
        [sys.executable, str(tool), "verify", str(target)], target
    )
    shutil.rmtree(fixture_venv)
    write(
        target,
        ".agents/skills/project-specific/SKILL.md",
        "---\nname: project-specific\ndescription: Project workflow.\n---\n",
    )
    RESULTS["project_skill_becomes_managed"] = {
        "before": baseline,
        "after": run(
            [sys.executable, str(tool), "verify", str(target)], target
        ),
    }


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="harness-audit-") as temporary:
        base = Path(temporary)
        test_selection(base)
        standards_and_exclusions(base)
        override_and_future_config(base)
        project_skills(base)
        serialized = json.dumps(RESULTS, indent=2)
        print(
            serialized.replace(str(base.resolve()), "<temporary>")
            .replace(str(base), "<temporary>")
            .replace(str(ROOT), "<repository>")
        )


if __name__ == "__main__":
    main()
