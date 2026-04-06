import discord
from discord.ext import commands
from bot.views.setup_view import SetupView


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        """Abre el panel de configuración"""

        view = SetupView(self.bot, ctx.guild)

        await ctx.send(
            embed=view.get_embed(),
            view=view
        )
