import discord
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

    async def log(self, guild, mensaje):
        cursor.execute("SELECT valor FROM config WHERE clave='logs_channel'")
        data = cursor.fetchone()
        if data:
            canal = guild.get_channel(int(data[0]))
            if canal:
                await canal.send(mensaje)

    @discord.ui.button(label="🔒 Cerrar", style=discord.ButtonStyle.red)
    async def cerrar(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not es_staff(interaction.user, interaction.guild):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        archivo = await generar_transcript(interaction.channel)

        cursor.execute("SELECT user_id FROM tickets WHERE channel_id=?", (interaction.channel.id,))
        data = cursor.fetchone()
        user = interaction.guild.get_member(data[0]) if data else None

        if user:
            try:
                await user.send("🧾 Aquí tienes tu ticket", file=discord.File(archivo))
            except:
                pass

        await self.log(interaction.guild, f"🔒 Ticket cerrado: {interaction.channel.name}")

        await interaction.channel.edit(name=f"cerrado-{interaction.channel.name}")
        await interaction.response.send_message("🔒 Cerrado", ephemeral=True)

    @discord.ui.button(label="👤 Reclamar", style=discord.ButtonStyle.green)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not es_staff(interaction.user, interaction.guild):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        cursor.execute(
            "UPDATE tickets SET claimed_by=? WHERE channel_id=?",
            (interaction.user.id, interaction.channel.id)
        )
        conn.commit()

        await self.log(interaction.guild, f"👤 {interaction.user} reclamó ticket")

        await interaction.response.send_message(f"👤 Reclamado por {interaction.user.mention}")

    @discord.ui.button(label="🧾 Transcript", style=discord.ButtonStyle.blurple)
    async def transcript(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not es_staff(interaction.user, interaction.guild):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        archivo = await generar_transcript(interaction.channel)

        await interaction.response.send_message(file=discord.File(archivo), ephemeral=True)
