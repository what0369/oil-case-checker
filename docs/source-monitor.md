# 官方來源定期監控

網站合併這項功能後，GitHub Actions 會在臺灣時間每天 **08:17**、**20:17** 執行，也可以從 Actions 頁面手動執行。

## 它會做什麼

1. 讀取 `data/sources.json` 內登錄的食藥署及地方衛生局官方頁面。
2. 找出與中聯油脂、問題油品、下游流向、下架及稽查相關的文字與附件連結。
3. 將本次指紋與 `data/source-state.json` 的上次結果比較。
4. 若有變更，更新監控報告並建立或更新草稿 PR，等待人工核對。
5. 若官方網站抓取失敗，建立或更新一則 GitHub Issue 告警；恢復正常後自動關閉。

監控不會自動合併 PR，也不會直接修改產品或店家資料。不同機關的 PDF、Excel 和網頁格式不一致，人工確認仍可避免誤判。

## 第一次啟用

請到 repository 的 **Settings → Actions → General → Workflow permissions**：

- 選擇 **Read and write permissions**，或保留預設並讓 workflow 內的明確權限生效。
- 勾選 **Allow GitHub Actions to create and approve pull requests**。

接著到 **Actions → Check official source updates → Run workflow** 手動跑一次，確認權限與來源網站都正常。

## 新增或調整來源

編輯 `data/sources.json`。每個來源至少需要：

```json
{
  "id": "唯一英文代號",
  "agency": "機關名稱",
  "name": "來源頁名稱",
  "url": "官方網頁網址"
}
```

若某個頁面使用不同詞彙，可在該來源加入 `keywords` 陣列，覆蓋預設關鍵字。

## 本機測試

```bash
python3 scripts/check_sources.py --result /tmp/source-monitor-result.json
```

只有建立第一份基準資料時才使用 `--initialize`。一般執行不要使用它。

> GitHub 對公開且 60 天沒有任何 repository 活動的排程 workflow 可能自動停用；若 Actions 沒再執行，請到 Actions 頁面重新啟用。
