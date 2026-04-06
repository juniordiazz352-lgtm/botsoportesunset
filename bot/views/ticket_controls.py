import discord
from discord.ui import View, button
import sqlite3
import datetime
import io

DB_PATH = "tickets.db"
STAFF_ROLE_ID = 123456789012345678  # 🔥 CAMBIAR POR TU ROL STAFF

class TicketControlsView(View):
    def __init__(self):
        super().__init__(timeout=None)

    # =========================
    # 🔒 BOTÓN CERRAR
    # =========================
    @button(label="Cerrar", style=discord.ButtonStyle.red, emoji="🔒", custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not self.is_staff(interaction):
            return await interaction.response.send_message("❌ No eres staff.", ephemeral=True)

        await interaction.response.send_message("🔒 Cerrando ticket...", ephemeral=True)

        await self.save_transcript(interaction)

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
    # 👤 BOTÓN RECLAMAR
    # =========================
    @button(label="Reclamar", style=discord.ButtonStyle.green, emoji="👤", custom_id="claim_ticket")
    async def claim_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not self.is_staff(interaction):
            return await interaction.response.send_message("❌ No eres staff.", ephemeral=True)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE tickets SET claimed_by = ? WHERE channel_id = ?",
            (interaction.user.id, interaction.channel.id)
        )

        conn.commit()
        conn.close()

        await interaction.response.send_message(f"👤 Ticket reclamado por {interaction.user.mention}")

    # =========================
    # 📄 BOTÓN TRANSCRIPT
    # =========================
    @button(label="Transcript", style=discord.ButtonStyle.blurple, emoji="📄", custom_id="transcript_ticket")
    async def transcript_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not self.is_staff(interaction):
            return await interaction.response.send_message("❌ No eres staff.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)

        transcript = await self.generate_transcript(interaction.channel)

        file = discord.File(io.BytesIO(transcript.encode()), filename="transcript.txt")

        await interaction.followup.send("📄 Transcript generado:", file=file, ephemeral=True)

    # =========================
    # 🧠 FUNCIONES AUXILIARES
    # =========================

    def is_staff(self, interaction: discord.Interaction):
        return any(role.id == STAFF_ROLE_ID for role in interaction.user.roles)

    async def generate_transcript(self, channel):
        messages = []
        async for msg in channel.history(limit=None, oldest_first=True):
            time = msg.created_at.strftime("%Y-%m-%d %H:%M")
            messages.append(f"[{time}] {msg.author}: {msg.content}")

        return "\n".join(messages)

    async def save_transcript(self, interaction):
        transcript = await self.generate_transcript(interaction.channel)

        file = discord.File(io.BytesIO(transcript.encode()), filename="transcript.txt")

        try:
            await interaction.user.send("📄 Aquí tienes el transcript del ticket:", file=file)
        except:
            pass
