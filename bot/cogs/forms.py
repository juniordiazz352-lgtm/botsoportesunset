import discord
from discord.ext import commands
from bot.views.form_panel import FormPanelView


class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def panel_form(self, ctx):

        embed = discord.Embed(
            title="📋 Formularios",
            description="Selecciona un formulario del menú de abajo",
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed, view=FormPanelView())


async def setup(bot):
    await bot.add_cog(Forms(bot))
