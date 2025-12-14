import re
from pyrogram import Client
from pyrogram.types import Message
from database.db import get_user_data, increment_stats, get_user_history, add_to_history
from utils.languages import t
from utils.auth import check_user_registration
from services.ai import generate_anime_recommendation, get_anime_info

async def recommend_handler(c: Client, m: Message):
    is_valid, lang = await check_user_registration(c, m)
    if not is_valid: return
    
    wait_msg = await m.reply_text(t("thinking", lang))
    
    user_id = m.from_user.id
    user_data = await get_user_data(user_id)
    saved_genres = user_data["genres"] if user_data else ""
    saved_mood = user_data["mood"] if user_data else ""
    
    history_list = await get_user_history(user_id)
    
    user_input = " ".join(m.command[1:]) if len(m.command) > 1 else ""

    recommendation = await generate_anime_recommendation(
        user_input=user_input, 
        mood=saved_mood, 
        genres=saved_genres, 
        lang=lang,
        excluded_list=history_list
    )
    
    match = re.search(r"🎬 \*\*(.*?)\*\*", recommendation)
    if match:
        anime_title = match.group(1)
        await add_to_history(user_id, anime_title)

    await increment_stats(user_id)
    await wait_msg.delete()
    await m.reply_text(f"{recommendation}", quote=True)

async def anime_info_handler(c: Client, m: Message):
    is_valid, lang = await check_user_registration(c, m)
    if not is_valid: return

    if len(m.command) < 2:
        await m.reply_text(t("anime_info_usage", lang), quote=True)
        return

    anime_name = " ".join(m.command[1:])
    wait_msg = await m.reply_text(t("searching", lang), quote=True)

    info = await get_anime_info(anime_name, lang)
    
    await wait_msg.delete()
    await m.reply_text(info, quote=True)