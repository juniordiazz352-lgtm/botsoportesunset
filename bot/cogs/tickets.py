import discord
from discord.ext import commands

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 Crear Ticket", style=discord.ButtonStyle.green)
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild
        category = discord.utils.get(guild.categories, name="TICKETS")

        if not category:
            category = await guild.create_category("TICKETS")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            overwrites=overwrites
        )

        await channel.send(f"🎟️ Ticket creado por {interaction.user.mention}")
        await interaction.response.send_message(f"✅ Ticket creado: {channel.mention}", ephemeral=True)


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def panel(self, ctx):
        embed = discord.Embed(
            title="🎫 Sistema de Tickets",
            description="Presiona el botón para crear un ticket",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed, view=TicketView())


async def setup(bot):
    await bot.add_cog(Tickets(bot))
