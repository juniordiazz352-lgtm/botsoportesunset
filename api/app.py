from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import sqlite3
import json
import os

app = FastAPI()

DB_PATH = "tickets.db"
FORMS_FILE = "forms.json"


# =========================
# 🏠 HOME
# =========================
@app.get("/", response_class=HTMLResponse)
def home():

    html = """
    <html>
    <head>
        <title>Panel Admin</title>
        <style>
            body { background:#111; color:#eee; font-family: Arial; }
            h1 { color:#00ffcc; }
            .box { margin:20px; padding:20px; background:#1e1e1e; border-radius:10px; }
        </style>
    </head>
    <body>
        <h1>🌐 Panel Admin</h1>

        <div class="box">
            <h2>📋 Formularios</h2>
            <a href="/forms">Ver formularios</a>
        </div>

        <div class="box">
            <h2>🎫 Tickets</h2>
            <a href="/tickets">Ver tickets</a>
        </div>

    </body>
    </html>
    """

    return html


# =========================
# 📋 FORMULARIOS
# =========================
@app.get("/forms", response_class=HTMLResponse)
def forms():

    data_html = ""

    if os.path.exists(FORMS_FILE):
        with open(FORMS_FILE, "r") as f:
            data = json.load(f)

        for nombre, preguntas in data.items():
            data_html += f"<h3>{nombre}</h3><ul>"
            for p in preguntas:
                data_html += f"<li>{p}</li>"
            data_html += "</ul>"

    return f"""
    <html>
    <body style="background:#111;color:#eee;font-family:Arial;">
        <h1>📋 Formularios creados</h1>
        {data_html}
        <br><a href="/">⬅ Volver</a>
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

    data_html = ""

    for row in rows:
        data_html += f"""
        <div style='border:1px solid #333;padding:10px;margin:10px;'>
            Channel ID: {row[0]}<br>
            User ID: {row[1]}<br>
            Claimed By: {row[2]}
        </div>
        """

    return f"""
    <html>
    <body style="background:#111;color:#eee;font-family:Arial;">
        <h1>🎫 Tickets activos</h1>
        {data_html}
        <br><a href="/">⬅ Volver</a>
    </body>
    </html>
    """
