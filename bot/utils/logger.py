import discord
import datetime

LOG_CHANNEL_ID = 1489086693188305040

async def log(guild, message):
    channel = guild.get_channel(LOG_CHANNEL_ID)
    if not channel:
        return

    embed = discord.Embed(
        description=message,
        color=discord.Color.dark_gray(),
        timestamp=datetime.datetime.utcnow()
    )

    await channel.send(embed=embed)
