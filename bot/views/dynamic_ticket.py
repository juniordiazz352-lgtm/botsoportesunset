import discord
from core.db import cursor
from bot.views.ticket_actions import TicketActions
from core.utils import create_ticket


class DynamicTicketView(discord.ui.View):
    def __init__(self, botones):
        super().__init__(timeout=None)

        for nombre in botones:
            self.add_item(TicketButton(nombre))


class TicketButton(discord.ui.Button):
    def __init__(self, nombre):
        super().__init__(label=nombre, style=discord.ButtonStyle.green)
        self.nombre_ticket = nombre

    async def callback(self, interaction):

        guild = interaction.guild
        user = interaction.user

        cursor.execute("SELECT valor FROM config WHERE clave='ticket_category'")
        data = cursor.fetchone()

        if not data:
            return await interaction.response.send_message("❌ No configurado", ephemeral=True)

        category = guild.get_channel(int(data[0]))

        # anti duplicados
        for ch in category.channels:
            if ch.topic and str(user.id) in ch.topic:
                return await interaction.response.send_message(
                    "❌ Ya tienes un ticket",
                    ephemeral=True
                )

        channel = await category.create_text_channel(
            name=f"{self.nombre_ticket}-{user.name}",
            topic=str(user.id)
        )

        create_ticket(channel.id, user.id, self.nombre_ticket)

        embed = discord.Embed(
            title=f"🎟️ {self.nombre_ticket}",
            description="Usa los botones para gestionar el ticket",
            color=discord.Color.green()
        )

        from bot.views.ticket_actions import TicketActions

        await channel.send(
            content=user.mention,
            embed=embed,
            view=TicketActions()
        )

        await interaction.response.send_message(
            f"✅ Ticket creado: {channel.mention}",
            ephemeral=True
        )
