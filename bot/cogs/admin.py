import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 💎 LISTA EMBED GOD
    @commands.command(name="comandos", help="Muestra todos los comandos del bot")
    async def comandos(self, ctx):

        await ctx.message.delete()

        embed = discord.Embed(
            title="📖 Panel de Comandos",
            description="Sistema completo del bot",
            color=discord.Color.blurple()
        )

        # 🎟️ Tickets
        embed.add_field(
            name="🎟️ Tickets",
            value=(
                "`!panelticket`\n"
                "Crear panel de tickets dinámico"
            ),
            inline=False
        )

        # 📋 Forms
        embed.add_field(
            name="📋 Formularios",
            value=(
                "`!crearform`\nCrear formulario con preguntas y canal\n\n"
                "`!panelform`\nCrear panel seleccionando formularios"
            ),
            inline=False
        )

        # 🛠️ Admin
        embed.add_field(
            name="🛠️ Administración",
            value=(
                "`!clear <cantidad/all>`\nBorrar mensajes\n\n"
                "`!say <mensaje>`\nEnviar mensaje como bot\n\n"
                "`!anuncio`\nCrear anuncio embed"
            ),
            inline=False
        )

        # 📖 Info
        embed.add_field(
            name="📖 Información",
            value=(
                "`!help`\nMenú interactivo\n\n"
                "`!comandos`\nLista de comandos"
            ),
            inline=False
        )

        embed.set_footer(text=f"Solicitado por {ctx.author}")
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)

        await ctx.send(embed=embed)

    # 🧹 CLEAR PRO LIMPIO
    @commands.command(name="clear", help="Borra mensajes")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: str = None):

        await ctx.message.delete()

        if not amount:
            msg = await ctx.send("❌ Uso: !clear <cantidad> o !clear all")
            return await msg.delete(delay=5)

        # 💀 BORRAR TODO
        if amount.lower() == "all":

            msg = await ctx.send("⚠️ Escribe `confirmar` para borrar todo")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                confirm = await self.bot.wait_for("message", check=check, timeout=15)

                if confirm.content.lower() != "confirmar":
                    cancel = await ctx.send("❌ Cancelado")
                    return await cancel.delete(delay=5)

                await confirm.delete()

                deleted = await ctx.channel.purge(limit=1000)

                info = await ctx.send(f"🧹 {len(deleted)} mensajes eliminados")
                await info.delete(delay=5)

            except:
                timeout = await ctx.send("⏳ Tiempo agotado")
                await timeout.delete(delay=5)

            return

        # 🔢 BORRAR NORMAL
        if not amount.isdigit():
            msg = await ctx.send("❌ Debe ser número o all")
            return await msg.delete(delay=5)

        amount = int(amount)

        if amount > 100:
            msg = await ctx.send("❌ Máximo 100")
            return await msg.delete(delay=5)

        deleted = await ctx.channel.purge(limit=amount + 1)

        info = await ctx.send(f"🧹 {len(deleted)-1} mensajes eliminados")
        await info.delete(delay=5)

    # 📢 SAY
    @commands.command(name="say", help="El bot repite tu mensaje")
    async def say(self, ctx, *, mensaje):

        await ctx.message.delete()
        await ctx.send(mensaje)

    # 📣 ANUNCIO PRO
    @commands.command(name="anuncio", help="Crear anuncio embed")
    async def anuncio(self, ctx):

        await ctx.message.delete()

        def check(m): return m.author == ctx.author and m.channel == ctx.channel

        msg1 = await ctx.send("📝 Título:")
        titulo_msg = await self.bot.wait_for("message", check=check)
        await msg1.delete()
        await titulo_msg.delete()

        msg2 = await ctx.send("📄 Descripción:")
        desc_msg = await self.bot.wait_for("message", check=check)
        await msg2.delete()
        await desc_msg.delete()

        embed = discord.Embed(
            title=titulo_msg.content,
            description=desc_msg.content,
            color=discord.Color.gold()
        )

        embed.set_footer(text=f"Anuncio por {ctx.author}")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Admin(bot))
