import discord
from discord.ext import commands
from bot.core.db import cursor, conn


class SetupView(discord.ui.View):
    def __init__(self, bot, guild):
        super().__init__(timeout=300)
        self.bot = bot
        self.guild = guild

    # 📊 RESUMEN
    @discord.ui.button(label="📊 Ver Configuración", style=discord.ButtonStyle.blurple)
    async def resumen(self, interaction: discord.Interaction, button):

        embed = discord.Embed(
            title="📊 Configuración actual",
            color=discord.Color.green()
        )

        def get(clave):
            cursor.execute("SELECT valor FROM config WHERE clave=?", (clave,))
            data = cursor.fetchone()
            return data[0] if data else None

        staff = get("staff_role")
        tickets = get("ticket_category")
        forms = get("forms_channel")
        logs = get("logs_channel")

        embed.add_field(
            name="👮 Staff",
            value=f"<@&{staff}>" if staff else "❌ No configurado",
            inline=False
        )

        embed.add_field(
            name="📁 Tickets",
            value=f"<#{tickets}>" if tickets else "❌ No configurado",
            inline=False
        )

        embed.add_field(
            name="📋 Formularios",
            value=f"<#{forms}>" if forms else "❌ No configurado",
            inline=False
        )

        embed.add_field(
            name="📝 Logs",
            value=f"<#{logs}>" if logs else "❌ No configurado",
            inline=False
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    # 👮 STAFF
    @discord.ui.button(label="👮 Configurar Staff", style=discord.ButtonStyle.gray)
    async def staff(self, interaction: discord.Interaction, button):

        await interaction.response.send_message("Menciona el rol:", ephemeral=True)

        def check(m):
            return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)
        role = msg.role_mentions[0]

        cursor.execute(
            "INSERT OR REPLACE INTO config VALUES (?, ?)",
            ("staff_role", role.id)
        )
        conn.commit()

        await interaction.followup.send("✅ Staff actualizado", ephemeral=True)

    # 📁 TICKETS
    @discord.ui.button(label="📁 Categoría Tickets", style=discord.ButtonStyle.green)
    async def tickets(self, interaction: discord.Interaction, button):

        await interaction.response.send_message("Menciona la categoría:", ephemeral=True)

        def check(m):
            return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)
        cat = msg.channel_mentions[0]

        cursor.execute(
            "INSERT OR REPLACE INTO config VALUES (?, ?)",
            ("ticket_category", cat.id)
        )
        conn.commit()

        await interaction.followup.send("✅ Categoría actualizada", ephemeral=True)

    # 📋 FORMS
    @discord.ui.button(label="📋 Canal Formularios", style=discord.ButtonStyle.blurple)
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

        await interaction.followup.send("✅ Canal actualizado", ephemeral=True)

    # 📝 LOGS
    @discord.ui.button(label="📝 Canal Logs", style=discord.ButtonStyle.red)
    async def logs(self, interaction: discord.Interaction, button):

        await interaction.response.send_message("Menciona el canal:", ephemeral=True)

        def check(m):
            return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)
        canal = msg.channel_mentions[0]

        cursor.execute(
            "INSERT OR REPLACE INTO config VALUES (?, ?)",
            ("logs_channel", canal.id)
        )
        conn.commit()

        await interaction.followup.send("✅ Logs actualizados", ephemeral=True)

    # 🔁 RESET
    @discord.ui.button(label="🔁 Resetear Todo", style=discord.ButtonStyle.danger)
    async def reset(self, interaction: discord.Interaction, button):

        await interaction.response.send_message(
            "⚠️ Escribe `CONFIRMAR` para resetear todo:",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)

        if msg.content != "CONFIRMAR":
            return await interaction.followup.send("❌ Cancelado", ephemeral=True)

        cursor.execute("DELETE FROM config")
        conn.commit()

        await interaction.followup.send("🔁 Configuración eliminada", ephemeral=True)
