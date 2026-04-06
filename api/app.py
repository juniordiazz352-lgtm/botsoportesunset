from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import httpx
import sqlite3
import json
import os
from bot.utils.bot_api import get_bot

app = FastAPI()

# 🔑 CONFIG
CLIENT_ID = 1485387890786697380
CLIENT_SECRET = eKd8rNscVk3QXcSrVu0jUr3wiqO9fAiY
REDIRECT_URI = https://botsoportesunset.onrender.com/callback

STAFF_ROLE_ID = 1472478801710678258

DB_PATH = "tickets.db"
FORMS_RESPONSES = "form_responses.json"


# =========================
# 🔐 LOGIN
# =========================
@app.get("/login")
def login():
    return RedirectResponse(
        f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify%20guilds.members.read"
    )


# =========================
# 🔁 CALLBACK (CHECK STAFF)
# =========================
@app.get("/callback", response_class=HTMLResponse)
async def callback(code: str):

    async with httpx.AsyncClient() as client:

        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        token = await client.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
        token_json = token.json()

        access_token = token_json.get("access_token")

        user = await client.get(
            "https://discord.com/api/users/@me",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        user_json = user.json()

    # 🔥 SOLO STAFF
    bot = get_bot()
    guild = bot.guilds[0]
    member = guild.get_member(int(user_json["id"]))

    if not member or not any(role.id == STAFF_ROLE_ID for role in member.roles):
        return "<h1>❌ No autorizado</h1>"

    return f"""
    <body style='background:#111;color:#eee'>
    <h1>Bienvenido {user_json['username']}</h1>

    <a href="/tickets">🎫 Tickets</a><br>
    <a href="/forms">📋 Formularios</a>
    </body>
    """


# =========================
# 🎫 TICKETS (REAL)
# =========================
@app.get("/tickets", response_class=HTMLResponse)
def tickets():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets")
    rows = cursor.fetchall()
    conn.close()

    html = "<h1>Tickets</h1>"

    for row in rows:
        html += f"""
        <div>
        Canal: {row[0]}<br>
        Usuario: {row[1]}<br>
        <a href="/close/{row[0]}">Cerrar</a>
        </div><hr>
        """

    return html


# =========================
# ❌ CERRAR TICKET REAL
# =========================
@app.get("/close/{channel_id}")
async def close_ticket(channel_id: int):

    bot = get_bot()
    channel = bot.get_channel(channel_id)

    if channel:
        await channel.delete()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tickets WHERE channel_id = ?", (channel_id,))
    conn.commit()
    conn.close()

    return RedirectResponse("/tickets")


# =========================
# 📋 FORMULARIOS
# =========================
@app.get("/forms", response_class=HTMLResponse)
def forms():

    if not os.path.exists(FORMS_RESPONSES):
        return "<h1>No hay formularios</h1>"

    with open(FORMS_RESPONSES, "r") as f:
        data = json.load(f)

    html = "<h1>Formularios</h1>"

    for i, form in enumerate(data):
        html += f"""
        <div>
        Usuario: {form['user']}<br>
        {form['answers']}<br>
        <a href="/reply/{i}">Responder</a>
        </div><hr>
        """

    return html


# =========================
# 💬 RESPONDER REAL
# =========================
@app.get("/reply/{index}", response_class=HTMLResponse)
def reply_form(index: int):
    return f"""
    <form action="/send/{index}" method="post">
        <input name="msg">
        <button>Enviar</button>
    </form>
    """


@app.post("/send/{index}")
async def send_reply(index: int, request: Request):

    form = await request.form()
    msg = form.get("msg")

    with open(FORMS_RESPONSES, "r") as f:
        data = json.load(f)

    user_name = data[index]["user"]

    bot = get_bot()

    # buscar usuario real
    for guild in bot.guilds:
        for member in guild.members:
            if str(member) == user_name:
                try:
                    await member.send(msg)
                except:
                    pass

    return RedirectResponse("/forms", status_code=303)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
    <style>
    body { margin:0; font-family:Arial; background:#313338; color:#fff; }
    .sidebar {
        width:220px; height:100vh;
        background:#1e1f22; position:fixed;
        padding:20px;
    }
    .sidebar h2 { color:#5865F2; }
    .sidebar a {
        display:block; color:#ccc;
        margin:10px 0; text-decoration:none;
    }
    .content {
        margin-left:240px; padding:20px;
    }
    .card {
        background:#2b2d31;
        padding:15px;
        border-radius:10px;
        margin:10px 0;
    }
    .btn {
        background:#5865F2;
        padding:6px 10px;
        border-radius:5px;
        text-decoration:none;
        color:white;
    }
    .danger { background:#ed4245; }
    </style>
    </head>

    <body>

    <div class="sidebar">
        <h2>🌐 Panel</h2>
        <a href="/dashboard">🏠 Inicio</a>
        <a href="/tickets">🎫 Tickets</a>
        <a href="/forms">📋 Formularios</a>
        <a href="/login">🔑 Login</a>
    </div>

    <div class="content">
        <h1>Bienvenido al Panel</h1>
        <p>Sistema profesional conectado a Discord</p>
    </div>

    </body>
    </html>
    """
