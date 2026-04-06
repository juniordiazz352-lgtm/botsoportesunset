import discord
from core.db import cursor


class SetupView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=120)
        self.bot = bot

    # 🎟️ CONFIG TICKETS
    @discord.ui.button(label="🎟️ Tickets", style=discord.ButtonStyle.green)
    async def tickets(self, interaction: discord.Interaction, button):

        await interaction.response.send_message(
            "📂 Envia el ID de la categoría de tickets",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)

        try:
            category_id = int(msg.content)

            cursor.execute(
                "INSERT OR REPLACE INTO config VALUES ('ticket_category', ?)",
                (str(category_id),)
            )
            cursor.connection.commit()

            await interaction.followup.send("✅ Categoría configurada", ephemeral=True)

        except:
            await interaction.followup.send("❌ ID inválido", ephemeral=True)

    # 📋 CONFIG FORMS (CANAL LOG)
    @discord.ui.button(label="📋 Formularios", style=discord.ButtonStyle.blurple)
    async def forms(self, interaction: discord.Interaction, button):

        await interaction.response.send_message(
            "📨 Envia el ID del canal de logs/forms",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)

        try:
            channel_id = int(msg.content)

            cursor.execute(
                "INSERT OR REPLACE INTO config VALUES ('forms_channel', ?)",
                (str(channel_id),)
            )
            cursor.connection.commit()

            await interaction.followup.send("✅ Canal configurado", ephemeral=True)

        except:
            await interaction.followup.send("❌ ID inválido", ephemeral=True)

    # 🛠️ CONFIG STAFF
    @discord.ui.button(label="🛠️ Staff", style=discord.ButtonStyle.red)
    async def staff(self, interaction: discord.Interaction, button):

        await interaction.response.send_message(
            "👑 Envia el ID del rol staff",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)

        try:
            role_id = int(msg.content)

            cursor.execute(
                "INSERT OR REPLACE INTO config VALUES ('staff_role', ?)",
                (str(role_id),)
            )
            cursor.connection.commit()

            await interaction.followup.send("✅ Rol staff configurado", ephemeral=True)

        except:
            await interaction.followup.send("❌ ID inválido", ephemeral=True)
