"""Fixed native defaults; project commands and native config stay authoritative."""

from pathlib import Path
import os
import shutil
import subprocess
import sys

from config import ConfigError, validate
from profiles import resolve
from source_paths import profile_for, walk_files


def run(command: list[str], target: Path) -> None:
    print(f"static: running {command!r}", flush=True)
    result = subprocess.run(command, cwd=target, check=False)
    if result.returncode:
        raise ValueError(f"native tool failed with exit {result.returncode}")


def python_tool(target: Path, name: str) -> list[str]:
    python = target / ".venv/bin/python"
    if not python.is_file() or not os.access(python, os.X_OK):
        raise ValueError(
            "project-local .venv/bin/python is required; run reviewed setup"
        )
    if name == "pyright":
        # The Python wrapper can query updates/install Node. Locate its bundled
        # native entrypoint instead; checks never bootstrap runtimes/packages.
        probe = subprocess.run(
            [
                str(python),
                "-c",
                "import importlib.util,pathlib; s=importlib.util.find_spec('pyright'); print(pathlib.Path(s.origin).parent/'dist/index.js' if s and s.origin else '')",
            ],
            cwd=target,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        entrypoint = probe.stdout.strip()
        node = shutil.which("node")
        if probe.returncode or not entrypoint or not Path(entrypoint).is_file():
            raise ValueError("required project-local bundled pyright missing")
        if not node:
            raise ValueError(
                "Node runtime required by Pyright; run reviewed setup"
            )
        return [node, entrypoint]
    probe = subprocess.run(
        [str(python), "-m", name, "--version"],
        cwd=target,
        capture_output=True,
        timeout=15,
        check=False,
    )
    if probe.returncode:
        raise ValueError(f"required {name} missing from project-local .venv")
    return [str(python), "-m", name]


def node_tool(target: Path, name: str) -> list[str]:
    path = target / "node_modules/.bin" / name
    if not path.is_file() or not os.access(path, os.X_OK):
        raise ValueError(
            f"required project-local {name} missing; run locked setup"
        )
    return [str(path)]


def execute(action: str, target: Path, config: dict) -> None:
    selection = resolve(target, config)
    if selection["issues"]:
        raise ValueError("; ".join(selection["issues"]))
    ran = False
    if "python" in selection["profiles"]:
        ruff = python_tool(target, "ruff")
        # Native discovery alone omits extensionless Python; include maintained
        # shebang files explicitly while Ruff retains its configured exclusions.
        scripts = [
            str(p.relative_to(target))
            for p in walk_files(
                target, [*config["analysis"]["exclude"], ".harness", ".agents"]
            )
            if profile_for(p) == "python" and p.suffix != ".py"
        ]
        if action == "format":
            run([*ruff, "format", ".", "--force-exclude", *scripts], target)
        else:
            run(
                [*ruff, "format", "--check", ".", "--force-exclude", *scripts],
                target,
            )
            run([*ruff, "check", ".", "--force-exclude", *scripts], target)
            run([*python_tool(target, "pyright"), "--project", "."], target)
        ran = True
    if "typescript" in selection["profiles"]:
        prettier = node_tool(target, "prettier")
        run(
            [*prettier, "--write" if action == "format" else "--check", "."],
            target,
        )
        if action == "check":
            run([*node_tool(target, "eslint"), "."], target)
            run([*node_tool(target, "tsc"), "--noEmit"], target)
        ran = True
    if action == "format" and not ran:
        raise ValueError(
            "no native formatter selected; declare commands.format"
        )
    if action == "check" and not ran:
        # Shell/Markdown are checked by the standards policy, not twice here.
        if not set(selection["profiles"]) & {"shell", "markdown"}:
            raise ValueError("no static scope selected; declare commands.check")


def main() -> int:
    try:
        action, target_name, config_name = sys.argv[1:]
        if action not in {"check", "format"}:
            raise ValueError("action must be check or format")
        execute(
            action, Path(target_name).resolve(), validate(Path(config_name))
        )
        return 0
    except ConfigError as error:
        print(f"config: {error}", file=sys.stderr)
        return 4
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(f"static: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
