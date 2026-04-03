from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from core.db import load, close_ticket, update_form_status

app = FastAPI()

@app.get("/")
def home():
    return HTMLResponse(open("web/templates/dashboard.html").read())

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
