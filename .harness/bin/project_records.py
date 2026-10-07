"""Fixed Markdown work-record contract; no second status database."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re

from source_paths import project_file

PLAN_NAME = re.compile(r"^(P\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*$")
TASK_NAME = re.compile(r"^(P\d{3}-T\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
TASK_STATES = {"planned", "ready", "active", "blocked", "partial", "complete"}
PLAN_STATES = {"proposed", "active", "blocked", "complete", "superseded"}
FIELD = re.compile(r"^- \*\*([^*]+):\*\* (.+)$", re.MULTILINE)


class WorkError(ValueError):
    pass


@dataclass
class Task:
    id: str
    title: str
    status: str
    outcome: str
    path: Path
    dependencies: list[str]


@dataclass
class Plan:
    id: str
    title: str
    status: str
    outcome: str
    path: Path
    tasks: list[Task]


def safe_path(root: Path, path: Path) -> Path:
    try:
        relative = path.relative_to(root).as_posix()
        return project_file(root, relative)
    except ValueError as error:
        raise WorkError(str(error)) from error


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match or not match[1].strip():
        raise WorkError(f"missing section: {heading}")
    return match[1].strip()


def metadata(path: Path, expected_id: str, states: set[str]) -> tuple:
    text = path.read_text(encoding="utf-8")
    heading = re.match(rf"# {expected_id} — (.+)\n", text)
    pairs = FIELD.findall(text.split("\n## ", 1)[0])
    fields = dict(pairs)
    if len(pairs) != len(fields):
        raise WorkError(f"duplicate metadata: {path}")
    if not heading or fields.get("ID") != expected_id:
        raise WorkError(f"ID/title does not match filename: {path}")
    if fields.get("Status") not in states:
        raise WorkError(f"invalid status: {path}")
    outcome = " ".join(section(text, "Outcome").split())
    if len(outcome.split()) > 60:
        raise WorkError(f"outcome must be at most 60 words: {path}")
    return text, fields, heading[1], outcome


def read_task(root: Path, path: Path, parent: str) -> Task:
    safe_path(root, path)
    match = TASK_NAME.fullmatch(path.name)
    if not match:
        raise WorkError(f"invalid task filename: {path}")
    task_id = match[1]
    text, fields, title, outcome = metadata(path, task_id, TASK_STATES)
    if task_id.split("-")[0] != parent or fields.get("Plan") != parent:
        raise WorkError(f"task parent mismatch: {path}")
    for heading in ("Implementation", "Review"):
        section(text, heading)
    acceptance = section(text, "Acceptance")
    checks = re.findall(r"^- \[([ xX])\] .+", acceptance, re.MULTILINE)
    if not checks or (fields["Status"] == "complete" and " " in checks):
        raise WorkError(f"missing or incomplete acceptance: {path}")
    if "Depends on" not in fields or "Evidence" not in fields:
        raise WorkError(f"missing dependency/evidence metadata: {path}")
    dependencies = fields["Depends on"]
    evidence = fields["Evidence"]
    if evidence == "pending":
        if fields["Status"] == "complete":
            raise WorkError(f"complete task needs evidence: {path}")
    else:
        validate_evidence(root, path, evidence)
    return Task(
        task_id,
        title,
        fields["Status"],
        outcome,
        path,
        [] if dependencies == "none" else dependencies.split(", "),
    )


def validate_evidence(root: Path, task: Path, value: str) -> None:
    for name in value.split(", "):
        if Path(name).is_absolute():
            raise WorkError(f"unsafe evidence path: {task}")
        path = task.parent / name
        # Resolve lexical '..' without following links, then validate parents.
        path = Path(os.path.abspath(path))
        safe_path(root, path)
        if not path.is_relative_to(task.parent.parent / "evidence"):
            raise WorkError(f"evidence must stay in its plan bundle: {task}")
        if not path.is_file():
            raise WorkError(f"missing evidence: {task}: {name}")


def read_plan(root: Path, bundle: Path, location: str) -> Plan:
    safe_path(root, bundle)
    match = PLAN_NAME.fullmatch(bundle.name)
    if not match or not bundle.is_dir():
        raise WorkError(f"invalid plan folder: {bundle}")
    path = safe_path(root, bundle / "README.md")
    text, fields, title, outcome = metadata(path, match[1], PLAN_STATES)
    for heading in ("Approach", "Architecture impact"):
        section(text, heading)
    if location == "archive" and fields["Status"] not in {
        "complete",
        "superseded",
    }:
        raise WorkError(f"unfinished plan in archive: {path}")
    task_dir = safe_path(root, bundle / "tasks")
    if not task_dir.is_dir():
        raise WorkError(f"missing tasks directory: {path}")
    tasks = [read_task(root, p, match[1]) for p in sorted(task_dir.iterdir())]
    if not tasks:
        raise WorkError(f"plan needs tasks: {path}")
    if fields["Status"] == "complete" and any(
        t.status != "complete" for t in tasks
    ):
        raise WorkError(f"complete plan has incomplete tasks: {path}")
    return Plan(match[1], title, fields["Status"], outcome, path, tasks)


def validate_dependencies(tasks: dict[str, Task]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str) -> None:
        if task_id in visiting:
            raise WorkError(f"dependency cycle: {task_id}")
        if task_id in visited:
            return
        visiting.add(task_id)
        task = tasks[task_id]
        for dependency in task.dependencies:
            if dependency not in tasks:
                raise WorkError(f"unknown dependency: {task_id}: {dependency}")
            visit(dependency)
            if task.status in {"ready", "active", "complete"} and (
                tasks[dependency].status != "complete"
            ):
                raise WorkError(
                    f"unfinished dependency: {task_id}: {dependency}"
                )
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in tasks:
        visit(task_id)


def read_project(root: Path) -> list[Plan]:
    root = root.resolve()
    project = root / "project"
    if not project.exists() and not project.is_symlink():
        return []
    marker = project / "FORMAT.md"
    if not marker.exists() and not marker.is_symlink():
        return []
    safe_path(root, project)
    safe_path(root, marker)
    if "Format: 1\n" not in marker.read_text():
        raise WorkError("unsupported project format; expected Format: 1")
    for name in ("README.md", "systems.md", "features.md"):
        path = safe_path(root, project / "architecture" / name)
        if not path.is_file():
            raise WorkError(f"missing architecture view: {name}")
    plans = []
    for location in ("plans", "archive"):
        directory = safe_path(root, project / location)
        if not directory.exists():
            continue
        for bundle in sorted(directory.iterdir()):
            if bundle.name == "README.md":
                continue
            plans.append(read_plan(root, bundle, location))
    ids = [p.id for p in plans]
    tasks = [t for p in plans for t in p.tasks]
    if len(ids) != len(set(ids)) or len(tasks) != len({t.id for t in tasks}):
        raise WorkError("duplicate plan/task ID")
    validate_dependencies({t.id: t for t in tasks})
    return sorted(plans, key=lambda p: p.id)
