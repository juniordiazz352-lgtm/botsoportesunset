import discord


class FormReviewView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Aprobar", style=discord.ButtonStyle.green)
    async def aprobar(self, interaction, button):

        footer = interaction.message.embeds[0].footer.text
        user_id = int(footer.split("|")[0].split(":")[1])
        form_name = footer.split("|")[1].split(":")[1]

        user = await interaction.client.fetch_user(user_id)

        await user.send(
            f"✅ **Formulario aprobado**\n📋 Formulario: {form_name}\n🎉 ¡Felicidades!"
        )

        await interaction.response.send_message("✅ Aprobado")

    @discord.ui.button(label="❌ Rechazar", style=discord.ButtonStyle.red)
    async def rechazar(self, interaction, button):

        footer = interaction.message.embeds[0].footer.text
        user_id = int(footer.split("|")[0].split(":")[1])
        form_name = footer.split("|")[1].split(":")[1]

        user = await interaction.client.fetch_user(user_id)

        await user.send(
            f"❌ **Formulario rechazado**\n📋 Formulario: {form_name}\n💡 Puedes intentarlo nuevamente."
        )

        await interaction.response.send_message("❌ Rechazado")
