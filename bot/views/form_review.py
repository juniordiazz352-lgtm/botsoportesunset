import discord
from discord.ui import View, button
from core.db import update_form_status
from core.logs import log

await log(interaction, f"Formulario {self.form_id} aprobado por {interaction.user}")

class FormReview(View):
    def __init__(self, form_id, user_id):
        super().__init__(timeout=None)
        self.form_id = form_id
        self.user_id = user_id

    @button(label="✅ Aprobar", style=discord.ButtonStyle.green)
    async def approve(self, interaction: discord.Interaction, _):
        update_form_status(self.form_id, "approved")

        user = await interaction.client.fetch_user(self.user_id)
        await user.send("✅ Tu formulario fue APROBADO")

        await interaction.response.send_message("Aprobado")

    @button(label="❌ Rechazar", style=discord.ButtonStyle.red)
    async def reject(self, interaction: discord.Interaction, _):
        update_form_status(self.form_id, "rejected")

        user = await interaction.client.fetch_user(self.user_id)
        await user.send("❌ Tu formulario fue RECHAZADO")

        await interaction.response.send_message("Rechazado")
