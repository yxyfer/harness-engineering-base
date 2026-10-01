"""Resolve Python runners and guard stdlib discovery against empty suites."""

from __future__ import annotations

from pathlib import Path
import json
import os
import sys
import unittest


def resolve_runner(target: Path) -> str:
    # Only metadata resolution uses Python 3.11; unittest execution may use the
    # application's Python 3.10 interpreter.
    import tomllib

    path = target / "pyproject.toml"
    if not path.is_file():
        return "pytest"
    with path.open("rb") as stream:
        config = tomllib.load(stream)
    tools = config.get("tool", {})
    if not isinstance(tools, dict):
        raise ValueError(f"{path}: tool must be a table")
    harness = tools.get("harness", {})
    if not isinstance(harness, dict):
        raise ValueError(f"{path}: tool.harness must be a table")
    if "tests" not in harness:
        return "pytest"
    settings = harness["tests"]
    if not isinstance(settings, dict) or set(settings) != {"runner"}:
        raise ValueError(f"{path}: tool.harness.tests requires only runner")
    runner = settings["runner"]
    if not isinstance(runner, str) or runner not in {"pytest", "unittest"}:
        raise ValueError(
            f"{path}: tool.harness.tests.runner must be pytest or unittest"
        )
    return runner


def run_unittest(start: Path) -> int:
    suite = unittest.defaultTestLoader.discover(str(start), pattern="test_*.py")
    count = suite.countTestCases()
    print(f"python-tests: collected {count} unittest case(s)", flush=True)
    result = unittest.TextTestRunner().run(suite)
    if report := os.environ.get("HARNESS_TEST_REPORT"):
        Path(report).write_text(
            json.dumps(
                {
                    "collected": count,
                    "executed": result.testsRun,
                    "failures": len(result.failures),
                    "errors": len(result.errors),
                    "skipped": len(result.skipped),
                    "expected_failures": len(result.expectedFailures),
                    "unexpected_successes": len(result.unexpectedSuccesses),
                    "retries": 0,
                }
            )
        )
    if count == 0:
        print("python-tests: zero required tests collected", file=sys.stderr)
        return 5
    return 0 if result.wasSuccessful() else 1


def main(arguments: list[str]) -> int:
    if len(arguments) != 2 or arguments[0] not in {"resolve", "unittest"}:
        print(
            "usage: python-tests.py resolve TARGET | unittest TEST_DIRECTORY",
            file=sys.stderr,
        )
        return 2
    try:
        if arguments[0] == "resolve":
            print(resolve_runner(Path(arguments[1])))
            return 0
        return run_unittest(Path(arguments[1]))
    except (OSError, ValueError, ImportError) as error:
        print(f"python-tests: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
