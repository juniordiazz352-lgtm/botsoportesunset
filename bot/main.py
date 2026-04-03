import discord
from discord.ext import commands
import os
from core.config import TOKEN, GUILD_ID

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def load():
    for f in os.listdir("./bot/cogs"):
        if f.endswith(".py"):
            await bot.load_extension(f"bot.cogs.{f[:-3]}")

@bot.event
async def on_ready():
    print("🔥 BOT PRO ACTIVO")
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))

import asyncio
asyncio.run(load())
