from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.db import is_user_registered, get_user_lang, get_sudoers
from utils.languages import t
from app.config import ADMIN_IDS

async def check_user_registration(c: Client, m: Message) -> tuple[bool, str]:
    user_id = m.from_user.id
    
    if not await is_user_registered(user_id):
        bot_username = (await c.get_me()).username
        deep_link = f"https://t.me/{bot_username}?start=register"
        
        msg_text = (
            "⚠️ **Registration Required / Kayıt Gerekli**\n\n"
            "🇹🇷 Lütfen dil seçimi yapmak için botu başlatın.\n"
            "🇬🇧 Please start the bot to select your language.\n\n"
            "👇 **Click Below / Aşağıya Tıkla**"
        )
        
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Start Bot / Botu Başlat", url=deep_link)]
        ])
        
        await m.reply_text(msg_text, reply_markup=kb, quote=True, disable_web_page_preview=True)
        return False, "en"

    lang = await get_user_lang(user_id)
    if not lang:
        await m.reply_text("⚠️ Please set your language first via /language.")
        return False, "en"
        
    return True, lang

async def is_admin(user_id: int) -> bool:
    if user_id in ADMIN_IDS:
        return True
    
    sudo_list = await get_sudoers()
    if user_id in sudo_list:
        return True
        
    return False