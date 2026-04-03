import discord
from discord.ui import View, button
from core.db import create_ticket
from bot.views.ticket_controls import TicketControls

class TicketPanel(View):
    def __init__(self, category_id):
        super().__init__(timeout=None)
        self.category_id = category_id

    @button(label="🎫 Crear Ticket", style=discord.ButtonStyle.green)
    async def create_ticket_btn(self, interaction: discord.Interaction, _):

        # anti duplicado
        for ch in interaction.guild.text_channels:
            if ch.name == f"ticket-{interaction.user.id}":
                return await interaction.response.send_message(
                    "❌ Ya tienes ticket", ephemeral=True
                )

        category = interaction.guild.get_channel(self.category_id)

        channel = await interaction.guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category
        )

        create_ticket(channel.id, interaction.user.id)

        await channel.send(
            f"{interaction.user.mention}",
            view=TicketControls()
        )

        await interaction.response.send_message(
            f"✅ Ticket creado: {channel.mention}",
            ephemeral=True
        )
