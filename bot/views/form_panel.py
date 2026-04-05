import discord
from bot.core.db import cursor

TIEMPO = 150  # 2 min 30 seg


class FormSelect(discord.ui.Select):
    def __init__(self):
        cursor.execute("SELECT nombre FROM formularios")
        forms = cursor.fetchall()

        options = [
            discord.SelectOption(label=f[0], value=f[0])
            for f in forms
        ]

        if not options:
            options = [discord.SelectOption(label="No hay formularios", value="none")]

        super().__init__(placeholder="Selecciona un formulario", options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "none":
            return await interaction.response.send_message("❌ No hay formularios", ephemeral=True)

        await interaction.response.send_message("📩 Revisa tu DM", ephemeral=True)
        await iniciar_formulario(interaction, self.values[0])


class FormPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(FormSelect())


async def iniciar_formulario(interaction, nombre_form):
    user = interaction.user
    bot = interaction.client

    cursor.execute("SELECT pregunta FROM preguntas WHERE formulario=?", (nombre_form,))
    preguntas = [p[0] for p in cursor.fetchall()]

    if not preguntas:
        return await user.send("❌ Sin preguntas")

    respuestas = []

    try:
        await user.send(
            f"📋 {nombre_form}\n⏱ Tienes 2:30 por pregunta"
        )
    except:
        return

    def check(m):
        return m.author == user and isinstance(m.channel, discord.DMChannel)

    for pregunta in preguntas:
        await user.send(pregunta)

        try:
            msg = await bot.wait_for("message", timeout=TIEMPO, check=check)
            respuestas.append(msg.content)
        except:
            await user.send("⏰ Tiempo agotado")
            return

    # enviar resultados
    cursor.execute("SELECT valor FROM config WHERE clave='forms_channel'")
    canal_id = cursor.fetchone()

    if canal_id:
        canal = interaction.guild.get_channel(int(canal_id[0]))

        embed = discord.Embed(title=f"Formulario: {nombre_form}")

        for i, p in enumerate(preguntas):
            embed.add_field(name=p, value=respuestas[i], inline=False)

        from bot.views.form_review import ReviewView
        await canal.send(embed=embed, view=ReviewView(user))

    await user.send("✅ Formulario enviado")
