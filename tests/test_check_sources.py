import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from check_sources import RelevantHTMLParser, diff_signals, normalize_text  # noqa: E402


class SourceMonitorTests(unittest.TestCase):
    def test_parser_keeps_relevant_links_and_attachments(self):
        parser = RelevantHTMLParser("https://example.gov.tw/news/", ["問題油品"])
        parser.feed(
            """
            <a href="detail/1">問題油品下游名單</a>
            <a href="/files/list.pdf">附件</a>
            <a href="unrelated">其他新聞</a>
            <script>問題油品不應從 script 被擷取</script>
            """
        )
        self.assertIn(
            "問題油品下游名單 | https://example.gov.tw/news/detail/1", parser.links
        )
        self.assertIn("附件 | https://example.gov.tw/files/list.pdf", parser.links)
        self.assertEqual(2, len(parser.links))

    def test_dynamic_view_count_is_removed(self):
        self.assertEqual("公告內容", normalize_text("公告內容 點閱次數：12,345"))

    def test_signal_diff_is_sorted_and_unique(self):
        added, removed = diff_signals(["b", "a"], ["b", "c", "c"])
        self.assertEqual(["c"], added)
        self.assertEqual(["a"], removed)


if __name__ == "__main__":
    unittest.main()
