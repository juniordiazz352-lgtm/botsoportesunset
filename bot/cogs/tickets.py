import discord
from discord.ext import commands
from bot.views.ticket_view import TicketView

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def panel(self, ctx):
        embed = discord.Embed(
            title="🎫 Soporte",
            description="Presiona el botón para crear un ticket"
        )
        await ctx.send(embed=embed, view=TicketView())

async def setup(bot):
    await bot.add_cog(Tickets(bot))
