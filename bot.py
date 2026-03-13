import re
import requests
import time
import os

BOT_TOKEN = "8799971120:AAHjV4JmOvOq9nxpynT0et3rvE04t43ojMw"
CHANNEL_ID = "-1002161382456"
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


def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "disable_web_page_preview": True
    }

    requests.post(url, data=data)


print("Amazon Bot Running...")

while True:

    try:

        for channel in SOURCE_CHANNELS:

            html = requests.get(f"https://t.me/s/{channel}").text

            messages = html.split("tgme_widget_message_text")

            for block in messages:

                link_match = re.search(r'https://www\.amazon\.in/[^\s"]+', block)

                if not link_match:
                    continue

                link = link_match.group()

                if link in posted:
                    continue

                price_match = re.search(r'₹\s?\d+', block)

                price = "N/A"
                if price_match:
                    price = price_match.group()

                posted.add(link)
                save_link(link)

                affiliate = add_tag(link)

                text = f"""🔥 Amazon Deal

💰 Price: {price}

🛒 Buy Now
{affiliate}
"""

                send_message(text)

                time.sleep(10)

    except Exception as e:
        print(e)

    time.sleep(120)
