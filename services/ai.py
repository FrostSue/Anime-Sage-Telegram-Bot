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
    """
    try:
        async with AsyncGroq(api_key=GROQ_API_KEY) as client:
            
            current_strategy = random.choice(STRATEGIES)

            system_instruction = (
                f"You are Anime Sage. Language: {lang}. "
                f"Task: Recommend ONE anime. "
                f"Current Strategy: {current_strategy} "
                f"IMPORTANT: Do not always recommend the most obvious/popular ones like Naruto or One Piece unless specifically asked. "
                f"Format exactly:\n"
                f"🎬 **Title** (Year)\n"
                f"⭐ Score: X/10\n"
                f"🎭 Genre: A, B\n"
                f"📝 **Overview:** A engaging description (2-3 sentences) explaining the hook."
            )

            context_parts = []
            if user_input: 
                context_parts.append(f"User Request: {user_input}")
                system_instruction += " (Prioritize User Request over Strategy)"
            
            if genres: context_parts.append(f"User Likes: {genres}")
            if mood: context_parts.append(f"User Mood: {mood}")
            
            if not context_parts: 
                context_parts.append("Surprise the user with something good.")

            final_user_content = ". ".join(context_parts)

            completion = await client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": final_user_content}
                ],
                model=GROQ_MODEL,
                temperature=0.85,
                max_tokens=300,
            )

            return completion.choices[0].message.content.strip()

    except Exception as e:
        error_msg = str(e)
        logging.error(f"Groq API Error: {error_msg}")
        
        if "404" in error_msg or "decommissioned" in error_msg:
            return "⚠️ Model şu an güncelleniyor, lütfen geliştiriciye bildirin."
        elif "429" in error_msg:
            return "⚠️ Çok fazla istek var, biraz bekleyin."
            
        return "⚠️ Bağlantı hatası oluştu."