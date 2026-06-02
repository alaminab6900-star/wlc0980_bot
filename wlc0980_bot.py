import asyncio
import random
import feedparser
import requests
import os
from telegram import Bot

TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = "@financebotai0"

bot = Bot(token=TOKEN)

# 🔹 RSS FEEDS (change/add more)
RSS_FEEDS = [
    "https://feeds.feedburner.com/entrepreneur/latest",
    "https://www.forbes.com/business/feed/"
]

posted_links = set()

# 🔹 Quotes API
def get_quote():
    try:
        res = requests.get("https://api.quotable.io/random")
        data = res.json()
        return f"💡 {data['content']}\n\n— {data['author']}"
    except:
        return "Stay focused. Work hard. 💪"

# 🔹 RSS পোস্ট
async def post_rss():
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:
            if entry.link not in posted_links:
                msg = f"📰 {entry.title}\n\nRead more: {entry.link}"
                await bot.send_message(chat_id=CHANNEL_ID, text=msg)
                posted_links.add(entry.link)
                return

# 🔹 Quote পোস্ট
async def post_quote():
    quote = get_quote()
    await bot.send_message(chat_id=CHANNEL_ID, text=quote)

# 🔹 Main loop
async def auto_post():
    while True:
        try:
            choice = random.choice(["rss", "quote"])

            if choice == "rss":
                await post_rss()
            else:
                await post_quote()

            await asyncio.sleep(1800)  # 30 min

        except Exception as e:
            print("Error:", e)
            await asyncio.sleep(60)

# 🔹 Run bot
asyncio.run(auto_post())
