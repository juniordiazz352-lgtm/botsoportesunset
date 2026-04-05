import discord
from discord.ext import commands
import asyncio
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Slash commands sincronizados: {len(synced)}")
    except Exception as e:
        print(e)


async def setup_bot():
    await bot.load_extension("bot.cogs.tickets")
    await bot.load_extension("bot.cogs.forms")


async def main():
    async with bot:
        await setup_bot()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
