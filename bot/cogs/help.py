import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):

        embed = discord.Embed(
            title="📖 Comandos del Bot",
            description="Lista oficial de comandos disponibles",
            color=discord.Color.blurple()
        )

        # ⚙️ Setup
        embed.add_field(
            name="⚙️ Setup",
            value="`!setup`",
            inline=False
        )

        # 🎫 Tickets
        embed.add_field(
            name="🎫 Tickets",
            value=(
                "`!crear_ticket_tipo` → crear tipo de ticket\n"
                "`!panel_ticket` → enviar panel de tickets\n"
                "`!agregar_usuario` → añadir usuario al ticket\n"
                "`!quitar_usuario` → quitar usuario del ticket"
            ),
            inline=False
        )

        # 📋 Formularios
        embed.add_field(
            name="📋 Formularios",
            value="`!panel_form` → enviar panel de formularios",
            inline=False
        )

        # 🎨 Utilidades
        embed.add_field(
            name="🎨 Utilidades",
            value=(
                "`!say` → el bot habla por ti\n"
                "`!embed` → crear embed interactivo\n"
                "`!crear_embed` → crear embed rápido"
            ),
            inline=False
        )

        embed.set_footer(text="Sistema Sunset Boulevard")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
