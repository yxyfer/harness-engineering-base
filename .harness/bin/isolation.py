"""External macOS Seatbelt launch; unavailable isolation never falls back."""

from __future__ import annotations

import os
from pathlib import Path
import sys

KIT = Path(__file__).resolve().parents[1]


def environment(target: Path, directory: Path) -> dict[str, str]:
    home = directory / "synthetic-home"
    home.mkdir(exist_ok=True)
    # Fixed allowlist: do not forward credentials, provider URLs, NODE_OPTIONS,
    # Python startup hooks, user package-manager auth or arbitrary HARNESS_*.
    return {
        "PATH": os.pathsep.join(
            [
                str(target / ".venv/bin"),
                os.environ.get("PATH", "/usr/bin:/bin"),
            ]
        ),
        "HOME": str(home),
        "TMPDIR": str(directory),
        "LANG": "en_US.UTF-8",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONNOUSERSITE": "1",
        "PIP_NO_INDEX": "1",
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "NPM_CONFIG_USERCONFIG": "/dev/null",
        "NPM_CONFIG_OFFLINE": "true",
        "HARNESS_ENVIRONMENT": "synthetic",
        "HARNESS_SYNTHETIC_TOKEN": "not-a-live-credential",
    }


def command(argv: list[str]) -> list[str]:
    executable = Path("/usr/bin/sandbox-exec")
    if sys.platform != "darwin" or not executable.is_file():
        raise ValueError(
            "external macOS isolation unavailable; no unsandboxed fallback"
        )
    return [str(executable), "-f", str(KIT / "security/loopback.sb"), *argv]
