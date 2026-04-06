from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import httpx
import sqlite3
import json
import os

app = FastAPI()

# =========================
# 🔑 CONFIG
# =========================
CLIENT_ID = "TU_CLIENT_ID"
CLIENT_SECRET = "TU_CLIENT_SECRET"
REDIRECT_URI = "https://tu-app.onrender.com/callback"

DB_PATH = "tickets.db"
FORMS_RESPONSES = "form_responses.json"


# =========================
# 🏠 HOME
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body style="background:#111;color:#eee;font-family:Arial;">
        <h1>🌐 Panel Admin</h1>
        <a href="/login">🔑 Iniciar sesión con Discord</a>
    </body>
    </html>
    """


# =========================
# 🔑 LOGIN
# =========================
@app.get("/login")
def login():
    return RedirectResponse(
        f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify"
    )


# =========================
# 🔁 CALLBACK
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

    return f"""
    <html>
    <body style="background:#111;color:#eee;font-family:Arial;">
        <h1>Bienvenido {user_json['username']}</h1>

        <a href="/tickets">🎫 Ver Tickets</a><br><br>
        <a href="/forms">📋 Ver Formularios</a>
    </body>
    </html>
    """


# =========================
# 🎫 TICKETS
# =========================
@app.get("/tickets", response_class=HTMLResponse)
def tickets():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets")
    rows = cursor.fetchall()

    conn.close()

    html = "<h1>🎫 Tickets</h1>"

    for row in rows:
        html += f"""
        <div style='border:1px solid #333;padding:10px;margin:10px;'>
            Channel ID: {row[0]}<br>
            User ID: {row[1]}<br>
            <a href="/close_ticket/{row[0]}">❌ Cerrar Ticket</a>
        </div>
        """

    return f"<body style='background:#111;color:#eee'>{html}</body>"


# =========================
# ❌ CERRAR TICKET (WEB)
# =========================
@app.get("/close_ticket/{channel_id}")
def close_ticket(channel_id: int):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tickets WHERE channel_id = ?", (channel_id,))
    conn.commit()
    conn.close()

    return RedirectResponse("/tickets")


# =========================
# 📋 FORMULARIOS (RESPUESTAS)
# =========================
@app.get("/forms", response_class=HTMLResponse)
def forms():

    if not os.path.exists(FORMS_RESPONSES):
        return "<h1>No hay formularios</h1>"

    with open(FORMS_RESPONSES, "r") as f:
        data = json.load(f)

    html = "<h1>📋 Formularios</h1>"

    for i, form in enumerate(data):
        html += f"""
        <div style='border:1px solid #333;padding:10px;margin:10px;'>
            Usuario: {form['user']}<br>
            Respuestas: {form['answers']}<br>
            <a href="/reply_form/{i}">💬 Responder</a>
        </div>
        """

    return f"<body style='background:#111;color:#eee'>{html}</body>"


# =========================
# 💬 RESPONDER FORM (WEB)
# =========================
@app.get("/reply_form/{index}", response_class=HTMLResponse)
def reply_form(index: int):

    return f"""
    <form action="/send_reply/{index}" method="post">
        <input name="msg" placeholder="Mensaje"><br>
        <button type="submit">Enviar</button>
    </form>
    """


@app.post("/send_reply/{index}")
async def send_reply(index: int, request: Request):

    form = await request.form()
    msg = form.get("msg")

    print("Respuesta enviada:", msg)

    return RedirectResponse("/forms", status_code=303)
