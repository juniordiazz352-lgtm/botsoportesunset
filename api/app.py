import os
import threading
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from bot.main import bot
from core.config import TOKEN
import discord
from bot.views.ticket_panel import TicketPanel
from bot.main import bot
import asyncio
import requests
from fastapi.responses import RedirectResponse
from core.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

# LOGIN
@app.get("/login")
def login():
    url = (
        "https://discord.com/api/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        "&response_type=code"
        "&scope=identify guilds"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return RedirectResponse(url)

# CALLBACK
@app.get("/callback")
def callback(code: str):

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token = requests.post(
        "https://discord.com/api/oauth2/token",
        data=data,
        headers=headers
    ).json()

    access_token = token["access_token"]

    user = requests.get(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    guilds = requests.get(
        "https://discord.com/api/users/@me/guilds",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    return {
        "user": user,
        "guilds": guilds,
        "token": access_token
    }

loop = asyncio.get_event_loop()

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

from fastapi import Request
from core.db import save_panel, get_panels
import asyncio

# CREAR PANEL DESDE WEB
@app.post("/create_panel")
async def create_panel(request: Request):
    data = await request.json()

    channel_id = int(data["channel_id"])
    title = data["title"]
    description = data["description"]
    botones = data["botones"]

    channel = bot.get_channel(channel_id)

    embed = discord.Embed(
        title=title,
        description=description
    )

   msg = await asyncio.run_coroutine_threadsafe(
    channel.send(embed=embed, view=TicketPanel(botones)),
    loop
).result()

    save_panel(channel_id, msg.id, botones)

    return {"ok": True}


# OBTENER PANELES
@app.get("/panels")
def panels():
    return get_panels()

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
