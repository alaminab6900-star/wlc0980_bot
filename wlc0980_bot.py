import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# 🔹 তোমার আগের imports + bot code থাকবে

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
# BOT LOOP
# -------------------------
async def auto_post():
    while True:
        print("Bot running...")
        await asyncio.sleep(30)

# -------------------------
# MAIN RUN
# -------------------------
def start_bot():
    asyncio.run(auto_post())

# 🔥 IMPORTANT: threading use করো
threading.Thread(target=start_bot).start()

# server main thread-এ run হবে
run_server()
