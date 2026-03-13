import time
import requests

BOT_TOKEN = "8799971120:AAHlHlFBghuS73mBBaUI27PA1Ih45f1NhCw"
CHANNEL_ID = "-1002161382456"

while True:

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHANNEL_ID,
        "text": "✅ Bot working!"
    }

    requests.post(url, data=data)

    time.sleep(60)
