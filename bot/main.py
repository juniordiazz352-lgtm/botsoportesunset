import discord
from discord.ext import commands
import asyncio
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
intents.message_content = True  # 🔥 IMPORTANTE

bot = commands.Bot(command_prefix="!", intents=intents)


async def setup_bot():
    await bot.load_extension("bot.cogs.forms")
    await bot.load_extension("bot.cogs.tickets")
    await bot.load_extension("bot.cogs.panel_creator")  # 🔥 ya lo tienes
    await bot.load_extension("bot.cogs.config")
    await bot.load_extension("bot.cogs.setup")
    
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"🔁 Slash sincronizados: {len(synced)}")
    except Exception as e:
        print(e)

    # 🔥 IMPORTANTE: registrar views persistentes
    from bot.views.ticket_panel import TicketPanelView
    from bot.views.ticket_controls import TicketControlsView
    from bot.views.form_panel import FormPanelView

    bot.add_view(TicketPanelView())
    bot.add_view(TicketControlsView())
    bot.add_view(FormPanelView())


async def main():
    async with bot:
        await setup_bot()
        await bot.start(TOKEN)


def run_bot():
    asyncio.run(main())
