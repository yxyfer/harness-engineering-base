"""Small offline security baseline delegated to maintained native tools."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile

from evidence_identity import digest, fingerprint
from evidence_runner import execute
from isolation import command as isolate, environment
from security_advisories import offline
from security_reports import apply_policy, finding, policy, read_json
from source_paths import profile_for, walk_files
from static import node_tool, python_tool

KIT = Path(__file__).resolve().parents[1]


def enabled(target: Path, config: dict) -> bool:
    return config["security"]["mode"] != "off" and (
        config["schema_version"] == 2
        or (target / ".harness/security.json").exists()
        or (target / ".harness/security.json").is_symlink()
    )


def scanner(argv, target, directory, env, report, parse):
    # Scanners run offline too. Never permit automatic downloads, project
    # allow-comments, native blanket ignores or successful exit without data.
    outcome = execute(
        isolate(argv), target, directory / "scanner.log", env, 120
    )
    (directory / "execution.json").write_text(json.dumps(outcome) + "\n")
    try:
        if outcome["reason"].startswith("interrupted"):
            raise KeyboardInterrupt
        if (
            outcome["exit"] not in {0, 1}
            or outcome["reason"]
            not in {"native command completed", "native command exited 1"}
            or outcome["truncated"]
        ):
            raise ValueError("scanner error: native execution failed")
        rows = parse(read_json(report))
    finally:
        if report.is_file() and not report.is_symlink():
            report.write_text("[]\n")
        (directory / "scanner.log").write_text(
            f"native scanner exit={outcome['exit']}; source snippets withheld\n"
        )
    if bool(rows) != bool(outcome["exit"]):
        raise ValueError("scanner error: exit contradicts native findings")
    return rows


def secrets(target, directory, env, snapshot):
    binary = KIT / "tmp/security-bin/gitleaks"
    version = directory / "gitleaks-version.log"
    result = execute([str(binary), "version"], target, version, env, 10)
    if result["reason"].startswith("interrupted"):
        raise KeyboardInterrupt
    if result["exit"] or version.read_text().strip() != "8.30.1":
        raise ValueError("required pinned Gitleaks 8.30.1 unavailable")
    with tempfile.TemporaryDirectory(
        prefix="secret-inputs-", dir=directory
    ) as temporary:
        stage = Path(temporary)
        for name in snapshot["files"]:
            if (
                name.startswith(("kit:", "mode:", "environment:", "advisory:"))
                or name == "selected-config"
            ):
                continue
            source = target / name
            destination = stage / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        report = directory / "secrets.native"

        def parse(native):
            if type(native) is not list:
                raise ValueError("missing Gitleaks findings")
            return [
                finding(
                    "secrets",
                    row["RuleID"],
                    Path(row["File"]).relative_to(stage).as_posix()
                    if Path(row["File"]).is_absolute()
                    else row["File"],
                    "critical",
                    line=row["StartLine"],
                )
                for row in native
            ]

        rows = scanner(
            [
                str(binary),
                "dir",
                str(stage),
                "--config",
                str(KIT / "security/gitleaks.toml"),
                "--gitleaks-ignore-path",
                str(stage / "no-ignore"),
                "--ignore-gitleaks-allow",
                "--redact=100",
                "--no-banner",
                "--no-color",
                "--report-format=json",
                "--report-path",
                str(report),
                "--timeout=90",
            ],
            target,
            directory,
            env,
            report,
            parse,
        )
        # Retain only sanitized fields; never native Match/Secret snippets.
        report.write_text(json.dumps(rows, indent=2) + "\n")
        return rows


def source(target, directory, env, snapshot, profile):
    # Consumer source excludes shipped machinery, never reviewed app files.
    # The authoring root explicitly covers maintained Python engine/tests;
    # nested language foundations and fixtures are independently verified.
    root_kit = target == KIT.parent
    scope = target
    excluded = [
        ".git",
        ".venv",
        "venv",
        "node_modules",
        "__pycache__",
        ".ruff_cache",
        ".pytest_cache",
        ".mypy_cache",
        ".next",
        ".harness/reports",
        ".harness/tmp",
    ]
    excluded += (
        [".harness/tests/fixtures", ".harness/templates"]
        if root_kit
        else [".harness", ".agents"]
    )
    files = [
        str(path)
        for path in walk_files(scope, excluded)
        if profile_for(path) == profile
    ]
    if not files:
        return None
    (directory / "scope.json").write_text(
        json.dumps([str(Path(name).relative_to(target)) for name in files])
        + "\n"
    )
    native = directory / "source.native"
    tool = (
        python_tool(target, "ruff")
        if profile == "python"
        else node_tool(target, "eslint")
    )
    version_log = directory / "tool-version.log"
    version_result = execute(
        isolate([*tool, "--version"]), target, version_log, env, 10
    )
    if version_result["reason"].startswith("interrupted"):
        raise KeyboardInterrupt
    if version_result["exit"] or version_result["truncated"]:
        raise ValueError("required native source scanner version unavailable")
    (directory / "tool.json").write_text(
        json.dumps(
            {
                "tool": version_log.read_text().strip(),
                "rules": ["S307", "S602", "S608"]
                if profile == "python"
                else ["no-eval", "no-new-func"],
            }
        )
        + "\n"
    )
    if profile == "python":
        argv = [
            *tool,
            "check",
            "--isolated",
            "--no-cache",
            "--ignore-noqa",
            "--select=S307,S602,S608",
            "--output-format=json",
            *files,
        ]

        def parse_python(data):
            if type(data) is not list:
                raise ValueError("missing Ruff security data")
            return [
                finding(
                    "source-python",
                    row["code"],
                    Path(row["filename"]).relative_to(target).as_posix(),
                    "high",
                    line=row["location"]["row"],
                )
                for row in data
            ]

        parser = parse_python
    else:
        argv = [
            *tool,
            "--no-ignore",
            "--no-inline-config",
            "--rule",
            "no-eval:error",
            "--rule",
            "no-new-func:error",
            "--format=json",
            *files,
        ]

        def parse_typescript(data):
            if type(data) is not list or len(data) != len(files):
                raise ValueError("missing ESLint security scope/data")
            rows = []
            for file in data:
                if file.get("fatalErrorCount") or any(
                    m.get("ruleId") is None for m in file["messages"]
                ):
                    raise ValueError(
                        "ESLint parser/config error or ignored source"
                    )
                for message in file["messages"]:
                    rows.append(
                        finding(
                            "source-typescript",
                            message["ruleId"],
                            Path(file["filePath"])
                            .relative_to(target)
                            .as_posix(),
                            "high",
                            line=message["line"],
                        )
                    )
            return rows

        parser = parse_typescript

    # Native JSON stdout is captured separately from diagnostic stderr by the
    # tool's own output flag. Both tools support --output-file.
    argv += ["--output-file", str(native)]
    rows = scanner(argv, target, directory, env, native, parser)
    native.write_text(json.dumps(rows, indent=2) + "\n")
    return rows


def run(
    target: Path, config_path: Path, config: dict, directory: Path
) -> list[dict]:
    # Imported lazily to share Step 08's exact evidence record shape.
    from verify import control

    settings = None
    setup_error = None
    try:
        settings = policy(target)
    except (OSError, ValueError, KeyError, TypeError):
        setup_error = "security policy missing, invalid or expired"
    snapshot = fingerprint(target, KIT, config_path)
    records = []
    interrupted = False
    for name in (
        "secrets",
        "dependencies",
        "source-python",
        "source-typescript",
    ):
        item = control("security-" + name, "reviewed offline security baseline")
        records.append(item)
        work = directory / item["name"]
        work.mkdir()
        env = environment(target, work)
        rows = []
        provenance = []
        try:
            if interrupted:
                raise KeyboardInterrupt
            if setup_error:
                raise ValueError(setup_error)
            assert settings is not None
            if name == "secrets":
                rows = secrets(target, work, env, snapshot)
                provenance = [{"tool": "Gitleaks 8.30.1 built-in rules"}]
            elif name == "dependencies":
                for lock in settings["locks"]:
                    found, metadata = offline(target, lock)
                    rows.extend(found)
                    provenance.append(metadata)
                if not settings["locks"]:
                    item.update(
                        required=False,
                        state="not-applicable",
                        reason="reviewed no dependencies: "
                        + settings["dependency_scope"],
                    )
                    continue
            else:
                profile = "python" if name == "source-python" else "typescript"
                found = source(target, work, env, snapshot, profile)
                if found is None:
                    item.update(
                        required=False,
                        state="not-applicable",
                        reason="no maintained " + profile + " source",
                    )
                    continue
                rows = found
                provenance = [read_json(work / "tool.json")]
            rows = apply_policy(rows, settings["exceptions"])
            blocked = sum(row["blocking"] for row in rows)
            item.update(
                state="failed" if blocked else "passed",
                exit=1 if blocked else 0,
                reason=f"{len(rows)} findings; {blocked} blocking; offline/native scope",
            )
        except KeyboardInterrupt:
            item["reason"] = "interrupted; security control not completed"
            interrupted = True
        except (OSError, ValueError, KeyError, TypeError) as error:
            # Exceptions may contain native source content. Never echo them.
            item["reason"] = setup_error or (
                str(error)
                if type(error) is ValueError
                else "unavailable security data/tool (native data omitted)"
            )
        execution = work / "execution.json"
        if execution.is_file():
            native = read_json(execution)
            item.update(
                command=native["command"],
                seconds=native["seconds"],
                truncated=native["truncated"],
            )
            if item["state"] == "unavailable":
                item["exit"] = native["exit"]
        artifact = directory / (item["name"] + ".json")
        artifact.write_text(
            json.dumps(
                {
                    "findings": rows,
                    "provenance": provenance,
                    "scope": read_json(work / "scope.json")
                    if (work / "scope.json").is_file()
                    else None,
                },
                indent=2,
            )
            + "\n"
        )
        item["artifacts"] = [
            {"path": artifact.name, "sha256": digest(artifact.read_bytes())}
        ]
    return records
