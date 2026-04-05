import discord
from discord.ext import commands
from core.db import create_form

class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def form(self, ctx):
        await ctx.send("📩 Revisa tu DM para completar el formulario")

        def check(m):
            return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

        await ctx.author.send("¿Cuál es tu nombre?")
        nombre = await self.bot.wait_for("message", check=check)

        await ctx.author.send("¿Por qué quieres entrar?")
        motivo = await self.bot.wait_for("message", check=check)

        data = f"Nombre: {nombre.content} | Motivo: {motivo.content}"

        create_form(ctx.author.id, ctx.guild.id, data)

        await ctx.author.send("✅ Formulario enviado correctamente")

async def setup(bot):
    await bot.add_cog(Forms(bot))
