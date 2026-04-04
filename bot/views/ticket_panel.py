import discord
from core.db import get_ticket_number
import datetime
import os
from core.db import get_ticket_number, add_log
import os

STAFF_ROLE_ID = 1472478801710678258 # ⚠️ CAMBIA ESTO

class TicketPanel(discord.ui.View):
    def __init__(self, botones):
        super().__init__(timeout=None)

        for b in botones:
            self.add_item(TicketButton(b))


class TicketButton(discord.ui.Button):
    def __init__(self, data):
        super().__init__(label=data["label"], style=discord.ButtonStyle.primary)
        self.data = data

    async def callback(self, interaction: discord.Interaction):

        if self.data["tipo"] == "ticket":

            guild = interaction.guild
            categoria = guild.get_channel(self.data["categoria_id"])

            number = get_ticket_number(self.data["categoria_id"])
            name = f"{self.data['label'].lower()}-{str(number).zfill(4)}"

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                guild.get_role(STAFF_ROLE_ID): discord.PermissionOverwrite(view_channel=True, send_messages=True)
            }

            channel = await guild.create_text_channel(
                name=name,
                category=categoria,
                overwrites=overwrites
            )

            await channel.send(
                f"{interaction.user.mention} 🎫 Ticket creado",
                view=TicketControls(interaction.user.id)
            )

            await interaction.response.send_message(
                f"✅ Ticket: {channel.mention}",
                ephemeral=True
            )

        elif self.data["tipo"] == "form":
            modal = FormModal(self.data["form"])
            await interaction.response.send_modal(modal)


# ===== BOTONES DENTRO DEL TICKET =====
class TicketControls(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=None)
        self.owner_id = owner_id

    @discord.ui.button(label="🔒 Cerrar", style=discord.ButtonStyle.danger)
async def close(self, interaction: discord.Interaction, button: discord.ui.Button):

    if not any(r.id == STAFF_ROLE_ID for r in interaction.user.roles):
        return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

    file = await create_transcript(interaction.channel, interaction.user)

    await interaction.response.send_message("📁 Transcript guardado", ephemeral=True)

    await interaction.channel.delete()

    @discord.ui.button(label="👤 Reclamar", style=discord.ButtonStyle.secondary)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not any(r.id == STAFF_ROLE_ID for r in interaction.user.roles):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        await interaction.response.send_message(f"👤 {interaction.user.mention} tomó el ticket")


# ===== TRANSCRIPTS =====
async def create_transcript(channel, closed_by):

    messages = [msg async for msg in channel.history(limit=100)]

    html = "<h1>Transcript</h1>"

    for msg in reversed(messages):
        html += f"<p><b>{msg.author}:</b> {msg.content}</p>"

    os.makedirs("transcripts", exist_ok=True)

    filename = f"transcripts/{channel.name}.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    # 💀 LOG
    add_log(str(closed_by), "cerró ticket", channel.name)

    return filename

# ===== FORM =====
class FormModal(discord.ui.Modal):
    def __init__(self, form_data):
        super().__init__(title=form_data["title"])

        for q in form_data["questions"]:
            self.add_item(discord.ui.TextInput(label=q))

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅ Form enviado", ephemeral=True)
