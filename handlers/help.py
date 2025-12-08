from pyrogram import Client
from pyrogram.types import Message
from utils.languages import t
from utils.auth import check_user_registration

async def help_handler(c: Client, m: Message):
    is_valid, lang = await check_user_registration(c, m)
    if not is_valid:
        return

    await m.reply_text(t("help_text", lang))