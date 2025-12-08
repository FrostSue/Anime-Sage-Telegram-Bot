import os
import sys
from pyrogram import Client, filters
from pyrogram.types import Message
from database.db import get_global_stats
from app.config import ADMIN_IDS

async def admin_panel(c: Client, m: Message):
    user_id = m.from_user.id
    
    if user_id not in ADMIN_IDS:
        return

    total_users, total_recs = await get_global_stats()
    
    py_ver = sys.version.split()[0]
    
    msg = (
        f"👮‍♂️ **Yönetici Kontrol Paneli**\n"
        f"──────────────────────\n"
        f"👥 **Toplam Kullanıcı:** `{total_users}`\n"
        f"🤖 **Toplam AI Önerisi:** `{total_recs}`\n"
        f"──────────────────────\n"
        f"🐍 **Python:** v{py_ver}\n"
        f"📡 **Durum:** Online ✅"
    )
    
    await m.reply_text(msg, quote=True)

async def language_handler(c, m): pass
async def lang_callback(c, q): pass