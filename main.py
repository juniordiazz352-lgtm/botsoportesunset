import threading
import asyncio
import uvicorn

import os

async def load():
    for root, dirs, files in os.walk("./bot/cogs"):
        for file in files:
            if file.endswith(".py"):
                ruta = os.path.join(root, file).replace("\\", ".").replace("/", ".")[:-3]
                try:
                    await bot.load_extension(ruta)
                    print(f"✅ Cargado: {ruta}")
                except Exception as e:
                    print(f"❌ Error en {ruta}: {e}")


asyncio.run(main())

from bot.main import main as bot_main

def run_bot():
    asyncio.run(bot_main())

def run_api():
    uvicorn.run("api.app:app", host="0.0.0.0", port=10000)

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()

    run_api()
