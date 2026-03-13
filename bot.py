import requests
import feedparser
import time

BOT_TOKEN = "8799971120:AAHjV4JmOvOq9nxpynT0et3rvE04t43ojMw"
CHANNEL_ID = "-1002161382456"
AFFILIATE_TAG = "partha07e-21"

RSS_URL = "https://rss.app/feeds/AmazonDeals.xml"

posted = set()

def add_tag(link):
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

    time.sleep(300)                        "text": caption,
                        "disable_web_page_preview": True
                    }

                    requests.post(url, data=data)

                time.sleep(15)

    except Exception as e:
        print(e)

    time.sleep(10)
