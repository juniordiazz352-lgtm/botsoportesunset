import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from core.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from core.db import save_user, save_guilds, get_user_guilds

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
