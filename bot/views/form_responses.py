import discord
from discord.ext import commands
from core.db import cursor


class FormResponses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ver_respuestas")
    async def ver_respuestas(self, ctx, usuario: discord.Member):

        cursor.execute(
            "SELECT formulario, pregunta, respuesta FROM respuestas WHERE user_id=?",
            (usuario.id,)
        )
        data = cursor.fetchall()

        from bot.core.logger import enviar_log

log = discord.Embed(
    title="📋 Formulario enviado",
    color=discord.Color.blue()
)
log.add_field(name="Usuario", value=user.mention)
log.add_field(name="Formulario", value=form_name)

await enviar_log(guild, log)

        if not data:
            return await ctx.send("❌ No hay respuestas")

        embed = discord.Embed(
            title=f"📊 Respuestas de {usuario}",
            color=discord.Color.green()
        )

        for f, p, r in data:
            embed.add_field(
                name=f"{f} | {p}",
                value=r,
                inline=False
            )

        await ctx.send(embed=embed)

log = discord.Embed(
    title="✅ Formulario aprobado",
    color=discord.Color.green()
)
log.add_field(name="Usuario", value=user.mention)
log.add_field(name="Staff", value=interaction.user.mention)

await enviar_log(interaction.guild, log)

log = discord.Embed(
    title="❌ Formulario rechazado",
    color=discord.Color.red()
)
log.add_field(name="Usuario", value=user.mention)
log.add_field(name="Staff", value=interaction.user.mention)

await enviar_log(interaction.guild, log)


async def setup(bot):
    await bot.add_cog(FormResponses(bot))
