import discord
from discord.ext import commands
from discord import app_commands
from core.db import create_form
from bot.views.form_builder import FormBuilder
from bot.views.dynamic_form import DynamicForm

class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="crear_form")
    async def create(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            "Nombre del formulario:", ephemeral=True
        )

        def check(m): return m.author == interaction.user
        msg = await self.bot.wait_for("message", check=check)

        create_form(msg.content)

        await interaction.followup.send(
            f"Formulario `{msg.content}` creado",
            view=FormBuilder(msg.content)
        )

    @app_commands.command(name="formulario")
    async def send_form(self, interaction: discord.Interaction, nombre: str):
        await interaction.response.send_modal(DynamicForm(nombre))

async def setup(bot):
    await bot.add_cog(Forms(bot))
