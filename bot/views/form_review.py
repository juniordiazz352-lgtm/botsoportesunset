import discord
from core.utils import send_log


class FormReviewView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Aprobar", style=discord.ButtonStyle.green)
    async def aprobar(self, interaction, button):

        user_id = int(interaction.message.embeds[0].footer.text.split(": ")[1])
        user = await interaction.client.fetch_user(user_id)

        await user.send("✅ Aprobado")

        await send_log(interaction.guild, f"✅ {user} aprobado por {interaction.user}")

        await interaction.response.send_message("✅ Aprobado")

    @discord.ui.button(label="❌ Rechazar", style=discord.ButtonStyle.red)
    async def rechazar(self, interaction, button):

        user_id = int(interaction.message.embeds[0].footer.text.split(": ")[1])
        user = await interaction.client.fetch_user(user_id)

        await user.send("❌ Rechazado")

        await send_log(interaction.guild, f"❌ {user} rechazado por {interaction.user}")

        await interaction.response.send_message("❌ Rechazado")
