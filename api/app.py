from fastapi import FastAPI
import threading
from bot.main import run_bot

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}



@app.get("/stats")
def stats():
    import sqlite3

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tickets")
    total = cursor.fetchone()[0]

    conn.close()

    return {"tickets": total}

threading.Thread(target=run_bot, daemon=True).start()
