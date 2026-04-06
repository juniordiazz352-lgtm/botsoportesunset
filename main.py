import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"🔥 Conectado como {bot.user}")


async def load_cogs():
    for file in os.listdir("./bot/cogs"):
        if file.endswith(".py") and file != "__init__.py":

            cog = f"bot.cogs.{file[:-3]}"

            try:
                await bot.load_extension(cog)
                print(f"✅ Cargado: {cog}")
            except Exception as e:
                print(f"❌ Error en {cog}: {e}")


async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv("TOKEN"))


asyncio.run(main())
