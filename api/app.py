import os
import threading
import asyncio
import requests
import discord
from core.db import delete_panel, update_panel
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import FileResponse
from core.db import get_logs
import os
from core.db import delete_panel
from bot.main import bot, setup_bot
from bot.views.ticket_panel import TicketPanel
from core.config import TOKEN, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from core.db import save_panel, get_panels

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecretkey123")

# ================= DASHBOARD =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(BASE_DIR, "web", "templates", "dashboard.html")

@app.get("/")
def home():
    if not os.path.exists(TEMPLATE_PATH):
        return JSONResponse({"error": "dashboard.html no encontrado"})
    return HTMLResponse(open(TEMPLATE_PATH, encoding="utf-8").read())

# ================= LOGIN =================
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
def callback(code: str, request: Request):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    token = requests.post(
        "https://discord.com/api/oauth2/token",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
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

    request.session["user"] = user
    request.session["guilds"] = guilds

    return RedirectResponse("/")

@app.get("/me")
def me(request: Request):
    return {
        "user": request.session.get("user"),
        "guilds": request.session.get("guilds")
    }

# ================= CANALES =================
@app.get("/channels/{guild_id}")
def get_channels(guild_id: int):
    guild = bot.get_guild(guild_id)
    if not guild:
        return []
    return [{"id": c.id, "name": c.name} for c in guild.text_channels]

# ================= CATEGORÍAS 💀 =================
@app.get("/categories/{guild_id}")
def get_categories(guild_id: int):
    guild = bot.get_guild(guild_id)
    if not guild:
        return []
    return [{"id": c.id, "name": c.name} for c in guild.categories]

# ================= CREAR PANEL =================
@app.post("/create_panel")
async def create_panel(request: Request):
    data = await request.json()

    channel = bot.get_channel(int(data["channel_id"]))

    embed = discord.Embed(
        title=data["title"],
        description=data["description"]
    )

    future = asyncio.run_coroutine_threadsafe(
        channel.send(embed=embed, view=TicketPanel(data["botones"])),
        bot.loop
    )

    msg = future.result()

    save_panel(channel.id, msg.id, data["botones"])

    return {"ok": True}

@app.get("/panels")
def panels():
    return get_panels()

@app.delete("/panel/{panel_id}")
def delete_panel_api(panel_id: int):
    delete_panel(panel_id)
    return {"ok": True}

@app.put("/panel/{panel_id}")
async def edit_panel(panel_id: int, request: Request):
    data = await request.json()
    update_panel(panel_id, data["botones"])
    return {"ok": True}

@app.get("/transcripts")
def transcripts():
    if not os.path.exists("transcripts"):
        return []

    files = os.listdir("transcripts")

    return files

@app.get("/transcript/{name}")
def get_transcript(name: str):
    path = f"transcripts/{name}"

    if not os.path.exists(path):
        return {"error": "no existe"}

    return FileResponse(path)

@app.get("/logs")
def logs():
    return get_logs()
# ================= BOT =================
def run_bot():
    async def start():
        await setup_bot()
        await bot.start(TOKEN)

    asyncio.run(start())

threading.Thread(target=run_bot).start()
