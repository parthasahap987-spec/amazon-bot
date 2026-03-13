import re
import requests
import time

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

posted_links = set()


def add_tag(link):
    link = link.split("?")[0]
    return f"{link}?tag={AFFILIATE_TAG}"


def get_product_image(link):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(link, headers=headers, timeout=10)
        html = r.text

        img = re.search(r'https://m\.media-amazon\.com/images/I/[^\"]+', html)

        if img:
            return img.group()

    except:
        pass

    return None


def send_photo(image, caption):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    data = {
        "chat_id": CHANNEL_ID,
        "photo": image,
        "caption": caption
    }

    requests.post(url, data=data)


print("Amazon Image Bot Running...")

while True:

    try:

        for channel in SOURCE_CHANNELS:

            url = f"https://t.me/s/{channel}"

            html = requests.get(url).text

            links = re.findall(r'https://www\.amazon\.in/[^\s"]+', html)

            for link in links:

                clean_link = link.split("?")[0]

                if clean_link in posted_links:
                    continue

                posted_links.add(clean_link)

                affiliate = add_tag(clean_link)

                image = get_product_image(clean_link)

                caption = f"""🔥 Amazon Deal

🛒 Buy Now
{affiliate}
"""

                if image:
                    send_photo(image, caption)

                time.sleep(15)

    except Exception as e:
        print(e)

    time.sleep(300)
