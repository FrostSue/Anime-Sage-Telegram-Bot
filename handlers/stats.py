from pyrogram import Client
from pyrogram.types import Message
from database.db import get_user_data
from utils.languages import t
from utils.auth import check_user_registration

async def stats_handler(c: Client, m: Message):
    is_valid, lang = await check_user_registration(c, m)
    if not is_valid: return

    user_data = await get_user_data(m.from_user.id)
    total = user_data["stats"] if user_data else 0
    
    await m.reply_text(t("stats_msg", lang, total=total))