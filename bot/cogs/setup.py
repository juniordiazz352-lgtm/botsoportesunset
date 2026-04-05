import discord
from discord.ext import commands
from bot.core.db import cursor, conn


class SetupView(discord.ui.View):
    def __init__(self, bot, ctx):
        super().__init__(timeout=300)
        self.bot = bot
        self.ctx = ctx
        self.step = 0
        self.data = {}

    async def ask(self, text):
        embed = discord.Embed(
            title="⚙️ Setup del Bot",
            description=text,
            color=discord.Color.blurple()
        )
        await self.ctx.send(embed=embed)

    async def wait_msg(self):
        def check(m):
            return m.author == self.ctx.author and m.channel == self.ctx.channel

        return await self.bot.wait_for("message", check=check, timeout=120)

    @discord.ui.button(label="🚀 Empezar Setup", style=discord.ButtonStyle.green)
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message("⚙️ Iniciando...", ephemeral=True)

        # Logs
        await self.ask("📌 Menciona el canal de **logs**")
        msg = await self.wait_msg()
        self.data["logs"] = msg.channel_mentions[0].id

        # Transcripts
        await self.ask("📌 Menciona el canal de **transcripts**")
        msg = await self.wait_msg()
        self.data["transcripts"] = msg.channel_mentions[0].id

        # Staff
        await self.ask("📌 Menciona el **rol staff**")
        msg = await self.wait_msg()
        self.data["staff"] = msg.role_mentions[0].id

        # Categoría
        await self.ask("📌 Escribe nombre de categoría tickets")
        msg = await self.wait_msg()

        categoria = discord.utils.get(self.ctx.guild.categories, name=msg.content)
        if not categoria:
            categoria = await self.ctx.guild.create_category(msg.content)

        self.data["categoria"] = categoria.id

        # Guardar
        for k, v in self.data.items():
            cursor.execute("INSERT OR REPLACE INTO config VALUES (?, ?)", (k, str(v)))

        conn.commit()

        await self.ctx.send("✅ Setup completado 🎉")


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="setup")
    async def setup(self, ctx):
        embed = discord.Embed(
            title="⚙️ Setup del Bot",
            description="Presiona el botón para configurar todo",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed, view=SetupView(self.bot, ctx))


async def setup(bot):
    await bot.add_cog(Setup(bot))
