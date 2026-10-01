"""Discovery boundaries independent of native tool configuration."""

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]


class SourcePathsTest(unittest.TestCase):
    def module(self):
        path = ROOT / ".harness/bin/source_paths.py"
        self.assertTrue(path.is_file(), "shared source discovery is required")
        spec = importlib.util.spec_from_file_location("source_paths", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_supported_shebangs_and_unknown_executables(self):
        module = self.module()
        cases = {
            "#!/usr/bin/python3": "python",
            "#!/usr/bin/env python": "python",
            "#!/usr/bin/env -S python3 -u": "python",
            "#!/opt/local/bin/python3.14 -u": "python",
            "#!/bin/sh": "shell",
            "#!/usr/bin/env bash": "shell",
            "#!/usr/bin/env -S bash -eu": "shell",
            "#!/bin/dash": "shell",
            "#!/usr/bin/env ruby": None,
            "#!/usr/bin/env FOO=bar python3": None,
            "ordinary executable text": None,
        }
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "worker with spaces"
            for shebang, expected in cases.items():
                with self.subTest(shebang=shebang):
                    path.write_text(shebang + "\n", encoding="utf-8")
                    path.chmod(0o755)
                    self.assertEqual(module.profile_for(path), expected)
            path.chmod(0o644)
            self.assertIsNone(module.profile_for(path))

    def test_prunes_excluded_directories_before_opening_them(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            for name in (
                "src/generated", "other/generated", "src/generated-copy",
                "src/nested/vendor", "vendor", "maintained",
            ):
                directory = root / name
                directory.mkdir(parents=True)
                (directory / "file.py").write_text("value = 1\n")
            original = module.os.scandir

            def guarded_scandir(path):
                relative = Path(path).relative_to(root).as_posix()
                self.assertNotIn(relative, {
                    "src/generated", "src/nested/vendor", "vendor",
                }, "excluded trees must not be opened")
                return original(path)

            with patch.object(module.os, "scandir", guarded_scandir):
                files = list(module.walk_files(
                    root, ["src/generated", "vendor"]
                ))
            self.assertEqual(
                {path.relative_to(root).as_posix() for path in files},
                {"other/generated/file.py", "src/generated-copy/file.py",
                 "maintained/file.py"},
            )

    def test_skips_file_directory_internal_and_cyclic_symlinks(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "root"
            root.mkdir()
            outside = base / "outside"
            outside.mkdir()
            (outside / "secret.py").write_text("outside\n")
            (root / "safe.py").write_text("value = 1\n")
            (root / "escape.py").symlink_to(outside / "secret.py")
            (root / "escape-dir").symlink_to(outside)
            (root / "internal.py").symlink_to(root / "safe.py")
            (root / "cycle").symlink_to(root)
            self.assertEqual(
                [path.name for path in module.walk_files(root, [])],
                ["safe.py"],
            )


if __name__ == "__main__":
    unittest.main()
