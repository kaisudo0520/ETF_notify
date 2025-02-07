# 股票 (ETF) 監測與加碼/買進機會訊號系統

此專案預設監測以下股票（ETF）：

- 00646.TW (元大S&P500)
- 00757.TW (統一FANG+)
- VT

此系統的主要功能是幫助原本有定期定額投資的使用者，透過逢低小額加碼的方式，降低持有均價，提升資產價值。

您可以根據需求，自行調整 `config.py` 中的 `STOCKS` 清單，以監測其他股票或 ETF。  
**注意：** 此專案 `config.py` 中的 `STOCKS` 已改用字典格式，格式為 `"顯示名稱": "Yahoo Finance 代碼"`，例如：
```python
STOCKS = {
    "00646(元大S&P500)": "00646.TW",
    "00757(統一FANG+)": "00757.TW",
    "VT(全球500)": "VT"
}
```

# ETF或股票加碼判斷

這個專案用 Python 開發，Cursor.ai 協助，功能如下：

- 從 Yahoo Finance (適用複數股票/ETF) 爬取股價資料
- 計算前 3 個月的移動平均股價（以約 63 個交易日作為窗口計算）
- 比較當日價格是否低於三個月移動平均價一定百分比（預設 5%），並做出「加碼」或「維持定期定額」的建議  
  輸出結果中，建議後面會附上今日價格與三個月均價的變化百分比，例如：
  ```
  維持定期定額 (+1.15%)
  ```
- 將結果存入 SQLite 資料庫
- 發送 Telegram 通知（當符合加碼判斷時）
- 提供查詢介面 (文字介面和 GUI 介面)

## 專案架構

- **config.py**  
  設定監控股票/ETF（以字典形式管理）、價格門檻、資料庫檔案路徑等參數。
  
- **data_fetch.py**  
  使用 `yfinance` 將股價歷史資料爬取下來。

- **analysis.py**  
  計算移動平均股價（依日期排序，資料量大於等於63天則使用63天移動平均，小於則直接計算全體平均），並根據門檻值判斷是否「加碼」。

- **storage.py**  
  使用 `sqlite3` 將結果存入 SQLite 資料庫，並提供查詢功能。

- **main.py**  
  主程式，串接各模組功能，並在輸出結果時顯示今日價格、前3個月移動平均股價及價格變化百分比。

- **notify.py**  
  負責透過 Telegram Bot 發送通知訊息 (當系統判斷加碼訊號時)。

- **console_query.py**
  提供文字介面的查詢功能。

- **gui_query.py**
  提供 GUI 介面的查詢功能。

## 使用方式

1. 安裝相依套件

   ```bash
   pip install -r requirements.txt
   ```

2. 配置 `.env` 檔案，在專案根目錄建立或更新，內容示例如下：
   ```plaintext
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   TELEGRAM_CHAT_ID=your_telegram_chat_id_here
   ```

3. 執行程式

    - 主要程式 (每日自動執行):
        ```bash
        python main.py
        ```
    - 文字介面查詢:
        ```bash
        python console_query.py
        ```
    - GUI 介面查詢:
        ```bash
        python gui_query.py
        ```

   執行 `main.py` 後，將依序輸出：
   - 今日價格
   - 前 3 個交易月移動平均股價
   - 建議（附上變化百分比，例如「維持定期定額 (+1.15%)」），並同時將結果存入 SQLite 資料庫。

## 定期執行

程式內建排程功能，預設每日早上 9:00 執行。您可以在 `main.py` 中修改 `schedule.every().day.at("09:00").do(job)` 這一行來調整執行時間。

## 適用性與建議

- 此程式僅適用於市值型ETF或個股（長期趨勢上升），其他種類的股票可能因波動過大或過小而不適用。
- 較適合每日或每週追蹤的投資人使用。
- 調整建議：
  - 若觸發買進訊號頻率過高，可將價格降幅閥值調整為6~7%。
  - 反之，若連續3~6個月都未觸發過買進訊號，可考慮將閥值調低至4%，以便更靈敏捕捉價格低位。
- 註：若長期未觸發買進訊號，表示持有標的市值穩定成長，是正面的趨勢指標。

## 版本資訊

- **版本**: v2.0 - 2025-02-16 (分支：`feature/sqlite-storage-with-query`)
    -   使用 SQLite 資料庫儲存資料。
    -   新增 `console_query.py` 和 `gui_query.py`，提供文字和 GUI 查詢介面。
    -   `storage.py` 新增資料排序功能。
    -   資料庫存入時加入執行時間紀錄。
    -   資料庫的股票代號移除 `.TW`。
    -   移除 `main.py` 中的查詢介面程式碼。
    -   `gui_query.py` 的日期查詢改用日期選擇器。

- **版本**: v1.2 - 2025.02.15  
- **版本更新說明**:
   - 修改 `config.py` 中 `STOCKS` 結構，調整為字典格式，並移除 IEF 與 BND。
   - 更新 `analysis.py`，透過移動窗口（63個交易日）計算前3個月的移動平均股價。
   - 更新 `main.py`，在輸出建議時於文字後面顯示今日價格與三個月均價之變化百分比。
   - 其他優化與錯誤處理。

- **版本**: v1.1 - 2025.02.01  
  - 新增 Telegram Bot 通知功能。
  - 更新 `requirements.txt`，加入 `python-dotenv` 套件以支援 .env 檔案環境變數載入。
  - 調整程式碼讀取 Telegram Bot 參數。

- **版本**: v1.0 - 2025.01.01  
  - 初始版本上線，包含基本的 Yahoo Finance 資料爬取、前3個完整月份平均股價計算、加碼判斷及 Excel 結果存檔功能。