import requests
import re
import time
from bs4 import BeautifulSoup

BOT_TOKEN = "8799971120:AAFzhADyO1e8A7UH5H80xOkrgCvSb3RBYjM"
TARGET_CHANNEL = "-1002161382456"

SOURCE_CHANNELS = [
    "idoffers",
    "flipshope",
    "eagledealsoffical"
]

last_ids = {}

def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": TARGET_CHANNEL,
        "text": text,
        "disable_web_page_preview": True
    }

    requests.post(url, data=data)


print("Bot started...")

while True:

    for channel in SOURCE_CHANNELS:

        try:

            url = f"https://t.me/s/{channel}?embed=1&mode=tme"

            html = requests.get(url, timeout=20).text

            soup = BeautifulSoup(html, "html.parser")

            posts = soup.select(".tgme_widget_message")

            if not posts:
                continue

            latest = posts[0]

            post_id = latest["data-post"]

            if last_ids.get(channel) == post_id:
                continue

            last_ids[channel] = post_id

            text_block = latest.get_text(" ", strip=True)

            links = re.findall(r'https?://\S+', text_block)

            for link in links:

                if "amazon" in link or "amzn" in link:

                    send_message(f"New Amazon Deal:\n{link}")

                    break

        except Exception as e:
            print("error:", e)

    time.sleep(10)
