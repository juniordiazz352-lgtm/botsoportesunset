import discord
from discord.ui import View, button
from core.db import add_question

class FormBuilder(View):
    def __init__(self, form_name):
        super().__init__(timeout=None)
        self.form_name = form_name

    @button(label="➕ Añadir pregunta", style=discord.ButtonStyle.green)
    async def add_q(self, interaction: discord.Interaction, _):

        await interaction.response.send_message(
            "Escribe la pregunta:", ephemeral=True
        )

        def check(m): return m.author == interaction.user
        msg = await interaction.client.wait_for("message", check=check)

        add_question(self.form_name, msg.content)

        await interaction.followup.send("✅ Pregunta añadida")

    @button(label="✅ Finalizar", style=discord.ButtonStyle.blurple)
    async def finish(self, interaction: discord.Interaction, _):
        await interaction.response.send_message("Formulario guardado")
