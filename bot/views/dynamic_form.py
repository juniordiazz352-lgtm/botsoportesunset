import discord
from discord.ui import Modal, TextInput
from core.db import get_forms, save_response

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
        save_response(interaction.user.id, self.name, answers)

        await interaction.response.send_message(
            "✅ Formulario enviado", ephemeral=True
        )
