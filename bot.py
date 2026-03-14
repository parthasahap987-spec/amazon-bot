import requests
import re
import time
from bs4 import BeautifulSoup

BOT_TOKEN = "8799971120:AAFzhADyO1e8A7UH5H80xOkrgCvSb3RBYjM"
TARGET_CHANNEL = "-1002161382456"
AFF_TAG = "partha07e-21"

SOURCE_CHANNELS = [
    "idoffers",
    "flipshope",
    "eagledealsoffical",
    "bestonlinedeals"
]

posted=set()

def expand(url):
    try:
        r=requests.head(url,allow_redirects=True,timeout=10)
        return r.url
    except:
        return url

def scrape_amazon(url):

    headers={"User-Agent":"Mozilla/5.0"}

    try:
        r=requests.get(url,headers=headers,timeout=15)
        soup=BeautifulSoup(r.text,"html.parser")

        price="N/A"
        discount="N/A"
        image=None

        price_tag=soup.select_one(".a-price-whole")
        if price_tag:
            price="₹"+price_tag.text.strip()

        discount_tag=soup.select_one(".savingsPercentage")
        if discount_tag:
            discount=discount_tag.text.strip()

        img=soup.find("meta",property="og:image")
        if img:
            image=img["content"]

        return image,price,discount

    except:
        return None,"N/A","N/A"

def send_photo(img,caption):

    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    data={
        "chat_id":TARGET_CHANNEL,
        "photo":img,
        "caption":caption
    }

    requests.post(url,data=data)

print("Bot Running...")

while True:

    for channel in SOURCE_CHANNELS:

        try:

            url=f"https://t.me/s/{channel}?embed=1&mode=tme"

            html=requests.get(url,timeout=15).text

            links=re.findall(r'https?://[^\s"<]+',html)

            for link in links:

                if "amzn." in link:
                    link=expand(link)

                if "amazon.in" not in link:
                    continue

                clean=link.split("?")[0]

                if clean in posted:
                    continue

                posted.add(clean)

                image,price,discount=scrape_amazon(clean)

                aff=f"{clean}?tag={AFF_TAG}"

                caption=f"""🔥 Amazon Deal

💰 Price: {price}
📉 Discount: {discount}

🛒 Buy Now
{aff}
"""

                if image:
                    send_photo(image,caption)

                time.sleep(4)

        except Exception as e:
            print(e)

    time.sleep(8)
