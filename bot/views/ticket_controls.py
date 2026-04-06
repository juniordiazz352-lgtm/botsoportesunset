import discord
from discord.ui import View, button
import sqlite3
import io
import datetime

DB_PATH = "tickets.db"
STAFF_ROLE_ID = 1472478801710678258
LOG_CHANNEL_ID = 1489086693188305040


class TicketControlsView(View):
    def __init__(self):
        super().__init__(timeout=None)

    # =========================
    # 🔒 CERRAR TICKET
    # =========================
    @button(label="Cerrar", style=discord.ButtonStyle.red, emoji="🔒", custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not self.is_staff(interaction):
            return await interaction.response.send_message("❌ No tienes permisos.", ephemeral=True)

        await interaction.response.send_message("🔒 Cerrando ticket...", ephemeral=True)

        transcript = await self.generate_html_transcript(interaction.channel)

        file = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript-{interaction.channel.name}.html"
        )

        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)

        if log_channel:
            await log_channel.send(
                content=f"📁 Ticket cerrado por {interaction.user.mention}",
                file=file
            )

        # borrar de DB
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM tickets WHERE channel_id = ?",
            (interaction.channel.id,)
        )

        conn.commit()
        conn.close()

        await interaction.channel.delete()

    # =========================
    # 👤 RECLAMAR
    # =========================
    @button(label="Reclamar", style=discord.ButtonStyle.green, emoji="👤", custom_id="claim_ticket")
    async def claim_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not self.is_staff(interaction):
            return await interaction.response.send_message("❌ No tienes permisos.", ephemeral=True)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT claimed_by FROM tickets WHERE channel_id = ?",
            (interaction.channel.id,)
        )
        result = cursor.fetchone()

        if result and result[0]:
            return await interaction.response.send_message("⚠️ Este ticket ya fue reclamado.", ephemeral=True)

        cursor.execute(
            "UPDATE tickets SET claimed_by = ? WHERE channel_id = ?",
            (interaction.user.id, interaction.channel.id)
        )

        conn.commit()
        conn.close()

        # renombrar canal
        try:
            await interaction.channel.edit(name=f"ticket-{interaction.user.name}")
        except:
            pass

        await interaction.response.send_message(f"👤 Ticket reclamado por {interaction.user.mention}")

        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(f"👤 {interaction.user.mention} reclamó {interaction.channel.mention}")

    # =========================
    # 🔓 REABRIR
    # =========================
    @button(label="Reabrir", style=discord.ButtonStyle.gray, emoji="🔓", custom_id="reopen_ticket")
    async def reopen_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not self.is_staff(interaction):
            return await interaction.response.send_message("❌ No tienes permisos.", ephemeral=True)

        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)

        await interaction.response.send_message("🔓 Ticket reabierto")

    # =========================
    # 🔐 BLOQUEAR
    # =========================
    @button(label="Bloquear", style=discord.ButtonStyle.gray, emoji="🔐", custom_id="lock_ticket")
    async def lock_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not self.is_staff(interaction):
            return await interaction.response.send_message("❌ No tienes permisos.", ephemeral=True)

        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)

        await interaction.response.send_message("🔐 Ticket bloqueado")

    # =========================
    # 📄 TRANSCRIPT HTML
    # =========================
    @button(label="Transcript", style=discord.ButtonStyle.blurple, emoji="📄", custom_id="transcript_ticket")
    async def transcript_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not self.is_staff(interaction):
            return await interaction.response.send_message("❌ No tienes permisos.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)

        transcript = await self.generate_html_transcript(interaction.channel)

        file = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript-{interaction.channel.name}.html"
        )

        await interaction.followup.send("📄 Transcript generado:", file=file, ephemeral=True)

    # =========================
    # 🧠 FUNCIONES
    # =========================

    def is_staff(self, interaction: discord.Interaction):
        return any(role.id == STAFF_ROLE_ID for role in interaction.user.roles)

    async def generate_html_transcript(self, channel):
        messages_html = ""

        async for msg in channel.history(limit=None, oldest_first=True):
            time = msg.created_at.strftime("%Y-%m-%d %H:%M")
            messages_html += f"""
            <p><strong>{msg.author}</strong> [{time}]<br>{msg.content}</p>
            """

        html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial; background: #111; color: #eee; }}
                p {{ border-bottom: 1px solid #333; padding: 5px; }}
            </style>
        </head>
        <body>
            <h2>Transcript - {channel.name}</h2>
            {messages_html}
        </body>
        </html>
        """

        return html
