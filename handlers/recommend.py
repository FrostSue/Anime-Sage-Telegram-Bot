from pyrogram import Client
from pyrogram.types import Message
from database.db import get_group_lang, get_user_data, increment_stats
from utils.languages import t
from services.ai import generate_anime_recommendation

async def recommend_handler(c: Client, m: Message):
    lang = await get_group_lang(m.chat.id)
    user_id = m.from_user.id
    
    wait_msg = await m.reply_text(t("thinking", lang))
    
    user_data = await get_user_data(user_id)
    saved_genres = user_data["genres"] if user_data else ""
    saved_mood = user_data["mood"] if user_data else ""
    
    user_input = " ".join(m.command[1:]) if len(m.command) > 1 else ""

    recommendation = await generate_anime_recommendation(
        user_input=user_input,
        mood=saved_mood,
        genres=saved_genres,
        lang=lang
    )
    
    await increment_stats(user_id, m.chat.id)
    await wait_msg.delete()
    await m.reply_text(f"{recommendation}", quote=True)