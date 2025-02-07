import tkinter as tk
from tkinter import ttk
import storage
from config import DATABASE_FILE
from tkcalendar import DateEntry  # 導入 DateEntry

def query_by_date():
    date_str = date_entry.get_date().strftime("%Y-%m-%d")  # 取得日期並格式化
    results = storage.query_results('date', date_str)
    display_results(results)

def query_by_stock():
    stock_code = stock_entry.get()
    results = storage.query_results('stock', stock_code)
    display_results(results)

def display_results(results):
    # 清空先前的結果
    for row in result_tree.get_children():
        result_tree.delete(row)

    if results:
        for row in results:
            # 移除 ID，並加入 execution_time，格式化價格
            formatted_row = (row[1], row[2], row[3], f"{row[4]:.2f}", f"{row[5]:.2f}", row[6], row[7])
            result_tree.insert("", "end", values=formatted_row)
    else:
        result_tree.insert("", "end", values=("", "查無資料", "", "", "", "", ""))

# 建立主視窗
root = tk.Tk()
root.title("股票資料查詢")

# 日期查詢
date_label = ttk.Label(root, text="依日期查詢:")
date_label.grid(row=0, column=0, padx=5, pady=5)
# 使用 DateEntry
date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
date_entry.grid(row=0, column=1, padx=5, pady=5)
date_button = ttk.Button(root, text="查詢", command=query_by_date)
date_button.grid(row=0, column=2, padx=5, pady=5)

# 股票代碼查詢
stock_label = ttk.Label(root, text="依股票代碼查詢:")
stock_label.grid(row=1, column=0, padx=5, pady=5)
stock_entry = ttk.Entry(root)
stock_entry.grid(row=1, column=1, padx=5, pady=5)
stock_button = ttk.Button(root, text="查詢", command=query_by_stock)
stock_button.grid(row=1, column=2, padx=5, pady=5)

# 顯示結果的 Treeview
# 移除 ID 欄位
result_tree = ttk.Treeview(root, columns=("股票名稱", "股票代碼", "日期", "當日價格", "三個月均價", "動作", "執行時間"), show="headings")
result_tree.heading("股票名稱", text="股票名稱")
result_tree.heading("股票代碼", text="股票代碼")
result_tree.heading("日期", text="日期")
result_tree.heading("當日價格", text="當日價格")
result_tree.heading("三個月均價", text="三個月均價")
result_tree.heading("動作", text="動作")
result_tree.heading("執行時間", text="執行時間")
result_tree.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

root.mainloop() 