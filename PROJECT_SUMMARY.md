# Anime Sage - Technical Summary

## Purpose
A high-performance Telegram bot providing tailored anime recommendations via AI.

## Architecture
- **Framework**: Pyrogram v2 (Async).
- **AI Engine**: Groq API (Llama 3 models) via `services/ai.py`.
- **Database**: SQLite with `aiosqlite`.
- **Logic**: User requests -> AI Prompt Engineering -> Structured Response.

## AI Logic
The bot acts as a middleman. It wraps user input with a strict system prompt to ensure:
1. Responses are short (max 40 words) to save tokens.
2. Output follows a specific format (Title, Score, Genre, Summary).
3. Context (User mood/genres) is injected automatically if no specific query is made.
