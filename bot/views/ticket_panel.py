import discord

class TicketPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Crear Ticket", style=discord.ButtonStyle.green, emoji="🎫")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild
        user = interaction.user

        # 🔒 categoría (poné tu ID si usás setup)
        category = discord.utils.get(guild.categories, name="Tickets")

        # permisos
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        # crear canal
        channel = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            overwrites=overwrites,
            category=category
        )

        embed = discord.Embed(
            title="🎫 Ticket creado",
            description="Un staff te atenderá pronto.",
            color=discord.Color.green()
        )

        await channel.send(content=user.mention, embed=embed)

        await interaction.response.send_message(
            f"✅ Ticket creado: {channel.mention}",
            ephemeral=True
        )
