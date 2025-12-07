from pyrogram import Client
from pyrogram.types import Message
from database.db import get_group_lang
from utils.languages import t

async def help_handler(c: Client, m: Message):
    lang = await get_group_lang(m.chat.id)
    await m.reply_text(t("help_text", lang))