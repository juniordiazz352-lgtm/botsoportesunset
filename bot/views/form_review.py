import discord

class FormReviewView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    # =========================
    # ✅ APROBAR
    # =========================
    @discord.ui.button(label="Aprobar", style=discord.ButtonStyle.green, emoji="✅")
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):

        user = interaction.guild.get_member(self.user_id)

        if user:
            try:
                await user.send("✅ Tu formulario fue aprobado.")
            except:
                pass

        await interaction.response.send_message("✅ Formulario aprobado", ephemeral=True)

    # =========================
    # ❌ RECHAZAR
    # =========================
    @discord.ui.button(label="Rechazar", style=discord.ButtonStyle.red, emoji="❌")
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):

        user = interaction.guild.get_member(self.user_id)

        if user:
            try:
                await user.send("❌ Tu formulario fue rechazado.")
            except:
                pass

        await interaction.response.send_message("❌ Formulario rechazado", ephemeral=True)

    # =========================
    # 💬 RESPONDER
    # =========================
    @discord.ui.button(label="Responder", style=discord.ButtonStyle.blurple, emoji="💬")
    async def responder(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_modal(ResponseModal(self.user_id))


# =========================
# 🧾 MODAL RESPUESTA
# =========================
class ResponseModal(discord.ui.Modal, title="Enviar respuesta"):

    mensaje = discord.ui.TextInput(
        label="Mensaje para el usuario",
        style=discord.TextStyle.paragraph
    )

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    async def on_submit(self, interaction: discord.Interaction):

        user = interaction.guild.get_member(self.user_id)

        if user:
            try:
                await user.send(f"💬 Respuesta del staff:\n\n{self.mensaje.value}")
                await interaction.response.send_message("✅ Mensaje enviado", ephemeral=True)
            except:
                await interaction.response.send_message("❌ No se pudo enviar DM", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Usuario no encontrado", ephemeral=True)
