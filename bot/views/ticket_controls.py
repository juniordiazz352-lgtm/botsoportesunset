import discord
from discord.ext import commands
from core.db import cursor, conn
from core.transcripts import generar_transcript


def es_staff(member, guild):
    cursor.execute("SELECT valor FROM config WHERE clave='staff_role'")
    data = cursor.fetchone()
    if not data:
        return False
    rol = guild.get_role(int(data[0]))
    return rol in member.roles if rol else False


class TicketControlsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # 🔒 CERRAR
    @discord.ui.button(label="🔒 Cerrar", style=discord.ButtonStyle.red)
    async def cerrar(self, interaction: discord.Interaction, button):

        if not es_staff(interaction.user, interaction.guild):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        archivo = await generar_transcript(interaction.channel)

        cursor.execute(
            "SELECT user_id FROM tickets WHERE channel_id=?",
            (interaction.channel.id,)
        )
        data = cursor.fetchone()

        user = interaction.guild.get_member(data[0]) if data else None

        if user:
            try:
                await user.send(
                    "🧾 Aquí tienes el transcript de tu ticket",
                    file=discord.File(archivo)
                )
            except:
                pass

        cursor.execute(
            "UPDATE tickets SET estado='cerrado' WHERE channel_id=?",
            (interaction.channel.id,)
        )
        conn.commit()

        await interaction.channel.edit(name=f"cerrado-{interaction.channel.name}")

        await interaction.response.send_message("🔒 Ticket cerrado", ephemeral=True)

    # 🗑 ELIMINAR
    @discord.ui.button(label="🗑 Eliminar", style=discord.ButtonStyle.gray)
    async def eliminar(self, interaction: discord.Interaction, button):

        if not es_staff(interaction.user, interaction.guild):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        await interaction.response.send_message("🗑 Eliminando ticket...", ephemeral=True)
        await interaction.channel.delete()

    # 👤 RECLAMAR
    @discord.ui.button(label="👤 Reclamar", style=discord.ButtonStyle.green)
    async def claim(self, interaction: discord.Interaction, button):

        if not es_staff(interaction.user, interaction.guild):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        cursor.execute(
            "UPDATE tickets SET claimed_by=? WHERE channel_id=?",
            (interaction.user.id, interaction.channel.id)
        )
        conn.commit()

        await interaction.response.send_message(
            f"👤 Ticket reclamado por {interaction.user.mention}"
        )

    # 🧾 TRANSCRIPT
    @discord.ui.button(label="🧾 Transcript", style=discord.ButtonStyle.blurple)
    async def transcript(self, interaction: discord.Interaction, button):

        if not es_staff(interaction.user, interaction.guild):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        archivo = await generar_transcript(interaction.channel)

        await interaction.response.send_message(
            "🧾 Transcript generado",
            file=discord.File(archivo),
            ephemeral=True
        )

    # ✏️ RENOMBRAR
    @discord.ui.button(label="✏️ Renombrar", style=discord.ButtonStyle.blurple)
    async def rename(self, interaction: discord.Interaction, button):

        if not es_staff(interaction.user, interaction.guild):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        await interaction.response.send_message("✍️ Escribe el nuevo nombre:", ephemeral=True)

        def check(m):
            return m.author == interaction.user

        try:
            msg = await interaction.client.wait_for("message", timeout=60, check=check)
        except:
            return await interaction.followup.send("⏰ Tiempo agotado", ephemeral=True)

        await interaction.channel.edit(name=msg.content)
        await interaction.followup.send("✅ Renombrado", ephemeral=True)

    # 🔓 REABRIR
    @discord.ui.button(label="🔓 Reabrir", style=discord.ButtonStyle.green)
    async def reopen(self, interaction: discord.Interaction, button):

        if not es_staff(interaction.user, interaction.guild):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        nombre = interaction.channel.name.replace("cerrado-", "")

        await interaction.channel.edit(name=nombre)

        cursor.execute(
            "UPDATE tickets SET estado='abierto' WHERE channel_id=?",
            (interaction.channel.id,)
        )
        conn.commit()

        await interaction.response.send_message("🔓 Ticket reabierto", ephemeral=True)

    # 🔐 BLOQUEAR
    @discord.ui.button(label="🔐 Bloquear", style=discord.ButtonStyle.gray)
    async def lock(self, interaction: discord.Interaction, button):

        if not es_staff(interaction.user, interaction.guild):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        await interaction.channel.set_permissions(
            interaction.guild.default_role,
            send_messages=False
        )

        await interaction.response.send_message("🔐 Ticket bloqueado", ephemeral=True)
