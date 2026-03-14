import re
import requests
from telethon import TelegramClient, events
from bs4 import BeautifulSoup

API_ID = 32958597
API_HASH = "a9abd4656d711a2d295168bcb539ebf9"

SESSION_NAME = "session"

TARGET_CHANNEL = -1002161382456

SOURCE_CHANNELS = [
    -1002165035485,
    -1001805243449,
    -1001659536566,
    -1001101071323,
    -1001927196795,
    -1001314450075,
    -1001979985045
]

AFFILIATE_TAG = "partha07e-21"

posted_links = set()

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


# -------- SHORT LINK EXPAND --------

def expand_link(url):

    try:
        r = requests.get(
            url,
            allow_redirects=True,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
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
        "Accept-Language": "en-IN,en;q=0.9"
    }

    r = requests.get(url, headers=headers, timeout=10)

    html = r.text

    soup = BeautifulSoup(html, "html.parser")

    price = "N/A"
    discount = "N/A"
    image = None

    # PRICE (stable selector)

    p = soup.select_one(".a-price .a-offscreen")

    if p:
        price = p.text.replace("₹", "").strip()

    # DISCOUNT

    d = soup.select_one(".savingsPercentage")

    if d:
        discount = d.text.strip()

    # IMAGE

    img = soup.select_one("#landingImage")

    if img:
        image = img.get("src")

    # IMAGE fallback

    if not image:

        m = re.search(
            r'"large":"(https://m\.media-amazon\.com/images/I/[^"]+)',
            html
        )

        if m:
            image = m.group(1)

    return price, discount, image


# -------- MESSAGE LISTENER --------

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):

    text = event.raw_text

    links = re.findall(r'https?://[^\s]+', text)

    for link in links:

        if "amazon" not in link and "amzn" not in link:
            continue

        # expand short link

        if "amzn" in link:
            link = expand_link(link)

        clean = link.split("?")[0]

        if clean in posted_links:
            continue

        posted_links.add(clean)

        affiliate_link = add_tag(link)

        price, discount, image = scrape_amazon(link)

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
