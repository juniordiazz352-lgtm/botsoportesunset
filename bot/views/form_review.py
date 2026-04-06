import discord


class FormReviewView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Aprobar", style=discord.ButtonStyle.green)
    async def aprobar(self, interaction: discord.Interaction, button):

        user_id = int(interaction.message.embeds[0].footer.text.split(": ")[1])
        user = await interaction.client.fetch_user(user_id)

        await user.send("✅ Tu formulario fue aprobado")
        await interaction.response.send_message("✅ Aprobado")

    @discord.ui.button(label="❌ Rechazar", style=discord.ButtonStyle.red)
    async def rechazar(self, interaction: discord.Interaction, button):

        user_id = int(interaction.message.embeds[0].footer.text.split(": ")[1])
        user = await interaction.client.fetch_user(user_id)

        await user.send("❌ Tu formulario fue rechazado")
        await interaction.response.send_message("❌ Rechazado")
