import discord
from core.utils import get_ticket, update_claim, close_ticket


class TicketActions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # 🙋 CLAIM
    @discord.ui.button(label="🙋 Claim", style=discord.ButtonStyle.blurple)
    async def claim(self, interaction, button):

        data = get_ticket(interaction.channel.id)

        if not data:
            return

        if data[3]:
            return await interaction.response.send_message(
                "❌ Ya está reclamado",
                ephemeral=True
            )

        update_claim(interaction.channel.id, interaction.user.id)

        await interaction.response.send_message(
            f"🙋 Ticket reclamado por {interaction.user.mention}"
        )

    # 🔒 CERRAR
    @discord.ui.button(label="🔒 Cerrar", style=discord.ButtonStyle.red)
    async def cerrar(self, interaction, button):

        data = get_ticket(interaction.channel.id)

        if not data:
            return

        user_id = int(data[1])

        # transcript
        messages = [msg async for msg in interaction.channel.history(limit=200)]

        transcript = "\n".join([
            f"{m.author}: {m.content}" for m in reversed(messages)
        ])

        user = await interaction.client.fetch_user(user_id)

        try:
            await user.send(
                f"📄 **Tu ticket fue cerrado**\n\n"
                f"📝 Transcript:\n```{transcript[:1900]}```"
            )
        except:
            pass

        close_ticket(interaction.channel.id)

        await interaction.response.send_message("🔒 Ticket cerrado")
        await interaction.channel.delete()

    # ➕ AÑADIR
    @discord.ui.button(label="➕ Añadir", style=discord.ButtonStyle.secondary)
    async def add(self, interaction, button):

        await interaction.response.send_message("Menciona usuario", ephemeral=True)

        def check(m): return m.author == interaction.user

        msg = await interaction.client.wait_for("message", check=check)

        if not msg.mentions:
            return

        user = msg.mentions[0]

        await interaction.channel.set_permissions(user, view_channel=True)

        await interaction.followup.send("✅ Añadido")

    # ➖ QUITAR
    @discord.ui.button(label="➖ Quitar", style=discord.ButtonStyle.secondary)
    async def remove(self, interaction, button):

        await interaction.response.send_message("Menciona usuario", ephemeral=True)

        def check(m): return m.author == interaction.user

        msg = await interaction.client.wait_for("message", check=check)

        if not msg.mentions:
            return

        user = msg.mentions[0]

        await interaction.channel.set_permissions(user, overwrite=None)

        await interaction.followup.send("❌ Quitado")

    # 🗑️ ELIMINAR
    @discord.ui.button(label="🗑️ Eliminar", style=discord.ButtonStyle.danger)
    async def delete(self, interaction, button):

        await interaction.response.send_message("🗑️ Eliminando...")
        await interaction.channel.delete()
