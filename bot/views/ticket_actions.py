import discord


class TicketActions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Cerrar", style=discord.ButtonStyle.red)
    async def cerrar(self, interaction, button):

        messages = [msg async for msg in interaction.channel.history(limit=100)]

        transcript = "\n".join([f"{m.author}: {m.content}" for m in reversed(messages)])

        user_id = int(interaction.channel.topic)
        user = await interaction.client.fetch_user(user_id)

        try:
            await user.send(f"📄 **Transcript del ticket:**\n```{transcript[:1900]}```")
        except:
            pass

        await interaction.response.send_message("🔒 Ticket cerrado")
        await interaction.channel.delete()
