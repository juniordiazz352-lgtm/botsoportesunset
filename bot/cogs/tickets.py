import discord
from discord.ext import commands
from discord import app_commands
from bot.views.ticket_panel import TicketPanel

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="crear_panel_ticket")
    async def crear_panel(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            "📌 Escribe el título del panel:", ephemeral=True
        )

        def check(m): return m.author == interaction.user
        msg1 = await self.bot.wait_for("message", check=check)

        await interaction.followup.send("📝 Escribe la descripción:")
        msg2 = await self.bot.wait_for("message", check=check)

        await interaction.followup.send("📂 Menciona la categoría:")
        msg3 = await self.bot.wait_for("message", check=check)

        if not msg3.channel_mentions:
            return await interaction.followup.send("❌ Debes mencionar una categoría")

        category = msg3.channel_mentions[0]

        embed = discord.Embed(
            title=msg1.content,
            description=msg2.content,
            color=discord.Color.green()
        )

        await interaction.channel.send(
            embed=embed,
            view=TicketPanel(category.id)
        )

        await interaction.followup.send("✅ Panel creado")

# obligatorio
async def setup(bot):
    await bot.add_cog(Tickets(bot))
