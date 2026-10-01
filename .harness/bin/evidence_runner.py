"""Bounded streaming logs and best-effort POSIX owned process-group cleanup."""

from __future__ import annotations

import os
from pathlib import Path
import re
import selectors
import signal
import shutil
import subprocess
import time

LOG_LIMIT = 65536


def tools(target: Path, directory: Path, env: dict) -> dict:
    versions = {
        "harness": (Path(__file__).resolve().parents[1] / "VERSION")
        .read_text()
        .strip()
    }
    for name in (
        "python3",
        "node",
        "npm",
        "shellcheck",
        "shfmt",
        "markdownlint-cli2",
    ):
        executable = shutil.which(name, path=env["PATH"])
        if executable:
            path = directory / f"version-{name}.log"
            run = execute([executable, "--version"], target, path, env, 5)
            if run["reason"].startswith("interrupted"):
                versions["interrupted"] = "version probe interrupted"
                return versions
            versions[name] = (
                path.read_text().strip()[:256]
                if run["exit"] == 0
                else "unavailable"
            )
    python = target / ".venv/bin/python"
    if python.exists():
        for module in ("ruff", "pyright", "pytest"):
            path = directory / f"version-{module}.log"
            outcome = execute(
                [
                    str(python),
                    "-c",
                    f"import importlib.metadata;print(importlib.metadata.version({module!r}))",
                ],
                target,
                path,
                env,
                5,
            )
            if outcome["reason"].startswith("interrupted"):
                versions["interrupted"] = "version probe interrupted"
                return versions
            versions[module] = (
                path.read_text().strip()[:256]
                if outcome["exit"] == 0
                else "unavailable"
            )
    for module in ("prettier", "eslint", "tsc"):
        executable = target / "node_modules/.bin" / module
        if executable.exists():
            path = directory / f"version-{module}.log"
            outcome = execute(
                [str(executable), "--version"], target, path, env, 5
            )
            if outcome["reason"].startswith("interrupted"):
                versions["interrupted"] = "version probe interrupted"
                return versions
            versions[module] = (
                path.read_text().strip()[:256]
                if outcome["exit"] == 0
                else "unavailable"
            )
    return versions


def redact(text: str) -> str:
    for key, value in os.environ.items():
        if (
            re.search(r"SECRET|TOKEN|PASSWORD|API_KEY|CREDENTIAL", key, re.I)
            and value
        ):
            text = text.replace(value, "[REDACTED]")
    return re.sub(
        r"(?i)(authorization\s*[:=]\s*(?:bearer\s+)?|(?:password|token|secret|api[_-]?key)\s*[:=]\s*)(?:\"[^\"]*\"|'[^']*'|[^\s\"']+)",
        r"\1[REDACTED]",
        text,
    )


def kill_group(process: subprocess.Popen) -> None:
    for sig in (signal.SIGTERM, signal.SIGKILL):
        # Reap the leader before signalling the remaining group. macOS can
        # reject SIGKILL against a group containing only an unreaped zombie.
        process.poll()
        try:
            os.killpg(process.pid, sig)
        except ProcessLookupError:
            pass
        except PermissionError as error:
            raise PermissionError(
                f"owned group {process.pid}: signal {sig.name} denied; parent exit={process.poll()}"
            ) from error
        if sig == signal.SIGTERM:
            time.sleep(0.1)
    process.wait(timeout=5)


def execute(
    command: list[str], target: Path, log: Path, env: dict, timeout: float
) -> dict:
    started = time.monotonic()
    process = subprocess.Popen(
        command,
        cwd=target,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    captured = bytearray()
    truncated = False
    reason = "native command completed"
    assert process.stdout is not None
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    try:
        while selector.get_map():
            if time.monotonic() - started >= timeout:
                reason = "timeout; owned process group terminated"
                break
            for key, _ in selector.select(0.05):
                chunk = os.read(key.fd, 8192)
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                room = LOG_LIMIT - len(captured)
                captured.extend(chunk[: max(0, room)])
                truncated |= len(chunk) > room
        if reason.startswith("timeout"):
            kill_group(process)
        else:
            process.wait(
                timeout=max(0.1, timeout - (time.monotonic() - started))
            )
    except KeyboardInterrupt:
        reason = "interrupted; owned process group terminated"
        kill_group(process)
    except subprocess.TimeoutExpired:
        reason = "timeout; owned process group terminated"
        kill_group(process)
    finally:
        # Also reap ordinary commands' descendants; no background services belong
        # to a completed verification control. Escaped sessions remain a limit.
        kill_group(process)
        selector.close()
        process.stdout.close()
    output = redact(captured.decode(errors="replace"))
    encoded = output.encode()
    truncated |= len(encoded) > LOG_LIMIT
    if truncated:
        trailer = b"\n[log truncated]\n"
        output = (
            encoded[: LOG_LIMIT - len(trailer)]
            .decode(errors="ignore")
            .rsplit("\n", 1)[0]
            + trailer.decode()
        )
    log.write_text(output)
    if reason == "native command completed" and process.returncode != 0:
        reason = f"native command exited {process.returncode}"
    return {
        "command": [redact(item) for item in command],
        "exit": process.returncode,
        "seconds": time.monotonic() - started,
        "reason": reason,
        "truncated": truncated,
    }
