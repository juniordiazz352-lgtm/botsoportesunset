import discord
from core.db import cursor
from bot.views.ticket_actions import TicketActions


class DynamicTicketView(discord.ui.View):
    def __init__(self, botones):
        super().__init__(timeout=None)

        for nombre in botones:
            self.add_item(TicketButton(nombre))


class TicketButton(discord.ui.Button):
    def __init__(self, nombre):
        super().__init__(label=nombre, style=discord.ButtonStyle.green)
        self.nombre_ticket = nombre

    async def callback(self, interaction: discord.Interaction):

        guild = interaction.guild
        user = interaction.user

        cursor.execute("SELECT valor FROM config WHERE clave='ticket_category'")
        data = cursor.fetchone()

        if not data:
            return await interaction.response.send_message("❌ No configurado", ephemeral=True)

        category = guild.get_channel(int(data[0]))

        if not category:
            return await interaction.response.send_message("❌ Categoría inválida", ephemeral=True)

        # 🚫 Anti duplicados
        for ch in category.channels:
            if ch.topic and str(user.id) in ch.topic:
                return await interaction.response.send_message(
                    "❌ Ya tienes un ticket abierto",
                    ephemeral=True
                )

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True)
        }

        channel = await category.create_text_channel(
            name=f"{self.nombre_ticket}-{user.name}".lower().replace(" ", "-"),
            overwrites=overwrites,
            topic=str(user.id)
        )

        embed = discord.Embed(
            title=f"🎟️ Ticket: {self.nombre_ticket}",
            description="Un staff te atenderá pronto.\nUsa los botones para gestionar el ticket.",
            color=discord.Color.green()
        )

        embed.set_footer(text=f"Usuario ID: {user.id}")

        await channel.send(
            content=user.mention,
            embed=embed,
            view=TicketActions()
        )

        await interaction.response.send_message(
            f"✅ Ticket creado: {channel.mention}",
            ephemeral=True
        )
