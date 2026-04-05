import discord
from discord.ext import commands
from core.db import cursor, conn
from views.ticket_controls import TicketControlsView

MAX_TICKETS = 4


class TicketPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        cursor.execute("SELECT nombre, emoji FROM ticket_types")
        tipos = cursor.fetchall()

        for nombre, emoji in tipos:
            self.add_item(TicketButton(nombre, emoji))


class TicketButton(discord.ui.Button):
    def __init__(self, nombre, emoji):
        super().__init__(
            label=nombre,
            emoji=emoji,
            style=discord.ButtonStyle.blurple
        )
        self.nombre = nombre

    async def callback(self, interaction: discord.Interaction):

        guild = interaction.guild
        user = interaction.user

        # 🚫 LIMITE DE 4 TICKETS
        cursor.execute(
            "SELECT COUNT(*) FROM tickets WHERE user_id=? AND estado='abierto'",
            (user.id,)
        )
        count = cursor.fetchone()[0]

        if count >= MAX_TICKETS:
            return await interaction.response.send_message(
                "❌ Ya tienes 4 tickets abiertos",
                ephemeral=True
            )

        # 📁 categoría
        cursor.execute(
            "SELECT categoria_id FROM ticket_types WHERE nombre=?",
            (self.nombre,)
        )
        data = cursor.fetchone()

        categoria = guild.get_channel(data[0]) if data else None

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }

        channel = await guild.create_text_channel(
            name=f"{self.nombre}-{user.name}",
            overwrites=overwrites,
            category=categoria
        )
        from bot.core.logger import enviar_log

log = discord.Embed(
    title="🎫 Ticket abierto",
    color=discord.Color.green()
)
log.add_field(name="Usuario", value=interaction.user.mention)
log.add_field(name="Tipo", value=self.nombre)
log.add_field(name="Canal", value=channel.mention)

await enviar_log(interaction.guild, log)

        cursor.execute(
            "INSERT INTO tickets VALUES (?, ?, ?, ?, ?)",
            (user.id, channel.id, self.nombre, "abierto", None)
        )
        conn.commit()

        # 📩 MENSAJE QUE PEDISTE
        embed = discord.Embed(
            title="🎫 Ticket abierto",
            description=(
                "Has abierto un ticket.\n\n"
                "El staff no tiene un horario establecido para responder el ticket,\n"
                "pero te llamarán en breve.\n\n"
                "⏰ Recuerda que únicamente tienes 24 horas para responder."
            ),
            color=discord.Color.green()
        )

        from bot.core.logger import enviar_log


        await channel.send(
            content=user.mention,
            embed=embed,
            view=TicketControlsView()
        )

        await interaction.response.send_message(
            f"✅ Ticket creado: {channel.mention}",
            ephemeral=True
        )
