# 股票監測系統

此專案用於監測以下股票與資產:

- 006208.TW
- 0050.TW
- VT
- %5EGSPC (S&P500)
- IEF
- BND

可自行調整 `config.py` 中的 `STOCKS` 清單，以監測其他股票/ETF。

# ETF或股票加碼判斷

這個專案用 Python 開發，Cursor.ai 協助，功能如下：
- 從 Yahoo Finance (適用複數股票/ETF) 爬取股價資料
- 計算前 3 個完整月份的平均收盤價
- 比較當日股價是否低於三個月平均價一定百分比（預設 5%）
- 輸出建議：「加碼」或「維持定期定額」
- 將結果存入 Excel 檔案
- 發送 Telegram 通知

## 專案架構

- **config.py**  
  設定股票代號、門檻、Excel 檔案路徑等參數。
  
- **data_fetch.py**  
  使用 `yfinance` 將股價歷史資料爬取下來。

- **analysis.py**  
  計算前三個完整月份的平均股價，並依據門檻來判斷是否「加碼」。

- **storage.py**  
  使用 `pandas` 將結果存入 Excel。

- **main.py**  
  主程式，與各模組之間的串接。

- **notify.py**  
  負責發送 Telegram 通知的功能。

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

## Telegram Bot 通知設定

本專案已整合 Telegram Bot 通知功能，當系統判斷有買進（"加碼"）訊號時，
將自動發送通知訊息至指定 Telegram 聊天 ID。

請在專案根目錄建立或更新 `.env` 檔案，加入以下環境變數：

.env 範例：
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

若未設定這些環境變數，則無法發送 Telegram 通知。

## 定期執行

可使用 Windows Task Scheduler 或 Linux cron 進行定時執行。

## 回測設定

若需要回測特定日期，可在 `config.py` 中設定 `TEST_DATE`（格式：YYYY-MM-DD），預設為 `None` 表示使用今日日期。

## 未來展望

- 整合永豐證券 API 自動下單

## 版本資訊

- ### 版本: v1.1 - 2025.02.01
   - 新增 Telegram Bot 通知功能，當系統判斷有買進（"加碼"）訊號時，會自動發送通知。
   - 更新 `requirements.txt`，新增 `python-dotenv` 套件以支援環境變數載入。
   - 調整程式碼以支援從 .env 檔案讀取 Telegram Bot 參數。

- ### 版本: v1.0 - 2025.01.01
   - 初始版本上線
   - 新增 Yahoo Finance 資料爬取功能（針對 "006208.TW"）
   - 計算前 3 個完整月份平均收盤價
   - 判斷「加碼」或「維持定期定額」決策
   - 結果儲存至 Excel 檔案