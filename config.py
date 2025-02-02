# config.py

## 定義要監控的股票/ETF，每個項目包含 Yahoo Finance 的代碼與顯示名稱
STOCKS = [
    {"code": "006208.TW", "name": "006208"},
    {"code": "0050.TW", "name": "0050"},
    {"code": "VT",       "name": "VT"},
    {"code": "%5EGSPC",  "name": "S&P500"},
    {"code": "IEF",      "name": "IEF"},
    {"code": "BND",      "name": "BND"}
]

# 當日價格相較前3個月平均降幅門檻 (%)，例如 0.05 表示低於三個月平均收盤價 5% 則符合加碼條件
THRESHOLD_PERCENT = 0.05

# Excel 結果儲存檔案路徑
EXCEL_FILE = "stock_results.xlsx"

# Optional: 用於回測的測試日期 (格式: YYYY-MM-DD)，若為 None 表示使用今日日期
TEST_DATE = None