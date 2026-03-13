import re
import requests
import time

BOT_TOKEN = "8799971120:AAFzhADyO1e8A7UH5H80xOkrgCvSb3RBYjM"
CHANNEL_ID = "-1002161382456"
AFFILIATE_TAG = "partha07e-21"

SOURCE_CHANNELS = [
    "idoffers",
    "flipshope",
    "eagledealsoffical"
]

posted_links = set()

def expand_short(url):
    try:
        r = requests.head(url, allow_redirects=True, timeout=10)
        return r.url
    except:
        return url


def extract_links(html):

    links = re.findall(r'https://[^\s"]+', html)

    return links


def scrape_amazon(link):

    headers = {"User-Agent": "Mozilla/5.0"}

    try:

        r = requests.get(link, headers=headers, timeout=10)
        html = r.text

        price = "N/A"
        discount = "N/A"
        image = None

        # price
        p = re.search(r'class="a-price-whole">([\d,]+)', html)
        if p:
            price = "₹" + p.group(1)

        # discount
        d = re.search(r'-(\d+)%', html)
        if d:
            discount = "-" + d.group(1) + "%"

        # image
        img = re.search(r'property="og:image"\s*content="([^"]+)', html)
        if img:
            image = img.group(1)

        return image, price, discount

    except:
        return None, "N/A", "N/A"


def affiliate(link):

    base = link.split("?")[0]

    return f"{base}?tag={AFFILIATE_TAG}"


def send_photo(photo, caption):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    data = {
        "chat_id": CHANNEL_ID,
        "photo": photo,
        "caption": caption
    }

    requests.post(url, data=data)


print("BOT STARTED...")

while True:

    for channel in SOURCE_CHANNELS:

        try:

            url = f"https://t.me/s/{channel}"

            html = requests.get(url).text

            links = extract_links(html)

            for link in links:

                if "amzn." in link:
                    link = expand_short(link)

                if "amazon.in" not in link:
                    continue

                clean = link.split("?")[0]

                if clean in posted_links:
                    continue

                posted_links.add(clean)

                img, price, discount = scrape_amazon(clean)

                aff = affiliate(clean)

                caption = f"""🔥 Amazon Deal

💰 Price: {price}
📉 Discount: {discount}

🛒 Buy Now
{aff}
"""

                if img:
                    send_photo(img, caption)

                time.sleep(4)

        except Exception as e:
            print("Error:", e)

    time.sleep(20)
