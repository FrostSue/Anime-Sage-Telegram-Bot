from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.db import update_user_pref
from utils.languages import t
from utils.auth import check_user_registration

GENRES_LIST = [
    "action", "adventure", "comedy", "drama", "fantasy", "horror",
    "mystery", "romance", "scifi", "sliceoflife", "sports", "supernatural"
]

MOODS_LIST = [
    "happy", "sad", "excited", "relaxed", 
    "dark", "romantic", "bored", "curious"
]

def build_keyboard(items: list, prefix: str, lang: str, cols: int = 2):
    """Butonları dinamik olarak oluşturan yardımcı fonksiyon"""
    buttons = []
    row = []
    for item in items:
        text = t(f"{prefix}_{item}", lang)
        row.append(InlineKeyboardButton(text, callback_data=f"set_{prefix}_{item}"))
        
        if len(row) == cols:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    buttons.append([InlineKeyboardButton(t("btn_cancel", lang), callback_data="cancel_pref")])
    return InlineKeyboardMarkup(buttons)

async def set_genres(c: Client, m: Message):
    is_valid, lang = await check_user_registration(c, m)
    if not is_valid: return

    kb = build_keyboard(GENRES_LIST, "genre", lang, cols=3)
    await m.reply_text(t("select_genre", lang), reply_markup=kb)

async def set_mood(c: Client, m: Message):
    is_valid, lang = await check_user_registration(c, m)
    if not is_valid: return

    kb = build_keyboard(MOODS_LIST, "mood", lang, cols=2)
    await m.reply_text(t("select_mood", lang), reply_markup=kb)

async def reset_prefs(c: Client, m: Message):
    is_valid, lang = await check_user_registration(c, m)
    if not is_valid: return

    await update_user_pref(m.from_user.id, "genres", "")
    await update_user_pref(m.from_user.id, "mood", "")
    await m.reply_text(t("reset_done", lang))


async def pref_callback_handler(c: Client, q: CallbackQuery):
    data = q.data
    user_id = q.from_user.id
    if data == "cancel_pref":
        await q.answer("İptal edildi / Cancelled")
        await q.message.delete()
        return

    parts = data.split("_")
    category = parts[1]
    value_key = parts[2]
    
    lang_key = f"{category}_{value_key}"

    await update_user_pref(user_id, "genres" if category == "genre" else "mood", value_key)
    
    await q.answer("Kaydedildi / Saved")
    await q.message.edit_text(f"✅ {category.capitalize()} updated: **{value_key.capitalize()}**")