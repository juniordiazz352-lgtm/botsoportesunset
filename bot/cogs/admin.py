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


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 📜 LISTA DE COMANDOS PRO
    @commands.command(name="comandos")
    async def comandos(self, ctx):

        embed = discord.Embed(
            title="📖 Lista de Comandos",
            description="Aquí tienes todos los comandos disponibles del bot",
            color=discord.Color.blurple()
        )

        for cog_name, cog in self.bot.cogs.items():

            comandos = []

            for command in cog.get_commands():
                if not command.hidden:
                    comandos.append(f"`!{command.name}`")

            if comandos:
                embed.add_field(
                    name=f"📂 {cog_name}",
                    value=" ".join(comandos),
                    inline=False
                )

        embed.set_footer(text=f"Solicitado por {ctx.author}")
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)

        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Admin(bot))
