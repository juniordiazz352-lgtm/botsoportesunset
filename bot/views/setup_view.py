import discord
from core.db import cursor, conn


class SetupView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot

    # 👮 STAFF
    @discord.ui.button(label="👮 Rol Staff", style=discord.ButtonStyle.blurple)
    async def staff(self, interaction: discord.Interaction, button):

        await interaction.response.send_message("Menciona el rol staff:", ephemeral=True)

        def check(m):
            return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)
        role = msg.role_mentions[0]

        cursor.execute(
            "INSERT OR REPLACE INTO config VALUES (?, ?)",
            ("staff_role", role.id)
        )
        conn.commit()

        await interaction.followup.send(f"✅ Rol guardado: {role.mention}", ephemeral=True)

    # 📁 CATEGORÍA TICKETS
    @discord.ui.button(label="📁 Categoría Tickets", style=discord.ButtonStyle.green)
    async def tickets(self, interaction: discord.Interaction, button):

        await interaction.response.send_message("Menciona la categoría:", ephemeral=True)

        def check(m):
            return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)
        categoria = msg.channel_mentions[0]

        cursor.execute(
            "INSERT OR REPLACE INTO config VALUES (?, ?)",
            ("ticket_category", categoria.id)
        )
        conn.commit()

        await interaction.followup.send("✅ Categoría guardada", ephemeral=True)

    # 📋 CANAL FORMULARIOS
    @discord.ui.button(label="📋 Canal Formularios", style=discord.ButtonStyle.gray)
    async def forms(self, interaction: discord.Interaction, button):

        await interaction.response.send_message("Menciona el canal:", ephemeral=True)

        def check(m):
            return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)
        canal = msg.channel_mentions[0]

        cursor.execute(
            "INSERT OR REPLACE INTO config VALUES (?, ?)",
            ("forms_channel", canal.id)
        )
        conn.commit()

        await interaction.followup.send("✅ Canal guardado", ephemeral=True)

    # 📝 LOGS
    @discord.ui.button(label="📝 Canal Logs", style=discord.ButtonStyle.red)
    async def logs(self, interaction: discord.Interaction, button):

        await interaction.response.send_message("Menciona el canal de logs:", ephemeral=True)

        def check(m):
            return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)
        canal = msg.channel_mentions[0]

        cursor.execute(
            "INSERT OR REPLACE INTO config VALUES (?, ?)",
            ("logs_channel", canal.id)
        )
        conn.commit()

        await interaction.followup.send("✅ Logs configurados", ephemeral=True)
