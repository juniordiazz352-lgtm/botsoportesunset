import discord
from discord.ext import commands
import os
from core.config import GUILD_ID

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def load():
    for f in os.listdir("./bot/cogs"):
        if f.endswith(".py"):
            try:
                await bot.load_extension(f"bot.cogs.{f[:-3]}")
                print(f"✅ Cargado: {f}")
            except Exception as e:
                print(f"❌ Error en {f}: {e}")

@bot.event
async def on_ready():
    print(f"🔥 BOT ONLINE: {bot.user}")
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))

import asyncio
asyncio.run(load())
