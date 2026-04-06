import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 📢 SAY
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, mensaje):

        await ctx.message.delete()

        embed = discord.Embed(
            description=mensaje,
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed)

    # 📣 ANUNCIO
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def anuncio(self, ctx, titulo, *, descripcion):

        embed = discord.Embed(
            title=f"📢 {titulo}",
            description=descripcion,
            color=discord.Color.gold()
        )

        embed.set_footer(text=f"Anuncio por {ctx.author}")
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.set_timestamp()

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Admin(bot))
