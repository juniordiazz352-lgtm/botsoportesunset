import discord
from discord.ext import commands
from core.db import cursor, conn
from bot.views.ticket_panel import TicketPanelView


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ➕ CREAR TIPO DE TICKET (SOLO OWNER)
    @commands.command()
    @commands.is_owner()
    async def crear_ticket_tipo(self, ctx, nombre, emoji, categoria: discord.CategoryChannel):

        cursor.execute(
            "INSERT OR REPLACE INTO ticket_types VALUES (?, ?, ?)",
            (nombre, emoji, categoria.id)
        )
        conn.commit()

        await ctx.send(f"✅ Tipo `{nombre}` creado")

    # 🎛 PANEL
    @commands.command()
    @commands.is_owner()
    async def panel_ticket(self, ctx):

        embed = discord.Embed(
            title="🎫 Soporte|SB",
            description="Selecciona una de las opciones de tickets con las que contamos,al presionar en ellas abriras un ticket",
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed, view=TicketPanelView())

    # 👤 AGREGAR USUARIO
    @commands.command()
    async def agregar_usuario(self, ctx, usuario: discord.Member):

        cursor.execute(
            "SELECT * FROM tickets WHERE channel_id=?",
            (ctx.channel.id,)
        )
        if not cursor.fetchone():
            return await ctx.send("❌ No es un ticket")

        await ctx.channel.set_permissions(
            usuario,
            read_messages=True,
            send_messages=True
        )

        await ctx.send(f"✅ {usuario.mention} agregado")

    # ❌ QUITAR USUARIO
    @commands.command()
    async def quitar_usuario(self, ctx, usuario: discord.Member):

        await ctx.channel.set_permissions(usuario, overwrite=None)
        await ctx.send(f"❌ {usuario.mention} removido")


async def setup(bot):
    await bot.add_cog(Tickets(bot))
