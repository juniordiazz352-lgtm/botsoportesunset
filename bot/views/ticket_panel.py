import discord
from core.db import cursor, conn
from views.ticket_controls import TicketControlsView


class TicketPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 Crear Ticket", style=discord.ButtonStyle.green)
    async def crear(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            overwrites=overwrites
        )

        cursor.execute(
            "INSERT INTO tickets (user_id, channel_id, claimed_by) VALUES (?, ?, ?)",
            (interaction.user.id, channel.id, None)
        )
        conn.commit()

        embed = discord.Embed(
            title="🎫 Ticket creado",
            description="Un staff te atenderá pronto",
            color=discord.Color.green()
        )

        await channel.send(
            content=interaction.user.mention,
            embed=embed,
            view=TicketControlsView()
        )

        await interaction.response.send_message("✅ Ticket creado", ephemeral=True)
