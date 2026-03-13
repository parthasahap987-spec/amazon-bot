import re
import requests
import time
import os

BOT_TOKEN = "8799971120:AAFzhADyO1e8A7UH5H80xOkrgCvSb3RBYjM"
CHANNEL_ID = "-1002161382456"
AFFILIATE_TAG = "partha07e-21"

SOURCE_CHANNELS = [
    "LootDealsIndia",
    "DealBee",
    "IndianDeals",
    "indiafreestffin",
    "freekart",
    "bestdealsdaily099",
    "idoffers",
    "flipshope",
    "eagledealsoffical"
]

POSTED_FILE = "posted_links.txt"

posted_links = set()

if os.path.exists(POSTED_FILE):
    with open(POSTED_FILE) as f:
        posted_links = set(f.read().splitlines())


def save_link(link):
    with open(POSTED_FILE, "a") as f:
        f.write(link + "\n")


def expand_short(link):

    try:
        r = requests.head(link, allow_redirects=True, timeout=10)
        return r.url
    except:
        return link


def extract_amazon_link(text):

    links = re.findall(r'https?://\S+', text)

    for link in links:

        if "amzn.to" in link:
            link = expand_short(link)

        if "amazon." in link:
            return link

    return None


def add_affiliate(link):

    clean = link.split("?")[0]

    return f"{clean}?tag={AFFILIATE_TAG}"


def get_product_data(link):

    headers = {"User-Agent": "Mozilla/5.0"}

    try:

        r = requests.get(link, headers=headers, timeout=10)

        html = r.text

        image = None
        price = "N/A"
        discount = ""

        img = re.search(r'"large":"(https://m\.media-amazon\.com/images/I/[^"]+)', html)
        if img:
            image = img.group(1)

        price_match = re.search(r'₹\s?[\d,]+', html)
        if price_match:
            price = price_match.group()

        discount_match = re.search(r'\d+%\s?off', html.lower())
        if discount_match:
            discount = discount_match.group()

        return image, price, discount

    except:
        return None, "N/A", ""


def send_photo(photo, caption):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    data = {
        "chat_id": CHANNEL_ID,
        "photo": photo,
        "caption": caption
    }

    requests.post(url, data=data)


print("Amazon Pro Affiliate Bot Running...")

while True:

    try:

        for channel in SOURCE_CHANNELS:

            html = requests.get(f"https://t.me/s/{channel}").text

            blocks = html.split("tgme_widget_message_text")

            for block in blocks:

                link = extract_amazon_link(block)

                if not link:
                    continue

                clean = link.split("?")[0]

                if clean in posted_links:
                    continue

                posted_links.add(clean)
                save_link(clean)

                affiliate = add_affiliate(clean)

                image, price, discount = get_product_data(clean)

                caption = f"""🔥 Amazon Deal

💰 Price: {price}
🔥 Discount: {discount}

🛒 Buy Now
{affiliate}
"""

                if image:
                    send_photo(image, caption)

                time.sleep(5)

    except Exception as e:
        print(e)

    time.sleep(20)
