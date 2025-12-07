from pyrogram import Client
from pyrogram.types import Message
from database.db import set_group_lang, get_group_lang
from utils.languages import t

async def start_handler(c: Client, m: Message):
    lang = await get_group_lang(m.chat.id)
    if m.chat.type in [str("group"), str("supergroup")]:
        await set_group_lang(m.chat.id, lang)
    
    await m.reply_text(t("welcome", lang, name=m.from_user.first_name))