import re
import requests
import time
import os

BOT_TOKEN = "8799971120:AAHjV4JmOvOq9nxpynT0et3rvE04t43ojMw"
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

if os.path.exists(POSTED_FILE):
    with open(POSTED_FILE) as f:
        posted = set(f.read().splitlines())


def save_link(link):
    with open(POSTED_FILE, "a") as f:
        f.write(link + "\n")


def add_tag(link):
    link = link.split("?")[0]
    return f"{link}?tag={AFFILIATE_TAG}"


def detect_price(text):

    price = re.findall(r'₹\s?\d+', text)

    if price:
        return price[0]

    return None


def send_photo(photo, caption):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    data = {
        "chat_id": TARGET_CHANNEL,
        "photo": photo,
        "caption": caption,
        "parse_mode": "Markdown"
    }

    requests.post(url, data=data)


print("Amazon Telegram Deal Bot Running...")

while True:

    try:

        for channel in SOURCE_CHANNELS:

            url = f"https://t.me/s/{channel}"

            html = requests.get(url).text

            links = re.findall(r'https://www\.amazon\.in/[^\s"]+', html)

            images = re.findall(r'https://[^"]+\.jpg', html)

            price = detect_price(html)

            for link in links:

                if link in posted:
                    continue

                posted.add(link)
                save_link(link)

                affiliate = add_tag(link)

                caption = f"""🔥 Amazon Deal

💰 Price: {price}

🛒 Buy Now
{affiliate}
"""

                photo = None

                if images:
                    photo = images[0]

                if photo:
                    send_photo(photo, caption)
                else:

                    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

                    data = {
                        "chat_id": TARGET_CHANNEL,
                        "text": caption,
                        "disable_web_page_preview": True
                    }

                    requests.post(url, data=data)

                time.sleep(15)

    except Exception as e:
        print(e)

    time.sleep(10)
