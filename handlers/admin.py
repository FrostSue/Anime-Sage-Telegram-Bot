from pyrogram import Client, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.db import get_group_lang, set_group_lang
from utils.languages import t

async def is_admin(c: Client, chat_id: int, user_id: int) -> bool:
    try:
        member = await c.get_chat_member(chat_id, user_id)
        return member.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]
    except:
        return False

async def admin_panel(c: Client, m: Message):
    lang = await get_group_lang(m.chat.id)
    if not await is_admin(c, m.chat.id, m.from_user.id):
        return await m.reply_text(t("admin_only", lang))

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("TR 🇹🇷", callback_data="lang_tr"), InlineKeyboardButton("EN 🇬🇧", callback_data="lang_en")]
    ])
    await m.reply_text(t("admin_panel_title", lang), reply_markup=kb)

async def language_handler(c: Client, m: Message):
    await admin_panel(c, m)

async def lang_callback(c: Client, q: CallbackQuery):
    if not await is_admin(c, q.message.chat.id, q.from_user.id):
        return await q.answer("Admin only!", show_alert=True)
    
    new_lang = q.data.split("_")[1]
    await set_group_lang(q.message.chat.id, new_lang)
    await q.answer()
    await q.message.edit_text(t("lang_changed", new_lang))