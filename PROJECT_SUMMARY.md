# Anime Sage - Technical Architecture (v1.3)

## Overview
Anime Sage is an asynchronous, AI-powered Telegram bot designed to provide personalized anime recommendations using Large Language Models (LLM). It features a robust, cross-platform architecture suitable for both high-performance Linux servers and Windows development environments.

## Core Stack
- **Language**: Python 3.10+
- **Framework**: Pyrogram v2 (MTProto Client)
- **Database**: SQLite (via `aiosqlite`) stored in `data/` directory.
- **AI Provider**: Groq Cloud (`llama-3.1-8b-instant`)
- **Containerization**: Docker & Docker Compose (Ubuntu/Debian compatible)

## Key Systems

### 1. Hybrid Handler Registration
- **Mechanism**: Manual registration via `app.add_handler()` in `main.py`.
- **Reason**: Prevents event loop conflicts (`RuntimeError`) on Windows and ensures deterministic startup order.
- **Scope**: All handlers are pure functions, decoupled from the global client instance.

### 2. User-Based Localization & Auth
- **System**: Users must register (private start) to select a language (TR/EN).
- **Storage**: `users` table stores language, genre, mood, and stats per user.
- **Auth Guard**: `utils.auth.check_user_registration` decorator enforces registration before core actions.

### 3. AI Service & Guardrails
- **Model**: `llama-3.1-8b-instant` via `AsyncGroq`.
- **Context**: Injects user preferences (Genre/Mood) into the system prompt.
- **Safety**: Includes strict system instructions to refuse off-topic (politics, coding) or unsafe inputs.
- **Diversity**: Randomization strategies prevent repetitive recommendations.

### 4. Interactive UI
- **Preferences**: Inline Keyboards for selecting Genres and Moods (no text input required).
- **Admin Panel**: Owner-only dashboard showing global user counts and interaction stats.

## Deployment Strategy
- **Docker**: Uses `python:3.10-slim` base image.
- **Persistence**: Database stored in a mounted `data/` volume to prevent data loss and Docker directory conflicts.
- **Logs**: Real-time logging via `PYTHONUNBUFFERED=1`.