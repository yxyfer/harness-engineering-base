import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from example_app.message import page_html


class PageHtmlTest(unittest.TestCase):
    def test_contains_golden_path_message(self) -> None:
        self.assertIn(b"Harness ready", page_html())


if __name__ == "__main__":
    unittest.main()
