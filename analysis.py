def compute_three_month_average(df):
    """
    計算傳入 DataFrame 中的三個月平均收盤價。
    假設傳入的 df 包含前3個完整月份的所有交易資料。
    """
    if df.empty:
        return None
    return df['Close'].mean()

def decide_action(today_price, monthly_avg, threshold_percent):
    """
    若當日價格低於前3個月平均價 threshold_percent (例如 5%)，
    則返回「加碼」，否則返回「維持定期定額」。
    """
    if today_price is None or monthly_avg is None:
        return "資料不足"
    if today_price < monthly_avg * (1 - threshold_percent):
        return "加碼"
    else:
        return "維持定期定額" 