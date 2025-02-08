# config.py

## 定義要監控的股票/ETF
## 請以如下格式來新增或更新股票/ETF：
## 格式： "顯示名稱": "Yahoo Finance 代碼"
STOCKS = {
    "00646(元大S&P500)": "00646.TW",
    "00757(統一FANG+)": "00757.TW",
    "VT(Vanguard 全世界股票 ETF)": "VT"
}

# 當日價格相較前3個月平均降幅門檻 (%)，
# 例如 0.05 表示若當日價格低於三個月移動平均收盤價 5% 則符合加碼條件
THRESHOLD_PERCENT = 0.05

# Excel 結果儲存檔案路徑 (已不再使用)
# EXCEL_FILE = "stock_results.xlsx"

# Optional: 用於回測的測試日期 (格式: YYYY-MM-DD)，若為 None 表示使用今日日期
TEST_DATE = None

# 資料庫檔案名稱
DATABASE_FILE = "stock_results.db"