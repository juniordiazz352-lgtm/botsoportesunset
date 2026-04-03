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
            "📌 ¿Cuántos botones quieres?", ephemeral=True
        )

        def check(m): return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)
        cantidad = int(msg.content)

        botones = []

        for i in range(cantidad):
            await interaction.followup.send(f"🔘 Nombre botón {i+1}:")
            nombre = await self.bot.wait_for("message", check=check)

            await interaction.followup.send(f"📂 Menciona categoría {i+1}:")
            cat_msg = await self.bot.wait_for("message", check=check)

            if not cat_msg.channel_mentions:
                return await interaction.followup.send("❌ Categoría inválida")

            categoria = cat_msg.channel_mentions[0]

            botones.append({
                "label": nombre.content,
                "categoria_id": categoria.id,
                "tipo": nombre.content.lower().replace(" ", "-")
            })

        await interaction.followup.send("📝 Título del panel:")
        titulo = await self.bot.wait_for("message", check=check)

        await interaction.followup.send("📄 Descripción:")
        desc = await self.bot.wait_for("message", check=check)

        embed = discord.Embed(
            title=titulo.content,
            description=desc.content,
            color=discord.Color.green()
        )

        await interaction.channel.send(
            embed=embed,
            view=TicketPanel(botones)
        )

        await interaction.followup.send("✅ Panel creado")

async def setup(bot):
    await bot.add_cog(Tickets(bot))
