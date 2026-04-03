from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import httpx
from core.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

router = APIRouter()
API = "https://discord.com/api"

@router.get("/login")
def login():
    return RedirectResponse(
        f"{API}/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify"
    )

@router.get("/callback")
async def callback(code: str):

    async with httpx.AsyncClient() as client:
        token = await client.post(f"{API}/oauth2/token", data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        })

        token = token.json()

        user = await client.get(
            f"{API}/users/@me",
            headers={"Authorization": f"Bearer {token['access_token']}"}
        )

    return user.json()
