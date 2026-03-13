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

posted = set()

if os.path.exists(POSTED_FILE):
    with open(POSTED_FILE) as f:
        posted = set(f.read().splitlines())


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


def scrape_amazon(link):

    headers = {"User-Agent": "Mozilla/5.0"}

    try:

        r = requests.get(link, headers=headers, timeout=10)

        html = r.text

        image = None
        price = "N/A"
        discount = ""

        # image
        img = re.search(r'"large":"(https://m\.media-amazon\.com/images/I/[^"]+)', html)
        if img:
            image = img.group(1)

        # discounted price
        price_match = re.search(r'class="a-price-whole">([\d,]+)', html)
        if price_match:
            price = "₹" + price_match.group(1)

        # discount
        discount_match = re.search(r'\((\d+)%\s*off\)', html.lower())
        if discount_match:
            discount = discount_match.group(1) + "% OFF"

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


def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "disable_web_page_preview": True
    }

    requests.post(url, data=data)


print("Amazon Affiliate Bot Running...")

while True:

    try:

        for channel in SOURCE_CHANNELS:

            html = requests.get(f"https://t.me/s/{channel}").text

            # latest posts only
            blocks = html.split("tgme_widget_message_text")[:5]

            for block in blocks:

                link = extract_amazon_link(block)

                if not link:
                    continue

                clean = link.split("?")[0]

                if clean in posted:
                    continue

                posted.add(clean)
                save_link(clean)

                image, price, discount = scrape_amazon(clean)

                affiliate = add_affiliate(clean)

                caption = f"""🔥 Amazon Deal

💰 Price: {price}
🔥 Discount: {discount}

🛒 Buy Now
{affiliate}
"""

                if image:
                    send_photo(image, caption)
                else:
                    send_message(caption)

                time.sleep(5)

    except Exception as e:
        print(e)

    time.sleep(20)
