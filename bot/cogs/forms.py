import discord
from discord.ext import commands
from core.db import cursor, conn


class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ✅ CREAR FORMULARIO
    @commands.command()
    @commands.is_owner()
    async def crear_formulario(self, ctx, nombre):
        cursor.execute("INSERT OR IGNORE INTO formularios VALUES (?)", (nombre,))
        conn.commit()

        await ctx.send(f"✅ Formulario `{nombre}` creado")

    # ➕ AGREGAR PREGUNTA
    @commands.command()
    @commands.is_owner()
    async def agregar_pregunta(self, ctx, formulario, *, pregunta):

        cursor.execute(
            "INSERT INTO preguntas VALUES (NULL, ?, ?)",
            (formulario, pregunta)
        )
        conn.commit()

        await ctx.send("✅ Pregunta agregada")

    # 🎛 PUBLICAR PANEL
    @commands.command()
    @commands.is_owner()
    async def panel_form(self, ctx):

        embed = discord.Embed(
            title="📋 Formularios SB",
            description="Selecciona un formulario si crees que estas capacitado,recuerda que hay un tiempo asignado,abajo en el menu veras los formularios!",
            color=discord.Color.blurple()
        )

        from views.form_panel import FormPanelView
        await ctx.send(embed=embed, view=FormPanelView())

    # 🎭 ASIGNAR ROL AUTOMÁTICO
    @commands.command()
    @commands.is_owner()
    async def set_form_role(self, ctx, formulario, role: discord.Role):

        cursor.execute(
            "INSERT OR REPLACE INTO form_roles VALUES (?, ?)",
            (formulario, role.id)
        )
        conn.commit()

        await ctx.send(f"✅ Rol {role.mention} asignado a `{formulario}`")

    # 📊 VER RESPUESTAS
    @commands.command()
    async def ver_respuestas(self, ctx, usuario: discord.Member):

        cursor.execute(
            "SELECT formulario, pregunta, respuesta FROM respuestas WHERE user_id=?",
            (usuario.id,)
        )
        data = cursor.fetchall()

        if not data:
            return await ctx.send("❌ No hay respuestas")

        embed = discord.Embed(
            title=f"📊 Respuestas de {usuario}",
            color=discord.Color.green()
        )

        for f, p, r in data:
            embed.add_field(
                name=f"{f} | {p}",
                value=r,
                inline=False
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Forms(bot))
