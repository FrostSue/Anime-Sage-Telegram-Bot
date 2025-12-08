from pyrogram.types import BotCommand

async def set_bot_commands(app):
    commands = [
        BotCommand("start", "Start Bot"),
        BotCommand("recommend", "Get Recommendation"),
        BotCommand("language", "Change Language"),
        BotCommand("mood", "Set Mood"),
        BotCommand("genre", "Set Genre"),
        BotCommand("settings", "My Profile & Settings"),
        BotCommand("resetprefs", "Reset Preferences"),
        BotCommand("help", "Command List"),
        BotCommand("stats", "Statistics")
    ]
    await app.set_bot_commands(commands)