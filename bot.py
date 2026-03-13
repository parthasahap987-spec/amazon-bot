import time
from telegram import Bot

BOT_TOKEN = "8799971120:AAHlHlFBghuS73mBBaUI27PA1Ih45f1NhCw"
CHANNEL_ID = -1002161382456

bot = Bot(token=BOT_TOKEN)

while True:
    bot.send_message(CHANNEL_ID, "✅ Bot working!")
    time.sleep(60)
