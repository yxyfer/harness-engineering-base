"""Conservative input identity: no Git tracked-only or analysis-scope shortcut."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import stat

RUNTIME = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".next",
}
OUTPUTS = {".harness/reports", ".harness/tmp"}


def raise_walk_error(error: OSError) -> None:
    raise error


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fingerprint(target: Path, kit: Path, config: Path) -> dict:
    files = {}
    for directory, dirs, names in os.walk(
        target, followlinks=False, onerror=raise_walk_error
    ):
        root = Path(directory)
        relative = root.relative_to(target)
        dirs[:] = sorted(
            name
            for name in dirs
            if name not in RUNTIME
            and (relative / name).as_posix() not in OUTPUTS
            and not (root.name == ".harness" and name in {"reports", "tmp"})
        )
        if any((root / name).is_symlink() for name in dirs):
            raise ValueError(
                "maintained directory symlink prevents complete input identity"
            )
        for name in sorted(
            names + [n for n in dirs if (root / n).is_symlink()]
        ):
            path = root / name
            key = path.relative_to(target).as_posix()
            if path.suffix in {".pyc", ".pyo"} or name == ".DS_Store":
                continue
            if path.is_symlink():
                raise ValueError(
                    "maintained file symlink prevents complete input identity"
                )
            if not path.is_file():
                raise ValueError(
                    "non-regular maintained input prevents complete identity"
                )
            data = path.read_bytes()
            files[key] = digest(data)
            files[f"mode:{key}"] = digest(
                str(stat.S_IMODE(path.stat().st_mode)).encode()
            )
    # Include external executing kit and selected config, not just target source.
    inventory = json.loads((kit / "release-files.json").read_text())
    for name in inventory:
        path = kit.parent / name
        files[f"kit:{name}"] = digest(path.read_bytes())
    files["selected-config"] = digest(config.read_bytes())
    for key in (
        "PATH",
        "HARNESS_CHECK_COMMAND",
        "HARNESS_TEST_COMMAND",
        "HARNESS_SMOKE_COMMAND",
        "HARNESS_CHECKS_DIR",
        "HARNESS_KIT_ROOT",
        "HARNESS_BASE_URL",
        "PYTEST_ADDOPTS",
        "NODE_OPTIONS",
    ):
        files[f"environment:{key}"] = digest(os.environ.get(key, "").encode())
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=target,
        capture_output=True,
        text=True,
        timeout=5,
    )
    return {
        "digest": digest(json.dumps(files, sort_keys=True).encode()),
        "files": files,
        "revision": revision.stdout.strip()
        if revision.returncode == 0
        else "unversioned",
    }
