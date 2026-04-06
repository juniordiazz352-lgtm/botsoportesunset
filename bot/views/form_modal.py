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

        embed.set_footer(text=f"Usuario: {interaction.user}")

        channel = interaction.guild.get_channel(1489086693188305040)

        if channel:
            await channel.send(embed=embed)

        await interaction.response.send_message(
            "✅ Formulario enviado correctamente",
            ephemeral=True
        )
