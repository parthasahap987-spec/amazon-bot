from telethon import TelegramClient, events
import re

api_id = 32958597
api_hash = "a9abd4656d711a2d295168bcb539ebf9"

TARGET_CHANNEL = -1002161382456
AFF_TAG = "partha07e-21"

SOURCE_CHANNELS = [
    "idoffers",
    "flipshope",
    "eagledealsoffical",
    "bestdealsdaily099"
]

client = TelegramClient("session", api_id, api_hash)

posted=set()

def convert(link):

    clean = link.split("?")[0]

    return f"{clean}?tag={AFF_TAG}"


@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):

    text = event.raw_text

    links = re.findall(r'https://\S+', text)

    for link in links:

        if "amazon" in link or "amzn" in link:

            clean = link.split("?")[0]

            if clean in posted:
                return

            posted.add(clean)

            aff = convert(clean)

            msg=f"""🔥 Amazon Deal

🛒 Buy Now
{aff}
"""

            await client.send_message(TARGET_CHANNEL,msg)

            print("POSTED:",aff)


client.start()

print("BOT RUNNING...")

client.run_until_disconnected()
