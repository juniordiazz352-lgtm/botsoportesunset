import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


async def setup_bot():
    await bot.load_extension("bot.cogs.ticket")
    await bot.load_extension("bot.cogs.forms")
    await bot.load_extension("bot.cogs.setup")
    await bot.load_extension("bot.cogs.panel_creator")



    @bot.event
async def on_ready():
    print(f"✅ {bot.user} listo")

    from bot.views.ticket_panel import TicketPanelView
    from bot.views.ticket_controls import TicketControlsView

    bot.add_view(TicketPanelView())
    bot.add_view(TicketControlsView())


async def main():
    async with bot:
        await setup_bot()
        await bot.start(os.getenv("TOKEN"))


def run_bot():
    asyncio.run(main())
