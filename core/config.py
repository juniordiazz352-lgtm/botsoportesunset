import os

TOKEN = os.getenv("TOKEN")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

GUILD_ID = int(os.getenv("GUILD_ID"))
STAFF_ROLE_ID = int(os.getenv("STAFF_ROLE_ID"))
FORMS_CHANNEL_ID = int(os.getenv("FORMS_CHANNEL_ID"))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

import discord
from discord.ext import commands
from bot.core.db import cursor, conn


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="set_logs")
    @commands.has_permissions(administrator=True)
    async def set_logs(self, ctx, canal: discord.TextChannel):
        cursor.execute(
            "INSERT OR REPLACE INTO config VALUES ('logs', ?)",
            (str(canal.id),)
        )
        conn.commit()

        await ctx.send(f"✅ Canal de logs configurado: {canal.mention}")

    @commands.hybrid_command(name="set_transcripts")
    @commands.has_permissions(administrator=True)
    async def set_transcripts(self, ctx, canal: discord.TextChannel):
        cursor.execute(
            "INSERT OR REPLACE INTO config VALUES ('transcripts', ?)",
            (str(canal.id),)
        )
        conn.commit()

        await ctx.send(f"✅ Canal de transcripts configurado: {canal.mention}")


async def setup(bot):
    await bot.add_cog(Config(bot))
