import tempfile
import unittest
from pathlib import Path
from main import extension_group, inventory, safe_target


class AutomationTests(unittest.TestCase):
    def test_extension_group(self):
        self.assertEqual(extension_group(Path("photo.PNG")), "png")
        self.assertEqual(extension_group(Path("LICENSE")), "no_extension")

    def test_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "note.txt").write_text("hello")
            rows = inventory(root)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["extension"], "txt")

    def test_safe_target_avoids_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "report.csv").write_text("existing")
            self.assertEqual(safe_target(root, "report.csv").name, "report_1.csv")


if __name__ == "__main__":
    unittest.main()
