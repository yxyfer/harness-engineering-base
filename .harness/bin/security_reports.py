"""Fixed native security report adapters and exact, expiring exceptions."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re

from evidence_identity import digest
from source_paths import project_file

BLOCKING = {"critical", "high", "unknown"}
SEVERITIES = BLOCKING | {"moderate", "low", "info"}


def read_json(path: Path):
    if path.is_symlink() or not path.is_file():
        raise ValueError("missing or unsafe security data")
    if path.stat().st_size > 4 * 1024 * 1024:
        raise ValueError("security data exceeds 4 MiB")
    return json.loads(path.read_text())


def finding(control, identifier, path, severity, component="", line=0):
    if (
        not all(type(v) is str and v for v in (identifier, path, severity))
        or type(component) is not str
        or type(line) is not int
        or line < 0
        or severity not in SEVERITIES
    ):
        raise ValueError("malformed native finding")
    row = dict(
        control=control,
        id=identifier,
        path=path,
        severity=severity,
        component=component,
        line=line,
    )
    row["fingerprint"] = digest(json.dumps(row, sort_keys=True).encode())
    return row


def dependencies(report, ecosystem: str, path: str) -> list[dict]:
    findings = []
    if ecosystem == "python":
        if (
            type(report) is not dict
            or type(report.get("dependencies")) is not list
        ):
            raise ValueError("missing pip-audit dependency data")
        for dep in report["dependencies"]:
            if (
                type(dep) is not dict
                or not dep.get("version")
                or type(dep.get("vulns")) is not list
                or dep.get("skip_reason")
            ):
                raise ValueError("pip-audit dependency missing/skipped")
            for vulnerability in dep["vulns"]:
                findings.append(
                    finding(
                        "dependencies",
                        vulnerability["id"],
                        path,
                        "unknown",
                        dep["name"] + "@" + dep["version"],
                    )
                )
    elif ecosystem == "npm":
        if (
            type(report) is not dict
            or report.get("error")
            or report.get("auditReportVersion") != 2
            or type(report.get("vulnerabilities")) is not dict
            or type(report.get("metadata", {}).get("dependencies")) is not dict
        ):
            raise ValueError("missing or failed npm audit data")
        for name, item in report["vulnerabilities"].items():
            for advisory in item["via"]:
                # String entries are transitive links; the native report also
                # contains their concrete advisory under the linked package.
                if type(advisory) is str:
                    if advisory not in report["vulnerabilities"]:
                        raise ValueError("npm advisory link has no data")
                    continue
                findings.append(
                    finding(
                        "dependencies",
                        str(advisory["source"]),
                        path,
                        advisory["severity"],
                        name + "@" + item["range"],
                    )
                )
    else:
        raise ValueError("unsupported lock ecosystem")
    return findings


def policy(target: Path) -> dict:
    settings = read_json(project_file(target, ".harness/security.json"))
    if (
        type(settings) is not dict
        or set(settings)
        != {"schema_version", "locks", "dependency_scope", "exceptions"}
        or settings["schema_version"] != 1
        or type(settings["locks"]) is not list
        or type(settings["exceptions"]) is not list
        or not isinstance(settings["dependency_scope"], str)
        or not settings["dependency_scope"].strip()
    ):
        raise ValueError(
            "security.json requires version, locks, scope and exceptions"
        )
    paths = set()
    for lock in settings["locks"]:
        if (
            type(lock) is not dict
            or set(lock) != {"path", "ecosystem"}
            or lock["ecosystem"] not in {"python", "npm"}
            or type(lock["path"]) is not str
        ):
            raise ValueError("unsupported or malformed lock declaration")
        name = lock["path"]
        if (
            not name
            or name.startswith("/")
            or any(p in {"", ".", ".."} for p in name.split("/"))
            or any(c in name for c in "\\:\n\r\t")
            or name in paths
        ):
            raise ValueError("unsafe or duplicate lock path")
        paths.add(name)
        if not project_file(target, name).is_file():
            raise ValueError("declared lock missing")
    if (target / "package.json").exists() and "package-lock.json" not in paths:
        raise ValueError(
            "root npm package requires package-lock.json; other managers unsupported"
        )
    python_metadata = any(
        (target / n).exists() for n in ("pyproject.toml", "requirements.txt")
    )
    if python_metadata and not any(
        lock["ecosystem"] == "python" for lock in settings["locks"]
    ):
        raise ValueError(
            "Python project metadata requires a reviewed supported lock"
        )
    validate_exceptions(settings["exceptions"])
    return settings


def validate_exceptions(exceptions: list[dict]) -> None:
    seen = set()
    now = datetime.now(timezone.utc)
    for row in exceptions:
        if (
            type(row) is not dict
            or set(row) != {"fingerprint", "owner", "reason", "expires"}
            or any(type(v) is not str or not v.strip() for v in row.values())
            or re.fullmatch(r"[a-f0-9]{64}", row["fingerprint"]) is None
            or row["fingerprint"] in seen
        ):
            raise ValueError(
                "exceptions require one exact fingerprint, owner, reason and expiry"
            )
        expiry = datetime.fromisoformat(row["expires"].replace("Z", "+00:00"))
        if (
            expiry.tzinfo is None
            or not 0 < (expiry - now).total_seconds() <= 90 * 86400
        ):
            raise ValueError("exception expired or exceeds 90 days")
        seen.add(row["fingerprint"])


def apply_policy(findings: list[dict], exceptions: list[dict]) -> list[dict]:
    validate_exceptions(exceptions)
    accepted = {row["fingerprint"] for row in exceptions}
    for row in findings:
        row["excepted"] = row["fingerprint"] in accepted
        if row["excepted"] and row["control"] == "secrets":
            raise ValueError(
                "secret findings cannot be excepted; remove synthetic/live value"
            )
        row["blocking"] = row["severity"] in BLOCKING and not row["excepted"]
    return findings
