import discord
from discord.ext import commands
import asyncio
import os
from bot.utils.bot_api import set_bot
set_bot(bot)
import threading
import asyncio
import uvicorn

from bot.main import main as bot_main  # tu bot
# 👆 si tu archivo se llama distinto avisame



def run_api():
    uvicorn.run("api.app:app", host="0.0.0.0", port=10000)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_bot)
    t1.start()

    run_api()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def setup_bot():
    await bot.load_extension("bot.cogs.ticket")
    await bot.load_extension("bot.cogs.forms")
    await bot.load_extension("bot.cogs.panel_creator")
    await bot.load_extension("bot.cogs.setup")
    await bot.load_extension("bot.cogs.utilidades")
    await bot.load_extension("bot.cogs.help")

@bot.event
async def on_ready():
    print(f"✅ {bot.user} listo")

    from bot.views.ticket_panel import TicketPanelView
    from bot.views.ticket_controls import TicketControlsView

    bot.add_view(TicketPanelView())
    bot.add_view(TicketControlsView())

@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):
        return await ctx.send("❌ No tienes permisos.")

    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send("⚠️ Argumentos faltantes.")

    if isinstance(error, commands.CommandNotFound):
        return

    print(f"ERROR: {error}")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Comandos sincronizados")

async def main():
    async with bot:
        await setup_bot()
        await bot.start(os.getenv("TOKEN"))


async def setup_bot():
    for filename in os.listdir("./bot/cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"bot.cogs.{filename[:-3]}")
                print(f"✅ Cargado: {filename}")
            except Exception as e:
                print(f"❌ Error en {filename}: {e}")

def run_bot():
    asyncio.run(main())

# 🔥 IMPORTANTE
if __name__ == "__main__":
    run_bot()
