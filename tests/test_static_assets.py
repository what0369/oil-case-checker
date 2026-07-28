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

    def test_camellia_oil_incident_is_separate_and_searchable(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn("<title>油品食安事件查詢系統</title>", html)
        self.assertIn("連淨苦茶油案", html)
        self.assertIn("事件二・獨立事件", html)
        self.assertIn("26V224XW01", html)
        self.assertIn("26S624XW01", html)
        self.assertIn("苯駢芘 2.9 μg/kg", html)
        self.assertIn("後續抽驗進行中", html)
        self.assertIn("https://www.fda.gov.tw/TC/newsContent.aspx?cid=4&amp;id=31669", html)
        self.assertIn("camelliaMatches", html)

    def test_all_source_types_share_one_unified_result_list(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        enterprise = (ROOT / "enterprise-tab.js").read_text(encoding="utf-8")

        self.assertNotIn('id="unified-enterprise-section"', html)
        self.assertNotIn('id="unified-business-section"', html)
        self.assertIn("findEnterpriseAnnouncementMatches(query)", html)
        self.assertIn("renderUnifiedMixedResults(query, matches, enterpriseMatches, filteredBusinesses)", html)
        self.assertIn("function renderUnifiedMixedResults", html)
        self.assertIn("官方產品／批號資料", html)
        self.assertIn("企業自主公告", html)
        self.assertIn("政府流向／業者紀錄", html)
        self.assertIn("mixed-source-icon", html)
        self.assertIn("mixed-source-copy", html)
        self.assertIn("全部來源搜尋結果", html)
        self.assertIn("function findEnterpriseAnnouncementMatches", enterprise)
        self.assertIn("A 級證據・企業自主公告", enterprise)

    def test_batch_statuses_are_nested_in_event_one_and_sections_are_distinct(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        css = (ROOT / "enterprise-tab.css").read_text(encoding="utf-8")

        event_one = html.index("事件一")
        batch_summary = html.index("115 年 4–6 月 30 批油品最新狀態")
        event_two = html.index("事件二・獨立事件")
        self.assertLess(event_one, batch_summary)
        self.assertLess(batch_summary, event_two)
        self.assertEqual(1, html.count('id="blocked-batch-list"'))
        self.assertEqual(1, html.count('id="relisted-batch-list"'))
        self.assertEqual(1, html.count('id="other-batch-list"'))
        self.assertIn("點選展開全部批號", html)
        self.assertIn("🔎 搜尋結果區", html)
        self.assertIn("📚 資料來源與備註（參考區）", html)
        self.assertIn("#single-result-card", css)
        self.assertIn("background: #eff6ff", css)
        self.assertIn("#source-notes", css)
        self.assertIn("background: #fff7e6", css)

    def test_latest_official_updates_are_included_without_changing_batch_counts(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        enterprise = (ROOT / "data" / "enterprise-announcements-draft.js").read_text(encoding="utf-8")

        self.assertIn("115.7.28", html)
        self.assertIn("7 月 27 日第三方獨立調查", html)
        self.assertIn("id=t634544", html)
        self.assertIn("33 瓶", html)
        self.assertIn("架上 0 瓶", html)
        self.assertIn("苦茶籽原料由中國輸入", html)
        self.assertIn("截至 115 年 7 月 28 日尚未公布結果", html)
        self.assertIn('reviewedAt: "2026-07-28"', enterprise)


if __name__ == "__main__":
    unittest.main()
