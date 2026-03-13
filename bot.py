import re
import requests
import time
import os

BOT_TOKEN = "8799971120:AAFzhADyO1e8A7UH5H80xOkrgCvSb3RBYjM"
CHANNEL_ID = "-1002161382456"
AFFILIATE_TAG = "partha07e-21"

SOURCE_CHANNELS = [
    "idoffers",
    "flipshope",
    "eagledealsoffical",
    "LootDealsIndia",
    "DealBee",
    "IndianDeals"
]

POSTED_FILE = "posted.txt"

posted = set()

if os.path.exists(POSTED_FILE):
    with open(POSTED_FILE) as f:
        posted = set(f.read().splitlines())


def save_post(link):
    with open(POSTED_FILE, "a") as f:
        f.write(link + "\n")


def expand_short(url):
    try:
        r = requests.head(url, allow_redirects=True, timeout=10)
        return r.url
    except:
        return url


def extract_amazon_link(text):

    links = re.findall(r'https?://\S+', text)

    for link in links:

        if "amzn.to" in link:
            link = expand_short(link)

        if "amazon.in" in link:
            return link

    return None


def add_affiliate(link):

    base = link.split("?")[0]

    return f"{base}?tag={AFFILIATE_TAG}"


def scrape_amazon(link):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        r = requests.get(link, headers=headers, timeout=10)

        html = r.text

        image = None
        price = "N/A"
        discount = "N/A"

        # image
        img = re.search(r'"large":"(https://m\.media-amazon\.com/images/I/[^"]+)', html)
        if img:
            image = img.group(1)

        # price
        price_match = re.search(r'a-price-whole">([\d,]+)', html)
        if price_match:
            price = "₹" + price_match.group(1)

        # discount
        disc_match = re.search(r'-(\d+)%', html)
        if disc_match:
            discount = "-" + disc_match.group(1) + "%"

        return image, price, discount

    except:
        return None, "N/A", "N/A"


def send_photo(img, caption):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    data = {
        "chat_id": CHANNEL_ID,
        "photo": img,
        "caption": caption
    }

    requests.post(url, data=data)


print("Affiliate bot running...")

while True:

    try:

        for ch in SOURCE_CHANNELS:

            html = requests.get(f"https://t.me/s/{ch}").text

            blocks = html.split("tgme_widget_message_text")[:6]

            for block in blocks:

                link = extract_amazon_link(block)

                if not link:
                    continue

                clean = link.split("?")[0]

                if clean in posted:
                    continue

                posted.add(clean)
                save_post(clean)

                img, price, discount = scrape_amazon(clean)

                aff = add_affiliate(clean)

                caption = f"""🔥 Amazon Deal

💰 Price: {price}
📉 Discount: {discount}

🛒 Buy Now
{aff}
"""

                if img:
                    send_photo(img, caption)

                time.sleep(6)

    except Exception as e:
        print(e)

    time.sleep(20)
