import discord
from core.db import cursor
from bot.views.ticket_controls import TicketControlsView

cooldowns = {}

class TicketPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        cursor.execute("SELECT nombre, emoji FROM ticket_types")
        tipos = cursor.fetchall()

        for nombre, emoji in tipos:
            self.add_item(TicketButton(nombre, emoji))


class TicketButton(discord.ui.Button):
    def __init__(self, nombre, emoji):
        super().__init__(
            label=nombre,
            emoji=emoji,
            style=discord.ButtonStyle.blurple
        import time

user_id = interaction.user.id
now = time.time()

if user_id in cooldowns and now - cooldowns[user_id] < 10:
    return await interaction.response.send_message(
        "⏳ Espera antes de crear otro ticket.",
        ephemeral=True
    )

cooldowns[user_id] = now)
        self.nombre = nombre

    async def callback(self, interaction: discord.Interaction):

        guild = interaction.guild
        user = interaction.user

        channel = await guild.create_text_channel(
            f"{self.nombre}-{user.name}"
        )

        await channel.send(
            f"{user.mention}",
            embed=discord.Embed(
                title="🎫 Ticket abierto",
                description="El Equipo de Soporte te respondera en un momento,No tienen un horario definido pero llegaran en breve,porfavor se paciente",
                color=discord.Color.green()
            ),
            view=TicketControlsView()
        )

        await interaction.response.send_message(
            f"✅ Ticket creado: {channel.mention}",
            ephemeral=True
        )
