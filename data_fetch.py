import yfinance as yf

def fetch_stock_data(stock_code, start_date, end_date):
    """
    從 Yahoo Finance 爬取指定期間內的股價歷史資料。
    注意：yfinance 的 end 參數為「資料結束日的隔日」。
    """
    ticker = yf.Ticker(stock_code)
    df = ticker.history(start=start_date, end=end_date)
    return df

def get_today_stock_price(stock_code):
    """
    取得當日收盤價，若資料更新有延遲，需考慮取最近交易日價格。
    """
    ticker = yf.Ticker(stock_code)
    df = ticker.history(period="1d")
    if not df.empty:
        return df['Close'].iloc[-1]
    return None 