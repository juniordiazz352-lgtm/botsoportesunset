import discord
from core.db import cursor


async def get_config(guild, key):
    cursor.execute("SELECT valor FROM config WHERE clave=?", (key,))
    data = cursor.fetchone()
    if not data:
        return None
    return guild.get_channel(int(data[0])) or guild.get_role(int(data[0]))


async def send_log(guild, message):

    cursor.execute("SELECT valor FROM config WHERE clave='logs_channel'")
    data = cursor.fetchone()

    if not data:
        return

    canal = guild.get_channel(int(data[0]))

    if canal:
        await canal.send(message)
