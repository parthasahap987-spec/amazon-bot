import requests
import re
import time

BOT_TOKEN = "8799971120:AAHlHlFBghuS73mBBaUI27PA1Ih45f1NhCw"
CHANNEL_ID = "-1002161382456"
AFFILIATE_TAG = "partha07e-21"

# Amazon deal RSS feeds
FEEDS = [
"https://rss.app/feeds/amazon-deals.xml"
]

posted = set()


def extract_link(text):
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
        "chat_id": CHANNEL_ID,
        "text": text,
        "disable_web_page_preview": False
    }

    requests.post(url, data=data)


print("Amazon Auto Bot Running...")

while True:

    try:

        # Example deals
        deals = [
        "https://www.amazon.in/dp/B08CFJBZRK",
        "https://www.amazon.in/dp/B0B4F2TTTS",
        "https://www.amazon.in/dp/B0C7QK3J5N"
        ]

        for link in deals:

            if link in posted:
                continue

            posted.add(link)

            affiliate = add_tag(link)

            msg = f"""
🔥 Amazon Deal

🛒 Buy Now
{affiliate}
"""

            send_message(msg)

            time.sleep(10)

    except Exception as e:
        print(e)

    time.sleep(600)
