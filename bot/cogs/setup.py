import discord
from discord.ext import commands
from bot.core.db import cursor, conn


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        await ctx.send("⚙️ **Configuración del bot iniciada**\nResponde a las siguientes preguntas:")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        # 📌 LOGS
        await ctx.send("📌 Menciona el canal de **logs**")
        msg = await self.bot.wait_for("message", check=check)
        canal_logs = msg.channel_mentions[0]

        cursor.execute("INSERT OR REPLACE INTO config VALUES ('logs', ?)", (str(canal_logs.id),))

        # 📌 TRANSCRIPTS
        await ctx.send("📌 Menciona el canal de **transcripts**")
        msg = await self.bot.wait_for("message", check=check)
        canal_transcripts = msg.channel_mentions[0]

        cursor.execute("INSERT OR REPLACE INTO config VALUES ('transcripts', ?)", (str(canal_transcripts.id),))

        # 📌 ROL STAFF
        await ctx.send("📌 Menciona el **rol staff**")
        msg = await self.bot.wait_for("message", check=check)
        rol = msg.role_mentions[0]

        cursor.execute("INSERT OR REPLACE INTO config VALUES ('staff_role', ?)", (str(rol.id),))

        # 📌 CATEGORÍA
        await ctx.send("📌 Escribe el nombre de la **categoría de tickets**")
        msg = await self.bot.wait_for("message", check=check)

        categoria = discord.utils.get(ctx.guild.categories, name=msg.content)

        if not categoria:
            categoria = await ctx.guild.create_category(msg.content)

        cursor.execute("INSERT OR REPLACE INTO config VALUES ('ticket_category', ?)", (str(categoria.id),))

        conn.commit()

        await ctx.send("✅ **Setup completado correctamente** 🎉")


async def setup(bot):
    await bot.add_cog(Setup(bot))
