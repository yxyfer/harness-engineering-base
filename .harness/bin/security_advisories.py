"""Explicit advisory setup and lock-bound offline report consumption."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import re
import sys

from evidence_identity import digest
from evidence_runner import execute
from isolation import environment
from security_reports import dependencies, policy, read_json
from source_paths import project_file

KIT = Path(__file__).resolve().parents[1]
VERSIONS = {"python": "pip-audit 2.10.1", "npm": "11.6.0"}
SOURCES = {
    "python": "https://pypi.org/pypi/{package}/{version}/json",
    "npm": "https://registry.npmjs.org/-/npm/v1/security/advisories/bulk",
}
MAX_AGE = 24 * 3600


def lock_id(target: Path, lock: dict) -> str:
    data = project_file(target, lock["path"]).read_bytes()
    if lock["ecosystem"] == "npm":
        native = json.loads(data)
        if (
            native.get("lockfileVersion") != 3
            or type(native.get("packages")) is not dict
        ):
            raise ValueError("only npm v3 lockfiles supported")
        manifest = project_file(
            target, str(Path(lock["path"]).parent / "package.json")
        )
        # Advisory evidence binds both native manifest and resolved lock.
        data += manifest.read_bytes()
    return digest(data)


def python_pins(path: Path) -> set[tuple[str, str]]:
    # This is a deliberately narrow supported lock contract, not dependency
    # resolution: flat exact name==version plus hashes/comments only. Native
    # pip-audit owns vulnerability matching. Other lock formats are unavailable.
    pins = set()
    text = path.read_text().replace("\\\n", " ")
    for line in text.splitlines():
        value = line.split("#", 1)[0].split("--hash=", 1)[0].strip()
        if not value:
            continue
        match = re.fullmatch(
            r"([A-Za-z0-9][A-Za-z0-9._-]*)==([A-Za-z0-9.!+_-]+)", value
        )
        if not match:
            raise ValueError(
                "unsupported Python lock: require flat exact pins, no URLs/includes"
            )
        name = re.sub(r"[-_.]+", "-", match[1]).lower()
        pin = (name, match[2])
        if any(existing[0] == name for existing in pins):
            raise ValueError("duplicate or contradictory Python lock pin")
        pins.add(pin)
    return pins


def coverage(target: Path, lock: dict, report: dict) -> None:
    if lock["ecosystem"] == "python":
        expected = python_pins(project_file(target, lock["path"]))
        observed = {
            (re.sub(r"[-_.]+", "-", dep["name"]).lower(), dep["version"])
            for dep in report["dependencies"]
        }
        if observed != expected or len(report["dependencies"]) != len(expected):
            raise ValueError(
                "missing/partial native advisory package collection"
            )
    else:
        lock_data = read_json(project_file(target, lock["path"]))
        expected = sum(
            bool(p.get("version"))
            for name, p in lock_data["packages"].items()
            if name
        )
        actual = report["metadata"]["dependencies"].get("total")
        if type(actual) is not int or actual != expected:
            raise ValueError(
                "missing/partial npm advisory dependency collection"
            )


def cache_path(target: Path, lock: dict) -> Path:
    name = digest(lock["path"].encode())
    return project_file(target, f".harness/reports/advisories/{name}.json")


def offline(target: Path, lock: dict) -> tuple[list[dict], dict]:
    saved = read_json(cache_path(target, lock))
    if (
        type(saved) is not dict
        or set(saved)
        != {"source", "fetched_at", "tool", "lock_digest", "exit", "report"}
        or saved["source"] != SOURCES[lock["ecosystem"]]
        or saved["tool"] != VERSIONS[lock["ecosystem"]]
        or saved["lock_digest"] != lock_id(target, lock)
        or type(saved["exit"]) is not int
        or saved["exit"] not in {0, 1}
    ):
        raise ValueError(
            "missing, failed or stale lock-bound advisory evidence"
        )
    fetched = datetime.fromisoformat(saved["fetched_at"].replace("Z", "+00:00"))
    if (
        fetched.tzinfo is None
        or not 0
        <= (datetime.now(timezone.utc) - fetched).total_seconds()
        <= MAX_AGE
    ):
        raise ValueError(
            "advisory data stale/future: refresh explicit setup (24h maximum)"
        )
    rows = dependencies(saved["report"], lock["ecosystem"], lock["path"])
    coverage(target, lock, saved["report"])
    if bool(rows) != bool(saved["exit"]):
        raise ValueError("native advisory exit contradicts finding data")
    provenance = {k: v for k, v in saved.items() if k != "report"}
    provenance["artifact_sha256"] = digest(
        cache_path(target, lock).read_bytes()
    )
    return rows, provenance


def setup(target: Path) -> int:
    settings = policy(target)
    failed = False
    for lock in settings["locks"]:
        path = cache_path(target, lock)
        path.parent.mkdir(parents=True, exist_ok=True)
        identity = lock_id(target, lock)
        if lock["ecosystem"] == "python":
            python_pins(project_file(target, lock["path"]))
        env = environment(target, path.parent)
        env.pop("NPM_CONFIG_OFFLINE")
        env.pop("PIP_NO_INDEX")
        env["NPM_CONFIG_CACHE"] = str(path.parent / "npm-cache")
        ecosystem = lock["ecosystem"]
        report_file = path.parent / "pip-audit.native"
        if ecosystem == "npm":
            executable = shutil.which("npm", path=env["PATH"])
            if not executable:
                raise ValueError("required npm missing")
            version = [executable, "--version"]
            argv = [
                executable,
                "audit",
                "--package-lock-only",
                "--json",
                "--ignore-scripts",
                "--update-notifier=false",
                "--loglevel=silent",
                "--registry=https://registry.npmjs.org",
            ]
            cwd = (target / lock["path"]).parent
        else:
            executable = str(KIT / "tmp/security-env/bin/python")
            version = [executable, "-m", "pip_audit", "--version"]
            argv = [
                executable,
                "-m",
                "pip_audit",
                "--disable-pip",
                "--no-deps",
                "--requirement",
                str(target / lock["path"]),
                "--format=json",
                "--progress-spinner=off",
                "--vulnerability-service=pypi",
            ]
            report_file.write_text("{}\n")
            argv += ["--output", str(report_file)]
            cwd = target
        version_log = path.parent / "version.log"
        check = execute(version, cwd, version_log, env, 10)
        if (
            check["exit"]
            or version_log.read_text().strip() != VERSIONS[ecosystem]
        ):
            raise ValueError("advisory scanner version missing or incompatible")
        # Never silently reuse old success after a failed explicit refresh.
        path.write_text(json.dumps({"error": "refresh pending/failed"}))
        native = path.parent / "native.log"
        result = execute(argv, cwd, native, env, 120)
        if (
            result["exit"] not in {0, 1}
            or result["reason"]
            not in {"native command completed", "native command exited 1"}
            or result["truncated"]
        ):
            raise ValueError("advisory scanner failed; see bounded setup log")
        raw = (
            read_json(report_file)
            if ecosystem == "python"
            else json.loads(native.read_text())
        )
        rows = dependencies(raw, ecosystem, lock["path"])
        coverage(target, lock, raw)
        if lock_id(target, lock) != identity:
            raise ValueError("lock changed during advisory setup")
        if bool(rows) != bool(result["exit"]):
            raise ValueError("advisory scanner returned contradictory result")
        path.write_text(
            json.dumps(
                {
                    "source": SOURCES[ecosystem],
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                    "tool": VERSIONS[ecosystem],
                    "lock_digest": identity,
                    "exit": result["exit"],
                    "report": raw,
                },
                indent=2,
            )
            + "\n"
        )
        print(
            f"advisories: {lock['path']}: {len(rows)} native findings; {path}"
        )
        failed |= bool(rows)
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        if len(sys.argv) != 3 or sys.argv[1] != "setup":
            raise ValueError(
                "usage: security_advisories.py setup TARGET (network-enabled setup)"
            )
        raise SystemExit(setup(Path(sys.argv[2]).resolve()))
    except (OSError, ValueError, KeyError, TypeError) as error:
        # Do not echo native report/source contents in error diagnostics.
        print(
            f"advisories: unavailable: {type(error).__name__}", file=sys.stderr
        )
        raise SystemExit(2)
