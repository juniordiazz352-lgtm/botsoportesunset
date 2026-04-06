import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🧹 CLEAR MENSAJES
    @commands.command(name="clear", help="Borra mensajes. Uso: !clear <cantidad> o !clear all")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: str = None):

        if not amount:
            return await ctx.send("❌ Uso: `!clear <cantidad>` o `!clear all`")

        # 🔥 BORRAR TODO
        if amount.lower() == "all":

            await ctx.send("⚠️ ¿Seguro que quieres borrar TODOS los mensajes? Escribe `confirmar`")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                msg = await self.bot.wait_for("message", check=check, timeout=15)

                if msg.content.lower() != "confirmar":
                    return await ctx.send("❌ Cancelado")

                deleted = await ctx.channel.purge(limit=1000)
                return await ctx.send(f"🧹 {len(deleted)} mensajes eliminados", delete_after=5)

            except:
                return await ctx.send("⏳ Tiempo agotado")

        # 🔢 BORRAR CANTIDAD
        if not amount.isdigit():
            return await ctx.send("❌ Debes poner un número o `all`")

        amount = int(amount)

        if amount > 100:
            return await ctx.send("❌ Máximo 100 mensajes")

        deleted = await ctx.channel.purge(limit=amount + 1)

        msg = await ctx.send(f"🧹 {len(deleted)-1} mensajes eliminados")
        await msg.delete(delay=5)

    # 📢 SAY
    @commands.command(name="say", help="El bot repite tu mensaje")
    async def say(self, ctx, *, mensaje):

        await ctx.message.delete()
        await ctx.send(mensaje)

    # 📣 ANUNCIO EMBED
    @commands.command(name="anuncio", help="Crear anuncio con embed")
    async def anuncio(self, ctx):

        def check(m): return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send("📝 Título:")
        titulo = (await self.bot.wait_for("message", check=check)).content

        await ctx.send("📄 Descripción:")
        descripcion = (await self.bot.wait_for("message", check=check)).content

        embed = discord.Embed(
            title=titulo,
            description=descripcion,
            color=discord.Color.gold()
        )

        embed.set_footer(text=f"Anuncio por {ctx.author}")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Admin(bot))
