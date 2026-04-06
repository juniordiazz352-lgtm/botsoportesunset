import discord
from core.utils import save_response
from bot.views.form_review import FormReviewView


class FormPanelView(discord.ui.View):
    def __init__(self, forms):
        super().__init__(timeout=None)

        options = [discord.SelectOption(label=name) for name in forms]
        self.add_item(FormSelect(forms, options))


class FormSelect(discord.ui.Select):
    def __init__(self, forms, options):
        super().__init__(placeholder="Selecciona un formulario", options=options)
        self.forms = forms

    async def callback(self, interaction):

        data = self.forms[self.values[0]]

        nombre = self.values[0]
        preguntas = data["questions"]
        canal_id = data["channel_id"]

        respuestas = []

        try:
            await interaction.user.send(f"📋 Formulario: {nombre}")

            for p in preguntas:
                await interaction.user.send(p)

                def check(m):
                    return m.author == interaction.user and isinstance(m.channel, discord.DMChannel)

                msg = await interaction.client.wait_for("message", check=check)
                respuestas.append(msg.content)

            save_response(interaction.user.id, nombre, respuestas)

            canal = interaction.guild.get_channel(canal_id)

            embed = discord.Embed(title=nombre, color=discord.Color.blue())

            for p, r in zip(preguntas, respuestas):
                embed.add_field(name=p, value=r, inline=False)

            embed.set_footer(text=f"user:{interaction.user.id}|form:{nombre}")

            await canal.send(embed=embed, view=FormReviewView())

            await interaction.response.send_message("📩 Revisa DM", ephemeral=True)

        except:
            await interaction.response.send_message("❌ DM desactivados", ephemeral=True)
