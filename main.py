from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from config import STOCK_CODE, THRESHOLD_PERCENT, TEST_DATE
from data_fetch import fetch_stock_data, get_today_stock_price
from analysis import compute_three_month_average, decide_action
from storage import store_excel_result

def get_previous_three_month_date_range(reference_date):
    """
    根據參考日期計算前三個完整月份的起始及結束日期。
    每月以該月的1號至月底為完整月份，最後傳回的 end_date 為最後完整月份下一個月的第一天。
    例如：若參考日期為 2024-10-06，
    則最後完整月份為 2024-09 (【9月】完整)，
    回傳起始日期為 2024-07-01（代表7月、8月、9月的資料），
    結束日期為 2024-10-01。
    """
    if reference_date.day == 1:
        # 若參考日期為每月第一日，上一個月視為完整月份
        last_complete_day = reference_date - timedelta(days=1)
    else:
        last_complete_day = reference_date - timedelta(days=reference_date.day)

    # 取得最後完整月份的第一天 (例如 2024-09-01)
    first_day_last_complete_month = date(last_complete_day.year, last_complete_day.month, 1)
    # 結束日期為最後完整月份下一個月的第一天 (例如 2024-09-01 加一個月 => 2024-10-01)
    end_date = first_day_last_complete_month + relativedelta(months=1)
    # 回測三個完整月份，起始日期為最後完整月份前兩個月的第一天 (例如 2024-09-01 減2個月 => 2024-07-01)
    start_date = first_day_last_complete_month - relativedelta(months=2)
    return start_date.isoformat(), end_date.isoformat()

def main():
    # 使用回測設定的 TEST_DATE，若為 None 則採用今日日期作為參考日期
    if TEST_DATE:
        reference_date = datetime.strptime(TEST_DATE, "%Y-%m-%d").date()
    else:
        reference_date = date.today()

    # 取得前3個完整月份的日期區間 (ISO 格式字串)
    start_date, end_date = get_previous_three_month_date_range(reference_date)
    
    # 爬取前3個月每日收盤價資料
    df_three_month = fetch_stock_data(STOCK_CODE, start_date, end_date)
    
    # 計算前3個月市場均價
    three_month_avg = compute_three_month_average(df_three_month)
    
    # 取得當日價格（若當日無資料，可能需要使用最近交易日價格）
    today_price = get_today_stock_price(STOCK_CODE)
    
    # 判斷是否符合加碼條件（以前3個月均價作為比較基準）
    action = decide_action(today_price, three_month_avg, THRESHOLD_PERCENT)
    
    print(f"今日價格: {today_price}")
    print(f"前3個月平均收盤價: {three_month_avg}")
    print(f"建議: {action}")
    
    # 儲存結果至 Excel
    result = {
        "date": datetime.today().strftime("%Y-%m-%d"),
        "today_price": today_price,
        "three_month_avg": three_month_avg,
        "action": action
    }
    
    store_excel_result(result)

if __name__ == "__main__":
    main() 