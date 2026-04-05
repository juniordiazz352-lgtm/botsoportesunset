from fastapi import FastAPI
import threading
from bot.main import run_bot

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Bot activo 🚀"}

# Ejecutar el bot en segundo plano
threading.Thread(target=run_bot).start()
