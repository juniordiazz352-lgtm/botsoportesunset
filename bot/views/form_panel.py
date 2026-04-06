import discord
from discord.ext import commands
from core.db import cursor, conn

TIEMPO = 150


class FormSelect(discord.ui.Select):
    def __init__(self):
        cursor.execute("SELECT nombre FROM formularios")
        forms = cursor.fetchall()

        options = [
            discord.SelectOption(
                label=f[0],
                description=f"Aplicar a {f[0]}",
                emoji="📋"
            )
            for f in forms
        ]

        super().__init__(
            placeholder="📋 Selecciona formulario",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="📩 Formulario enviado",
            description="Revisa tu DM",
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

        await iniciar_formulario(interaction, self.values[0])


class FormPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(FormSelect())


async def iniciar_formulario(interaction, nombre):
    user = interaction.user
    bot = interaction.client

    cursor.execute("SELECT pregunta FROM preguntas WHERE formulario=?", (nombre,))
    preguntas = [p[0] for p in cursor.fetchall()]

    respuestas = []

    await user.send(f"📋 {nombre}\n⏱ 2:30 por pregunta")

    def check(m):
        return m.author == user and isinstance(m.channel, discord.DMChannel)

    for p in preguntas:
        await user.send(f"❓ {p}")

        try:
            msg = await bot.wait_for("message", timeout=TIEMPO, check=check)
            respuestas.append(msg.content)

            cursor.execute(
                "INSERT INTO respuestas VALUES (NULL, ?, ?, ?, ?)",
                (user.id, nombre, p, msg.content)
            )
            conn.commit()

        except:
            return await user.send("⏰ Tiempo agotado")

    cursor.execute("SELECT valor FROM config WHERE clave='forms_channel'")
    canal = cursor.fetchone()

    if canal:
        canal = interaction.guild.get_channel(int(canal[0]))

        embed = discord.Embed(
            title="📥 Nuevo formulario",
            description=f"👤 {user.mention}\n📋 {nombre}",
            color=discord.Color.blurple()
        )

        from views.form_review import ReviewView
        await canal.send(embed=embed, view=ReviewView(user, nombre))

    await user.send("✅ Formulario enviado")
