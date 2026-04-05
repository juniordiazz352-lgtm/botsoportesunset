import discord
from core.db import cursor, conn
from views.ticket_controls import TicketControlsView


MAX_TICKETS = 4


class TicketPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(TicketButton("soporte", "🛠 Soporte", discord.ButtonStyle.green))
        self.add_item(TicketButton("compras", "💰 Compras", discord.ButtonStyle.blurple))
        self.add_item(TicketButton("staff", "👮 Staff", discord.ButtonStyle.red))


class TicketButton(discord.ui.Button):
    def __init__(self, tipo, label, style):
        super().__init__(label=label, style=style)
        self.tipo = tipo

    async def callback(self, interaction: discord.Interaction):

        guild = interaction.guild
        user = interaction.user

        # 🚫 LIMITE DE TICKETS
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

        # 📁 obtener categoría desde config
        cursor.execute(
            "SELECT valor FROM config WHERE clave=?",
            (f"ticket_cat_{self.tipo}",)
        )
        data = cursor.fetchone()

        categoria = guild.get_channel(int(data[0])) if data else None

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }

        channel = await guild.create_text_channel(
            name=f"{self.tipo}-{user.name}",
            overwrites=overwrites,
            category=categoria
        )

        cursor.execute(
            "INSERT INTO tickets VALUES (?, ?, ?, ?, ?)",
            (user.id, channel.id, self.tipo, "abierto", None)
        )
        conn.commit()

        embed = discord.Embed(
            title=f"🎫 Ticket {self.tipo}",
            description="Un staff te atenderá pronto",
            color=discord.Color.green()
        )

        await channel.send(
            content=user.mention,
            embed=embed,
            view=TicketControlsView()
        )

        await interaction.response.send_message(
            f"✅ Ticket creado: {channel.mention}",
            ephemeral=True
        )
