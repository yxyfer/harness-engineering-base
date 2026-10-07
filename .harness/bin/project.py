#!/usr/bin/env python3
"""Public structured-project command; no dependency or network setup."""

from pathlib import Path
import sys

from project_records import WorkError
from project_work import archive_plan, check_indexes, sync_indexes


def main(arguments: list[str]) -> int:
    if not arguments or arguments[0] not in {"check", "sync", "archive"}:
        print("usage: ./harness project check|sync [target]", file=sys.stderr)
        print("       ./harness project archive PNNN [target]", file=sys.stderr)
        return 2
    action = arguments[0]
    minimum = 2 if action == "archive" else 1
    if len(arguments) not in {minimum, minimum + 1} or any(
        value.startswith("-") for value in arguments[1:]
    ):
        return 2
    root = Path(
        arguments[minimum] if len(arguments) > minimum else "."
    ).resolve()
    try:
        if action == "archive":
            archive_plan(root, arguments[1])
        elif action == "sync":
            sync_indexes(root)
        else:
            check_indexes(root)
    except (WorkError, OSError) as error:
        print(f"project: {error}", file=sys.stderr)
        return 1
    if action == "check" and not (root / "project/FORMAT.md").is_file():
        print("project: not-applicable (format not adopted)")
    else:
        print(f"project: {action} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
