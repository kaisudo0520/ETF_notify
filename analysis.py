def compute_three_month_average(df):
    """
    計算三個月的移動平均股價：
    - 對資料依日期排序（假設 DataFrame 的 index 為日期）。
    - 若資料天數 ≥ 63 (約三個月的交易天數)，以 63 為窗口計算移動平均，
      並取最後一天的移動平均值作為計算結果。
    - 若資料不足 63 天，則回傳所有資料的平均值。
    """
    df = df.sort_index()
    if len(df) >= 63:
        # 使用窗口大小63計算 63 天移動平均，並取最後一天的值
        return df["Close"].rolling(window=63).mean().iloc[-1]
    else:
        return df["Close"].mean()

def decide_action(today_price, monthly_avg, threshold_percent):
    """
    若當日價格低於前3個月移動平均價格 threshold_percent (例如 5%)，
    則返回「加碼」，否則返回「維持定期定額」。
    """
    if today_price is None or monthly_avg is None:
        return "資料不足"
    if today_price < monthly_avg * (1 - threshold_percent):
        return "加碼"
    else:
        return "維持定期定額" 