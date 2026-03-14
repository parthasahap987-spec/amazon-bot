import re
import requests
from telethon import TelegramClient, events
from bs4 import BeautifulSoup

# ===== TELEGRAM API =====

API_ID = 32958597
API_HASH = "a9abd4656d711a2d295168bcb539ebf9"

SESSION_NAME = "session"

# ===== CHANNEL SETTINGS =====

TARGET_CHANNEL = -1002161382456

SOURCE_CHANNELS = [
    "idoffers",
    "flipshope",
    "eagledealsoffical",
    "bestdealsdaily099"
]

# ===== AMAZON AFFILIATE =====

AFFILIATE_TAG = "partha07e-21"

posted_links = set()

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


# ===== SHORT LINK EXPAND =====

def expand_link(link):

    try:
        r = requests.get(link, timeout=10)
        return r.url
    except:
        return link


# ===== ADD AFFILIATE TAG =====

def add_affiliate(link):

    link = link.split("?")[0]

    return f"{link}?tag={AFFILIATE_TAG}"


# ===== AMAZON SCRAPER =====

def scrape_amazon(link):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(link, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    price = "N/A"
    discount = "N/A"
    image = None

    price_tag = soup.select_one(".a-price-whole")

    if price_tag:
        price = price_tag.text.strip()

    discount_tag = soup.select_one(".savingsPercentage")

    if discount_tag:
        discount = discount_tag.text.strip()

    img = soup.find("img", {"id": "landingImage"})

    if img:
        image = img.get("src")

    return price, discount, image


# ===== NEW MESSAGE LISTENER =====

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):

    text = event.raw_text

    links = re.findall(r'https?://[^\s]+', text)

    for link in links:

        if "amazon" not in link and "amzn.in" not in link:
            continue

        if "amzn.in" in link:
            link = expand_link(link)

        clean = link.split("?")[0]

        if clean in posted_links:
            return

        posted_links.add(clean)

        affiliate_link = add_affiliate(link)

        price, discount, image = scrape_amazon(affiliate_link)

        caption = f"""🔥 Amazon Deal

💰 Price: ₹{price}
🏷 Discount: {discount}

🛒 Buy Now
{affiliate_link}
"""

        try:

            if image:

                await client.send_file(
                    TARGET_CHANNEL,
                    image,
                    caption=caption,
                    link_preview=False
                )

            else:

                await client.send_message(
                    TARGET_CHANNEL,
                    caption,
                    link_preview=False
                )

        except Exception as e:

            print(e)


print("BOT RUNNING...")

client.start()

client.run_until_disconnected()
