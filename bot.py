import requests
import re
import time

BOT_TOKEN = "8799971120:AAFzhADyO1e8A7UH5H80xOkrgCvSb3RBYjM"
CHANNEL_ID = "-1002161382456"
AFFILIATE_TAG = "partha07e-21"

SOURCE_CHANNELS = [
    "idoffers",
    "flipshope",
    "eagledealsoffical"
]

last_ids = {}

def expand(url):
    try:
        r = requests.head(url, allow_redirects=True, timeout=10)
        return r.url
    except:
        return url


def scrape_amazon(link):

    headers = {"User-Agent":"Mozilla/5.0"}

    try:

        r = requests.get(link, headers=headers, timeout=10)

        html = r.text

        price = "N/A"
        discount = "N/A"
        image = None

        p = re.search(r'a-price-whole">([\d,]+)', html)
        if p:
            price = "₹" + p.group(1)

        d = re.search(r'-(\d+)%', html)
        if d:
            discount = "-" + d.group(1) + "%"

        img = re.search(r'property="og:image"\s*content="([^"]+)', html)
        if img:
            image = img.group(1)

        return image, price, discount

    except:
        return None, "N/A", "N/A"


def send(photo, caption):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    data = {
        "chat_id": CHANNEL_ID,
        "photo": photo,
        "caption": caption
    }

    requests.post(url, data=data)


print("BOT STARTED")

while True:

    for channel in SOURCE_CHANNELS:

        try:

            html = requests.get(f"https://t.me/s/{channel}").text

            posts = re.findall(r'data-post="([^"]+)"', html)

            if not posts:
                continue

            latest = posts[0]

            if channel in last_ids and last_ids[channel] == latest:
                continue

            last_ids[channel] = latest

            links = re.findall(r'https://[^\s"]+', html)

            for link in links:

                if "amzn." in link:
                    link = expand(link)

                if "amazon.in" not in link:
                    continue

                clean = link.split("?")[0]

                image, price, discount = scrape_amazon(clean)

                aff = f"{clean}?tag={AFFILIATE_TAG}"

                caption = f"""🔥 Amazon Deal

💰 Price: {price}
📉 Discount: {discount}

🛒 Buy Now
{aff}
"""

                if image:
                    send(image, caption)

                break

        except Exception as e:
            print("error:", e)

    time.sleep(20)
