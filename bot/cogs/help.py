import discord
from discord.ext import commands


class HelpMenu(discord.ui.View):
    def __init__(self, bot, ctx):
        super().__init__(timeout=120)
        self.bot = bot
        self.ctx = ctx

        self.cogs_list = [cog for cog in bot.cogs.keys()]
        self.index = 0

        self.update_buttons()

    def get_embed(self):

        cog_name = self.cogs_list[self.index]
        cog = self.bot.get_cog(cog_name)

        embed = discord.Embed(
            title=f"📂 {cog_name}",
            description="Lista de comandos:",
            color=discord.Color.blurple()
        )

        for command in cog.get_commands():
            if not command.hidden:
                embed.add_field(
                    name=f"!{command.name}",
                    value=command.help or "Sin descripción",
                    inline=False
                )

        embed.set_footer(
            text=f"Página {self.index + 1}/{len(self.cogs_list)} • {self.ctx.author}"
        )

        if self.ctx.guild.icon:
            embed.set_thumbnail(url=self.ctx.guild.icon.url)

        return embed

    def update_buttons(self):
        self.clear_items()

        self.add_item(PrevButton())
        self.add_item(NextButton())
        self.add_item(CloseButton())


class PrevButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="⬅️", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        view: HelpMenu = self.view

        if interaction.user != view.ctx.author:
            return await interaction.response.send_message("❌ No puedes usar este menú", ephemeral=True)

        view.index = (view.index - 1) % len(view.cogs_list)

        await interaction.response.edit_message(embed=view.get_embed(), view=view)


class NextButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="➡️", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        view: HelpMenu = self.view

        if interaction.user != view.ctx.author:
            return await interaction.response.send_message("❌ No puedes usar este menú", ephemeral=True)

        view.index = (view.index + 1) % len(view.cogs_list)

        await interaction.response.edit_message(embed=view.get_embed(), view=view)


class CloseButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="❌ Cerrar", style=discord.ButtonStyle.red)

    async def callback(self, interaction: discord.Interaction):
        view: HelpMenu = self.view

        if interaction.user != view.ctx.author:
            return await interaction.response.send_message("❌ No puedes cerrar este menú", ephemeral=True)

        await interaction.message.delete()


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@commands.command(name="help")
async def help(self, ctx):

    await ctx.message.delete()

    view = HelpMenu(self.bot, ctx)
    await ctx.send(embed=view.get_embed(), view=view)


async def setup(bot):
    await bot.add_cog(Help(bot))
