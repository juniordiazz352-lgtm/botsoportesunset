from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from api.auth import router as auth_router
from core.db import load

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def home():
    html = open("web/templates/dashboard.html").read()
    return HTMLResponse(html)

@app.get("/data")
def data():
    return load()
