import sqlite3
from config import DATABASE_FILE
from datetime import datetime

def create_table():
    """建立資料庫表格 (如果表格不存在)。"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_name TEXT,
            stock_code TEXT,
            date TEXT,
            today_price REAL,
            three_month_avg REAL,
            action TEXT,
            execution_time TEXT  -- 新增執行時間欄位
        )
    ''')
    conn.commit()
    conn.close()

def store_result(result):
    """將資料插入資料庫。"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO stock_results (stock_name, stock_code, date, today_price, three_month_avg, action, execution_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (result['stock_name'], result['stock_code'], result['date'], result['today_price'], result['three_month_avg'], result['action'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  # 加入執行時間

    conn.commit()
    conn.close()

def query_results(query_type, value, sort_by="stock"):
    """
    查詢資料。

    Args:
        query_type: 查詢類型 ('date' 或 'stock')。
        value: 查詢的值 (日期或股票代碼)。
        sort_by: 排序依據 ('stock' 或 'date'，預設為 'stock')。

    Returns:
        查詢結果 (list of tuples)。
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    if query_type == 'date':
        query = '''
            SELECT * FROM stock_results WHERE date = ?
        '''
    elif query_type == 'stock':
        query = '''
            SELECT * FROM stock_results WHERE stock_code = ?
        '''
    else:
        return []

    # 加入排序
    if sort_by == 'stock':
        query += ' ORDER BY stock_code, date'
    elif sort_by == 'date':
        query += ' ORDER BY date, stock_code'

    cursor.execute(query, (value,))
    results = cursor.fetchall()
    conn.close()
    return results 