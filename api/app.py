import os
import threading
import asyncio
import requests

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

import discord
from discord.ext import commands

from bot.main import bot, setup_bot
from bot.views.ticket_panel import TicketPanel
from core.config import TOKEN, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from core.db import save_panel, get_panels
from fastapi import FastAPI
import threading
from bot.main import run_bot

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

# correr el bot en segundo plano
threading.Thread(target=run_bot).start()


# =========================
# DASHBOARD
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(BASE_DIR, "web", "templates", "dashboard.html")

@app.get("/")
def home():
    if not os.path.exists(TEMPLATE_PATH):
        return JSONResponse({"error": "dashboard.html no encontrado"})

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


# =========================
# LOGIN DISCORD
# =========================

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

    access_token = token.get("access_token")

    if not access_token:
        return {"error": "No se pudo obtener token"}

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
        "guilds": guilds
    }


# =========================
# CREAR PANEL
# =========================

@app.post("/create_panel")
async def create_panel(request: Request):
    data = await request.json()

    channel_id = int(data["channel_id"])
    title = data["title"]
    description = data["description"]
    botones = data["botones"]

    channel = bot.get_channel(channel_id)

    if not channel:
        return {"error": "Canal no encontrado"}

    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blue()
    )

    future = asyncio.run_coroutine_threadsafe(
        channel.send(embed=embed, view=TicketPanel(botones)),
        bot.loop
    )

    msg = future.result()

    save_panel(channel_id, msg.id, botones)

    return {"ok": True}


# =========================
# PANELES
# =========================

@app.get("/panels")
def panels():
    return get_panels()


# =========================
# INICIAR BOT EN THREAD
# =========================

def run_bot():
    async def start():
        await setup_bot()
        await bot.start(TOKEN)

    asyncio.run(start())


threading.Thread(target=run_bot, daemon=True).start()
