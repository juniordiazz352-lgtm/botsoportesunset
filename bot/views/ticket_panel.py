import discord

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

        # ===== TICKETS =====
        if self.data["tipo"] == "ticket":

            guild = interaction.guild
            category = guild.get_channel(self.data["categoria_id"])

            ticket_name = f"{interaction.user.name}-ticket"

            channel = await guild.create_text_channel(
                name=ticket_name,
                category=category
            )

            await interaction.response.send_message(
                f"🎫 Ticket creado: {channel.mention}",
                ephemeral=True
            )

        # ===== FORMULARIOS =====
        elif self.data["tipo"] == "form":

            modal = FormModal(self.data["form"])
            await interaction.response.send_modal(modal)


# ===== MODAL =====
class FormModal(discord.ui.Modal):
    def __init__(self, form_data):
        super().__init__(title=form_data["title"])

        for q in form_data["questions"]:
            self.add_item(discord.ui.TextInput(
                label=q,
                required=True
            ))

    async def on_submit(self, interaction: discord.Interaction):

        respuestas = [c.value for c in self.children]

        await interaction.response.send_message(
            "✅ Formulario enviado correctamente",
            ephemeral=True
        )

        print("RESPUESTAS:", respuestas)
