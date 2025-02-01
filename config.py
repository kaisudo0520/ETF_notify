# config.py

# 股票代號（006208 為預設值），Yahoo Finance 台股需加上 .TW 後綴
STOCK_CODE = "006208.TW"

# 當日價格相較前3個月平均降幅門檻 (%)，例如 0.05 表示低於三個月平均收盤價 5% 則符合加碼條件
THRESHOLD_PERCENT = 0.05

# Excel 結果儲存檔案路徑
EXCEL_FILE = "stock_results.xlsx"

# Optional: 用於回測的測試日期 (格式: YYYY-MM-DD)，若為 None 表示使用今日日期
TEST_DATE = None