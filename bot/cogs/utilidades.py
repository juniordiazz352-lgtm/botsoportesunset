import discord
from discord.ext import commands

class Utilidades(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # AUTO BORRAR COMANDO
    # =========================
    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            await ctx.message.delete()
        except:
            pass

    # =========================
    # !say
    # =========================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, *, mensaje):
        await ctx.send(mensaje)

    # =========================
    # !embed
    # =========================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def embed(self, ctx, *, descripcion):
        embed = discord.Embed(
            title="Soporte SB",
            description=descripcion,
            color=discord.Color.blurple()
        )
        await ctx.send(embed=embed)

    # =========================
    # !embedpro
    # =========================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def embedpro(self, ctx, titulo, *, descripcion):
        embed = discord.Embed(
            title=titulo,
            description=descripcion,
            color=discord.Color.blurple()
        )

        embed.set_footer(
            text=f"Enviado por {ctx.author}",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.send(embed=embed)

    # =========================
    # !anuncio
    # =========================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def anuncio(self, ctx, rol: discord.Role, *, mensaje):
        embed = discord.Embed(
            title="📢 Anuncio Importante",
            description=mensaje,
            color=discord.Color.red()
        )

        embed.set_footer(text="Soporte SB")

        await ctx.send(content=rol.mention, embed=embed)

    # =========================
    # !saypanel
    # =========================
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def saypanel(self, ctx):
        from bot.views.ticket_panel import TicketPanel

        botones = [
            {"label": "Soporte", "style": 1, "custom_id": "soporte"},
            {"label": "Ayuda General", "style": 2, "custom_id": "ayuda"},
        ]

        embed = discord.Embed(
            title="🎫 Panel de Tickets",
            description="Selecciona una opción",
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed, view=TicketPanel(botones))


# =========================
# SETUP
# =========================
async def setup(bot):
    await bot.add_cog(Utilidades(bot))
