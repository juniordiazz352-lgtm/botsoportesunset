import discord
from bot.core.db import cursor, conn

TIEMPO = 150  # 2 min 30 seg


# 🔘 SELECT MENU
class FormSelect(discord.ui.Select):
    def __init__(self):
        cursor.execute("SELECT nombre FROM formularios")
        forms = cursor.fetchall()

        options = []

        for f in forms:
            options.append(
                discord.SelectOption(
                    label=f[0],
                    description=f"Completar formulario {f[0]}",
                    value=f[0]
                )
            )

        if not options:
            options.append(
                discord.SelectOption(
                    label="Sin formularios",
                    value="none"
                )
            )

        super().__init__(
            placeholder="📋 Selecciona un formulario",
            options=options,
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "none":
            return await interaction.response.send_message("❌ No hay formularios", ephemeral=True)

        nombre = self.values[0]

        await interaction.response.send_message(
            "📩 Revisa tu DM\n⏱ Tienes 2 minutos 30 segundos por pregunta",
            ephemeral=True
        )

        await iniciar_formulario(interaction, nombre)


# 🎛 VIEW
class FormPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(FormSelect())


# 🧠 SISTEMA DE FORMULARIO
async def iniciar_formulario(interaction: discord.Interaction, nombre_form):

    user = interaction.user
    bot = interaction.client

    # 🔍 obtener preguntas
    cursor.execute("SELECT pregunta FROM preguntas WHERE formulario=?", (nombre_form,))
    data = cursor.fetchall()

    if not data:
        return await user.send("❌ Este formulario no tiene preguntas")

    preguntas = [p[0] for p in data]
    respuestas = []

    try:
        await user.send(
            f"📋 **Formulario: {nombre_form}**\n\n"
            "⏱ Tienes 2 minutos 30 segundos por pregunta.\n"
            "Si no respondes a tiempo, se cancelará."
        )
    except:
        return await interaction.followup.send("❌ No puedo enviarte DM", ephemeral=True)

    def check(m):
        return m.author == user and isinstance(m.channel, discord.DMChannel)

    # 🔁 preguntas
    for pregunta in preguntas:
        await user.send(f"❓ {pregunta}")

        try:
            msg = await bot.wait_for("message", timeout=TIEMPO, check=check)
            respuestas.append(msg.content)

        except:
            await user.send("⏰ Tiempo agotado, formulario cancelado")
            return

    # 📤 enviar a staff
    cursor.execute("SELECT valor FROM config WHERE clave='logs'")
    canal_data = cursor.fetchone()

    if canal_data:
        canal = interaction.guild.get_channel(int(canal_data[0]))
    else:
        canal = None

    embed = discord.Embed(
        title=f"📋 Nuevo formulario: {nombre_form}",
        color=discord.Color.blurple()
    )

    for i, pregunta in enumerate(preguntas):
        embed.add_field(name=pregunta, value=respuestas[i], inline=False)

    embed.add_field(name="Usuario", value=user.mention)

    if canal:
        from bot.views.form_review import ReviewView
        await canal.send(embed=embed, view=ReviewView(user))

    await user.send("✅ Formulario enviado correctamente")
