import discord
from core.db import cursor


def es_staff(member, guild):
    cursor.execute("SELECT valor FROM config WHERE clave='staff_role'")
    data = cursor.fetchone()
    if not data:
        return False
    rol = guild.get_role(int(data[0]))
    return rol in member.roles if rol else False


class ReviewView(discord.ui.View):
    def __init__(self, user, form):
        super().__init__(timeout=None)
        self.user = user
        self.form = form

    @discord.ui.button(label="✅ Aprobar", style=discord.ButtonStyle.green)
    async def aprobar(self, interaction: discord.Interaction, button):

        if not es_staff(interaction.user, interaction.guild):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        await interaction.response.send_message("✍️ Escribe mensaje:", ephemeral=True)

        def check(m):
            return m.author == interaction.user

        msg = await interaction.client.wait_for("message", check=check)

        # 🎭 dar rol automático
        cursor.execute(
            "SELECT role_id FROM form_roles WHERE formulario=?",
            (self.form,)
        )
        data = cursor.fetchone()

        if data:
            role = interaction.guild.get_role(int(data[0]))
            if role:
                await self.user.add_roles(role)

        await self.user.send(
            f"🎉 Aprobado\n📋 {self.form}\n📩 {msg.content}"
        )

        await interaction.followup.send("Aprobado", ephemeral=True)

    @discord.ui.button(label="❌ Rechazar", style=discord.ButtonStyle.red)
    async def rechazar(self, interaction: discord.Interaction, button):

        if not es_staff(interaction.user, interaction.guild):
            return await interaction.response.send_message("❌ Solo staff", ephemeral=True)

        await interaction.response.send_message("Motivo:", ephemeral=True)

        def check(m):
            return m.author == interaction.user

        msg = await interaction.client.wait_for("message", check=check)

        await self.user.send(
            f"❌ Rechazado\n📋 {self.form}\n📩 {msg.content}"
        )

        await interaction.followup.send("Rechazado", ephemeral=True)
