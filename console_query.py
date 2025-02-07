import storage
from config import DATABASE_FILE

def main():
    """提供查詢介面"""
    while True:
        print("\n請選擇查詢方式：")
        print("1. 依日期查詢")
        print("2. 依股票代碼查詢")
        print("3. 離開")

        choice = input("請輸入選項 (1/2/3): ")

        if choice == '1':
            date_str = input("請輸入日期 (YYYY-MM-DD): ")
            results = storage.query_results('date', date_str)
            if results:
                print("\n查詢結果：")
                print("股票名稱 | 股票代碼 | 日期 | 當日價格 | 三個月均價 | 動作 | 執行時間")
                print("-" * 70)
                for row in results:
                    print(f"{row[1]} | {row[2]} | {row[3]} | {row[4]:.2f} | {row[5]:.2f} | {row[6]} | {row[7]}")
            else:
                print("查無資料。")
        elif choice == '2':
            stock_code = input("請輸入股票代碼: ")
            results = storage.query_results('stock', stock_code)
            if results:
                print("\n查詢結果：")
                print("股票名稱 | 股票代碼 | 日期 | 當日價格 | 三個月均價 | 動作 | 執行時間")
                print("-" * 70)
                for row in results:
                    print(f"{row[1]} | {row[2]} | {row[3]} | {row[4]:.2f} | {row[5]:.2f} | {row[6]} | {row[7]}")
            else:
                print("查無資料。")
        elif choice == '3':
            break
        else:
            print("無效的選項。")

if __name__ == "__main__":
    main() 