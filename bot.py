import re
import requests
import time

BOT_TOKEN = "8799971120:AAHlHlFBghuS73mBBaUI27PA1Ih45f1NhCw"
TARGET_CHANNEL = "-1002161382456"
AFFILIATE_TAG = "partha07e-21"

# deal source channel usernames
SOURCE_CHANNELS = [
    "LootDealsIndia",
    "DealBee",
    "IndianDeals"
]

posted = set()


def extract_amazon_link(text):

    links = re.findall(r'https?://\S+', text)

    for link in links:
        if "amazon." in link or "amzn.to" in link:
            return link

    return None


def add_tag(link):

    link = link.split("?")[0]

    return f"{link}?tag={AFFILIATE_TAG}"


def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": TARGET_CHANNEL,
        "text": text,
        "disable_web_page_preview": False
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
