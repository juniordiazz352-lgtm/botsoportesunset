import discord
from discord.ui import View, button, Modal, TextInput
from core.db import close_ticket
from core.config import STAFF_ROLE_ID
from core.transcripts import generar_transcript

def is_staff(interaction):
    role = interaction.guild.get_role(STAFF_ROLE_ID)
    return role in interaction.user.roles

# ===== MODAL RENOMBRE =====
class RenameModal(Modal, title="Renombrar Ticket"):
    nombre = TextInput(label="Nuevo nombre")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.channel.edit(name=self.nombre.value)
        await interaction.response.send_message("✅ Nombre cambiado", ephemeral=True)

# ===== CONTROLES =====
class TicketControls(View):
    def __init__(self):
        super().__init__(timeout=None)

   from core.db import cursor
from core.transcripts import generar_transcript


@discord.ui.button(label="🔒 Cerrar", style=discord.ButtonStyle.red)
async def cerrar(self, interaction: discord.Interaction, button: discord.ui.Button):

    channel = interaction.channel

    # 🧠 obtener dueño del ticket
    cursor.execute("SELECT user_id FROM tickets WHERE channel_id=?", (channel.id,))
    data = cursor.fetchone()

    user = None
    if data:
        user = interaction.guild.get_member(data[0])

    # 🧾 generar transcript
    archivo = await generar_transcript(channel)

    # 📩 enviar al usuario
    if user:
        try:
            await user.send(
                f"🧾 Aquí está el transcript de tu ticket `{channel.name}`",
                file=discord.File(archivo)
            )
        except:
            pass

    # 📨 enviar a canal transcripts
    cursor.execute("SELECT valor FROM config WHERE clave='transcripts'")
    canal_data = cursor.fetchone()

    if canal_data:
        canal = interaction.guild.get_channel(int(canal_data[0]))
        if canal:
            await canal.send(
                f"🧾 Transcript de {channel.name}",
                file=discord.File(archivo)
            )

    # 📝 logs
    cursor.execute("SELECT valor FROM config WHERE clave='logs'")
    log = cursor.fetchone()

    if log:
        canal_log = interaction.guild.get_channel(int(log[0]))
        if canal_log:
            await canal_log.send(f"🔒 Ticket cerrado: {channel.name}")

    await interaction.response.send_message("🔒 Ticket cerrado", ephemeral=True)

    await channel.edit(name=f"cerrado-{channel.name}")

    @button(label="👤 Claim", style=discord.ButtonStyle.gray)
    async def claim(self, interaction: discord.Interaction, _):
        if not is_staff(interaction):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        await interaction.response.send_message(
            f"{interaction.user.mention} tomó el ticket"
        )

    @button(label="✏️ Renombrar", style=discord.ButtonStyle.blurple)
    async def rename(self, interaction: discord.Interaction, _):


    @discord.ui.button(label="🧾 Transcript", style=discord.ButtonStyle.blurple)
async def transcript(self, interaction: discord.Interaction, button: discord.ui.Button):

    archivo = await generar_transcript(interaction.channel)

    await interaction.response.send_message(
        "🧾 Transcript generado",
        file=discord.File(archivo),
        ephemeral=True
    )


from core.transcript import generate_transcript
from core.logs import log


    html = generate_transcript(messages)

    file = discord.File(
        fp=bytes(html, "utf-8"),
        filename="transcript.html"
    )

    await interaction.channel.send("📄 Transcript generado", file=file)

    await log(interaction, f"{interaction.user} cerró ticket {interaction.channel.name}")

    close_ticket(interaction.channel.id)
    await interaction.channel.delete()        
        if not is_staff(interaction):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        await interaction.response.send_modal(RenameModal())
