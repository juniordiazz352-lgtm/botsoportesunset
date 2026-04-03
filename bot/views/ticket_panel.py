import discord
from discord.ui import View, Button
from core.db import create_ticket, get_ticket_number
from bot.views.ticket_controls import TicketControls

class TicketPanel(View):
    def __init__(self, botones):
        super().__init__(timeout=None)

        # botones = lista de dicts
        # [{label, categoria_id, tipo}]

        for b in botones:
            self.add_item(TicketButton(b["label"], b["categoria_id"], b["tipo"]))


class TicketButton(Button):
    def __init__(self, label, category_id, tipo):
       super().__init__(
    label=label,
    style=discord.ButtonStyle.green,
    custom_id=f"ticket_{tipo}"
)
        self.category_id = category_id
        self.tipo = tipo

    async def callback(self, interaction: discord.Interaction):

        # anti duplicado
        for ch in interaction.guild.text_channels:
            if str(interaction.user.id) in ch.name:
                return await interaction.response.send_message(
                    "❌ Ya tienes un ticket abierto", ephemeral=True
                )

        category = interaction.guild.get_channel(self.category_id)

        numero = get_ticket_number(self.tipo)
        nombre = f"{self.tipo}-{numero}"

        channel = await interaction.guild.create_text_channel(
            name=nombre,
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
