import discord
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ===== EVENTO READY =====
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

# ===== SETUP DE COGS =====
async def setup_bot():
    await bot.load_extension("bot.cogs.utilidades")
