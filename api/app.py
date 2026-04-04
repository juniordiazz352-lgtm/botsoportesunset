import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from core.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from core.db import save_user, save_guilds, get_user_guilds
from core.db import update_panel, get_panel
import discord
import asyncio
from bot.views.ticket_panel import TicketPanel

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(BASE_DIR, "web", "templates", "dashboard.html")

# HOME
@app.get("/")
def home():
    return HTMLResponse(open(TEMPLATE_PATH).read())

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

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

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

    # 💀 SOLO TU PUEDES ENTRAR
    if user["id"] != OWNER_ID:
        return {"error": "No autorizado"}

    response = RedirectResponse("/dashboard")
    response.set_cookie("user_id", user["id"])

    return response
# DASHBOARD PROTEGIDO
@app.get("/dashboard")
def dashboard(request: Request):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return RedirectResponse("/login")

    return HTMLResponse(open(TEMPLATE_PATH).read())

# GUILDS DEL USUARIO
@app.get("/guilds")
def guilds(request: Request):
    user_id = request.cookies.get("user_id")

    if not user_id:
        return JSONResponse({"error": "no auth"})

    return get_user_guilds(user_id)

@app.get("/guilds")
def guilds():
    return [{"id": GUILD_ID, "name": "Mi servidor"}]

@app.post("/create_panel")
async def create_panel(request: Request):
    data = await request.json()
    save_panel(channel.id, msg.id, data["botones"])

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

@app.get("/panel/{panel_id}")
def get_panel_api(panel_id: int):
    return get_panel(panel_id)

@app.put("/edit_panel/{panel_id}")
async def edit_panel(panel_id: int, request: Request):

    data = await request.json()

    # 💀 obtener panel de DB
    panel = get_panel(panel_id)

    channel = bot.get_channel(int(panel["channel_id"]))

    message = await channel.fetch_message(int(panel["message_id"]))

    embed = discord.Embed(
        title=data["title"],
        description=data["description"]
    )

    # 💀 editar mensaje EN DISCORD
    future = asyncio.run_coroutine_threadsafe(
        message.edit(
            embed=embed,
            view=TicketPanel(data["botones"])
        ),
        bot.loop
    )

    future.result()

    # 💀 guardar cambios
    update_panel(panel_id, data)

    return {"ok": True}
