import discord
from discord.ext import commands

from bot.views.ticket_panel import TicketPanelView
from bot.views.form_panel import FormPanelView

PANELES = {}


class PanelCreator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="crear_panel")
    async def crear_panel(self, ctx, tipo: str, nombre: str, titulo: str, *, descripcion: str):
        tipo = tipo.lower()

        if tipo not in ["ticket", "form"]:
            return await ctx.send("❌ Tipo inválido (ticket/form)")

        PANELES[nombre] = {
            "tipo": tipo,
            "titulo": titulo,
            "descripcion": descripcion
        }

        await ctx.send(f"✅ Panel `{nombre}` creado")

    @commands.hybrid_command(name="eliminar_panel")
    async def eliminar_panel(self, ctx, nombre: str):
        if nombre not in PANELES:
            return await ctx.send("❌ No existe ese panel")

        del PANELES[nombre]
        await ctx.send(f"🗑️ Panel `{nombre}` eliminado")

    @commands.hybrid_command(name="ver_paneles")
    async def ver_paneles(self, ctx):
        if not PANELES:
            return await ctx.send("❌ No hay paneles")

        texto = "\n".join([f"• {p} ({PANELES[p]['tipo']})" for p in PANELES])
        await ctx.send(f"📋 Paneles:\n{texto}")

    @commands.hybrid_command(name="publicar_panel")
    async def publicar_panel(self, ctx, nombre: str):
        panel = PANELES.get(nombre)

        if not panel:
            return await ctx.send("❌ Panel no existe")

        embed = discord.Embed(
            title=panel["titulo"],
            description=panel["descripcion"],
            color=discord.Color.blurple()
        )

        if panel["tipo"] == "ticket":
            view = TicketPanelView()

        elif panel["tipo"] == "form":
            view = FormPanelView()

        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(PanelCreator(bot))
