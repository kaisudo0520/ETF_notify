import pandas as pd
from config import EXCEL_FILE
import os

def store_excel_result(result):
    """
    將計算結果存入 Excel。
    若檔案已存在，則以追加的方式合併資料後重新儲存。
    
    result: dict, 例如 {"date": "YYYY-MM-DD", "today_price": ..., "three_month_avg": ..., "action": ...}
    """
    df_new = pd.DataFrame([result])
    if os.path.exists(EXCEL_FILE):
        # 若檔案存在，讀取資料後合併
        df_existing = pd.read_excel(EXCEL_FILE)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
    # 儲存 Excel (使用 openpyxl 作為 engine)
    df_combined.to_excel(EXCEL_FILE, index=False) 