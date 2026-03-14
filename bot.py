import re
import requests
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from bs4 import BeautifulSoup


# ====================================
# A) TELEGRAM LOGIN DETAILS
# ====================================

API_ID = 32958597
API_HASH = "a9abd4656d711a2d295168bcb539ebf9"
SESSION_STRING = "1BVtsOIgBuw0tMgFampSRLXt8FbREcLX30z9aWlgIDgqM_2i-IQFdIIYWKuJvUnGNVV4SA_PW-4LIz6d9s7AydpL3a4kBae5FRaybwFwrrOym3w-SSWkgjrEUlNVa3PrPmVk2vQ_302sKdMc58D98p3Damn55e5Spy7fY2ZVyhWBrioNhvPylc9DlEgPuMeCqUvsetdv4IeNawY-GVAWZFkq6yTVM0WJtPVHipiUeuO27E0aU4h-68CWhGFqulQJXOd2_B_-QEpNC3NkGz6hklEsSALrMK1qklfMdTCTrobMTD2kNZvaXfuA3CNm6SFVLC35OimYkdvxgrWYCTmF5BoQgP_QcxrA="


# ====================================
# TELEGRAM CLIENT START
# ====================================

client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH
)


# ====================================
# B) TARGET CHANNEL
# ====================================

TARGET_CHANNEL = -1002161382456


# ====================================
# C) SOURCE CHANNELS
# ====================================

SOURCE_CHANNELS = [
-1002165035485,
-1001805243449,
-1001659536566,
-1001101071323,
-1001927196795,
-1001314450075,
-1001979985045
]


# ====================================
# AMAZON AFFILIATE TAG
# ====================================

AFFILIATE_TAG = "partha07e-21"

posted_links = set()


# ====================================
# SHORT LINK EXPAND
# ====================================

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


# ====================================
# ADD AFFILIATE TAG
# ====================================

def add_tag(url):

    clean = url.split("?")[0]

    return f"{clean}?tag={AFFILIATE_TAG}"


# ====================================
# AMAZON SCRAPER
# ====================================

def scrape_amazon(url):

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-IN,en;q=0.9"
    }

    r = requests.get(url, headers=headers, timeout=10)

    html = r.text

    soup = BeautifulSoup(html, "html.parser")

    price = None
    discount = None
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


    if not image:

        m = re.search(
            r'"large":"(https://m\.media-amazon\.com/images/I/[^"]+)',
            html
        )

        if m:
            image = m.group(1)


    if not price:
        price = "Check on Amazon"

    if not discount:
        discount = "Deal Available"


    return price, discount, image


# ====================================
# LINK EXTRACTOR
# ====================================

def extract_links(event):

    links = []

    text = event.raw_text

    links += re.findall(r'https?://[^\s]+', text)


    if event.message.entities:

        for e in event.message.entities:

            if hasattr(e, "url"):
                links.append(e.url)


    return links


# ====================================
# TELEGRAM LISTENER
# ====================================

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):

    links = extract_links(event)

    for link in links:

        if "amazon" not in link and "amzn" not in link:
            continue


        if "amzn" in link:
            link = expand_link(link)


        clean = link.split("?")[0]


        if clean in posted_links:
            continue


        posted_links.add(clean)


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
