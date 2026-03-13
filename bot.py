import requests
import feedparser
import time

BOT_TOKEN = "8799971120:AAHlHlFBghuS73mBBaUI27PA1Ih45f1NhCw"
CHANNEL_ID = "-1002161382456"
AFFILIATE_TAG = "partha07e-21"

# working RSS source
RSS_URL = "https://rss.app/feeds/v1.1/_amazon.xml"

posted_links = set()

def add_affiliate(link):
    link = link.split("?")[0]
    return f"{link}?tag={AFFILIATE_TAG}"

def send_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHANNEL_ID,
        "text": msg,
        "disable_web_page_preview": True
    }

    requests.post(url, data=data)

print("Amazon Auto Bot Running...")

while True:

    try:

        feed = feedparser.parse(RSS_URL)

        for item in feed.entries:

            link = item.link

            if link in posted_links:
                continue

            posted_links.add(link)

            aff_link = add_affiliate(link)

            msg = f"""🔥 Amazon Deal

🛒 Buy Now
{aff_link}
"""

            send_message(msg)

            time.sleep(20)

    except Exception as e:
        print("Error:", e)

    time.sleep(600)
