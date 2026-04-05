@commands.command()
@commands.is_owner()
async def panel_form(self, ctx):

    embed = discord.Embed(
        title="📋 Formularios",
        description="Selecciona un formulario del menu de aqui abajo,encontraras una variedad,solamente presiona en ellos si crees que estas capacitado",
        color=discord.Color.blurple()
    )

    from views.form_panel import FormPanelView
    await ctx.send(embed=embed, view=FormPanelView())
