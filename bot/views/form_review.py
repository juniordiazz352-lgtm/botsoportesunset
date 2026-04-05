import discord


class ReviewView(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=None)
        self.user = user

    @discord.ui.button(label="✅ Aprobar", style=discord.ButtonStyle.green)
    async def aprobar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.user.send("🎉 Aprobado")
        await interaction.response.send_message("Aprobado", ephemeral=True)

    @discord.ui.button(label="❌ Rechazar", style=discord.ButtonStyle.red)
    async def rechazar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.user.send("❌ Rechazado")
        await interaction.response.send_message("Rechazado", ephemeral=True)
