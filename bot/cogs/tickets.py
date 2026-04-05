import discord
from discord.ext import commands
from discord.ui import View, Button

# 🔘 BOTÓN CREAR TICKET
class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎟 Crear Ticket", style=discord.ButtonStyle.green, custom_id="crear_ticket")
    async def crear_ticket(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        user = interaction.user

        # evitar duplicados
        existing = discord.utils.get(guild.text_channels, name=f"ticket-{user.name}".lower())
        if existing:
            await interaction.response.send_message("❌ Ya tienes un ticket abierto", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            overwrites=overwrites
        )

        embed = discord.Embed(
            title="🎟 Ticket creado",
            description="Un staff te atenderá pronto.\nPresiona 🔒 para cerrar.",
            color=discord.Color.green()
        )

        await channel.send(content=user.mention, embed=embed, view=CloseView())

        await interaction.response.send_message(f"✅ Ticket creado: {channel.mention}", ephemeral=True)

# 🔘 BOTÓN CERRAR
class CloseView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Cerrar Ticket", style=discord.ButtonStyle.red, custom_id="cerrar_ticket")
    async def cerrar_ticket(self, interaction: discord.Interaction, button: Button):
        channel = interaction.channel

        await interaction.response.send_message("🔒 Cerrando ticket...", ephemeral=True)

        mensajes = []
        async for msg in channel.history(limit=100):
            mensajes.append(f"{msg.author}: {msg.content}")

        transcript = "\n".join(mensajes)

        file = discord.File(
            fp=bytes(transcript, "utf-8"),
            filename="transcript.txt"
        )

        await channel.send("📄 Transcript:", file=file)

        await channel.delete()

# 🎟 COMANDO PANEL
class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def panel(self, ctx):
        try:
            await ctx.message.delete()
        except:
            pass

        embed = discord.Embed(
            title="🎟 Soporte SB",
            description="Presiona el botón para abrir un ticket",
            color=discord.Color.blue()
        )

        await ctx.send(embed=embed, view=TicketView())

async def setup(bot):
    await bot.add_cog(Tickets(bot))
