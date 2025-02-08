from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from config import STOCKS, THRESHOLD_PERCENT, TEST_DATE, DATABASE_FILE
from data_fetch import fetch_stock_data, get_today_stock_price
from analysis import compute_three_month_average, decide_action
from notify import send_telegram_message
import schedule
import time
import storage  # 導入 storage 模組

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

def job():
    # 使用今日作為參考日期
    reference_date = date.today()
    start_date, end_date = get_previous_three_month_date_range(reference_date)
    
    results = []  # 儲存各股票結果（如欲後續使用）
    
    # 組合通知訊息
    message_report = f"股票監測報告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    message_report += "========================================\n\n"
    
    # 逐一監測每個股票/ETF (依據 STOCKS 清單)
    for name, code in STOCKS.items():
        # 爬取前3個月每日收盤價資料
        df_three_month = fetch_stock_data(code, start_date, end_date)
        
        # 計算前三個月市場均價
        three_month_avg = compute_three_month_average(df_three_month)
        
        # 取得當日收盤價 (如無資料則使用最近交易日價格)
        today_price = get_today_stock_price(code)
        
        # 判斷是否符合加碼條件（以前三個月均價作為基準）
        action = decide_action(today_price, three_month_avg, THRESHOLD_PERCENT)
        
        # 格式化價格 (保留小數點後2位)
        today_price_fmt = f"{today_price:.2f}"
        three_month_avg_fmt = f"{three_month_avg:.2f}"
        
        # 計算價格變化百分比
        if three_month_avg != 0:
            pct_diff = ((today_price - three_month_avg) / three_month_avg) * 100
        else:
            pct_diff = 0
        pct_diff_fmt = f"{pct_diff:+.2f}%"
        
        result = {
            "stock_name": name,
            "stock_code": code.replace(".TW", ""),  # 移除 .TW
            "date": datetime.today().strftime("%Y-%m-%d"),
            "today_price": today_price_fmt,
            "three_month_avg": three_month_avg_fmt,
            "action": action
        }
        results.append(result)
        
        # 將結果存入資料庫
        storage.store_result(result)
        
        # 加入當前股票訊息區塊
        message_report += f"股票名稱: {name}\n"
        message_report += f"股票代碼: {code.replace('.TW', '')}\n"
        message_report += f"今日價格: {today_price_fmt}\n"
        message_report += f"前三月均價: {three_month_avg_fmt}\n"
        message_report += f"價格變化: {pct_diff_fmt}\n"
        message_report += f"建議: {action}\n"
        message_report += "----------------------------------------\n"
    
    # 以 Telegram 傳送整體報告
    send_telegram_message(message_report)
    print(message_report)

# 設定每日09:10與21:10執行 job 函數
schedule.every().day.at("09:10").do(job)
schedule.every().day.at("21:10").do(job)

if __name__ == "__main__":
    # 建立資料庫表格 (只需第一次執行)
    storage.create_table()

    # 初始執行一次
    job()

    while True:
        schedule.run_pending()
        time.sleep(60)  # 每60秒檢查一次是否有排程任務需要執行 