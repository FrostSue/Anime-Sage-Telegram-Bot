from pyrogram.types import BotCommand

async def set_bot_commands(app):
    commands = [
        BotCommand("start", "Start Bot"),
        BotCommand("help", "Help & Info"),
        BotCommand("recommend", "Get AI Recommendation"),
        BotCommand("setgenres", "Set Genres"),
        BotCommand("setmood", "Set Mood"),
        BotCommand("resetprefs", "Reset Profile"),
        BotCommand("stats", "Group Stats"),
        BotCommand("language", "Change Language (Admin)"),
        BotCommand("adminpanel", "Admin Controls")
    ]
    await app.set_bot_commands(commands)