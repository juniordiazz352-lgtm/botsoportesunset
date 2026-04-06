import discord
from discord.ext import commands
from bot.views.setup_view import SetupView


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def setup(self, ctx):

        embed = discord.Embed(
            title="⚙️ Panel de Configuración",
            description="Usa los botones para configurar o ver el estado",
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed, view=SetupView(self.bot, ctx.guild))


async def setup(bot):
    await bot.add_cog(Setup(bot))
