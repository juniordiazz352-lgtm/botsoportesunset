import discord
from discord.ext import commands
import json
from bot.utils.perms import is_admin
from bot.views.ticket_panel import TicketPanelView

class Utilidades(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # 📢 SAY
    # =========================
    @commands.command()
    @is_admin()
    async def say(self, ctx, *, mensaje):
        await ctx.message.delete()
        await ctx.send(mensaje)

    # =========================
    # 📦 EMBED PRO
    # =========================
    @commands.command()
    @is_admin()
    async def embed(self, ctx, titulo, *, descripcion):

        embed = discord.Embed(
            title=titulo,
            description=descripcion,
            color=discord.Color.blurple()
        )

        embed.set_footer(text=f"Enviado por {ctx.author}")
        await ctx.send(embed=embed)

    # =========================
    # ⚙️ SETUP
    # =========================
    @commands.command()
    @is_admin()
    async def setup(self, ctx, categoria_id: int):

        config = {
            "category_id": categoria_id
        }

        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)

        await ctx.send(f"✅ Categoría configurada correctamente")

    # =========================
    # 🎫 PANEL
    # =========================
    @commands.command()
    @is_admin()
    async def panel(self, ctx):

        embed = discord.Embed(
            title="🎫 Sistema de Tickets",
            description="Presioná el botón para crear un ticket",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed, view=TicketPanelView())
