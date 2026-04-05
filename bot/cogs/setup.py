import discord
from discord.ext import commands
from views.setup_view import SetupView


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def setup(self, ctx):

        embed = discord.Embed(
            title="⚙️ Setup del Bot",
            description=(
                "Configura el bot usando los botones\n\n"
                "👮 Rol Staff\n"
                "📁 Categoría Tickets\n"
                "📋 Canal Formularios\n"
                "📝 Canal Logs"
            ),
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed, view=SetupView(self.bot))


async def setup(bot):
    await bot.add_cog(Setup(bot))
