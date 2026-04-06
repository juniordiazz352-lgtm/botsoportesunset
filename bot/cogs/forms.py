import discord
from discord.ext import commands
import json
import os

FORMS_FILE = "forms.json"


class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 🧾 CREAR FORMULARIO
    # =========================
    @commands.command()
    async def crear_form(self, ctx, nombre, *, preguntas):

        preguntas_lista = [p.strip() for p in preguntas.split("|") if p.strip()]

        if not preguntas_lista:
            return await ctx.send("❌ Debes poner al menos una pregunta.")

        data = {}

        if os.path.exists(FORMS_FILE):
            with open(FORMS_FILE, "r") as f:
                data = json.load(f)

        data[nombre.lower()] = preguntas_lista

        with open(FORMS_FILE, "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"✅ Formulario `{nombre}` creado con {len(preguntas_lista)} preguntas.")

    # =========================
    # 📋 PANEL FORMULARIOS
    # =========================
    @commands.command()
    async def panel_form(self, ctx):

        from bot.views.form_panel import FormPanel

        embed = discord.Embed(
            title="📋 Sistema de Formularios",
            description=(
                "Selecciona un formulario del menú.\n\n"
                "📌 Completa la información correctamente.\n"
                "⚠️ Evita enviar spam."
            ),
            color=discord.Color.orange()
        )

        embed.set_footer(text="Sistema Sunset Boulevard")

        await ctx.send(embed=embed, view=FormPanel())


async def setup(bot):
    await bot.add_cog(Forms(bot))
