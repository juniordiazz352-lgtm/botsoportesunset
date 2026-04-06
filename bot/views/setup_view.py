import discord
from core.db import cursor


# 🔍 OBTENER CONFIG ACTUAL
def get_current_config(guild):
    data = {}

    cursor.execute("SELECT * FROM config")
    for key, value in cursor.fetchall():
        data[key] = value

    return {
        "ticket_category": guild.get_channel(int(data.get("ticket_category", 0))),
        "forms_channel": guild.get_channel(int(data.get("forms_channel", 0))),
        "staff_role": guild.get_role(int(data.get("staff_role", 0)))
    }


# 🔍 BUSCAR CATEGORÍA
def find_category(guild, text):
    # ID
    if text.isdigit():
        ch = guild.get_channel(int(text))
        if isinstance(ch, discord.CategoryChannel):
            return ch

    # nombre
    for cat in guild.categories:
        if cat.name.lower() == text.lower():
            return cat

    return None


class SetupView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=180)
        self.bot = bot

        self.add_item(SetupSelect(bot))
        self.add_item(StatusButton())


# 🔽 SELECT CONFIG
class SetupSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot

        options = [
            discord.SelectOption(label="🎟️ Tickets", description="Configurar categoría"),
            discord.SelectOption(label="📋 Formularios", description="Configurar canal"),
            discord.SelectOption(label="🛠️ Staff", description="Configurar rol")
        ]

        super().__init__(
            placeholder="Selecciona qué configurar",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        opcion = self.values[0]

        await interaction.response.send_message(
            "✏️ Envía: ID / mención / nombre",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user

        msg = await self.bot.wait_for("message", check=check)

        try:

            # 🎟️ CATEGORÍA TICKETS
            if "Tickets" in opcion:
                categoria = find_category(interaction.guild, msg.content)

                if not categoria:
                    return await interaction.followup.send("❌ Categoría inválida", ephemeral=True)

                cursor.execute(
                    "INSERT OR REPLACE INTO config VALUES ('ticket_category', ?)",
                    (str(categoria.id),)
                )

            # 📋 CANAL FORM
            elif "Formularios" in opcion:
                canal = None

                if msg.channel_mentions:
                    canal = msg.channel_mentions[0]
                elif msg.content.isdigit():
                    canal = interaction.guild.get_channel(int(msg.content))

                if not canal:
                    return await interaction.followup.send("❌ Canal inválido", ephemeral=True)

                cursor.execute(
                    "INSERT OR REPLACE INTO config VALUES ('forms_channel', ?)",
                    (str(canal.id),)
                )

            # 🛠️ ROL STAFF
            elif "Staff" in opcion:
                rol = None

                if msg.role_mentions:
                    rol = msg.role_mentions[0]
                elif msg.content.isdigit():
                    rol = interaction.guild.get_role(int(msg.content))

                if not rol:
                    return await interaction.followup.send("❌ Rol inválido", ephemeral=True)

                cursor.execute(
                    "INSERT OR REPLACE INTO config VALUES ('staff_role', ?)",
                    (str(rol.id),)
                )

            cursor.connection.commit()

            await interaction.followup.send("✅ Configurado correctamente", ephemeral=True)

        except Exception as e:
            await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)


# 📊 BOTÓN VER CONFIG
class StatusButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="📊 Ver Configuración", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):

        config = get_current_config(interaction.guild)

        embed = discord.Embed(
            title="📊 Configuración Actual",
            color=discord.Color.green()
        )

        embed.add_field(
            name="🎟️ Tickets",
            value=config["ticket_category"].name if config["ticket_category"] else "No configurado",
            inline=False
        )

        embed.add_field(
            name="📋 Formularios",
            value=config["forms_channel"].mention if config["forms_channel"] else "No configurado",
            inline=False
        )

        embed.add_field(
            name="🛠️ Staff",
            value=config["staff_role"].mention if config["staff_role"] else "No configurado",
            inline=False
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)
