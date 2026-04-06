import threading
import asyncio
import uvicorn

from bot.main import main as bot_main

def run_bot():
    asyncio.run(bot_main())

def run_api():
    uvicorn.run("api.app:app", host="0.0.0.0", port=10000)

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()

    run_api()
