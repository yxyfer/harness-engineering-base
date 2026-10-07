"""Structured work records and reversible whole-plan archiving."""

from pathlib import Path
import subprocess
import json
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
from project_records import WorkError, read_project
from project_work import archive_plan, check_indexes, sync_indexes


class ProjectWorkTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="project work ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        architecture = self.root / "project/architecture"
        architecture.mkdir(parents=True)
        (self.root / "project/FORMAT.md").write_text("Format: 1\n")
        for name in ("README.md", "systems.md", "features.md"):
            (architecture / name).write_text("# Architecture\n")
        self.bundle = self.root / "project/plans/P001-example"
        (self.bundle / "tasks").mkdir(parents=True)
        (self.bundle / "evidence").mkdir()
        (self.bundle / "evidence/result.md").write_text("# Result\n")
        self.plan = self.bundle / "README.md"
        self.plan.write_text(
            "# P001 — Example\n\n- **ID:** P001\n"
            "- **Status:** active\n\n## Outcome\n\nUseful behaviour.\n"
            "\n## Approach\n\nSmall change.\n"
            "\n## Architecture impact\n\nNo runtime change.\n"
        )
        self.task = self.bundle / "tasks/P001-T001-example.md"
        self.task.write_text(
            "# P001-T001 — Example task\n\n- **ID:** P001-T001\n"
            "- **Plan:** P001\n- **Status:** complete\n"
            "- **Depends on:** none\n"
            "- **Evidence:** ../evidence/result.md\n"
            "\n## Outcome\n\nUseful behaviour.\n"
            "\n## Implementation\n\nLinked source.\n"
            "\n## Acceptance\n\n- [x] Behaviour proved.\n"
            "\n## Review\n\nRevert source; no deployment.\n"
        )

    def replace_task(self, before, after):
        self.task.write_text(self.task.read_text().replace(before, after))

    def test_indexes_derive_progress_and_detect_stale_status(self):
        sync_indexes(self.root)
        check_indexes(self.root)
        self.assertIn("1/1", (self.root / "project/README.md").read_text())
        self.replace_task("Status:** complete", "Status:** active")
        self.replace_task("[x]", "[ ]")
        with self.assertRaisesRegex(WorkError, "stale index"):
            check_indexes(self.root)
        sync_indexes(self.root)
        self.assertIn("0/1", (self.root / "project/README.md").read_text())

    def test_wrong_parent_and_duplicate_ids_fail(self):
        self.replace_task("Plan:** P001", "Plan:** P002")
        with self.assertRaisesRegex(WorkError, "parent"):
            read_project(self.root)
        self.replace_task("Plan:** P002", "Plan:** P001")
        (self.bundle / "tasks/P001-T001-duplicate.md").write_text(
            self.task.read_text()
        )
        with self.assertRaisesRegex(WorkError, "duplicate"):
            read_project(self.root)

    def test_missing_dependency_and_cycle_fail(self):
        self.replace_task("Depends on:** none", "Depends on:** P001-T002")
        with self.assertRaisesRegex(WorkError, "unknown dependency"):
            read_project(self.root)
        other = self.bundle / "tasks/P001-T002-other.md"
        other.write_text(
            self.task.read_text()
            .replace("P001-T001", "P001-T002")
            .replace("Depends on:** P001-T002", "Depends on:** P001-T001")
        )
        with self.assertRaisesRegex(WorkError, "cycle"):
            read_project(self.root)

    def test_complete_requires_acceptance_and_safe_evidence(self):
        self.replace_task("[x]", "[ ]")
        with self.assertRaisesRegex(WorkError, "acceptance"):
            read_project(self.root)
        self.replace_task("[ ]", "[x]")
        self.replace_task("../evidence/result.md", "../../../../outside.md")
        with self.assertRaisesRegex(WorkError, "evidence"):
            read_project(self.root)

    def test_symlinked_work_and_evidence_are_rejected(self):
        evidence = self.bundle / "evidence/result.md"
        evidence.unlink()
        evidence.symlink_to(self.plan)
        with self.assertRaisesRegex(WorkError, "symlink"):
            read_project(self.root)
        evidence.unlink()
        evidence.write_text("# Result\n")
        self.task.unlink()
        self.task.symlink_to(self.plan)
        with self.assertRaisesRegex(WorkError, "symlink"):
            read_project(self.root)

    def test_archive_moves_bundle_preserves_evidence_and_repairs_links(self):
        self.task.write_text(
            self.task.read_text() + "\n[Evidence](../evidence/result.md)\n"
        )
        sync_indexes(self.root)
        caller = self.root / "docs/caller.md"
        caller.parent.mkdir()
        caller.write_text(
            "# Caller\n\n[Task](../project/plans/P001-example/"
            "tasks/P001-T001-example.md#outcome)\n"
        )
        before = (self.bundle / "evidence/result.md").read_bytes()
        archive_plan(self.root, "P001")
        archived = self.root / "project/archive/P001-example"
        self.assertFalse(self.bundle.exists())
        self.assertEqual((archived / "evidence/result.md").read_bytes(), before)
        self.assertIn("project/archive/", caller.read_text())
        self.assertIn(
            "Status:** complete", (archived / "README.md").read_text()
        )
        self.assertIn(
            "[Evidence](../evidence/result.md)",
            (archived / "tasks/P001-T001-example.md").read_text(),
        )
        check_indexes(self.root)

    def test_archive_write_error_restores_bundle_and_indexes(self):
        sync_indexes(self.root)
        index = self.root / "project/README.md"
        original = index.read_text()
        native_write = Path.write_text
        failed = False

        def write(path, text, *args, **kwargs):
            nonlocal failed
            if path == index and not failed:
                failed = True
                raise OSError("synthetic write failure")
            return native_write(path, text, *args, **kwargs)

        with patch.object(Path, "write_text", write):
            with self.assertRaisesRegex(OSError, "synthetic write"):
                archive_plan(self.root, "P001")
        self.assertTrue(self.bundle.is_dir())
        self.assertEqual(index.read_text(), original)
        check_indexes(self.root)

    def test_incomplete_archive_does_not_change_files(self):
        self.replace_task("Status:** complete", "Status:** blocked")
        self.replace_task("[x]", "[ ]")
        before = self.plan.read_bytes()
        with self.assertRaisesRegex(WorkError, "incomplete"):
            archive_plan(self.root, "P001")
        self.assertEqual(self.plan.read_bytes(), before)
        self.assertTrue(self.bundle.is_dir())

    def test_archive_does_not_rewrite_shipped_harness_links(self):
        kit = self.root / ".harness"
        kit.mkdir()
        managed = kit / "owned.md"
        content = "# Owned\n\n[Plan](../project/plans/P001-example/README.md)\n"
        managed.write_text(content)
        (kit / "release-files.json").write_text(
            json.dumps([".harness/owned.md"])
        )
        with self.assertRaisesRegex(WorkError, "managed link"):
            archive_plan(self.root, "P001")
        self.assertEqual(managed.read_text(), content)
        self.assertTrue(self.bundle.is_dir())

    def test_legacy_projects_are_not_forced_to_migrate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "project/src").mkdir(parents=True)
            self.assertEqual(read_project(root), [])
            check_indexes(root)
            (root / "project").rename(root / "source")
            (root / "project").symlink_to(
                root / "source", target_is_directory=True
            )
            self.assertEqual(read_project(root), [])
            check_indexes(root)

    def test_public_command_and_documentation_gate_enforce_records(self):
        kit = Path(__file__).resolve().parents[2]
        result = subprocess.run(
            [str(kit / "harness"), "project", "sync", str(self.root)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.replace_task("Plan:** P001", "Plan:** P002")
        result = subprocess.run(
            [
                sys.executable,
                str(kit / ".harness/checks/documentation/check"),
                str(self.root),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("parent mismatch", result.stderr)


if __name__ == "__main__":
    unittest.main()
