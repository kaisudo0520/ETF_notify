import os
import requests

def send_telegram_message(message: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("Telegram bot token 或 chat id 未設定。")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print("發送 Telegram 訊息失敗:", response.text)
    except Exception as e:
        print("發送 Telegram 訊息時發生例外:", e) 