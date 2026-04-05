import discord
from discord.ext import commands
from bot.views.form_panel import FormPanelView
from bot.views.form_builder import FormBuilderView


class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 📋 Panel público
    @commands.command()
    async def panel_form(self, ctx):
        embed = discord.Embed(
            title="📋 Formularios",
            description="Presiona el botón para completar un formulario",
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed, view=FormPanelView())

    # 🛠 Crear formulario (USA TU BUILDER REAL)
    @commands.command()
    async def crear_form(self, ctx):
        await ctx.send(
            "🛠 Creador de formularios",
            view=FormBuilderView(ctx.author)
        )


async def setup(bot):
    await bot.add_cog(Forms(bot))
