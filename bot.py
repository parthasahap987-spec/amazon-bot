import requests
import re
import time
from bs4 import BeautifulSoup

BOT_TOKEN = "8799971120:AAFzhADyO1e8A7UH5H80xOkrgCvSb3RBYjM"
CHANNEL_ID = "-1002161382456"
AFF_TAG = "partha07e-21"

SOURCE_CHANNELS = [
"idoffers",
"flipshope",
"eagledealsoffical",
"bestdealsdaily099"
]

posted=set()

def send(text):

    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data={
    "chat_id":CHANNEL_ID,
    "text":text,
    "disable_web_page_preview":True
    }

    requests.post(url,data=data)


print("BOT RUNNING")

while True:

    for ch in SOURCE_CHANNELS:

        try:

            html=requests.get(f"https://t.me/s/{ch}").text

            links=re.findall(r'https://www\.amazon\.in/(?:dp|gp/product)/[A-Z0-9]+',html)

            for link in links:

                if link in posted:
                    continue

                posted.add(link)

                aff=f"{link}?tag={AFF_TAG}"

                msg=f"""🔥 Amazon Deal

🛒 Buy Now
{aff}
"""

                send(msg)

                print("POSTED:",aff)

                time.sleep(5)

        except Exception as e:
            print(e)

    time.sleep(15)
