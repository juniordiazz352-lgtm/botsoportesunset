import discord
from discord.ext import commands
from core.db import cursor, conn


class FormBuilder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ✅ CREAR FORM
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
        cursor.execute("INSERT INTO preguntas VALUES (NULL, ?, ?)", (formulario, pregunta))
        conn.commit()
        await ctx.send("✅ Pregunta agregada")

    # 📋 PUBLICAR PANEL
    @commands.command()
    @commands.is_owner()
    async def panel_form(self, ctx):

        embed = discord.Embed(
            title="📋 Formularios",
            description="Selecciona un formulario",
            color=discord.Color.blurple()
        )

        from views.form_panel import FormPanelView
        await ctx.send(embed=embed, view=FormPanelView())


async def setup(bot):
    await bot.add_cog(FormBuilder(bot))
