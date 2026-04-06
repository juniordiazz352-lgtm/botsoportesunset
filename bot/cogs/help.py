import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):

        embed = discord.Embed(
            title="📖 Comandos del Bot",
            description="Lista completa de comandos disponibles:",
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

        embed.set_footer(text="Sistema de soporte")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
