from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from core.db import load, close_ticket, update_form_status

app = FastAPI()

@app.get("/")

@app.get("/data")
def data():
    return load()

@app.post("/close_ticket/{id}")
def close(id: str):
    close_ticket(id)
    return {"ok": True}

@app.post("/form/{id}/{action}")
def form_action(id: str, action: str):
    update_form_status(id, action)
    return {"ok": True}

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(BASE_DIR, "web", "templates", "dashboard.html")


def home():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)
