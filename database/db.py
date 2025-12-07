import aiosqlite

DB_PATH = "anime_sage.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                group_id INTEGER PRIMARY KEY,
                language TEXT DEFAULT 'en',
                settings TEXT DEFAULT '{}'
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                group_id INTEGER,
                genres TEXT DEFAULT '',
                mood TEXT DEFAULT '',
                stats INTEGER DEFAULT 0
            )
        """)
        await db.commit()

async def get_group_lang(group_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT language FROM groups WHERE group_id = ?", (group_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else "en"

async def set_group_lang(group_id: int, lang: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR REPLACE INTO groups (group_id, language) VALUES (?, ?)", (group_id, lang))
        await db.commit()

async def update_user_pref(user_id: int, group_id: int, key: str, value: str):
    async with aiosqlite.connect(DB_PATH) as db:
        exists = await db.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
        if not await exists.fetchone():
            await db.execute("INSERT INTO users (user_id, group_id) VALUES (?, ?)", (user_id, group_id))
        
        await db.execute(f"UPDATE users SET {key} = ? WHERE user_id = ?", (value, user_id))
        await db.commit()

async def get_user_data(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchone()

async def increment_stats(user_id: int, group_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id, group_id, stats) VALUES (?, ?, 0)", (user_id, group_id))
        await db.execute("UPDATE users SET stats = stats + 1 WHERE user_id = ?", (user_id,))
        await db.commit()

async def get_group_stats(group_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*), SUM(stats) FROM users WHERE group_id = ?", (group_id,)) as cursor:
            return await cursor.fetchone()