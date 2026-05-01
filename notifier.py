import requests, os

BOT = os.getenv("TELEGRAM_BOT_TOKEN")
CID = os.getenv("TELEGRAM_CHAT_ID")

def notify(ip, count, total_visits):
    msg = f"🧠 مُدرِك\nمستخدم جديد: {ip}\nاستخدم: {count}/3\nإجمالي اليوم: {total_visits}"
    requests.post(f"https://api.telegram.org/bot{BOT}/sendMessage",
                  json={"chat_id": CID, "text": msg})