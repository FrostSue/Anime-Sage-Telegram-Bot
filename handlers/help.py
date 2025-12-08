from pyrogram import Client
from pyrogram.types import Message
from utils.languages import t
from utils.auth import check_user_registration, is_admin

async def help_handler(c: Client, m: Message):
    is_valid, lang = await check_user_registration(c, m)
    if not is_valid:
        return

    user_is_admin = await is_admin(m.from_user.id)
    
    if user_is_admin:
        help_key = "help_text_admin"
    else:
        help_key = "help_text"

    await m.reply_text(t(help_key, lang))