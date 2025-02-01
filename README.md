# 006208 投資加碼判斷

這個專案用 Python 開發，功能如下：
- 從 Yahoo Finance (適用 `"006208.TW"`) 爬取股價資料
- 計算前 3 個完整月份的平均收盤價
- 比較當日股價是否低於三個月平均價一定百分比（預設 5%）
- 輸出建議：「加碼」或「維持定期定額」
- 將結果存入 Excel 檔案

## 專案架構

- **config.py**  
  設定股票代號、門檻、Excel 檔案路徑等參數。
  
- **data_fetch.py**  
  使用 `yfinance` 將股價歷史資料爬取下來。

- **analysis.py**  
  計算前三個完整月份的平均股價，並依據門檻來判斷是否「加碼」。

- **storage.py**  
  使用 `pandas` 將結果存入 Excel，後續可擴充 Notion API。

- **main.py**  
  主程式，包括回測日期設定（若有需要）與各模組之間的串接。

## 使用方式

1. 安裝相依套件

   ```bash
   pip install -r requirements.txt
   ```

2. 執行程式

   ```bash
   python main.py
   ```

   執行後會顯示：
   - 今日價格
   - 前 3 個完整月份平均收盤價
   - 建議動作（加碼 / 維持定期定額）
   
   同時會在專案目錄產生或更新 `stock_results.xlsx`。

## 回測設定

若需要回測特定日期，可在 `config.py` 中設定 `TEST_DATE`（格式：YYYY-MM-DD），預設為 `None` 表示使用今日日期。

## 未來展望

- 加入 Windows Task Scheduler 或 Linux cron 進行定時執行
- 擴充 Email / Telegram 通知功能
- 整合永豐證券 API 自動下單及 Notion API 儲存結果 

## 版本資訊

- **版本**: v1.0 - 2025.02.01
- **版本更新說明**:
   - 初始版本上線
   - 新增 Yahoo Finance 資料爬取功能（針對 "006208.TW"）
   - 計算前 3 個完整月份平均收盤價
   - 判斷「加碼」或「維持定期定額」決策
   - 結果儲存至 Excel 檔案