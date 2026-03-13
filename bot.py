import re
import requests
import time

BOT_TOKEN = "8799971120:AAHlHlFBghuS73mBBaUI27PA1Ih45f1NhCw"
CHANNEL_ID = "-1002161382456"
AFFILIATE_TAG = "partha07e-21"

def get_amazon_link(text):
    links = re.findall(r'https?://\S+', text)
    for link in links:
        if "amazon." in link or "amzn.to" in link:
            return link
    return None

def add_tag(link):
    link = link.split("?")[0]
    return f"{link}?tag={AFFILIATE_TAG}"

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": msg,
        "disable_web_page_preview": True
    }
    requests.post(url, data=data)

print("Amazon bot started")

while True:

    link = "https://www.amazon.in/dp/B0CXXXXXXX"

    affiliate = add_tag(link)

    text = f"""
🔥 Amazon Deal

🛒 Buy Now
{affiliate}
"""

    send(text)

    time.sleep(3600)
