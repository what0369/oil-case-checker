import json
import re
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

    def test_current_batch_statuses_are_complete_and_separated(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        data = (ROOT / "batch-status-data.js").read_text(encoding="utf-8")

        self.assertEqual(7, data.count('status: "blocked"'))
        self.assertEqual(19, data.count('status: "relisted"'))
        self.assertEqual(3, data.count('status: "held"'))
        self.assertEqual(1, data.count('status: "no-specimen"'))
        self.assertEqual(30, data.count('batch: "'))
        batches = re.findall(r'batch: "([^"]+)"', data)
        self.assertEqual(30, len(set(batches)))
        self.assertIn("2026/07/22 13:34", data)
        self.assertIn("forcedOperatorRows: 5139", data)
        self.assertIn("function findBatchStatus", html)
        self.assertIn("產品或店家名稱命中舊流向資料時，不再自動判定為目前仍下架", html)


if __name__ == "__main__":
    unittest.main()
