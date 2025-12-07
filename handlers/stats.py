from pyrogram import Client
from pyrogram.types import Message
from database.db import get_group_lang, get_group_stats
from utils.languages import t

async def stats_handler(c: Client, m: Message):
    lang = await get_group_lang(m.chat.id)
    stats = await get_group_stats(m.chat.id)
    users = stats[0] if stats else 0
    total = stats[1] if stats and stats[1] else 0
    
    await m.reply_text(t("stats_msg", lang, users=users, total=total))