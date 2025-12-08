from pyrogram import Client
from pyrogram.types import Message
from database.db import update_user_pref
from utils.languages import t
from utils.auth import check_user_registration

async def set_genres(c: Client, m: Message):
    is_valid, lang = await check_user_registration(c, m)
    if not is_valid: return

    if len(m.command) < 2:
        await m.reply_text(t("missing_genres", lang))
        return
    
    genres = " ".join(m.command[1:])
    await update_user_pref(m.from_user.id, "genres", genres)
    await m.reply_text(t("genres_set", lang, genres=genres))

async def set_mood(c: Client, m: Message):
    is_valid, lang = await check_user_registration(c, m)
    if not is_valid: return

    if len(m.command) < 2:
        await m.reply_text(t("missing_mood", lang))
        return

    mood = " ".join(m.command[1:])
    await update_user_pref(m.from_user.id, "mood", mood)
    await m.reply_text(t("mood_set", lang, mood=mood))

async def reset_prefs(c: Client, m: Message):
    is_valid, lang = await check_user_registration(c, m)
    if not is_valid: return

    await update_user_pref(m.from_user.id, "genres", "")
    await update_user_pref(m.from_user.id, "mood", "")
    await m.reply_text(t("reset_done", lang))