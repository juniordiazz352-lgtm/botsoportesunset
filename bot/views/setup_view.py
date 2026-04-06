import discord
from discord.ext import commands
from core.db import cursor, conn


class SetupView(discord.ui.View):
    def __init__(self, bot, guild):
        super().__init__(timeout=600)
        self.bot = bot
        self.guild = guild

    # 🔧 DETECTOR PRO (ID o mención)
    def parse_id(self, text):
        text = text.strip()

        if text.isdigit():
            return int(text)

        if text.startswith("<") and text.endswith(">"):
            return int("".join(filter(str.isdigit, text)))

        return None

    # 📊 DASHBOARD PRINCIPAL
    def get_embed(self):
        embed = discord.Embed(
            title="⚙️ Panel de Configuración",
            description="Configura todo tu sistema desde aquí 🚀",
            color=discord.Color.blurple()
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
            inline=True
        )

        embed.add_field(
            name="🎟️ Tickets",
            value=f"<#{tickets}>" if tickets else "❌ No configurado",
            inline=True
        )

        embed.add_field(
            name="📋 Formularios",
            value=f"<#{forms}>" if forms else "❌ No configurado",
            inline=True
        )

        embed.add_field(
            name="📝 Logs",
            value=f"<#{logs}>" if logs else "❌ No configurado",
            inline=True
        )

        embed.set_footer(text="Sistema Sunset 🌇 | Setup PRO")
        return embed

    # 🔄 REFRESH
    async def refresh(self, interaction):
        await interaction.message.edit(embed=self.get_embed(), view=self)

    # 👮 STAFF
    @discord.ui.button(label="👮 Staff", style=discord.ButtonStyle.secondary)
    async def staff(self, interaction: discord.Interaction, button):

        await interaction.response.send_message(
            "👮 Envía el **ID o menciona el rol staff**",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)

        role_id = self.parse_id(msg.content)
        role = interaction.guild.get_role(role_id) if role_id else None

        if not role:
            return await interaction.followup.send("❌ Rol inválido", ephemeral=True)

        cursor.execute(
            "INSERT OR REPLACE INTO config VALUES (?, ?)",
            ("staff_role", role.id)
        )
        conn.commit()

        await interaction.followup.send("✅ Staff configurado correctamente", ephemeral=True)
        await self.refresh(interaction)

    # 🎟️ TICKETS
    @discord.ui.button(label="🎟️ Tickets", style=discord.ButtonStyle.success)
    async def tickets(self, interaction: discord.Interaction, button):

        await interaction.response.send_message(
            "📁 Envía el **ID o menciona la categoría de tickets**",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)

        cat_id = self.parse_id(msg.content)
        category = interaction.guild.get_channel(cat_id) if cat_id else None

        if not category or category.type != discord.ChannelType.category:
            return await interaction.followup.send("❌ Categoría inválida", ephemeral=True)

        cursor.execute(
            "INSERT OR REPLACE INTO config VALUES (?, ?)",
            ("ticket_category", category.id)
        )
        conn.commit()

        await interaction.followup.send("✅ Sistema de tickets configurado", ephemeral=True)
        await self.refresh(interaction)

    # 📋 FORMULARIOS
    @discord.ui.button(label="📋 Formularios", style=discord.ButtonStyle.primary)
    async def forms(self, interaction: discord.Interaction, button):

        await interaction.response.send_message(
            "📨 Envía el **ID o menciona el canal de formularios**",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)

        canal_id = self.parse_id(msg.content)
        canal = interaction.guild.get_channel(canal_id) if canal_id else None

        if not canal:
            return await interaction.followup.send("❌ Canal inválido", ephemeral=True)

        cursor.execute(
            "INSERT OR REPLACE INTO config VALUES (?, ?)",
            ("forms_channel", canal.id)
        )
        conn.commit()

        await interaction.followup.send("✅ Canal de formularios configurado", ephemeral=True)
        await self.refresh(interaction)

    # 📝 LOGS
    @discord.ui.button(label="📝 Logs", style=discord.ButtonStyle.danger)
    async def logs(self, interaction: discord.Interaction, button):

        await interaction.response.send_message(
            "📄 Envía el **ID o menciona el canal de logs**",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)

        canal_id = self.parse_id(msg.content)
        canal = interaction.guild.get_channel(canal_id) if canal_id else None

        if not canal:
            return await interaction.followup.send("❌ Canal inválido", ephemeral=True)

        cursor.execute(
            "INSERT OR REPLACE INTO config VALUES (?, ?)",
            ("logs_channel", canal.id)
        )
        conn.commit()

        await interaction.followup.send("✅ Logs configurados", ephemeral=True)
        await self.refresh(interaction)

    # 🔁 RESET
    @discord.ui.button(label="🔁 Reset", style=discord.ButtonStyle.gray)
    async def reset(self, interaction: discord.Interaction, button):

        await interaction.response.send_message(
            "⚠️ Escribe `CONFIRMAR` para borrar TODO",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)

        if msg.content != "CONFIRMAR":
            return await interaction.followup.send("❌ Cancelado", ephemeral=True)

        cursor.execute("DELETE FROM config")
        conn.commit()

        await interaction.followup.send("🧹 Configuración reiniciada", ephemeral=True)
        await self.refresh(interaction)
