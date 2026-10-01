#!/usr/bin/env python3
"""Generate or verify the installed harness managed-file manifest."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
from typing import Any


INSTALLATION_EXIT = 5
MANIFEST_SCHEMA_VERSION = 1
INVENTORY = ".harness/release-files.json"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
HASH = re.compile(r"^sha256:[0-9a-f]{64}$")
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
    Path(".harness/manifest.json"),
}


class ManifestError(Exception):
    pass


def digest(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def valid_release_path(name: Any) -> bool:
    if type(name) is not str or not name:
        return False
    if (
        "\\" in name
        or ":" in name
        or any(ord(c) < 32 or ord(c) == 127 for c in name)
    ):
        return False
    path = PurePosixPath(name)
    if path.is_absolute() or path.as_posix() != name:
        return False
    if any(part in {".", "..", ""} for part in name.split("/")):
        return False
    local_parts = IGNORED_PARTS | {".venv", "venv", ".git", ".env"}
    if set(path.parts) & local_parts or Path(name) in PROJECT_OWNED_PATHS:
        return False
    if path.suffix in IGNORED_SUFFIXES | {".env", ".pem"}:
        return False
    return name == "harness" or name.startswith(
        (".harness/", ".agents/skills/")
    )


def shipped_file(root: Path, name: str) -> Path:
    """Check links and regular-file type before opening a release input."""
    path = root
    for part in PurePosixPath(name).parts:
        path = path / part
        try:
            mode = path.lstat().st_mode
        except FileNotFoundError as error:
            raise ManifestError(f"managed file missing: {name}") from error
        if stat.S_ISLNK(mode):
            raise ManifestError(f"symlink in shipped destination: {name}")
        if path != root / name and not stat.S_ISDIR(mode):
            raise ManifestError(f"non-directory shipped parent: {name}")
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ManifestError(f"managed file is not regular: {name}")
    return path


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ManifestError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def read_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=unique_object
        )
    except json.JSONDecodeError as error:
        raise ManifestError(f"invalid JSON in {path.name}: {error}") from error


def release_inventory(root: Path) -> list[str]:
    try:
        path = shipped_file(root, INVENTORY)
    except ManifestError as error:
        raise ManifestError(
            f"release inventory missing or unsafe: {error}"
        ) from error
    names = read_json(path)
    if type(names) is not list or not names:
        raise ManifestError("release inventory must be a non-empty path list")
    if any(not valid_release_path(name) for name in names):
        raise ManifestError("release inventory contains an invalid path")
    if len(set(names)) != len(names):
        raise ManifestError("release inventory contains duplicate paths")
    if len({name.casefold() for name in names}) != len(names):
        raise ManifestError("release inventory contains case-colliding paths")
    if not {"harness", ".harness/VERSION", INVENTORY}.issubset(names):
        raise ManifestError("release inventory lacks mandatory shipped inputs")
    return sorted(names)


def managed_paths(root: Path) -> list[Path]:
    # Ownership comes only from the reviewed inventory, never tree discovery.
    return [shipped_file(root, name) for name in release_inventory(root)]


def valid_timestamp(value: Any) -> bool:
    if type(value) is not str or not value.endswith("Z") or "T" not in value:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def generate(root: Path, installed_at: str | None = None) -> dict[str, Any]:
    paths = managed_paths(root)
    version_path = shipped_file(root, ".harness/VERSION")
    version = version_path.read_text(encoding="utf-8").strip()
    if not SEMVER.fullmatch(version):
        raise ManifestError(
            f".harness/VERSION is not semantic versioning: {version!r}"
        )
    timestamp = installed_at or datetime.now(timezone.utc).isoformat().replace(
        "+00:00", "Z"
    )
    if not valid_timestamp(timestamp):
        raise ManifestError("installed_at must be an ISO-8601 UTC timestamp")
    return {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "harness_version": version,
        "installed_at": timestamp,
        "managed_files": {
            path.relative_to(root).as_posix(): digest(path) for path in paths
        },
    }


def load(root: Path) -> dict[str, Any]:
    manifest = read_json(shipped_file(root, ".harness/manifest.json"))
    expected = {
        "schema_version",
        "harness_version",
        "installed_at",
        "managed_files",
    }
    if type(manifest) is not dict or set(manifest) != expected:
        raise ManifestError(
            f"manifest keys must be exactly: {', '.join(sorted(expected))}"
        )
    if (
        type(manifest["schema_version"]) is not int
        or manifest["schema_version"] != MANIFEST_SCHEMA_VERSION
    ):
        raise ManifestError(
            f"unsupported manifest schema: {manifest['schema_version']!r}"
        )
    version = manifest["harness_version"]
    if type(version) is not str or not SEMVER.fullmatch(version):
        raise ManifestError(f"invalid harness_version: {version!r}")
    installed_at = manifest["installed_at"]
    if not valid_timestamp(installed_at):
        raise ManifestError(
            "installed_at must be an ISO-8601 UTC timestamp ending in Z"
        )
    files = manifest["managed_files"]
    if type(files) is not dict or not files:
        raise ManifestError("managed_files must be a non-empty object")
    for name, expected_hash in files.items():
        valid_hash = type(expected_hash) is str and HASH.fullmatch(
            expected_hash
        )
        valid_path = valid_release_path(name)
        if not valid_path or not valid_hash:
            raise ManifestError(f"invalid managed file entry: {name!r}")
    return manifest


def verify(root: Path) -> int:
    manifest = load(root)
    names = release_inventory(root)
    if set(manifest["managed_files"]) != set(names):
        raise ManifestError("manifest/release inventory mismatch")
    paths = {name: shipped_file(root, name) for name in names}
    version = (
        shipped_file(root, ".harness/VERSION")
        .read_text(encoding="utf-8")
        .strip()
    )
    if manifest["harness_version"] != version:
        raise ManifestError(
            "harness version mismatch: manifest "
            f"{manifest['harness_version']!r}, VERSION {version!r}"
        )
    for name, expected in manifest["managed_files"].items():
        path = paths[name]
        if digest(path) != expected:
            raise ManifestError(f"checksum mismatch: {name}")
    count = len(manifest["managed_files"])
    print(
        f"manifest: valid (schema {MANIFEST_SCHEMA_VERSION}, {count} managed files)"
    )
    return 0


def usage() -> None:
    print(
        "usage: manifest.py verify ROOT | generate-release ROOT [INSTALLED_AT]",
        file=sys.stderr,
    )


def main(arguments: list[str]) -> int:
    if len(arguments) < 2:
        usage()
        return 2
    command = arguments[0]
    root = Path(arguments[1]).expanduser().absolute()
    try:
        if root.is_symlink():
            raise ManifestError("symlink installation root")
        if command == "verify" and len(arguments) == 2:
            return verify(root)
        if command == "generate-release" and len(arguments) in {2, 3}:
            installed_at = arguments[2] if len(arguments) == 3 else None
            print(
                json.dumps(
                    generate(root, installed_at), indent=2, sort_keys=True
                )
            )
            return 0
        usage()
        return 2
    except (ManifestError, OSError, UnicodeError) as error:
        print(f"manifest: {root}: {error}", file=sys.stderr)
        return INSTALLATION_EXIT


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
