import discord
from bot.core.db import cursor


async def enviar_log(guild, embed):

    cursor.execute("SELECT valor FROM config WHERE clave='logs_channel'")
    data = cursor.fetchone()

    if not data:
        return

    canal = guild.get_channel(int(data[0]))

    if canal:
        await canal.send(embed=embed)
