import discord


class ReviewView(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=None)
        self.user = user
@discord.ui.button(label="✅ Aprobar", style=discord.ButtonStyle.green)
async def aprobar(self, interaction: discord.Interaction, button: discord.ui.Button):

    await interaction.response.send_message(
        "✍️ Escribe el mensaje que quieres enviar al usuario:",
        ephemeral=True
    )

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    try:
        msg = await interaction.client.wait_for("message", timeout=60, check=check)
    except:
        return await interaction.followup.send("⏰ Tiempo agotado", ephemeral=True)

    # enviar mensaje personalizado
    await self.user.send(f"🎉 Has sido aprobado\n\n📩 Mensaje:\n{msg.content}")

    await interaction.followup.send("✅ Aprobado correctamente", ephemeral=True)

    @discord.ui.button(label="❌ Rechazar", style=discord.ButtonStyle.red)
    async def rechazar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.user.send("❌ Rechazado")
        await interaction.response.send_message("Rechazado", ephemeral=True)
