import aiosqlite

DB_PATH = "anime_sage.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                group_id INTEGER PRIMARY KEY
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                language TEXT DEFAULT NULL,
                genres TEXT DEFAULT '',
                mood TEXT DEFAULT '',
                stats INTEGER DEFAULT 0
            )
        """)
        await db.commit()


async def register_user(user_id: int):
    """Kullanıcıyı veritabanına ekler (Varsa atlar)."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def is_user_registered(user_id: int) -> bool:
    """Kullanıcı kayıtlı mı kontrol eder."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchone() is not None

async def get_user_lang(user_id: int) -> str:
    """Kullanıcının dilini döndürür. Ayarlı değilse None döner."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT language FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row and row[0] else None

async def set_user_lang(user_id: int, lang: str):
    """Kullanıcının dilini günceller."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.execute("UPDATE users SET language = ? WHERE user_id = ?", (lang, user_id))
        await db.commit()


async def update_user_pref(user_id: int, key: str, value: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(f"UPDATE users SET {key} = ? WHERE user_id = ?", (value, user_id))
        await db.commit()

async def get_user_data(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchone()

async def increment_stats(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET stats = stats + 1 WHERE user_id = ?", (user_id,))
        await db.commit()

async def get_global_stats():
    """
    Admin paneli için global istatistikleri çeker.
    Dönüş: (toplam_kullanıcı, toplam_öneri_sayısı)
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*), SUM(stats) FROM users") as cursor:
            row = await cursor.fetchone()
            if row:
                total_users = row[0]
                total_recs = row[1] if row[1] is not None else 0
                return total_users, total_recs
            return 0, 0