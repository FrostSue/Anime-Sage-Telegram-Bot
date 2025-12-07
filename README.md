# 🧙‍♂️ Anime Sage - AI Powered Recommender Bot

**Anime Sage** is a high-performance, asynchronous Telegram bot designed to provide personalized anime recommendations.

It utilizes the **Groq API (Llama 3.1)** to analyze user viewing history, favorite genres, and current mood to deliver pinpoint suggestions. Built with a robust architecture that ensures stability on both Windows and Linux environments.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Pyrogram](https://img.shields.io/badge/Pyrogram-v2-orange) ![AI](https://img.shields.io/badge/AI-Llama%203.1-green) ![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 🚀 Features

-   **🧠 AI-Powered:** Uses the `llama-3.1-8b-instant` model for context-aware, intelligent recommendations.
-   **🎲 Diversity Strategy:** Avoids repetitive suggestions by randomly selecting strategies (e.g., "Hidden Gems", "Cult Classics", "Modern Hits").
-   **🌍 Multi-Language Support:** Independent **English (EN)** and **Turkish (TR)** language settings for each group.
-   **💾 Personalization:** Stores user favorite genres and moods in a local SQLite database.
-   **⚡ High Performance:**
    -   Utilizes `uvloop` on Linux servers for maximum speed.
    -   Fully compatible with Windows via standard `asyncio` fallback (Cross-Platform).
-   **🛡️ Stable Architecture:** Implements a "Manual Handler Registration" system to prevent `RuntimeError` and Event Loop conflicts.

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/anime-sage-bot.git](https://github.com/YOUR_USERNAME/anime-sage-bot.git)
cd anime-sage-bot
````

### 2\. Install Requirements

```bash
pip install -r requirements.txt
```

*(Note: `uvloop` is automatically skipped on Windows systems.)*

### 3\. Configuration (.env)

Create a `.env` file in the root directory and fill in the following details:

```ini
# Telegram API Credentials (my.telegram.org)
API_ID=123456
API_HASH=your_api_hash_here
BOT_TOKEN=your_bot_token_here

# Admin IDs (Comma separated)
ADMIN_IDS=123456789,987654321

# AI Configuration (console.groq.com)
GROQ_API_KEY=gsk_your_groq_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

### 4\. Run the Bot

```bash
python main.py
```

## 🎮 Commands

| Command | Description |
| :--- | :--- |
| `/start` | Initializes the bot and checks language settings. |
| `/recommend` | **(Core Feature)** Get an AI anime recommendation. <br> *Ex: `/recommend something like Naruto but darker`* |
| `/setgenres` | Save your favorite genres. *Ex: `/setgenres Action, Horror`* |
| `/setmood` | Save your current mood. *Ex: `/setmood Depressed`* |
| `/resetprefs` | Reset your saved preferences. |
| `/stats` | View group usage statistics. |
| `/adminpanel` | Open the admin control panel. |
| `/language` | Change the bot's language (Admins Only). |

## 📂 Project Structure

```text
anime-sage-bot/
├── main.py            # Entry point & Handler registration
├── app/               # Bot configuration
├── database/          # SQLite database layer (async)
├── services/          # Groq AI integration layer
├── handlers/          # Command handlers (Pure functions)
├── utils/             # Language & Menu utilities
└── lang/              # JSON language files (tr.json, en.json)
```

## ⚠️ Troubleshooting

  * **`uvloop` warning on Windows:** This is normal behavior. The bot automatically falls back to standard `asyncio` on Windows to ensure compatibility.
  * **Groq 404/Decommissioned Error:** Ensure your `.env` file is set to `GROQ_MODEL=llama-3.1-8b-instant`. Older Llama 3 models have been deprecated by Groq.

## 📜 License

This project is licensed under the MIT License.
