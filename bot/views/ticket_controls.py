import discord
from discord.ui import View, button, Modal, TextInput
from core.db import close_ticket
from core.config import STAFF_ROLE_ID

def is_staff(interaction):
    role = interaction.guild.get_role(STAFF_ROLE_ID)
    return role in interaction.user.roles

# ===== MODAL RENOMBRE =====
class RenameModal(Modal, title="Renombrar Ticket"):
    nombre = TextInput(label="Nuevo nombre")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.channel.edit(name=self.nombre.value)
        await interaction.response.send_message("✅ Nombre cambiado", ephemeral=True)

# ===== CONTROLES =====
class TicketControls(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label="🔒 Cerrar", style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, _):
        if not is_staff(interaction):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        close_ticket(interaction.channel.id)
        await interaction.channel.delete()

    @button(label="👤 Claim", style=discord.ButtonStyle.gray)
    async def claim(self, interaction: discord.Interaction, _):
        if not is_staff(interaction):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        await interaction.response.send_message(
            f"{interaction.user.mention} tomó el ticket"
        )

    @button(label="✏️ Renombrar", style=discord.ButtonStyle.blurple)
    async def rename(self, interaction: discord.Interaction, _):
        if not is_staff(interaction):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        await interaction.response.send_modal(RenameModal())
