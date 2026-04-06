import discord
from discord.ext import commands
from bot.views.form_panel import FormPanelView


class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def panel_form(self, ctx):

        embed = discord.Embed(
            title="📋 Formularios",
            description="Selecciona un formulario del menú de abajo",
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed, view=FormPanelView())

import discord
from discord.ext import commands
import json
import os

FORMS_FILE = "forms.json"


class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def crear_form(self, ctx, nombre, *, preguntas):

        try:
            preguntas_lista = preguntas.split("|")
        except:
            return await ctx.send("❌ Usa: !crear_form nombre pregunta1 | pregunta2 | pregunta3")

        data = {}

        if os.path.exists(FORMS_FILE):
            with open(FORMS_FILE, "r") as f:
                data = json.load(f)

        data[nombre] = preguntas_lista

        with open(FORMS_FILE, "w") as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"✅ Formulario `{nombre}` creado con {len(preguntas_lista)} preguntas.")


async def setup(bot):
    await bot.add_cog(Forms(bot))
