from fastapi import FastAPI
import threading
from bot.main import run_bot

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

threading.Thread(target=run_bot, daemon=True).start()
