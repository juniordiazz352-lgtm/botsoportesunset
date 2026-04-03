import threading
import discord
from discord.ext import commands
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

# -------- CONFIG --------
TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

# -------- BOT --------
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🔥 Bot conectado: {bot.user}")
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))

# -------- INICIAR BOT EN THREAD --------
def run_bot():
    bot.run(TOKEN)

threading.Thread(target=run_bot).start()

# -------- WEB --------
app = FastAPI()

@app.get("/")
def home():
    return HTMLResponse("""
    <h1 style='color:white;background:#0f172a;padding:20px'>
    🚀 BOT + DASHBOARD ACTIVO
    </h1>
    """)
