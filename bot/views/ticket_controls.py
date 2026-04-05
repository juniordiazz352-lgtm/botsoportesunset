import discord
from core.db import cursor, conn
from core.transcripts import generar_transcript


class TicketControlsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # 🔒 CERRAR
    @discord.ui.button(label="🔒 Cerrar", style=discord.ButtonStyle.red)
    async def cerrar(self, interaction: discord.Interaction, button: discord.ui.Button):

        channel = interaction.channel

        cursor.execute("SELECT user_id FROM tickets WHERE channel_id=?", (channel.id,))
        data = cursor.fetchone()

        user = interaction.guild.get_member(data[0]) if data else None

        archivo = await generar_transcript(channel)

        # DM usuario
        if user:
            try:
                await user.send(
                    f"🧾 Transcript de tu ticket `{channel.name}`",
                    file=discord.File(archivo)
                )
            except:
                pass

        # logs
        await interaction.response.send_message("🔒 Ticket cerrado", ephemeral=True)

        await channel.edit(name=f"cerrado-{channel.name}")

    # 🗑 ELIMINAR
    @discord.ui.button(label="🗑 Eliminar", style=discord.ButtonStyle.gray)
    async def eliminar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🗑 Eliminando...", ephemeral=True)
        await interaction.channel.delete()

    # ✏️ RENOMBRAR
    @discord.ui.button(label="✏️ Renombrar", style=discord.ButtonStyle.blurple)
    async def rename(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message("✍️ Escribe el nuevo nombre:", ephemeral=True)

        def check(m):
            return m.author == interaction.user

        try:
            msg = await interaction.client.wait_for("message", timeout=60, check=check)
        except:
            return await interaction.followup.send("⏰ Tiempo agotado", ephemeral=True)

        await interaction.channel.edit(name=msg.content)
        await interaction.followup.send("✅ Renombrado", ephemeral=True)

    # 👤 CLAIM
    @discord.ui.button(label="👤 Reclamar", style=discord.ButtonStyle.green)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):

        cursor.execute(
            "UPDATE tickets SET claimed_by=? WHERE channel_id=?",
            (interaction.user.id, interaction.channel.id)
        )
        conn.commit()

        await interaction.response.send_message(
            f"👤 Ticket reclamado por {interaction.user.mention}"
        )

    # 🔓 REABRIR
    @discord.ui.button(label="🔓 Reabrir", style=discord.ButtonStyle.green)
    async def reopen(self, interaction: discord.Interaction, button: discord.ui.Button):

        nombre = interaction.channel.name.replace("cerrado-", "")

        await interaction.channel.edit(name=nombre)

        await interaction.response.send_message("🔓 Ticket reabierto")

    # 🔐 BLOQUEAR
    @discord.ui.button(label="🔐 Bloquear", style=discord.ButtonStyle.gray)
    async def lock(self, interaction: discord.Interaction, button: discord.ui.Button):

        user = interaction.guild.default_role

        await interaction.channel.set_permissions(user, send_messages=False)

        await interaction.response.send_message("🔐 Ticket bloqueado")

    # 🧾 TRANSCRIPT
    @discord.ui.button(label="🧾 Transcript", style=discord.ButtonStyle.blurple)
    async def transcript(self, interaction: discord.Interaction, button: discord.ui.Button):

        archivo = await generar_transcript(interaction.channel)

        await interaction.response.send_message(
            "🧾 Transcript generado",
            file=discord.File(archivo),
            ephemeral=True
        )
