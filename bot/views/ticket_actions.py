import discord
from core.utils import send_log


class TicketActions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.claimed_by = None

    @discord.ui.button(label="🔒 Cerrar", style=discord.ButtonStyle.red)
    async def cerrar(self, interaction: discord.Interaction, button):

        await interaction.channel.set_permissions(
            interaction.guild.default_role,
            view_channel=False
        )

        await send_log(interaction.guild, f"🔒 Ticket cerrado por {interaction.user}")

        await interaction.response.send_message("🔒 Ticket cerrado")

    @discord.ui.button(label="🔓 Reabrir", style=discord.ButtonStyle.green)
    async def reabrir(self, interaction: discord.Interaction, button):

        await interaction.channel.set_permissions(
            interaction.guild.default_role,
            view_channel=False
        )

        await send_log(interaction.guild, f"🔓 Ticket reabierto por {interaction.user}")

        await interaction.response.send_message("🔓 Ticket reabierto")

    @discord.ui.button(label="🙋 Claim", style=discord.ButtonStyle.blurple)
    async def claim(self, interaction, button):

        if self.claimed_by:
            return await interaction.response.send_message(
                f"❌ Ya reclamado por {self.claimed_by}",
                ephemeral=True
            )

        self.claimed_by = interaction.user

        await send_log(interaction.guild, f"🙋 {interaction.user} reclamó un ticket")

        await interaction.response.send_message(f"🙋 {interaction.user.mention} reclamó el ticket")

    @discord.ui.button(label="🗑️ Eliminar", style=discord.ButtonStyle.danger)
    async def delete(self, interaction, button):

        await send_log(interaction.guild, f"🗑️ Ticket eliminado por {interaction.user}")

        await interaction.response.send_message("🗑️ Eliminando...")
        await interaction.channel.delete()
