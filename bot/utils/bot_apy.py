bot_instance = None

def set_bot(bot):
    global bot_instance
    bot_instance = bot


def get_bot():
    return bot_instance
