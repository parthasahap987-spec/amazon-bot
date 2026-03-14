import requests
import re
import time

BOT_TOKEN = "8799971120:AAFzhADyO1e8A7UH5H80xOkrgCvSb3RBYjM"
CHANNEL_ID = "-1002161382456"
AFFILIATE_TAG = "partha07e-21"

SOURCE_CHANNELS = [
    "idoffers",
    "flipshope",
    "eagledealsoffical",
    "indiadealszone"
]

last_post = {}

def expand(link):
    try:
        r = requests.head(link, allow_redirects=True, timeout=10)
        return r.url
    except:
        return link


def scrape_amazon(url):

    headers = {"User-Agent":"Mozilla/5.0"}

    try:

        r = requests.get(url, headers=headers, timeout=10)

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


def send_photo(img, caption):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    data = {
        "chat_id": CHANNEL_ID,
        "photo": img,
        "caption": caption
    }

    requests.post(url, data=data)


print("BOT RUNNING")

while True:

    for ch in SOURCE_CHANNELS:

        try:

            page = requests.get(f"https://t.me/s/{ch}").text

            posts = re.findall(r'data-post="([^"]+)"', page)

            if not posts:
                continue

            latest = posts[0]

            if last_post.get(ch) == latest:
                continue

            last_post[ch] = latest

            links = re.findall(r'https://[^\s"]+', page)

            for link in links:

                # detect amazon short link
                if "amzn." in link or "amazon.in" in link:

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
                        send_photo(image, caption)

                    break

        except Exception as e:
            print(e)

    time.sleep(20)
