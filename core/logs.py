from core.config import LOG_CHANNEL_ID

async def log(interaction, text):
    channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(f"📜 {text}")
