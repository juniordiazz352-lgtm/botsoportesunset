import discord
from discord.ext import commands


# 🎛️ VIEW PRINCIPAL
class ComandosView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=120)
        self.ctx = ctx

    def get_embed(self, categoria):

        embed = discord.Embed(color=discord.Color.blurple())

        # 🎟️ TICKETS
        if categoria == "tickets":
            embed.title = "🎟️ Sistema de Tickets"
            embed.description = "Gestión avanzada de tickets"
            embed.add_field(
                name="Comandos",
                value=(
                    "`!panelticket`\nCrear panel de tickets\n\n"
                    "`!closeticket`\nCerrar ticket manualmente"
                ),
                inline=False
            )

        # 📋 FORMS
        elif categoria == "forms":
            embed.title = "📋 Formularios"
            embed.description = "Sistema de formularios con aprobación"
            embed.add_field(
                name="Comandos",
                value=(
                    "`!crearform`\nCrear formulario\n\n"
                    "`!panelform`\nCrear panel de formularios"
                ),
                inline=False
            )

        # 🛠️ ADMIN
        elif categoria == "admin":
            embed.title = "🛠️ Administración"
            embed.description = "Herramientas de moderación"
            embed.add_field(
                name="Comandos",
                value=(
                    "`!clear`\nBorrar mensajes\n\n"
                    "`!say`\nEnviar mensaje\n\n"
                    "`!anuncio`\nCrear anuncio embed"
                ),
                inline=False
            )

        # 👑 STAFF
        elif categoria == "staff":
            embed.title = "👑 Staff System"
            embed.description = "Control y gestión de staff"
            embed.add_field(
                name="Comandos",
                value=(
                    "`!setstaff`\nConfigurar rol staff\n\n"
                    "`!staffsay`\nMensaje staff\n\n"
                    "`!stafflogs`\nVer logs"
                ),
                inline=False
            )

        # ⚙️ SETUP
        elif categoria == "setup":
            embed.title = "⚙️ Configuración"
            embed.description = "Configurar el bot"
            embed.add_field(
                name="Comandos",
                value="`!setup`\nAbrir panel de configuración",
                inline=False
            )

        # 📖 INFO
        elif categoria == "info":
            embed.title = "📖 Información"
            embed.description = "Ayuda del bot"
            embed.add_field(
                name="Comandos",
                value=(
                    "`!help`\nMenú interactivo\n\n"
                    "`!comandos`\nLista de comandos"
                ),
                inline=False
            )

        embed.set_footer(text=f"Usuario: {self.ctx.author}")
        if self.ctx.guild.icon:
            embed.set_thumbnail(url=self.ctx.guild.icon.url)

        return embed

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("❌ No puedes usar este menú", ephemeral=True)
            return False
        return True

    # 🎟️ BOTONES
    @discord.ui.button(label="🎟️", style=discord.ButtonStyle.secondary)
    async def tickets(self, interaction, button):
        await interaction.response.edit_message(embed=self.get_embed("tickets"), view=self)

    @discord.ui.button(label="📋", style=discord.ButtonStyle.secondary)
    async def forms(self, interaction, button):
        await interaction.response.edit_message(embed=self.get_embed("forms"), view=self)

    @discord.ui.button(label="🛠️", style=discord.ButtonStyle.secondary)
    async def admin(self, interaction, button):
        await interaction.response.edit_message(embed=self.get_embed("admin"), view=self)

    @discord.ui.button(label="👑", style=discord.ButtonStyle.secondary)
    async def staff(self, interaction, button):
        await interaction.response.edit_message(embed=self.get_embed("staff"), view=self)

    @discord.ui.button(label="⚙️", style=discord.ButtonStyle.secondary)
    async def setup(self, interaction, button):
        await interaction.response.edit_message(embed=self.get_embed("setup"), view=self)

    @discord.ui.button(label="📖", style=discord.ButtonStyle.secondary)
    async def info(self, interaction, button):
        await interaction.response.edit_message(embed=self.get_embed("info"), view=self)

    @discord.ui.button(label="❌", style=discord.ButtonStyle.red)
    async def cerrar(self, interaction, button):
        await interaction.message.delete()


# 📜 COMANDO
class Comandos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="comandos")
    async def comandos(self, ctx):

        await ctx.message.delete()

        view = ComandosView(ctx)

        await ctx.send(
            embed=view.get_embed("tickets"),
            view=view
        )


async def setup(bot):
    await bot.add_cog(Comandos(bot))
