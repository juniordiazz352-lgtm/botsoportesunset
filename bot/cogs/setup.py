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
            title="⚙️ Panel de Configuración",
            description="Configura el sistema del bot",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="🎟️ Tickets",
            value="Configurar categoría de tickets",
            inline=False
        )

        embed.add_field(
            name="📋 Formularios",
            value="Configurar canal de formularios",
            inline=False
        )

        embed.add_field(
            name="🛠️ Staff",
            value="Configurar rol staff",
            inline=False
        )

        embed.set_footer(text=f"Setup por {ctx.author}")

        await ctx.send(embed=embed, view=SetupView(self.bot))


async def setup(bot):
    await bot.add_cog(Setup(bot))
