import discord
from discord.ext import commands
from core.db import cursor, conn
from views.ticket_panel import TicketPanelView


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

        await ctx.send(f"✅ Tipo `{nombre}` creado con {emoji}")

    # 🎛 PANEL DE TICKETS (SOLO OWNER)
    @commands.command()
    @commands.is_owner()
    async def panel_ticket(self, ctx):

        cursor.execute("SELECT nombre, emoji FROM ticket_types")
        tipos = cursor.fetchall()

        if not tipos:
            return await ctx.send("❌ No hay tipos de ticket creados")

        embed = discord.Embed(
            title="🎫Soporte | SB",
            description="Selecciona un tipo de ticket y presiona en el y abriras un ticket",
            color=discord.Color.blurple()
        )

        for nombre, emoji in tipos:
            embed.add_field(
                name=f"{emoji} {nombre}",
                value="Haz clic en el botón",
                inline=False
            )

        await ctx.send(embed=embed, view=TicketPanelView())


async def setup(bot):
    await bot.add_cog(Tickets(bot))
