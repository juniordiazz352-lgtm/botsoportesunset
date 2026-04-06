import discord


class TicketActions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.claimed_by = None

    # 🔒 Cerrar
    @discord.ui.button(label="🔒 Cerrar", style=discord.ButtonStyle.red)
    async def cerrar(self, interaction: discord.Interaction, button):

        await interaction.channel.set_permissions(
            interaction.guild.default_role,
            view_channel=False
        )

        await interaction.response.send_message("🔒 Ticket cerrado")

    # 🔓 Reabrir
    @discord.ui.button(label="🔓 Reabrir", style=discord.ButtonStyle.green)
    async def reabrir(self, interaction: discord.Interaction, button):

        await interaction.channel.set_permissions(
            interaction.guild.default_role,
            view_channel=False
        )

        await interaction.response.send_message("🔓 Ticket reabierto")

    # 🙋 Claim
    @discord.ui.button(label="🙋 Reclamar", style=discord.ButtonStyle.blurple)
    async def claim(self, interaction: discord.Interaction, button):

        if self.claimed_by:
            return await interaction.response.send_message(
                f"❌ Ya reclamado por {self.claimed_by}",
                ephemeral=True
            )

        self.claimed_by = interaction.user

        await interaction.response.send_message(
            f"🙋 Ticket reclamado por {interaction.user.mention}"
        )

    # ➕ Añadir usuario
    @discord.ui.button(label="➕ Añadir", style=discord.ButtonStyle.secondary)
    async def add_user(self, interaction: discord.Interaction, button):

        await interaction.response.send_message(
            "👤 Menciona al usuario a añadir",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user

        msg = await interaction.client.wait_for("message", check=check)

        if not msg.mentions:
            return await interaction.followup.send("❌ Usuario inválido", ephemeral=True)

        user = msg.mentions[0]

        await interaction.channel.set_permissions(
            user,
            view_channel=True,
            send_messages=True
        )

        await interaction.followup.send(f"✅ {user.mention} añadido")

    # ➖ Quitar usuario
    @discord.ui.button(label="➖ Quitar", style=discord.ButtonStyle.secondary)
    async def remove_user(self, interaction: discord.Interaction, button):

        await interaction.response.send_message(
            "👤 Menciona al usuario a quitar",
            ephemeral=True
        )

        def check(m):
            return m.author == interaction.user

        msg = await interaction.client.wait_for("message", check=check)

        if not msg.mentions:
            return await interaction.followup.send("❌ Usuario inválido", ephemeral=True)

        user = msg.mentions[0]

        await interaction.channel.set_permissions(user, overwrite=None)

        await interaction.followup.send(f"❌ {user.mention} eliminado")

    # 🗑️ Eliminar
    @discord.ui.button(label="🗑️ Eliminar", style=discord.ButtonStyle.danger)
    async def delete(self, interaction: discord.Interaction, button):

        await interaction.response.send_message("🗑️ Eliminando ticket...")
        await interaction.channel.delete()
