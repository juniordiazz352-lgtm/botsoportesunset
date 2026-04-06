@commands.command()
@commands.has_permissions(administrator=True)
async def panelticket(self, ctx):

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("📝 Título del panel:")
    titulo = (await self.bot.wait_for("message", check=check)).content

    await ctx.send("📄 Descripción:")
    descripcion = (await self.bot.wait_for("message", check=check)).content

    await ctx.send("🎟️ Escribe los nombres de los tickets uno por uno.\nEscribe `listo` para terminar.")

    botones = []

    while True:
        msg = await self.bot.wait_for("message", check=check)

        if msg.content.lower() == "listo":
            break

        botones.append(msg.content)

    from bot.views.dynamic_ticket import DynamicTicketView

    embed = discord.Embed(
        title=titulo,
        description=descripcion,
        color=discord.Color.blurple()
    )

    await ctx.send(embed=embed, view=DynamicTicketView(botones))
