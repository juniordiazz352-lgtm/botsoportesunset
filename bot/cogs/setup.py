import discord
from discord.ext import commands
from bot.views.setup_view import SetupView
from core.db import cursor


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):

        await ctx.message.delete()

        embed = discord.Embed(
            title="⚙️ Setup GOD++",
            description="Configura el bot usando el menú interactivo",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="🎟️ Tickets",
            value="Configura categoría de tickets",
            inline=False
        )

        embed.add_field(
            name="📋 Formularios",
            value="Configura canal de logs/forms",
            inline=False
        )

        embed.add_field(
            name="🛠️ Staff",
            value="Configura rol staff",
            inline=False
        )

        embed.add_field(
            name="📊 Estado",
            value="Ver configuración actual",
            inline=False
        )

        await ctx.send(embed=embed, view=SetupView(self.bot))


async def setup(bot):
    await bot.add_cog(Setup(bot))
