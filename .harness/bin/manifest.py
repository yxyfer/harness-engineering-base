#!/usr/bin/env python3
"""Generate or verify the installed harness managed-file manifest."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any


INSTALLATION_EXIT = 5
MANIFEST_SCHEMA_VERSION = 1
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
HASH = re.compile(r"^sha256:[0-9a-f]{64}$")
MANAGED_ROOTS = ("harness", ".harness", ".agents/skills")
IGNORED_PARTS = {
    "__pycache__",
    ".mypy_cache",
    ".next",
    ".pytest_cache",
    ".ruff_cache",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "tmp",
}
IGNORED_SUFFIXES = {".pyc", ".pyo", ".DS_Store"}
PROJECT_OWNED_PATHS = {
    Path(".harness/config.toml"),
    Path(".harness/exceptions.yml"),
}


class ManifestError(Exception):
    pass


def digest(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def managed_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for name in MANAGED_ROOTS:
        candidate = root / name
        if candidate.is_file():
            paths.append(candidate)
        elif candidate.is_dir():
            for path in candidate.rglob("*"):
                relative = path.relative_to(root)
                if not path.is_file() or any(part in IGNORED_PARTS for part in relative.parts):
                    continue
                if path.name in IGNORED_SUFFIXES or path.suffix in IGNORED_SUFFIXES:
                    continue
                if relative == Path(".harness/manifest.json") or relative in PROJECT_OWNED_PATHS:
                    continue
                paths.append(path)
    return sorted(set(paths), key=lambda path: path.as_posix())


def generate(root: Path, installed_at: str | None = None) -> dict[str, Any]:
    version_path = root / ".harness" / "VERSION"
    if not version_path.is_file():
        raise ManifestError(".harness/VERSION is missing")
    version = version_path.read_text(encoding="utf-8").strip()
    if not SEMVER.fullmatch(version):
        raise ManifestError(f".harness/VERSION is not semantic versioning: {version!r}")
    timestamp = installed_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "harness_version": version,
        "installed_at": timestamp,
        "managed_files": {
            path.relative_to(root).as_posix(): digest(path) for path in managed_paths(root)
        },
    }


def load(root: Path) -> dict[str, Any]:
    path = root / ".harness" / "manifest.json"
    if not path.is_file():
        raise ManifestError(".harness/manifest.json is missing")
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ManifestError(f"manifest JSON is invalid: {error}") from error
    expected = {"schema_version", "harness_version", "installed_at", "managed_files"}
    if type(manifest) is not dict or set(manifest) != expected:
        raise ManifestError(f"manifest keys must be exactly: {', '.join(sorted(expected))}")
    if (
        type(manifest["schema_version"]) is not int
        or manifest["schema_version"] != MANIFEST_SCHEMA_VERSION
    ):
        raise ManifestError(f"unsupported manifest schema: {manifest['schema_version']!r}")
    version = manifest["harness_version"]
    if type(version) is not str or not SEMVER.fullmatch(version):
        raise ManifestError(f"invalid harness_version: {version!r}")
    installed_at = manifest["installed_at"]
    if type(installed_at) is not str or not installed_at.endswith("Z"):
        raise ManifestError("installed_at must be an ISO-8601 UTC timestamp ending in Z")
    files = manifest["managed_files"]
    if type(files) is not dict or not files:
        raise ManifestError("managed_files must be a non-empty object")
    for name, expected_hash in files.items():
        pure_path = PurePosixPath(name) if type(name) is str else None
        valid_hash = type(expected_hash) is str and HASH.fullmatch(expected_hash)
        valid_path = (
            pure_path is not None
            and not pure_path.is_absolute()
            and ".." not in pure_path.parts
        )
        if not valid_path or not valid_hash:
            raise ManifestError(f"invalid managed file entry: {name!r}")
    return manifest


def verify(root: Path) -> int:
    manifest = load(root)
    version = (root / ".harness" / "VERSION").read_text(encoding="utf-8").strip()
    if manifest["harness_version"] != version:
        raise ManifestError(
            "harness version mismatch: manifest "
            f"{manifest['harness_version']!r}, VERSION {version!r}"
        )
    recorded = set(manifest["managed_files"])
    current = {path.relative_to(root).as_posix() for path in managed_paths(root)}
    unrecorded = sorted(current - recorded)
    if unrecorded:
        raise ManifestError(f"unrecorded managed file: {unrecorded[0]}")
    for name, expected in manifest["managed_files"].items():
        path = root / name
        if not path.is_file():
            raise ManifestError(f"managed file missing: {name}")
        if digest(path) != expected:
            raise ManifestError(f"checksum mismatch: {name}")
    count = len(manifest["managed_files"])
    print(f"manifest: valid (schema {MANIFEST_SCHEMA_VERSION}, {count} managed files)")
    return 0


def usage() -> None:
    print(
        "usage: manifest.py verify ROOT | generate ROOT [INSTALLED_AT]",
        file=sys.stderr,
    )


def main(arguments: list[str]) -> int:
    if len(arguments) < 2:
        usage()
        return 2
    command = arguments[0]
    root = Path(arguments[1]).expanduser().resolve()
    try:
        if command == "verify" and len(arguments) == 2:
            return verify(root)
        if command == "generate" and len(arguments) in {2, 3}:
            installed_at = arguments[2] if len(arguments) == 3 else None
            print(json.dumps(generate(root, installed_at), indent=2, sort_keys=True))
            return 0
        usage()
        return 2
    except (ManifestError, OSError) as error:
        print(f"manifest: {root}: {error}", file=sys.stderr)
        return INSTALLATION_EXIT


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
