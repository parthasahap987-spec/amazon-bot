import re
import requests
import time
import os

BOT_TOKEN = "8799971120:AAHlHlFBghuS73mBBaUI27PA1Ih45f1NhCw"
TARGET_CHANNEL = "-1002161382456"
AFFILIATE_TAG = "partha07e-21"

SOURCE_CHANNELS = [
    "LootDealsIndia",
    "DealBee",
    "IndianDeals",
    "indiafreestffin",
    "freekart",
    "bestdealsdaily099"
]

POSTED_FILE = "posted_links.txt"

posted = set()

# load old posted links
if os.path.exists(POSTED_FILE):
    with open(POSTED_FILE, "r") as f:
        posted = set(f.read().splitlines())


def save_link(link):
    with open(POSTED_FILE, "a") as f:
        f.write(link + "\n")


def add_tag(link):
    link = link.split("?")[0]
    return f"{link}?tag={AFFILIATE_TAG}"


def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": TARGET_CHANNEL,
        "text": text,
        "disable_web_page_preview": True
    }

    requests.post(url, data=data)


print("Auto Amazon Telegram Bot Running...")

while True:

    try:

        for channel in SOURCE_CHANNELS:

            url = f"https://t.me/s/{channel}"

            html = requests.get(url).text

            links = re.findall(r'https://www\.amazon\.in/\S+', html)

            for link in links:

                if link in posted:
                    continue

                posted.add(link)
                save_link(link)

                affiliate = add_tag(link)

                msg = f"""🔥 Amazon Deal

🛒 Buy Now
{affiliate}
"""

                send_message(msg)

                time.sleep(20)

    except Exception as e:
        print(e)

    time.sleep(600)
