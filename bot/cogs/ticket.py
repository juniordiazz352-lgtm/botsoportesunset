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

# 👤 AGREGAR USUARIO AL TICKET
@commands.command()
async def agregar_usuario(self, ctx, usuario: discord.Member):

    from core.db import cursor

    # 🔒 verificar si es ticket
    cursor.execute(
        "SELECT * FROM tickets WHERE channel_id=?",
        (ctx.channel.id,)
    )
    data = cursor.fetchone()

    if not data:
        return await ctx.send("❌ Este canal no es un ticket")

    # 🔒 verificar staff
    cursor.execute("SELECT valor FROM config WHERE clave='staff_role'")
    rol_data = cursor.fetchone()

    if not rol_data:
        return await ctx.send("❌ No hay rol staff configurado")

    rol = ctx.guild.get_role(int(rol_data[0]))

    if rol not in ctx.author.roles:
        return await ctx.send("❌ Solo staff puede usar esto")

    # ✅ agregar permisos
    await ctx.channel.set_permissions(
        usuario,
        read_messages=True,
        send_messages=True
    )

    await ctx.send(f"✅ {usuario.mention} fue agregado al ticket")

# ❌ QUITAR USUARIO
@commands.command()
async def quitar_usuario(self, ctx, usuario: discord.Member):

    from core.db import cursor

    cursor.execute(
        "SELECT * FROM tickets WHERE channel_id=?",
        (ctx.channel.id,)
    )
    data = cursor.fetchone()

    if not data:
        return await ctx.send("❌ No es un ticket")

    cursor.execute("SELECT valor FROM config WHERE clave='staff_role'")
    rol_data = cursor.fetchone()

    rol = ctx.guild.get_role(int(rol_data[0]))

    if rol not in ctx.author.roles:
        return await ctx.send("❌ Solo staff")

    await ctx.channel.set_permissions(usuario, overwrite=None)

    await ctx.send(f"❌ {usuario.mention} fue removido del ticket")


async def setup(bot):
    await bot.add_cog(Tickets(bot))
