"""Literal directory exclusions and language discovery for harness scans.

Native tools keep their own scope. Symlinks are never scanned or descended.
"""

from __future__ import annotations

import ast
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import sys
import tomllib


SOURCE_SUFFIXES = {
    "python": {".py"},
    "typescript": {".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx"},
    "shell": {".sh"},
    "markdown": {".md", ".mdx"},
}


def load_config(target: Path) -> dict:
    configured = os.environ.get("CONFIG_PATH")
    project = target / ".harness/config.toml"
    path = (Path(configured) if configured else project if project.is_file()
            else Path(__file__).parent.parent / "default-config.toml")
    with path.open("rb") as stream:
        return tomllib.load(stream)


def excluded_directory(relative: Path, excluded: list[str]) -> bool:
    for rule in excluded:
        parts = PurePosixPath(rule).parts
        if "/" not in rule.rstrip("/") and parts:
            if parts[0] in relative.parts:
                return True
        elif relative.parts[:len(parts)] == parts:
            return True
    return False


def walk_files(target: Path, excluded: list[str]):
    """Yield regular files, pruning excluded directories before opening them."""
    target = target.resolve()

    def descend(directory: Path):
        with os.scandir(directory) as entries:
            ordered = sorted(entries, key=lambda entry: entry.name)
        for entry in ordered:
            path = Path(entry.path)
            if entry.is_symlink():
                continue
            if entry.is_dir(follow_symlinks=False):
                if not excluded_directory(path.relative_to(target), excluded):
                    yield from descend(path)
            elif entry.is_file(follow_symlinks=False):
                yield path

    if not excluded_directory(Path("."), excluded):
        yield from descend(target)


def project_file(target: Path, relative: str) -> Path:
    """Canonical policy inputs cannot be supplied through symlink components."""
    path = target
    for part in PurePosixPath(relative).parts:
        path = path / part
        if path.is_symlink():
            raise ValueError(f"canonical context cannot be a symlink: {relative}")
    return path


def profile_for(path: Path) -> str | None:
    if path.is_symlink():
        return None
    for profile, suffixes in SOURCE_SUFFIXES.items():
        if path.suffix in suffixes:
            return profile
    if path.suffix or not path.stat().st_mode & 0o111:
        return None
    with path.open("rb") as stream:
        first_line = stream.readline(512)
    if not first_line.startswith(b"#!"):
        return None
    try:
        words = shlex.split(first_line[2:].decode("utf-8").strip())
    except (UnicodeDecodeError, ValueError):
        return None
    if not words:
        return None
    interpreter = Path(words[0]).name
    if interpreter == "env":
        words = words[1:]
        if words[:1] == ["-S"]:
            words = words[1:]
        if not words:
            return None
        interpreter = words[0]
    if re.fullmatch(r"python(?:3(?:\.\d+)?)?", interpreter):
        return "python"
    if interpreter in {"sh", "bash", "dash"}:
        return "shell"
    return None


def check_python_syntax(target: Path) -> int:
    count = 0
    for path in walk_files(target, load_config(target)["analysis"]["exclude"]):
        if profile_for(path) != "python":
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, UnicodeDecodeError) as error:
            print(f"python syntax: {path.relative_to(target)}: {error}",
                  file=sys.stderr)
            return 1
        count += 1
    print(f"python syntax: pass ({count} maintained Python files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(check_python_syntax(Path(sys.argv[1]).resolve()))
