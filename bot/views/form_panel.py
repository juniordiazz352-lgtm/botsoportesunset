import discord
from discord.ui import View, Select
import json
from bot.views.form_modal import DynamicFormModal

FORMS_FILE = "forms.json"


class FormSelect(Select):
    def __init__(self):

        options = []

        try:
            with open(FORMS_FILE, "r") as f:
                data = json.load(f)

            for name in data.keys():
                options.append(
                    discord.SelectOption(
                        label=name.capitalize(),
                        description=f"Formulario: {name}",
                        emoji="📋"
                    )
                )

        except:
            pass

        if not options:
            options.append(
                discord.SelectOption(
                    label="No hay formularios",
                    description="Crea uno con !crear_form",
                    emoji="⚠️"
                )
            )

        super().__init__(
            placeholder="📋 Selecciona un formulario",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="form_select"
        )

    async def callback(self, interaction: discord.Interaction):

        form_name = self.values[0].lower()

        with open(FORMS_FILE, "r") as f:
            data = json.load(f)

        preguntas = data.get(form_name, [])

        modal = DynamicFormModal(form_name, preguntas)

        await interaction.response.send_modal(modal)


class FormPanel(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(FormSelect())
