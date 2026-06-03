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
CHANNELS = ["@financebotai0", "@earnex_bdt"]

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

# 🖼️ Image posts (FIXED SOURCE ✅)
image_posts = [
    {
        "image": "https://picsum.photos/800/600",
        "caption": "💰 Discipline builds wealth\n\n📈 Follow: https://t.me/financebotai0"
    },
    {
        "image": "https://images.unsplash.com/photo-1518546305927-5a555bb7020d",
        "caption": "🚀 Start investing today!\n\n🔥 Grow your money smartly"
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
                msg = f"📰 {entry.title}\n\nRead more: {entry.link}"
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
# AUTO LOOP
# -------------------------

async def auto_post():
    print("Bot started 🔥")

    while True:
        try:
            choice = random.choice(["rss", "quote", "image"])

            if choice == "rss":
                await post_rss()
            elif choice == "quote":
                await post_quote()
            else:
                await post_image()

            print("Posted successfully ✅")

            await asyncio.sleep(1800)  # ⏱️ 30 minutes

        except Exception as e:
            print("Error:", e)
            await asyncio.sleep(60)

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
# MAIN RUN
# -------------------------

# 🔥 server background-এ
threading.Thread(target=run_server).start()

# 🔥 bot main-এ
asyncio.run(auto_post())
