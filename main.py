import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"🔥 Bot conectado como {bot.user}")


# 🔥 CARGAR TODOS LOS COGS AUTOMÁTICO
async def load_cogs():
    for root, dirs, files in os.walk("./bot/cogs"):
        for file in files:
            if file.endswith(".py"):
                ruta = os.path.join(root, file)\
                    .replace("\\", ".")\
                    .replace("/", ".")[:-3]

                try:
                    await bot.load_extension(ruta)
                    print(f"✅ Cargado: {ruta}")
                except Exception as e:
                    print(f"❌ Error en {ruta}: {e}")


async def main():
    async with bot:
        await load_cogs()
        import os

await bot.start(os.getenv("TOKEN"))

asyncio.run(main())
