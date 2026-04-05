import discord
from discord.ext import commands
from views.ticket_panel import TicketPanelView


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def panel_ticket(self, ctx):

        embed = discord.Embed(
            title="🎫 Soporte",
            description="Selecciona una opcion y aprieta en ella para abrir un ticket",
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed, view=TicketPanelView())


async def setup(bot):
    await bot.add_cog(Tickets(bot))
