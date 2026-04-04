import discord
from discord.ext import commands

class Utilidades(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # !say
    # =========================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, *, mensaje):
        try:
            await ctx.message.delete()
        except:
            pass

        await ctx.send(mensaje)

    # =========================
    # !embed básico
    # =========================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def embed(self, ctx, *, descripcion):
        try:
            await ctx.message.delete()
        except:
            pass

        embed = discord.Embed(
            title="Soporte SB",
            description=descripcion,
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed)

    # =========================
    # !embedpro (full custom)
    # =========================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def embedpro(self, ctx, titulo, *, descripcion):
        try:
            await ctx.message.delete()
        except:
            pass

        embed = discord.Embed(
            title=titulo,
            description=descripcion,
            color=discord.Color.blurple()
        )

        embed.set_footer(text=f"Enviado por {ctx.author}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

    # =========================
    # !anuncio (con ping rol)
    # =========================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def anuncio(self, ctx, rol: discord.Role, *, mensaje):
        try:
            await ctx.message.delete()
        except:
            pass

        embed = discord.Embed(
            title="📢 Anuncio Importante",
            description=mensaje,
            color=discord.Color.red()
        )

        embed.set_footer(text="Soporte SB")

        await ctx.send(content=rol.mention, embed=embed)

    # =========================
    # !saypanel (envía panel tickets)
    # =========================
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def saypanel(self, ctx):
        from bot.views.ticket_panel import TicketPanel

        try:
            await ctx.message.delete()
        except:
            pass

        botones = [
            {"label": "Soporte", "style": 1, "custom_id": "soporte"},
            {"label": "Ayuda General", "style": 2, "custom_id": "ayuda"},
        ]

        embed = discord.Embed(
            title="🎫 Panel de Tickets",
            description="Selecciona una opción para abrir ticket",
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed, view=TicketPanel(botones))


# =========================
# SETUP
# =========================
async def setup(bot):
    await bot.add_cog(Utilidades(bot))
