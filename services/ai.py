import logging
import random
from groq import AsyncGroq
from app.config import GROQ_API_KEY, GROQ_MODEL

STRATEGIES = [
    "Recommend a highly-rated masterpiece.",
    "Recommend a hidden gem that is underrated.",
    "Recommend a cult classic.",
    "Recommend a visually stunning modern anime.",
    "Recommend something with a unique plot twist.",
    "Recommend a currently trending or recent hit."
]

async def generate_anime_recommendation(user_input: str, mood: str, genres: str, lang: str, excluded_list: list = None) -> str:
    try:
        async with AsyncGroq(api_key=GROQ_API_KEY) as client:
            lang_name = "Turkish" if lang == "tr" else "English"
            
            avoid_text = ""
            if excluded_list and len(excluded_list) > 0:
                avoid_list_str = ", ".join(excluded_list)
                avoid_text = f"🚫 **AVOID THESE ANIMES**: Do NOT recommend these again: {avoid_list_str}. Find something different!"

            system_instruction = (
                f"You are Anime Sage, an expert Anime Recommendation Assistant.\n"
                f"Your Goal: Recommend ONE perfect anime based on the user's mood and genres.\n\n"
                f"🚨 **CRITICAL RULES (FOLLOW STRICTLY)** 🚨\n"
                f"1. **NO TRANSLATED TITLES**: You MUST use the original Japanese Romaji title or the official English title. NEVER translate the title into Turkish.\n"
                f"2. **SPECIFY FORMAT**: You MUST state if it is a TV Series, Movie, OVA, or ONA.\n"
                f"3. **BE RELEVANT**: Respect the Genres: {genres} and Mood: {mood}.\n"
                f"4. **LANGUAGE**: Write the description and headers in {lang_name}, but keep the Title in English/Romaji.\n"
                f"5. **RECENCY**: Don't just recommend old classics. Consider modern, airing, or recent anime (2020-2024) if they fit.\n"
                f"{avoid_text}\n\n"
                f"📝 **OUTPUT FORMAT**:\n"
                f"🎬 **Title** (Year) - [Format]\n"
                f"⭐ Score: X/10\n"
                f"🎭 Genre: A, B\n"
                f"📝 **Overview:** Write a engaging description (2-3 sentences) in {lang_name} explaining why it fits the user's request."
            )

            context_parts = []
            if user_input: context_parts.append(f"User Request: {user_input}")
            if genres: context_parts.append(f"User Likes Genres: {genres}")
            if mood: context_parts.append(f"User Mood: {mood}")
            
            current_strategy = random.choice(STRATEGIES)
            context_parts.append(f"Strategy: {current_strategy}")
            
            final_user_content = ". ".join(context_parts)

            completion = await client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": final_user_content}
                ],
                model=GROQ_MODEL,
                temperature=0.85,
                max_tokens=400,
            )

            return completion.choices[0].message.content.strip()

    except Exception as e:
        error_msg = str(e)
        logging.error(f"Groq API Error: {error_msg}")
        if lang == "tr":
            if "404" in error_msg: return "⚠️ Model şu an bakımda."
            if "429" in error_msg: return "⚠️ Çok fazla istek var, lütfen bekleyin."
            return "⚠️ Bağlantı hatası oluştu."
        else:
            if "404" in error_msg: return "⚠️ Model is under maintenance."
            if "429" in error_msg: return "⚠️ Too many requests, please wait."
            return "⚠️ Connection error occurred."

async def get_anime_info(anime_name: str, lang: str) -> str:
    try:
        async with AsyncGroq(api_key=GROQ_API_KEY) as client:
            lang_name = "Turkish" if lang == "tr" else "English"
            system_instruction = (
                f"You are Anime Sage, an expert Anime Encyclopedia.\n"
                f"Task: Provide detailed information about the anime requested by the user.\n\n"
                f"🚨 **CRITICAL RULES** 🚨\n"
                f"1. **NO TRANSLATED TITLES**: Use the original Japanese Romaji or official English title. NEVER translate the title into Turkish.\n"
                f"2. **FORMAT**: State if it is TV, Movie, OVA, etc.\n"
                f"3. **SPOILER FREE**: Provide a compelling summary without spoiling key plot points.\n"
                f"4. **LANGUAGE**: Write the description and labels in {lang_name}, but keep the Title and Studio names original.\n\n"
                f"📝 **OUTPUT FORMAT**:\n"
                f"🎬 **Title** (Year) - [Format]\n"
                f"🏢 Studio: X\n"
                f"⭐ Score: X/10\n"
                f"🎭 Genre: A, B\n"
                f"📜 **Status:** Finished / Airing\n"
                f"📝 **Synopsis:** Write a concise, engaging summary (2-3 sentences) in {lang_name}."
            )
            completion = await client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": f"Tell me about this anime: {anime_name}"}
                ],
                model=GROQ_MODEL,
                temperature=0.5,
                max_tokens=450,
            )
            return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"