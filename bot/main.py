import discord
from discord.ext import commands
import os
from bot.utils.logger import logger

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Bot conectado como {bot.user}")

async def load_cogs():
    for file in os.listdir("./bot/cogs"):
        if file.endswith(".py"):
            try:
                await bot.load_extension(f"bot.cogs.{file[:-3]}")
                logger.info(f"Cog cargado: {file}")
            except Exception as e:
                logger.error(f"Error cargando {file}: {e}")

@bot.event
async def setup_hook():
    await load_cogs()

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"❌ Error: {error}")

bot.run(os.getenv("TOKEN"))
