import discord
from discord.ext import commands
from bot.views.ticket_panel import TicketPanelView

STAFF_ROLE_NAME = "Staff"


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 Crear Ticket", style=discord.ButtonStyle.green)
    async def crear_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild

        category = discord.utils.get(guild.categories, name="TICKETS")
        if not category:
            category = await guild.create_category("TICKETS")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
        }

        staff_role = discord.utils.get(guild.roles, name=STAFF_ROLE_NAME)
        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True)

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            overwrites=overwrites
        )

        view = TicketControlView()

        await channel.send(
            f"🎟️ Ticket de {interaction.user.mention}",
            view=view
        )

        await interaction.response.send_message(
            f"✅ Ticket creado: {channel.mention}",
            ephemeral=True
        )


class TicketControlView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Cerrar", style=discord.ButtonStyle.red)
    async def cerrar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.send("🔒 Ticket cerrado")
        await interaction.channel.edit(name=f"cerrado-{interaction.channel.name}")

    @discord.ui.button(label="🗑️ Eliminar", style=discord.ButtonStyle.gray)
    async def eliminar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.delete()


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="panel")
    async def panel(self, ctx):
        embed = discord.Embed(
            title="🎫 Sistema de Tickets",
            description="Presiona el botón para abrir un ticket",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed, view=TicketView())


async def setup(bot):
    await bot.add_cog(Tickets(bot))
