"""Relevant context presence/unfinished policy, not prose quality grading."""

from pathlib import Path
from typing import Any
import sys

from config import validate
from profiles import resolve
from source_paths import project_file


def context_status(target: Path, config: dict[str, Any], selection):
    rows = []
    for name in ["AGENTS.md", *selection["documents"]]:
        relative = name if name == "AGENTS.md" else f"docs/{name}"
        try:
            path = project_file(target, relative)
            if not path.is_file() or not path.read_text().strip():
                state = "missing"
            elif "Status: needs-project-input" in path.read_text():
                state = "needs-project-input"
            else:
                state = "present"
            blocking = state == "missing" or (
                state == "needs-project-input"
                and config["readiness"]["fail_on_needs_input"]
            )
            rows.append(
                {"path": relative, "state": state, "blocking": blocking}
            )
        except (OSError, ValueError) as error:
            rows.append(
                {"path": relative, "state": str(error), "blocking": True}
            )
    return rows


if __name__ == "__main__":
    target = Path(sys.argv[1]).resolve()
    config = validate(Path(sys.argv[2]))
    for row in context_status(target, config, resolve(target, config)):
        print(f"    {row['path']}: {row['state']}")
