import discord
from core.db import cursor
from bot.views.form_review import FormReviewView
from core.utils import send_log


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

        nombre = self.values[0]
        preguntas = self.forms[nombre]
        respuestas = []

        try:
            await interaction.user.send(f"📋 {nombre}")

            for p in preguntas:
                await interaction.user.send(p)

                def check(m):
                    return m.author == interaction.user and isinstance(m.channel, discord.DMChannel)

                msg = await interaction.client.wait_for("message", check=check)
                respuestas.append(msg.content)

            cursor.execute("SELECT valor FROM config WHERE clave='forms_channel'")
            data = cursor.fetchone()

            canal = interaction.guild.get_channel(int(data[0]))

            embed = discord.Embed(title=nombre, color=discord.Color.blue())

            for p, r in zip(preguntas, respuestas):
                embed.add_field(name=p, value=r, inline=False)

            embed.set_footer(text=f"Usuario: {interaction.user.id}")

            await canal.send(embed=embed, view=FormReviewView())

            await send_log(interaction.guild, f"📋 Form enviado por {interaction.user}")

            await interaction.response.send_message("📩 Revisa DM", ephemeral=True)

        except:
            await interaction.response.send_message("❌ No puedo enviarte DM", ephemeral=True)
