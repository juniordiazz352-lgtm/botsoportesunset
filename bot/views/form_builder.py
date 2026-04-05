import discord
from discord.ext import commands
from bot.core.db import cursor, conn


class FormBuilder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="crear_formulario")
    async def crear_formulario(self, ctx, nombre: str):
        cursor.execute("INSERT OR IGNORE INTO formularios VALUES (?)", (nombre,))
        conn.commit()
        await ctx.send(f"✅ Formulario `{nombre}` creado")

    @commands.hybrid_command(name="agregar_pregunta")
    async def agregar_pregunta(self, ctx, formulario: str, *, pregunta: str):
        cursor.execute("INSERT INTO preguntas (formulario, pregunta) VALUES (?, ?)", (formulario, pregunta))
        conn.commit()
        await ctx.send("✅ Pregunta agregada")

    @commands.hybrid_command(name="ver_formulario")
    async def ver_formulario(self, ctx, formulario: str):
        cursor.execute("SELECT pregunta FROM preguntas WHERE formulario=?", (formulario,))
        data = cursor.fetchall()

        if not data:
            return await ctx.send("❌ Sin preguntas")

        texto = "\n".join([f"{i+1}. {p[0]}" for i, p in enumerate(data)])
        await ctx.send(f"📋 {formulario}:\n{texto}")


async def setup(bot):
    await bot.add_cog(FormBuilder(bot))
