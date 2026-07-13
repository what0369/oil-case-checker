#!/usr/bin/env python3
"""Monitor official source pages for relevant content or attachment changes."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

USER_AGENT = (
    "Mozilla/5.0 (compatible; OilCaseCheckerSourceMonitor/1.0; "
    "+https://github.com/what0369/oil-case-checker)"
)
DOWNLOAD_HINT = re.compile(
    r"(?:\.pdf|\.xlsx?|\.csv|\.ods|download|uploaddowndoc|getfile|attachment)",
    re.IGNORECASE,
)
DYNAMIC_TEXT = (
    (re.compile(r"(?:瀏覽|點閱|觀看)(?:人次|次數)?\s*[:：]?\s*[\d,]+"), ""),
    (re.compile(r"目前在線人數\s*[:：]?\s*[\d,]+"), ""),
)


def normalize_text(value: str) -> str:
    value = html.unescape(value).replace("\u3000", " ")
    for pattern, replacement in DYNAMIC_TEXT:
        value = pattern.sub(replacement, value)
    return re.sub(r"\s+", " ", value).strip()


class RelevantHTMLParser(HTMLParser):
    def __init__(self, base_url: str, keywords: list[str]) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.keywords = keywords
        self.skip_depth = 0
        self.anchor_href: str | None = None
        self.anchor_text: list[str] = []
        self.links: set[str] = set()
        self.snippets: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "svg"}:
            self.skip_depth += 1
            return
        if self.skip_depth or tag != "a":
            return
        href = dict(attrs).get("href")
        self.anchor_href = href.strip() if href else None
        self.anchor_text = []

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"} and self.skip_depth:
            self.skip_depth -= 1
            return
        if self.skip_depth or tag != "a" or not self.anchor_href:
            return
        label = normalize_text(" ".join(self.anchor_text))
        absolute = urljoin(self.base_url, self.anchor_href)
        candidate = f"{label} {absolute}".lower()
        if DOWNLOAD_HINT.search(absolute) or any(word.lower() in candidate for word in self.keywords):
            self.links.add(f"{label or '(無標題附件)'} | {absolute}")
        self.anchor_href = None
        self.anchor_text = []

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = normalize_text(data)
        if not text:
            return
        if self.anchor_href:
            self.anchor_text.append(text)
        if any(word.lower() in text.lower() for word in self.keywords):
            self.snippets.add(text[:500])


def fetch(url: str, attempts: int = 3, timeout: int = 35) -> tuple[bytes, str, str]:
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            request = Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8",
                    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.5",
                },
            )
            with urlopen(request, timeout=timeout) as response:
                return (
                    response.read(),
                    response.geturl(),
                    response.headers.get("Content-Type", ""),
                )
        except (HTTPError, URLError, TimeoutError, OSError) as error:
            last_error = error
            if attempt + 1 < attempts:
                time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"抓取失敗：{last_error}")


def decode_html(body: bytes, content_type: str) -> str:
    match = re.search(r"charset=([\w-]+)", content_type, re.IGNORECASE)
    encodings = [match.group(1)] if match else []
    encodings.extend(["utf-8", "big5", "cp950"])
    for encoding in encodings:
        try:
            return body.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            pass
    return body.decode("utf-8", errors="replace")


def inspect_source(source: dict[str, Any], default_keywords: list[str]) -> dict[str, Any]:
    body, final_url, content_type = fetch(source["url"])
    keywords = source.get("keywords", default_keywords)
    if "html" not in content_type.lower() and not body.lstrip().startswith(b"<"):
        signals = [f"binary-sha256:{hashlib.sha256(body).hexdigest()}"]
    else:
        parser = RelevantHTMLParser(final_url, keywords)
        parser.feed(decode_html(body, content_type))
        signals = sorted(parser.links) + sorted(f"文字 | {item}" for item in parser.snippets)
    if not signals:
        raise RuntimeError("頁面可開啟，但找不到關鍵字或附件；網站版型可能已變更")
    payload = json.dumps(signals, ensure_ascii=False, separators=(",", ":"))
    return {
        "fingerprint": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        "final_url": final_url,
        "signal_count": len(signals),
        "signals": signals,
    }


def atomic_json_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def diff_signals(before: list[str], after: list[str]) -> tuple[list[str], list[str]]:
    return sorted(set(after) - set(before)), sorted(set(before) - set(after))


def markdown_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_report(
    checked_at: str,
    rows: list[dict[str, Any]],
    changes: list[dict[str, Any]],
    errors: list[dict[str, str]],
) -> str:
    lines = [
        "# 官方來源監控報告",
        "",
        f"檢查時間（UTC）：`{checked_at}`",
        "",
        "> 本報告只指出官方頁面或附件可能有變更；資料寫入網站前仍須人工核對。",
        "",
        "| 機關 | 來源 | 結果 | 訊號數 | 網址 |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {markdown_escape(row['agency'])} | {markdown_escape(row['name'])} | "
            f"{row['status']} | {row.get('signal_count', '—')} | [開啟]({row['url']}) |"
        )
    if changes:
        lines.extend(["", "## 偵測到的變更", ""])
        for change in changes:
            lines.extend(
                [
                    f"### {change['agency']} — {change['name']}",
                    "",
                    f"指紋：`{change['before'][:12] or '新來源'}` → `{change['after'][:12]}`",
                    "",
                ]
            )
            for label, items in (("新增訊號", change["added"]), ("移除訊號", change["removed"])):
                lines.append(f"**{label}**")
                lines.append("")
                if items:
                    lines.extend(f"- {item}" for item in items[:25])
                    if len(items) > 25:
                        lines.append(f"- ……另有 {len(items) - 25} 項")
                else:
                    lines.append("- 無")
                lines.append("")
    if errors:
        lines.extend(["", "## 抓取錯誤", ""])
        lines.extend(f"- **{item['agency']}**：{item['error']}" for item in errors)
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=Path, default=Path("data/sources.json"))
    parser.add_argument("--state", type=Path, default=Path("data/source-state.json"))
    parser.add_argument("--report", type=Path, default=Path("outputs/source-check-report.md"))
    parser.add_argument("--result", type=Path, default=Path(".source-monitor-result.json"))
    parser.add_argument("--initialize", action="store_true")
    args = parser.parse_args()

    config = json.loads(args.sources.read_text(encoding="utf-8"))
    state = {"schema_version": 1, "sources": {}}
    if args.state.exists():
        state = json.loads(args.state.read_text(encoding="utf-8"))

    checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    previous_sources = state.setdefault("sources", {})
    rows: list[dict[str, Any]] = []
    changes: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    for source in config["sources"]:
        base_row = {key: source[key] for key in ("id", "agency", "name", "url")}
        try:
            observation = inspect_source(source, config["default_keywords"])
            previous = previous_sources.get(source["id"])
            is_changed = previous is not None and (
                previous.get("fingerprint") != observation["fingerprint"]
                or previous.get("url") != source["url"]
            )
            is_new = previous is None
            status = "建立基準" if args.initialize else "有變更" if (is_changed or is_new) else "無變更"
            rows.append({**base_row, "status": status, "signal_count": observation["signal_count"]})
            if args.initialize or is_changed or is_new:
                old_signals = previous.get("signals", []) if previous else []
                added, removed = diff_signals(old_signals, observation["signals"])
                previous_sources[source["id"]] = {
                    "agency": source["agency"],
                    "name": source["name"],
                    "url": source["url"],
                    "final_url": observation["final_url"],
                    "fingerprint": observation["fingerprint"],
                    "signal_count": observation["signal_count"],
                    "signals": observation["signals"],
                    "last_observed_at": checked_at,
                }
                if not args.initialize:
                    changes.append(
                        {
                            **base_row,
                            "before": previous.get("fingerprint", "") if previous else "",
                            "after": observation["fingerprint"],
                            "added": added,
                            "removed": removed,
                        }
                    )
        except Exception as error:  # each source must fail independently
            message = str(error)
            errors.append({**base_row, "error": message})
            rows.append({**base_row, "status": "抓取失敗", "error": message})

    if args.initialize or changes:
        state["last_changed_at"] = checked_at
        atomic_json_write(args.state, state)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(render_report(checked_at, rows, changes, errors), encoding="utf-8")

    result = {
        "checked_at": checked_at,
        "changed_count": len(changes),
        "changed_sources": [item["id"] for item in changes],
        "error_count": len(errors),
        "errors": errors,
    }
    atomic_json_write(args.result, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if args.initialize and errors else 0


if __name__ == "__main__":
    sys.exit(main())
