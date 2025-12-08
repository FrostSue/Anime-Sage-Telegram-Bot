import asyncio
import logging
import os
from dotenv import load_dotenv
from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from database.db import init_db
from utils.languages import load_languages
from utils.menu import set_bot_commands
from handlers.start import start_handler, lang_callback_handler, language_command_handler
from handlers.recommend import recommend_handler
from handlers.preferences import set_genres, set_mood, reset_prefs, pref_callback_handler
from handlers.help import help_handler
from handlers.stats import stats_handler
from handlers.admin import admin_panel

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

async def main():
    logger.info("⏳ Veritabanı başlatılıyor...")
    await init_db()
    
    logger.info("🌍 Diller yükleniyor...")
    load_languages()

    app = Client("data/anime_sage_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

    logger.info("⚙️ Komutlar sisteme kaydediliyor...")
    app.add_handler(MessageHandler(start_handler, filters.command("start")))
    app.add_handler(MessageHandler(language_command_handler, filters.command("language")))
    app.add_handler(CallbackQueryHandler(lang_callback_handler, filters.regex(r"^setlang_")))
    app.add_handler(MessageHandler(recommend_handler, filters.command("recommend")))
    app.add_handler(MessageHandler(set_genres, filters.command("setgenres")))
    app.add_handler(MessageHandler(set_mood, filters.command("setmood")))
    app.add_handler(MessageHandler(reset_prefs, filters.command("resetprefs")))
    app.add_handler(CallbackQueryHandler(pref_callback_handler, filters.regex(r"^(set_|cancel_)")))
    app.add_handler(MessageHandler(help_handler, filters.command("help")))
    app.add_handler(MessageHandler(stats_handler, filters.command("stats")))
    app.add_handler(MessageHandler(admin_panel, filters.command("adminpanel")))

    async with app:
        me = await app.get_me()
        logger.info(f"✅ ANIME SAGE AKTİF: @{me.username}")
        await set_bot_commands(app)
        await idle()

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(main())
    except KeyboardInterrupt: pass
    except RuntimeError: pass