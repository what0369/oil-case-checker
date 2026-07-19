import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class StaticAssetsTests(unittest.TestCase):
    def test_tailwind_is_built_locally(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        stylesheet = ROOT / "styles.css"

        self.assertNotIn("cdn.tailwindcss.com", html)
        self.assertIn('href="./styles.css"', html)
        self.assertTrue(stylesheet.is_file())
        self.assertGreater(stylesheet.stat().st_size, 1_000)
        self.assertEqual(package["devDependencies"]["tailwindcss"], "4.3.3")
        self.assertEqual(package["devDependencies"]["@tailwindcss/cli"], "4.3.3")

    def test_multi_keyword_and_search_is_present(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn("多個關鍵字請用空格分隔，結果需同時符合", html)
        self.assertIn("function splitSearchTerms", html)
        self.assertIn("function matchesEverySearchTerm", html)
        self.assertIn("terms.every(term =>", html)


if __name__ == "__main__":
    unittest.main()
