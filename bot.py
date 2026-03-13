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

POSTED_FILE = "posted.txt"

posted = set()

if os.path.exists(POSTED_FILE):
    with open(POSTED_FILE) as f:
        posted = set(f.read().splitlines())


def save(link):
    with open(POSTED_FILE, "a") as f:
        f.write(link + "\n")


def add_tag(link):
    link = link.split("?")[0]
    return f"{link}?tag={AFFILIATE_TAG}"


def send(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": TARGET_CHANNEL,
        "text": text,
        "disable_web_page_preview": True
    }

    requests.post(url, data=data)


print("Bot running...")

while True:

    try:

        for channel in SOURCE_CHANNELS:

            page = requests.get(f"https://t.me/s/{channel}").text

            links = re.findall(r'https://www\.amazon\.in/[^\s"]+', page)

            prices = re.findall(r'₹\s?\d+', page)

            price = None
            if prices:
                price = prices[0]

            for link in links:

                if link in posted:
                    continue

                posted.add(link)
                save(link)

                aff = add_tag(link)

                msg = f"""🔥 Amazon Deal

💰 Price: {price}

🛒 Buy Now
{aff}
"""

                send(msg)

                time.sleep(10)

    except Exception as e:
        print(e)

    time.sleep(10)
