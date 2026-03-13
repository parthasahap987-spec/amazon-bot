import re
import requests
import time

BOT_TOKEN = "8799971120:AAEVSONtxInLeFj82UXIy93hU0kG1w7Pgiw"
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

posted_links = set()


def expand_short_link(link):

    try:
        r = requests.head(link, allow_redirects=True, timeout=10)
        return r.url
    except:
        return link


def extract_amazon_link(text):

    links = re.findall(r'https?://\S+', text)

    for link in links:

        if "amzn.to" in link:
            link = expand_short_link(link)

        if "amazon." in link:
            return link

    return None


def add_affiliate(link):

    clean = link.split("?")[0]

    return f"{clean}?tag={AFFILIATE_TAG}"


def get_product_image(link):

    headers = {"User-Agent": "Mozilla/5.0"}

    try:

        r = requests.get(link, headers=headers, timeout=10)

        html = r.text

        img = re.search(r'"large":"(https://m\.media-amazon\.com/images/I/[^"]+)', html)

        if img:
            return img.group(1)

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


print("Amazon Affiliate Bot Running...")

while True:

    try:

        for channel in SOURCE_CHANNELS:

            html = requests.get(f"https://t.me/s/{channel}").text

            messages = html.split("tgme_widget_message_text")

            for block in messages:

                link = extract_amazon_link(block)

                if not link:
                    continue

                clean = link.split("?")[0]

                if clean in posted_links:
                    continue

                posted_links.add(clean)

                affiliate = add_affiliate(clean)

                image = get_product_image(clean)

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

    time.sleep(120)
