import discord
from discord.ext import commands
import os

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# 🔥 Cargar cogs correctamente
async def setup_bot():
    await bot.load_extension("bot.cogs.utilidades")
    # agrega más cogs acá si tienes

# 🔥 Esto se ejecuta cuando el bot inicia
@bot.event
async def setup_hook():
    await setup_bot()

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

# 🔥 Iniciar bot
def run_bot():
    TOKEN = os.getenv("TOKEN")
    bot.run(TOKEN)"bot.cogs.utilidades")
