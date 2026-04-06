import discord
from core.db import cursor


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


class SetupView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=180)
        self.bot = bot

        self.add_item(SetupSelect(bot))
        self.add_item(StatusButton())


class SetupSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot

        options = [
            discord.SelectOption(label="🎟️ Tickets", description="Configurar categoría"),
            discord.SelectOption(label="📋 Formularios", description="Configurar canal"),
            discord.SelectOption(label="🛠️ Staff", description="Configurar rol")
        ]

        super().__init__(placeholder="Selecciona qué configurar", options=options)

    async def callback(self, interaction: discord.Interaction):

        opcion = self.values[0]

        await interaction.response.send_message(
            "✏️ Envía una mención (canal/rol/categoría)",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user

        msg = await self.view.bot.wait_for("message", check=check)

        try:

            # 🎟️ Tickets
            if "Tickets" in opcion:
                if msg.channel_mentions:
                    categoria = msg.channel_mentions[0]

                    cursor.execute(
                        "INSERT OR REPLACE INTO config VALUES ('ticket_category', ?)",
                        (str(categoria.id),)
                    )

            # 📋 Forms
            elif "Formularios" in opcion:
                if msg.channel_mentions:
                    canal = msg.channel_mentions[0]

                    cursor.execute(
                        "INSERT OR REPLACE INTO config VALUES ('forms_channel', ?)",
                        (str(canal.id),)
                    )

            # 🛠️ Staff
            elif "Staff" in opcion:
                if msg.role_mentions:
                    rol = msg.role_mentions[0]

                    cursor.execute(
                        "INSERT OR REPLACE INTO config VALUES ('staff_role', ?)",
                        (str(rol.id),)
                    )

            cursor.connection.commit()

            await interaction.followup.send("✅ Configurado correctamente", ephemeral=True)

        except:
            await interaction.followup.send("❌ Error en configuración", ephemeral=True)


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
            value=config["ticket_category"].mention if config["ticket_category"] else "No configurado",
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
