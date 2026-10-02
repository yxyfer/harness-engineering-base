"""Authoring CI security gate and external isolation for existing test phases."""

import json
from pathlib import Path
import sys
import tempfile

KIT = Path(__file__).resolve().parents[1]
ROOT = KIT.parent
sys.path.insert(0, str(KIT / "bin"))
from config import validate  # noqa: E402
from evidence_runner import execute  # noqa: E402
from isolation import command, environment  # noqa: E402
from security import run  # noqa: E402


def main(phase: str) -> int:
    output = KIT / "reports"
    output.mkdir(exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="security-ci-", dir=output))
    if phase == "security":
        config_path = KIT / "config.toml"
        rows = run(ROOT, config_path, validate(config_path), directory)
        (directory / "controls.json").write_text(
            json.dumps(rows, indent=2) + "\n"
        )
        for row in rows:
            print(f"{row['name']}: {row['state']}: {row['reason']}")
        return int(any(r["required"] and r["state"] != "passed" for r in rows))
    if phase not in {"static", "contracts", "fixtures", "negatives"}:
        raise ValueError("unknown fixed CI phase")
    env = environment(ROOT, directory)
    preflight = execute(
        command([sys.executable, str(KIT / "bin/isolation_probe.py")]),
        ROOT,
        directory / "isolation.log",
        env,
        10,
    )
    if preflight["exit"]:
        print("CI isolation unavailable; test phase not executed")
        return 1
    python = ROOT / ".venv/bin/python"
    if not python.is_file():
        raise ValueError("required authoring CI environment missing")
    outcome = execute(
        command([str(python), str(KIT / "ci/run.py"), phase]),
        ROOT,
        directory / "phase.log",
        env,
        600,
    )
    print((directory / "phase.log").read_text())
    print(f"CI phase {phase}: {outcome['reason']}; logs {directory}")
    return int(
        outcome["exit"] != 0 or outcome["reason"] != "native command completed"
    )


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1]))
    except (OSError, ValueError, IndexError):
        print("CI security/isolation unavailable; no fallback", file=sys.stderr)
        raise SystemExit(1)
