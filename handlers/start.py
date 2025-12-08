from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.db import register_user, get_user_lang, set_user_lang
from utils.languages import t

LANG_KB = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Türkçe 🇹🇷", callback_data="setlang_tr"),
        InlineKeyboardButton("English 🇬🇧", callback_data="setlang_en")
    ]
])

async def start_handler(c: Client, m: Message):
    user_id = m.from_user.id
    
    await register_user(user_id)
    
    lang = await get_user_lang(user_id)
    
    if m.chat.type == enums.ChatType.PRIVATE:
        if not lang:
            await m.reply_text(
                "👋 **Welcome / Hoş Geldiniz!**\n\n"
                "Lütfen bir dil seçin / Please select a language:",
                reply_markup=LANG_KB
            )
            return
        
        await m.reply_text(t("welcome", lang, name=m.from_user.first_name))
    else:
        if not lang:
            bot_username = (await c.get_me()).username
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("Ayarla / Setup", url=f"https://t.me/{bot_username}?start=lang")]])
            await m.reply_text("Please set your language privately first.", reply_markup=kb)
        else:
            await m.reply_text(t("welcome", lang, name=m.from_user.first_name))

async def lang_callback_handler(c: Client, q: CallbackQuery):
    lang_code = q.data.split("_")[1] 
    
    await set_user_lang(q.from_user.id, lang_code)
    
    success_msg = "🇹🇷 Dil Türkçe olarak ayarlandı! Artık botu kullanabilirsiniz." if lang_code == "tr" else "🇬🇧 Language set to English! You can now use the bot."
    
    await q.answer(success_msg)
    await q.message.edit_text(
        f"{success_msg}\n\n👉 /recommend",
        reply_markup=None
    )

async def language_command_handler(c: Client, m: Message):
    await m.reply_text("Dil seçimi / Language selection:", reply_markup=LANG_KB)