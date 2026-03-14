import re
import requests
from telethon import TelegramClient, events
from bs4 import BeautifulSoup

API_ID = 32958597
API_HASH = "a9abd4656d711a2d295168bcb539ebf9"

SESSION_NAME = "session"

TARGET_CHANNEL = -1002161382456

SOURCE_CHANNELS = [
    "idoffers",
    "flipshope",
    "eagledealsoffical",
    "bestdealsdaily099"
    "freekart"
]

AFFILIATE_TAG = "partha07e-21"

posted = set()

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


# -------- SHORT LINK EXPAND --------

def expand_link(url):

    try:
        r = requests.get(url, timeout=10, allow_redirects=True)
        return r.url
    except:
        return url


# -------- ADD AFFILIATE TAG --------

def add_tag(url):

    clean = url.split("?")[0]

    return f"{clean}?tag={AFFILIATE_TAG}"


# -------- AMAZON SCRAPER --------

def scrape_amazon(url):

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    r = requests.get(url, headers=headers, timeout=10)

    soup = BeautifulSoup(r.text, "html.parser")

    price = "N/A"
    discount = "N/A"
    image = None

    # PRICE

    p = soup.select_one(".a-price .a-offscreen")

    if p:
        price = p.text.replace("₹","").strip()

    # DISCOUNT

    d = soup.select_one(".savingsPercentage")

    if d:
        discount = d.text.strip()

    # IMAGE

    img = soup.select_one("#landingImage")

    if img:
        image = img.get("src")

    # FALLBACK IMAGE (JSON)

    if not image:

        m = re.search(r'"large":"(https://m\.media-amazon\.com/images/I/[^"]+)', r.text)

        if m:
            image = m.group(1)

    return price, discount, image


# -------- MESSAGE LISTENER --------

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):

    text = event.raw_text

    links = re.findall(r'https?://[^\s]+', text)

    for link in links:

        if "amazon" not in link and "amzn.in" not in link:
            continue

        # expand short link

        if "amzn.in" in link:
            link = expand_link(link)

        clean = link.split("?")[0]

        if clean in posted:
            return

        posted.add(clean)

        aff = add_tag(link)

        price, discount, image = scrape_amazon(link)

        caption = f"""🔥 Amazon Deal

💰 Price: ₹{price}
🏷 Discount: {discount}

🛒 Buy Now
{aff}
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
