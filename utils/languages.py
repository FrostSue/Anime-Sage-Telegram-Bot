import json
import os

LANG_CACHE = {}

def load_languages():
    lang_dir = "lang"
    for filename in os.listdir(lang_dir):
        if filename.endswith(".json"):
            lang_code = filename.split(".")[0]
            with open(os.path.join(lang_dir, filename), "r", encoding="utf-8") as f:
                LANG_CACHE[lang_code] = json.load(f)

def t(key: str, lang: str = "en", **kwargs) -> str:
    text = LANG_CACHE.get(lang, {}).get(key, LANG_CACHE.get("en", {}).get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text