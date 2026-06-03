import asyncio
import random
import feedparser
import requests
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Bot
import threading

# 🔹 CONFIG
TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = "@financebotai0"

bot = Bot(token=TOKEN)

# -------------------------
# CONTENT SYSTEM
# -------------------------

RSS_FEEDS = [
    "https://feeds.feedburner.com/entrepreneur/latest",
    "https://www.forbes.com/business/feed/"
]

posted_links = set()

# 💬 Quote
def get_quote():
    try:
        res = requests.get("https://api.quotable.io/random")
        data = res.json()
        return f"💡 {data['content']}\n\n— {data['author']}"
    except:
        return "Stay focused. Work hard 💪"

# 🖼️ Image পোস্ট
image_posts = [
    {
        "image": "https://i.imgur.com/3GvwNBf.jpg",
        "caption": "💰 Discipline builds wealth\n\n🔥 Join: https://t.me/financebotai0"
    },
    {
        "image": "https://i.imgur.com/ZV6vM9P.jpg",
        "caption": "🚨 Stop wasting money!\n\n📈 Start investing today!"
    }
]

# -------------------------
# POST FUNCTIONS
# -------------------------

async def post_rss():
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:
            if entry.link not in posted_links:
                msg = f"📰 {entry.title}\n\nRead: {entry.link}"
                await bot.send_message(chat_id=CHANNEL_ID, text=msg)
                posted_links.add(entry.link)
                return

async def post_quote():
    await bot.send_message(chat_id=CHANNEL_ID, text=get_quote())

async def post_image():
    post = random.choice(image_posts)
    await bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=post["image"],
        caption=post["caption"]
    )

# -------------------------
# AUTO LOOP (FIXED)
# -------------------------

async def auto_post():
    print("Bot started 🔥")
    while True:
        try:
            print("Running loop...")

            # 🔥 TEST POST (first time confirm)
            await bot.send_message(chat_id=CHANNEL_ID, text="TEST POST ✅")

            choice = random.choice(["rss", "quote", "image"])

            if choice == "rss":
                await post_rss()
            elif choice == "quote":
                await post_quote()
            else:
                await post_image()

            print("Posted successfully ✅")

            await asyncio.sleep(60)  # 🔥 TEST MODE (1 min)

        except Exception as e:
            print("Error:", e)
            await asyncio.sleep(30)

# -------------------------
# HTTP SERVER (Render fix)
# -------------------------

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_server():
    server = HTTPServer(("0.0.0.0", 10000), Handler)
    server.serve_forever()

# -------------------------
# MAIN RUN (FIXED)
# -------------------------

# 🔥 server background-এ run
threading.Thread(target=run_server).start()

# 🔥 bot main thread-এ run
asyncio.run(auto_post())
