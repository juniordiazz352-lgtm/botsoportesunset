import discord
from discord.ext import commands
from discord.ui import Modal, TextInput
from core.db import get_forms, save_response
from core.config import FORMS_CHANNEL_ID
from bot.views.form_review import FormReview

class DynamicForm(Modal):
    def __init__(self, name):
        super().__init__(title=name)
        self.name = name
        self.inputs = []

        for q in get_forms()[name]:
            inp = TextInput(label=q)
            self.inputs.append(inp)
            self.add_item(inp)

    async def on_submit(self, interaction: discord.Interaction):

        answers = {i.label: i.value for i in self.inputs}

        form_id = save_response(interaction.user.id, self.name, answers)

        channel = interaction.guild.get_channel(FORMS_CHANNEL_ID)

        embed = discord.Embed(
            title=f"📋 Nuevo formulario #{form_id}",
            description=f"Usuario: {interaction.user.mention}"
        )

        for k, v in answers.items():
            embed.add_field(name=k, value=v, inline=False)

        await channel.send(
            embed=embed,
            view=FormReview(form_id, interaction.user.id)
        )

        await interaction.response.send_message(
            "✅ Formulario enviado", ephemeral=True
        )
