import asyncio
import random
import feedparser
import requests
import os
import sqlite3
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Bot
import threading

# -------------------------
# LOGGING (PRO)
# -------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# -------------------------
# CONFIG
# -------------------------
TOKEN = os.environ.get("TOKEN")
CHANNELS = ["@financebotai0", "@earnex_bdt"]

bot = Bot(token=TOKEN)

# -------------------------
# DATABASE (IMPORTANT 🔥)
# -------------------------
conn = sqlite3.connect("bot.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS posted_links (
    link TEXT PRIMARY KEY
)
""")
conn.commit()

# -------------------------
# CONTENT SYSTEM
# -------------------------
RSS_FEEDS = [
    "https://feeds.feedburner.com/entrepreneur/latest",
    "https://www.forbes.com/business/feed/"
]

# -------------------------
# QUOTE
# -------------------------
def get_quote():
    try:
        res = requests.get("https://api.quotable.io/random", timeout=10)
        data = res.json()
        return f"💡 {data['content']}\n\n— {data['author']}"
    except:
        return "Stay focused. Work hard 💪"

# -------------------------
# IMAGE
# -------------------------
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
# SAFE SEND
# -------------------------
async def send_to_all(text=None, photo=None, caption=None):
    success = False

    for ch in CHANNELS:
        try:
            if photo:
                await bot.send_photo(chat_id=ch, photo=photo, caption=caption)
            else:
                await bot.send_message(chat_id=ch, text=text)

            logging.info(f"Sent to {ch}")
            success = True

        except Exception as e:
            logging.error(f"Error in {ch}: {e}")

    return success

# -------------------------
# CHECK DB
# -------------------------
def is_posted(link):
    cur.execute("SELECT 1 FROM posted_links WHERE link=?", (link,))
    return cur.fetchone() is not None

def save_post(link):
    try:
        cur.execute("INSERT INTO posted_links (link) VALUES (?)", (link,))
        conn.commit()
    except:
        pass

# -------------------------
# POST FUNCTIONS
# -------------------------

async def post_rss():
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:5]:
                if not is_posted(entry.link):

                    msg = f"📰 {entry.title}\n\n🔗 {entry.link}"

                    success = await send_to_all(text=msg)

                    if success:
                        save_post(entry.link)
                        return True

        except Exception as e:
            logging.error(f"RSS Error: {e}")

    return False


async def post_quote():
    text = get_quote()
    await send_to_all(text=text)


async def post_image():
    post = random.choice(image_posts)
    await send_to_all(photo=post["image"], caption=post["caption"])

# -------------------------
# AUTO LOOP
# -------------------------

async def auto_post():
    logging.info("Bot started 🚀")

    while True:
        try:
            choice = random.choice(["rss", "quote", "image"])

            if choice == "rss":
                success = await post_rss()

                if not success:
                    logging.info("RSS empty → fallback quote")
                    await post_quote()

            elif choice == "quote":
                await post_quote()

            else:
                await post_image()

            logging.info("Posted successfully ✅")

            await asyncio.sleep(1800)  # 30 min

        except Exception as e:
            logging.error(f"Main Error: {e}")
            await asyncio.sleep(60)

# -------------------------
# HTTP SERVER
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

if __name__ == "__main__":
    threading.Thread(target=run_server).start()
    asyncio.run(auto_post())
