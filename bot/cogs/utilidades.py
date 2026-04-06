import discord
from discord.ext import commands


class PanelCreator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🗣 SAY (el bot habla por ti)
    @commands.command()
    @commands.is_owner()
    async def say(self, ctx, *, mensaje):

        await ctx.message.delete()  # borra tu mensaje
        await ctx.send(mensaje)


    # 🎨 EMBED (panel personalizado)
    @commands.command()
    @commands.is_owner()
    async def embed(self, ctx):

        def check(m):
            return m.author == ctx.author

        # 📝 título
        await ctx.send("📝 Escribe el título del embed:")
        titulo = (await self.bot.wait_for("message", check=check)).content

        # 📄 descripción
        await ctx.send("📄 Escribe la descripción:")
        descripcion = (await self.bot.wait_for("message", check=check)).content

        # 🎨 color opcional
        await ctx.send("🎨 Color en HEX (ej: 0x5865F2) o escribe `skip`:")

        color_msg = (await self.bot.wait_for("message", check=check)).content

        if color_msg.lower() == "skip":
            color = discord.Color.blurple()
        else:
            color = int(color_msg, 16)

        embed = discord.Embed(
            title=titulo,
            description=descripcion,
            color=color
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(PanelCreator(bot))
