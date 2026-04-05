async def generar_transcript(channel):
    mensajes = []

    async for msg in channel.history(limit=None, oldest_first=True):
        mensajes.append(f"{msg.author}: {msg.content}\n")

    nombre = f"transcript-{channel.id}.txt"

    with open(nombre, "w", encoding="utf-8") as f:
        f.writelines(mensajes)

    return nombre
