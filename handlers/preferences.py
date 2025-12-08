from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.db import update_user_pref, get_user_data
from utils.languages import t
from utils.auth import check_user_registration

async def show_profile(c: Client, m: Message):
    is_valid, lang = await check_user_registration(c, m)
    if not is_valid: return

    user_id = m.from_user.id
    user_data = await get_user_data(user_id)
    
    mood = user_data["mood"] if user_data and user_data["mood"] else "❌"
    genres = user_data["genres"] if user_data and user_data["genres"] else "❌"
    
    msg = t("profile_msg", lang, 
            name=m.from_user.first_name, 
            mood=mood, 
            genre=genres)
            
    await m.reply_text(msg, quote=True)

async def mood_menu_handler(c: Client, m: Message):
    is_valid, lang = await check_user_registration(c, m)
    if not is_valid: return

    user_id = m.from_user.id
    
    buttons = [
        [
            InlineKeyboardButton(t("mood_happy", lang), callback_data=f"set_mood|Happy|{user_id}"),
            InlineKeyboardButton(t("mood_sad", lang), callback_data=f"set_mood|Sad|{user_id}")
        ],
        [
            InlineKeyboardButton(t("mood_exciting", lang), callback_data=f"set_mood|Exciting|{user_id}"),
            InlineKeyboardButton(t("mood_relaxing", lang), callback_data=f"set_mood|Relaxing|{user_id}")
        ],
        [
            InlineKeyboardButton(t("mood_dark", lang), callback_data=f"set_mood|Dark|{user_id}"),
            InlineKeyboardButton(t("mood_romantic", lang), callback_data=f"set_mood|Romantic|{user_id}")
        ]
    ]
    
    await m.reply_text(t("msg_select_mood", lang), reply_markup=InlineKeyboardMarkup(buttons), quote=True)

async def genre_menu_handler(c: Client, m: Message):
    is_valid, lang = await check_user_registration(c, m)
    if not is_valid: return

    user_id = m.from_user.id
    
    buttons = [
        [
            InlineKeyboardButton(t("genre_shonen", lang), callback_data=f"set_genre|Shonen|{user_id}"),
            InlineKeyboardButton(t("genre_seinen", lang), callback_data=f"set_genre|Seinen|{user_id}")
        ],
        [
            InlineKeyboardButton(t("genre_isekai", lang), callback_data=f"set_genre|Isekai|{user_id}"),
            InlineKeyboardButton(t("genre_sliceoflife", lang), callback_data=f"set_genre|SliceOfLife|{user_id}")
        ],
        [
            InlineKeyboardButton(t("genre_romance", lang), callback_data=f"set_genre|Romance|{user_id}"),
            InlineKeyboardButton(t("genre_scifi", lang), callback_data=f"set_genre|SciFi|{user_id}")
        ],
        [
             InlineKeyboardButton(t("genre_horror", lang), callback_data=f"set_genre|Horror|{user_id}")
        ]
    ]
    
    await m.reply_text(t("msg_select_genre", lang), reply_markup=InlineKeyboardMarkup(buttons), quote=True)

async def reset_prefs(c: Client, m: Message):
    is_valid, lang = await check_user_registration(c, m)
    if not is_valid: return

    user_id = m.from_user.id
    
    await update_user_pref(user_id, "genres", "")
    await update_user_pref(user_id, "mood", "")
    
    await m.reply_text(t("reset_done", lang))

async def pref_callback_handler(c: Client, q: CallbackQuery):
    data = q.data
    
    parts = data.split("|")
    action_type = parts[0]
    value = parts[1]
    owner_id = int(parts[2])

    clicker_id = q.from_user.id
    
    user_data = await get_user_data(clicker_id)
    lang = user_data["language"] if user_data and user_data["language"] else "en"

    if clicker_id != owner_id:
        await q.answer(t("err_not_your_menu", lang), show_alert=True)
        return

    if action_type == "set_mood":
        await update_user_pref(owner_id, "mood", value)
        final_msg = t("msg_mood_updated", lang, mood=value)
        
    elif action_type == "set_genre":
        await update_user_pref(owner_id, "genres", value)
        final_msg = t("msg_genre_updated", lang, genre=value)

    await q.answer("Kaydedildi / Saved")
    await q.edit_message_text(final_msg)