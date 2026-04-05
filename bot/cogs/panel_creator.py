import discord
from discord.ext import commands


class PanelCreator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def crear_embed(self, ctx):

        def check(m):
            return m.author == ctx.author

        await ctx.send("📝 Título:")
        titulo = (await self.bot.wait_for("message", check=check)).content

        await ctx.send("📄 Descripción:")
        desc = (await self.bot.wait_for("message", check=check)).content

        await ctx.send("🎨 Color (ej: 0x5865F2):")
        color = int((await self.bot.wait_for("message", check=check)).content, 16)

        embed = discord.Embed(
            title=titulo,
            description=desc,
            color=color
        )

        await ctx.send("📌 Embed creado:", embed=embed)


async def setup(bot):
    await bot.add_cog(PanelCreator(bot))
