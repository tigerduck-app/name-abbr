<div align="center">

[![License](https://img.shields.io/github/license/tigerduck-app/name-abbr?style=for-the-badge)](LICENSE)

**繁體中文** | [English](README.en.md)
</div>

## 總覽

NTUST 課程名稱與教室名稱的縮寫對照表，供 [TigerDuck](https://github.com/tigerduck-app/tigerduck-app) 各平台客戶端與後端共用。

## 檔案

| 檔案 | 說明 |
|------|------|
| `class-name-abbr.json` | 英文課程全名 → 縮寫 |
| `classroom-name-abbr.json` | 教室代號 → 縮寫 / 拼音 / 英譯 |

## 更新

每學期開課資料公布後，執行腳本從 NTUST 選課系統 API 抓取新課程：

```bash
python3 update_abbr.py --semester 1151
```

- 包含大學部、研究所、三校課程（台大、台師大）
- 既有條目不會被覆蓋，只新增缺少的名稱
- 教室資料可能在學期初期尚未公布

## 授權

[MIT](LICENSE)
