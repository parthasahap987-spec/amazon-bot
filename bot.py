import requests
import re
import time
from bs4 import BeautifulSoup

SOURCE_CHANNELS = [
    "idoffers",
    "flipshope",
    "eagledealsoffical",
    "bestdealsdaily099"
]

last_ids = {}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Cache-Control": "no-cache"
}

print("BOT RUNNING...")

while True:

    for ch in SOURCE_CHANNELS:

        try:

            url = f"https://t.me/s/{ch}?embed=1&mode=tme"

            r = requests.get(url, headers=headers, timeout=15)

            soup = BeautifulSoup(r.text, "html.parser")

            posts = soup.find_all("div", {"class": "tgme_widget_message"})

            if not posts:
                continue

            latest = posts[0]

            post_id = latest.get("data-post")

            if last_ids.get(ch) == post_id:
                continue

            last_ids[ch] = post_id

            text = latest.get_text(" ", strip=True)

            links = re.findall(r'https?://\S+', text)

            for link in links:

                if "amazon" in link or "amzn" in link:

                    print("NEW AMAZON LINK:", link)

        except Exception as e:
            print("ERROR:", e)

    time.sleep(5)
