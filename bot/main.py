import discord
from discord.ext import commands
import os
from core.config import GUILD_ID

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def setup_bot():
    for f in os.listdir("./bot/cogs"):
        if f.endswith(".py"):
            try:
                await bot.load_extension(f"bot.cogs.{f[:-3]}")
                print(f"✅ Cargado: {f}")
            except Exception as e:
                print(f"❌ Error en {f}: {e}")

@bot.event
async def on_ready():
    print(f"🔥 BOT ONLINE: {bot.user}")
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))

from core.db import get_panels
from bot.views.ticket_panel import TicketPanel

@bot.event
async def on_ready():
    print(f"🔥 BOT ONLINE: {bot.user}")

    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))

    # 💀 RESTAURAR PANELES
    panels = get_panels()

    for p in panels:
        try:
            channel = bot.get_channel(p["channel_id"])
            if not channel:
                continue

            message = await channel.fetch_message(p["message_id"])

            await message.edit(
                view=TicketPanel(p["botones"])
            )

            print(f"✅ Panel restaurado en {channel.id}")

        except Exception as e:
            print("❌ Error restaurando panel:", e)
