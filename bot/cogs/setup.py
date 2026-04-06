import discord
from discord.ext import commands
from bot.views.setup_view import SetupView
from core.db import cursor


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ⚙️ SETUP PANEL
    @commands.command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):

        await ctx.message.delete()

        embed = discord.Embed(
            title="⚙️ Setup GOD++",
            description="Configura el bot con el menú interactivo",
            color=discord.Color.blurple()
        )

        embed.add_field(name="🎟️ Tickets", value="Categoría de tickets", inline=False)
        embed.add_field(name="📋 Formularios", value="Canal de logs/forms", inline=False)
        embed.add_field(name="🛠️ Staff", value="Rol staff", inline=False)

        await ctx.send(embed=embed, view=SetupView(self.bot))

    # 💀 RESET SETUP
    @commands.command(name="resetsetup")
    @commands.has_permissions(administrator=True)
    async def resetsetup(self, ctx):

        await ctx.message.delete()

        cursor.execute("DELETE FROM config")
        cursor.connection.commit()

        msg = await ctx.send("💀 Configuración reiniciada")
        await msg.delete(delay=5)


async def setup(bot):
    await bot.add_cog(Setup(bot))
