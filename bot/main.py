import discord
from discord.ext import commands
import asyncio
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


async def setup_bot():
    await bot.load_extension("bot.cogs.forms")
    await bot.load_extension("bot.cogs.tickets")


@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")


async def main():
    async with bot:
        await setup_bot()
        await bot.start(TOKEN)


def run_bot():
    asyncio.run(main())
