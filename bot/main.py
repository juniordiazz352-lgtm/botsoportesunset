import discord
from discord.ext import commands
import os

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# 🔥 Cargar TODOS tus cogs
async def setup_bot():
    await bot.load_extension("bot.cogs.utilidades")
    await bot.load_extension("bot.cogs.tickets")
    await bot.load_extension("bot.cogs.forms")
    await bot.load_extension("bot.cogs.panel_creator")

@bot.event
async def setup_hook():
    await setup_bot()

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

# 🔥 Ejecutar bot
def run_bot():
    TOKEN = os.getenv("TOKEN")

    if not TOKEN:
        print("❌ ERROR: No hay TOKEN")
        return

    bot.run(TOKEN)
