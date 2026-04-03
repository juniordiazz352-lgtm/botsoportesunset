import os
import threading
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from bot.main import bot
from core.config import TOKEN

app = FastAPI()

# ===== PATH CORRECTO =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(BASE_DIR, "web", "templates", "dashboard.html")

# ===== DASHBOARD =====
@app.get("/")
def home():
    try:
        if not os.path.exists(TEMPLATE_PATH):
            return JSONResponse({"error": "dashboard.html no encontrado"})

        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())

    except Exception as e:
        return JSONResponse({"error": str(e)})

# ===== BOT THREAD =====
import threading
import asyncio
from bot.main import bot, setup_bot
from core.config import TOKEN

def run_bot():
    async def start():
        await setup_bot()
        await bot.start(TOKEN)

    asyncio.run(start())

threading.Thread(target=run_bot).start()
