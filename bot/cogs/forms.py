from discord.ext import commands
import discord
from core.utils import save_form, get_forms


class Forms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🔥 CREAR FORM BIEN HECHO
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def crearform(self, ctx):

        def check(m): return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send("📝 Nombre del formulario:")
        nombre = (await self.bot.wait_for("message", check=check)).content

        await ctx.send("📄 Canal donde se enviarán respuestas (ID o mención):")
        canal_msg = await self.bot.wait_for("message", check=check)

        canal_id = int("".join(filter(str.isdigit, canal_msg.content)))
        canal = ctx.guild.get_channel(canal_id)

        if not canal:
            return await ctx.send("❌ Canal inválido")

        await ctx.send("❓ Preguntas (`listo` para terminar):")

        preguntas = []
        while True:
            msg = await self.bot.wait_for("message", check=check)

            if msg.content.lower() == "listo":
                break

            preguntas.append(msg.content)

        save_form(nombre, preguntas, canal.id)

        await ctx.send(f"✅ Form `{nombre}` creado en {canal.mention}")

    # 🔥 PANEL FORM PRO
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def panelform(self, ctx):

        def check(m): return m.author == ctx.author and m.channel == ctx.channel

        forms = get_forms()

        if not forms:
            return await ctx.send("❌ No hay formularios")

        await ctx.send("📝 Título del panel:")
        titulo = (await self.bot.wait_for("message", check=check)).content

        await ctx.send("📄 Descripción:")
        descripcion = (await self.bot.wait_for("message", check=check)).content

        await ctx.send(
            "📋 Formularios disponibles:\n" +
            "\n".join([f"- {f}" for f in forms.keys()])
        )

        await ctx.send("✏️ Escribe los nombres que quieres usar (`listo` para terminar)")

        seleccionados = {}

        while True:
            msg = await self.bot.wait_for("message", check=check)

            if msg.content.lower() == "listo":
                break

            if msg.content in forms:
                seleccionados[msg.content] = forms[msg.content]
            else:
                await ctx.send("❌ No existe")

        from bot.views.dynamic_form import FormPanelView

        embed = discord.Embed(
            title=titulo,
            description=descripcion,
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed, view=FormPanelView(seleccionados))


async def setup(bot):
    await bot.add_cog(Forms(bot))
