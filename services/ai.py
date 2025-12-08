import logging
import random
from groq import AsyncGroq
from app.config import GROQ_API_KEY, GROQ_MODEL

STRATEGIES = [
    "Recommend a highly-rated masterpiece.",
    "Recommend a hidden gem that is underrated.",
    "Recommend a cult classic from the past.",
    "Recommend a visually stunning modern anime.",
    "Recommend something with a very unique plot twist.",
    "Recommend a fan-favorite trending anime."
]

async def generate_anime_recommendation(user_input: str, mood: str, genres: str, lang: str) -> str:
    """
    Kullanıcı girdisini alır, rastgele bir strateji seçer ve AI'dan buna göre öneri ister.
    Dil zorlaması içerir.
    """
    try:
        async with AsyncGroq(api_key=GROQ_API_KEY) as client:
            
            current_strategy = random.choice(STRATEGIES)

            lang_name = "Turkish" if lang == "tr" else "English"
            
            system_instruction = (
                f"You are Anime Sage. "
                f"CRITICAL RULE: You MUST write the entire response in {lang_name} language ONLY.\n"
                f"Task: Recommend ONE anime.\n"
                f"Strategy: {current_strategy}\n"
                f"Constraint: Do not always recommend Naruto/One Piece.\n\n"
                f"Format exactly like this (Translate headers to {lang_name}):\n"
                f"🎬 **Title** (Year)\n"
                f"⭐ Score: X/10\n"
                f"🎭 Genre: A, B\n"
                f"📝 **Overview:** Write a engaging description (2-3 sentences) in {lang_name} explaining the hook."
            )

            context_parts = []
            if user_input: 
                context_parts.append(f"User Request: {user_input}")
                system_instruction += " (Prioritize User Request)"
            
            if genres: context_parts.append(f"User Likes: {genres}")
            if mood: context_parts.append(f"User Mood: {mood}")
            
            if not context_parts: 
                context_parts.append("Surprise the user.")

            final_user_content = ". ".join(context_parts)

            completion = await client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": final_user_content}
                ],
                model=GROQ_MODEL,
                temperature=0.85,
                max_tokens=350,
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