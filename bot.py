import re
import requests
from telethon import TelegramClient, events
from bs4 import BeautifulSoup

# ===== TELEGRAM API =====

API_ID = 32958597
API_HASH = "a9abd4656d711a2d295168bcb539ebf9"
SESSION_NAME = "1BVtsOIgBuw0tMgFampSRLXt8FbREcLX30z9aWlgIDgqM_2i-IQFdIIYWKuJvUnGNVV4SA_PW-4LIz6d9s7AydpL3a4kBae5FRaybwFwrrOym3w-SSWkgjrEUlNVa3PrPmVk2vQ_302sKdMc58D98p3Damn55e5Spy7fY2ZVyhWBrioNhvPylc9DlEgPuMeCqUvsetdv4IeNawY-GVAWZFkq6yTVM0WJtPVHipiUeuO27E0aU4h-68CWhGFqulQJXOd2_B_-QEpNC3NkGz6hklEsSALrMK1qklfMdTCTrobMTD2kNZvaXfuA3CNm6SFVLC35OimYkdvxgrWYCTmF5BoQgP_QcxrA="

# ===== CHANNEL SETTINGS =====

TARGET_CHANNEL = -1001234567890

SOURCE_CHANNELS = [
-1002165035485,
-1001805243449,
-1001659536566,
-1001101071323,
-1001927196795,
-1001314450075,
-1001979985045
]

# ===== AMAZON AFFILIATE =====

AFFILIATE_TAG = "partha07e-21"

posted_links = set()

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


# ===== AMAZON LINK EXTRACT =====

def extract_amazon_link(text):

    urls = re.findall(r'(https?://\S+)', text)

    for url in urls:

        if "amazon.in" in url or "amzn.to" in url or "amznn.cc" in url:

            try:
                r = requests.get(url, allow_redirects=True, timeout=10)
                final = r.url
                return final
            except:
                return url

    return None


# ===== ADD AFFILIATE TAG =====

def convert_affiliate(url):

    if "tag=" in url:
        return url

    if "?" in url:
        return url + "&tag=" + AFFILIATE_TAG
    else:
        return url + "?tag=" + AFFILIATE_TAG


# ===== AMAZON SCRAPER =====

def get_amazon_data(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        r = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.find(id="productTitle")
        if title:
            title = title.get_text().strip()
        else:
            title = "Amazon Product"

        price = soup.find("span", {"class": "a-offscreen"})
        if price:
            price = price.get_text()
        else:
            price = "Check on Amazon"

        discount = soup.find("span", {"class": "savingsPercentage"})
        if discount:
            discount = discount.get_text()
        else:
            discount = "Check on Amazon"

        image = soup.find(id="landingImage")

        if image:
            image = image.get("src")
        else:
            image = None

        return title, price, discount, image

    except:

        return "Amazon Product", "Check on Amazon", "Check on Amazon", None


# ===== TELEGRAM EVENT =====

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):

    text = event.raw_text

    url = extract_amazon_link(text)

    if not url:
        return

    if url in posted_links:
        return

    posted_links.add(url)

    url = convert_affiliate(url)

    title, price, discount, image = get_amazon_data(url)

    message = f"""
🔥 Amazon Deal

{title}

💰 Price: {price}

🏷 Discount: {discount}

🛒 Buy Now
{url}
"""

    if image:

        await client.send_file(
            TARGET_CHANNEL,
            image,
            caption=message,
            link_preview=False
        )

    else:

        await client.send_message(
            TARGET_CHANNEL,
            message,
            link_preview=False
        )


print("BOT RUNNING...")

client.start()

client.run_until_disconnected()
