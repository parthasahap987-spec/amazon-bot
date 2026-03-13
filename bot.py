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


def save(link):
    with open(POSTED_FILE, "a") as f:
        f.write(link + "\n")


def add_tag(link):
    link = link.split("?")[0]
    return f"{link}?tag={AFFILIATE_TAG}"


def get_image(link):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        r = requests.get(link, headers=headers)

        html = r.text

        img = re.search(r'https://m\.media-amazon\.com/images/I/[^\"]+', html)

        if img:
            return img.group()

    except:
        pass

    return None


def send_photo(photo, caption):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    data = {
        "chat_id": CHANNEL_ID,
        "photo": photo,
        "caption": caption
    }

    requests.post(url, data=data)


print("Amazon Image Bot Running...")

while True:

    try:

        for channel in SOURCE_CHANNELS:

            html = requests.get(f"https://t.me/s/{channel}").text

            links = re.findall(r'https://www\.amazon\.in/[^\s"]+', html)

            for link in links:

                if link in posted:
                    continue

                posted.add(link)
                save(link)

                affiliate = add_tag(link)

                image = get_image(link)

                caption = f"""🔥 Amazon Deal

🛒 Buy Now
{affiliate}
"""

                if image:
                    send_photo(image, caption)
                else:

                    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

                    data = {
                        "chat_id": CHANNEL_ID,
                        "text": caption,
                        "disable_web_page_preview": True
                    }

                    requests.post(url, data=data)

                time.sleep(10)

    except Exception as e:
        print(e)

    time.sleep(30)
