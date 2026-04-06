import discord


class DynamicFormModal(discord.ui.Modal):

    def __init__(self, nombre, preguntas):
        super().__init__(title=f"Formulario: {nombre}")

        self.nombre = nombre

        for pregunta in preguntas[:5]:
            self.add_item(
                discord.ui.TextInput(
                    label=pregunta[:45],
                    required=True
                )
            )

  from bot.views.form_review import FormReviewView

async def on_submit(self, interaction: discord.Interaction):

    respuestas = "\n".join(
        f"**{child.label}**\n{child.value}"
        for child in self.children
    )

    embed = discord.Embed(
        title=f"📋 Nuevo formulario: {self.nombre}",
        description=respuestas,
        color=discord.Color.orange()
    )

    import json, os

FILE = "form_responses.json"

data = []

if os.path.exists(FILE):
    with open(FILE, "r") as f:
        data = json.load(f)

data.append({
    "user": str(interaction.user),
    "answers": respuestas
})

with open(FILE, "w") as f:
    json.dump(data, f, indent=4)
    
    embed.set_footer(text=f"Usuario: {interaction.user} | ID: {interaction.user.id}")

    channel = interaction.guild.get_channel(1489086693188305040)

    if channel:
        await channel.send(
            embed=embed,
            view=FormReviewView(interaction.user.id)
        )

    await interaction.response.send_message(
        "✅ Formulario enviado correctamente",
        ephemeral=True
    )
