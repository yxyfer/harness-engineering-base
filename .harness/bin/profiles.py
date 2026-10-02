"""Read-only applicability, independent of prerequisite availability."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from config import ConfigError, validate
from source_paths import profile_for, project_file, walk_files

BASE_DOCUMENTS = {"PRODUCT.md", "ARCHITECTURE.md", "QUALITY.md", "DECISIONS.md"}
CAPABILITY_DOCUMENTS = {
    "browser-ui": {"DESIGN.md"},
    "identity": {"SECURITY.md"},
    "multi-tenancy": {"DATA.md", "SECURITY.md"},
    "persistence": {"DATA.md"},
    "file-upload": {"DATA.md", "SECURITY.md"},
    "external-integrations": {"DATA.md", "SECURITY.md"},
    "background-jobs": {"DATA.md"},
}
INTERNAL_DIRECTORIES = [
    ".harness",
    ".agents",
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
]


def project_evidence(target: Path, config: dict[str, Any]):
    evidence: dict[str, list[str]] = {}
    packages: dict[str, dict[str, Any]] = {}
    issues: list[str] = []
    files = list(
        walk_files(
            target, [*config["analysis"]["exclude"], *INTERNAL_DIRECTORIES]
        )
    )
    for path in files:
        profile = profile_for(path)
        if profile and profile not in evidence:
            evidence[profile] = [
                f"maintained source {path.relative_to(target)}"
            ]
    metadata = {
        path.relative_to(target).as_posix()
        for path in files
        if path.name in {"package.json", "pyproject.toml", "requirements.txt"}
    }
    # Canonical root manifests cannot be hidden by analysis exclusions.
    metadata |= {
        name
        for name in ("package.json", "pyproject.toml", "requirements.txt")
        if (target / name).exists() or (target / name).is_symlink()
    }
    for name in sorted(metadata):
        try:
            path = project_file(target, name)
            if path.name == "package.json":
                package = json.loads(path.read_text())
                if type(package) is not dict:
                    raise ValueError(f"{name} must be a JSON object")
                for field in ("dependencies", "devDependencies", "scripts"):
                    if field in package and type(package[field]) is not dict:
                        raise ValueError(f"{name}: {field} must be an object")
                packages[name] = package
                evidence.setdefault("typescript", []).append(f"manifest {name}")
            else:
                evidence.setdefault("python", []).append(f"manifest {name}")
        except (OSError, ValueError) as error:
            issues.append(f"invalid project metadata: {error}")
    return evidence, packages, metadata, issues


def reviewed_selection(detected, reviewed, label, reasons, issues):
    selected = set(detected)
    if reviewed != ["auto"]:
        selected.update(reviewed)
        for name in reviewed:
            reasons.setdefault(name, []).append(f"reviewed project.{label}")
        extra = set(detected) - set(reviewed)
        if extra:
            issues.append(
                f"contradiction: detected {label} {sorted(extra)} absent "
                "from reviewed requirements; controls retained"
            )
    return selected


def root_issues(target: Path, declared: list[str], metadata, packages):
    issues = []
    for name in declared:
        try:
            if not project_file(target, name).is_dir():
                issues.append(f"project root missing: {name}")
        except ValueError as error:
            issues.append(str(error))
    nested = {
        str(Path(name).parent)
        for name in metadata
        if Path(name).parent != Path(".")
    }
    workspaces = any(package.get("workspaces") for package in packages.values())
    if declared != ["."] or nested or workspaces:
        issues.append(
            "unsupported multi-package scope: "
            f"declared={declared}, discovered={sorted(nested)}, "
            f"workspaces={bool(workspaces)}; aggregation is not implemented; "
            "invoke the harness separately on each package root"
        )
    return issues


def initial_nextjs_contract(target: Path, packages: dict) -> bool:
    """Reviewed native initial controls, not complete browser assurance."""
    scripts = packages.get("package.json", {}).get("scripts", {})
    if not all(
        isinstance(scripts.get(name), str) and scripts[name].strip()
        for name in ("build", "test", "smoke")
    ):
        return False
    try:
        path = project_file(target, ".harness/evidence.json")
        evidence = json.loads(path.read_text())
        return (
            set(evidence) == {"adapter", "command"}
            and evidence["adapter"] in {"junit", "unittest"}
            and type(evidence["command"]) is list
            and bool(evidence["command"])
            and all(type(part) is str and part for part in evidence["command"])
        )
    except (OSError, ValueError, TypeError):
        return False


def resolve(target: Path, config: dict[str, Any]) -> dict[str, Any]:
    target = target.resolve()
    evidence, packages, metadata, issues = project_evidence(target, config)
    project = config["project"]
    reasons = {name: list(values) for name, values in evidence.items()}
    profiles = reviewed_selection(
        evidence, project["profiles"], "profiles", reasons, issues
    )
    detected_frameworks = set()
    for name, package in packages.items():
        for field in ("dependencies", "devDependencies"):
            if "next" in package.get(field, {}):
                detected_frameworks.add("nextjs")
                reasons.setdefault("nextjs", []).append(f"{name} {field}.next")
    frameworks = reviewed_selection(
        detected_frameworks,
        project.get("frameworks", ["auto"]),
        "frameworks",
        reasons,
        issues,
    )
    capabilities = set(project.get("capabilities", []))
    for name in capabilities:
        reasons.setdefault(name, []).append("reviewed project.capabilities")
    if "nextjs" in frameworks:
        profiles.add("typescript")
        reasons.setdefault("typescript", []).append(
            "required by nextjs framework"
        )
        capabilities.add("browser-ui")
        reasons.setdefault("browser-ui", []).append(
            "required by nextjs framework"
        )
    roots = project.get("roots", ["."])
    issues.extend(root_issues(target, roots, metadata, packages))
    controls = []
    for name in sorted(profiles):
        controls.append(
            {
                "name": f"{name}-static",
                "status": "implemented",
                "reason": "; ".join(reasons[name]),
            }
        )
        if name in {"python", "typescript"}:
            controls.append(
                {
                    "name": f"{name}-tests",
                    "status": "implemented",
                    "reason": f"application test command for {name}",
                }
            )
    initial_nextjs = "nextjs" in frameworks and initial_nextjs_contract(
        target, packages
    )
    for name in sorted(frameworks | capabilities):
        reason = "; ".join(reasons[name])
        if initial_nextjs and name in {"nextjs", "browser-ui"}:
            controls.append(
                {
                    "name": name,
                    "status": "implemented",
                    "reason": reason + "; initial native production build, "
                    "reported application tests and project browser smoke; "
                    "not full accessibility/performance/security assurance",
                }
            )
            continue
        controls.append(
            {"name": name, "status": "unsupported", "reason": reason}
        )
        issues.append(
            f"unsupported control {name}: {reason}; no executable "
            "framework/capability verification is shipped yet"
        )
    documents = set(config["readiness"]["required_documents"])
    if config["schema_version"] == 2:
        documents.discard("auto")
        documents |= BASE_DOCUMENTS
        for name in capabilities:
            documents |= CAPABILITY_DOCUMENTS.get(name, {"SECURITY.md"})
    warnings = []
    mode = config["security"]["mode"]
    from security import enabled

    if enabled(target, config):
        documents.add("SECURITY.md")
        controls.extend(
            [
                {
                    "name": "security-baseline",
                    "status": "implemented",
                    "reason": "reviewed security mode and explicit policy (schema 1 opt-in)",
                },
                {
                    "name": "test-isolation",
                    "status": "implemented",
                    "reason": "required external macOS direct-egress isolation",
                },
            ]
        )
    elif config["schema_version"] == 1:
        warnings.append(
            "schema 1 compatibility: reviewed documents preserved; "
            "review config-v2.example.toml to opt in; no files changed"
        )
        warnings.append(
            f"deprecated schema 1 security.mode={mode}: no scanner "
            "selection or security assurance; mode was historically inert"
        )
    else:
        warnings.append(
            "security.mode=off: no automated scanner assurance; "
            "capability requirements remain in force"
        )
    return {
        "profiles": sorted(profiles),
        "frameworks": sorted(frameworks),
        "capabilities": sorted(capabilities),
        "roots": roots,
        "documents": sorted(documents),
        "controls": controls,
        "reasons": reasons,
        "issues": issues,
        "warnings": warnings,
    }


def print_selection(selection: dict[str, Any]) -> None:
    for name in (
        "profiles",
        "frameworks",
        "capabilities",
        "roots",
        "documents",
    ):
        print(
            f"selection: {name}={json.dumps(selection[name], separators=(',', ':'))}"
        )
    for control in selection["controls"]:
        print(
            f"selection: {control['name']}: {control['status']}; {control['reason']}"
        )
    for warning in selection["warnings"]:
        print(f"selection: warning: {warning}")
    for issue in selection["issues"]:
        print(f"selection: blocked: {issue}")


def main() -> int:
    if len(sys.argv) != 4 or sys.argv[1] not in {"resolve", "summary"}:
        print(
            "usage: profiles.py resolve|summary TARGET CONFIG", file=sys.stderr
        )
        return 2
    try:
        selection = resolve(
            Path(sys.argv[2]).resolve(), validate(Path(sys.argv[3]))
        )
        if sys.argv[1] == "resolve":
            print(json.dumps(selection))
        else:
            print_selection(selection)
        return 1 if selection["issues"] else 0
    except ConfigError as error:
        print(f"config: {error}", file=sys.stderr)
        return 4
    except (OSError, ValueError) as error:
        print(f"selection: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
