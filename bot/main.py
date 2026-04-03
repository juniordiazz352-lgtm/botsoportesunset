import discord
from discord.ext import commands
import os
from core.config import TOKEN, GUILD_ID

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("🔥 BOT ONLINE")
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))

async def load():
    for f in os.listdir("./bot/cogs"):
        if f.endswith(".py"):
            await bot.load_extension(f"bot.cogs.{f[:-3]}")

import asyncio
asyncio.run(load())

bot.run(TOKEN)
