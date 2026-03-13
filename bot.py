import requests
import re
import feedparser
from telegram import Bot

BOT_TOKEN = "8799971120:AAHlHlFBghuS73mBBaUI27PA1Ih45f1NhCw"
CHANNEL_ID = -1002161382456
AFFILIATE_TAG = "partha07e-21"

bot = Bot(token=BOT_TOKEN)

posted = set()

def get_amazon_link(text):
    links = re.findall(r'https?://\S+', text)
    for link in links:
        if "amazon." in link or "amzn.to" in link:
            return link
    return None

def add_tag(link):
    link = link.split("?")[0]
    return f"{link}?tag={AFFILIATE_TAG}"

def get_deals():

    feeds = [
        "https://rss.app/feeds/AmazonDeals.xml"
    ]

    deals = []

    for url in feeds:
        feed = feedparser.parse(url)

        for entry in feed.entries:
            deals.append(entry)

    return deals


while True:

    deals = get_deals()

    for deal in deals:

        title = deal.title
        link = deal.link

        if link in posted:
            continue

        posted.add(link)

        affiliate = add_tag(link)

        text = f"""
🔥 Amazon Deal

{title}

🛒 Buy Now
{affiliate}
"""

        bot.send_message(CHANNEL_ID, text, disable_web_page_preview=True)

    import time
    time.sleep(600)
