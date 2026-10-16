"""
Facebook Reels Automation - Bilingual English/Punjabi Content Generator
IMPROVED VERSION: Better backgrounds, English categories, no repeats, VELOCITY PUNJABI branding
Rounded container style from Habla Verse
"""

import os
import sys
import json
import random
import asyncio
import subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")
load_dotenv()

POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY")
AI_MODEL = os.getenv("AI_MODEL")

if not AI_MODEL:
    raise ValueError(
        "AI_MODEL not set! Please add 'AI_MODEL=gemini-fast' to your .env file. "
        "For GitHub Actions: Add AI_MODEL to repository secrets."
    )
OUTPUT_DIR = BASE_DIR / "output"
IMAGES_DIR = OUTPUT_DIR / "images"
AUDIO_DIR = OUTPUT_DIR / "audio"
VIDEO_DIR = OUTPUT_DIR / "video"
HISTORY_DIR = OUTPUT_DIR / "history"

for d in [OUTPUT_DIR, IMAGES_DIR, AUDIO_DIR, VIDEO_DIR, HISTORY_DIR]:
    d.mkdir(exist_ok=True)

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 30

CATEGORIES_ENGLISH = [
    "Greetings",
    "Basic Phrases",
    "Common Expressions",
    "Travel",
    "Restaurant",
    "Shopping",
    "Emergency",
    "Family Terms",
    "Numbers",
    "Time",
    "Motivation",
    "Love",
    "Success",
    "Wisdom",
    "Happiness",
    "Self Improvement",
    "Gratitude",
    "Friendship",
    "Hope",
    "Creativity",
    "Inner Peace",
    "Confidence",
    "Perseverance",
    "Inspiration",
    "Positive Life",
    "Courage",
    "Kindness",
    "Patience",
    "Forgiveness",
    "Strength",
    "Joy",
    "Balance",
    "Growth",
    "Purpose",
    "Mindfulness",
    "Daily Routine",
    "Weather",
    "Feelings",
    "Food",
    "Health",
    "Work",
    "Technology",
    "Nature",
    "Animals",
    "Colors",
    "Directions",
    "Body Parts",
    "Clothes",
    "Music",
    "Sports",
    "Holidays",
    "Education",
    "Culture",
    "Finance",
    "Relationships",]

CATEGORIES_NATIVE = {
    "Greetings": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ",
    "Basic Phrases": "ਮੁੱਢਲੇ ਵਾਕ",
    "Common Expressions": "ਆਮ ਸਮੀਕਰਨ",
    "Travel": "ਯਾਤਰਾ",
    "Restaurant": "ਰੈਸਟੋਰੈਂਟ",
    "Shopping": "ਖਰੀਦਦਾਰੀ",
    "Emergency": "ਐਮਰਜੈਂਸੀ",
    "Family Terms": "ਪਰਿਵਾਰਕ ਸ਼ਬਦ",
    "Numbers": "ਨੰਬਰ",
    "Time": "ਸਮਾਂ",
    "Motivation": "ਪ੍ਰੇਰਣਾ",
    "Love": "ਪਿਆਰ",
    "Success": "ਸਫਲਤਾ",
    "Wisdom": "ਬੁੱਧੀ",
    "Happiness": "ਖੁਸ਼ੀ",
    "Self Improvement": "ਸਵੈ-ਸੁਧਾਰ",
    "Gratitude": "ਸ਼ੁਕਰਗੁਜ਼ਾਰ",
    "Friendship": "ਦੋਸਤੀ",
    "Hope": "ਉਮੀਦ",
    "Creativity": "ਸਿਰਜਣਾਤਮਕਤਾ",
    "Inner Peace": "ਅੰਦਰੂਨੀ ਸ਼ਾਂਤੀ",
    "Confidence": "ਵਿਸ਼ਵਾਸ",
    "Perseverance": "ਦ੍ਰਿੜਤਾ",
    "Inspiration": "ਪ੍ਰੇਰਨਾ",
    "Positive Life": "ਸਕਾਰਾਤਮਕ ਜੀਵਨ",
    "Courage": "ਹਿੰਮਤ",
    "Kindness": "ਦਿਆਲਤਾ",
    "Patience": "ਧੀਰਜ",
    "Forgiveness": "ਮਾਫੀ",
    "Strength": "ਤਾਕਤ",
    "Joy": "ਅਨੰਦ",
    "Balance": "ਸੰਤੁਲਨ",
    "Growth": "ਵਿਕਾਸ",
    "Purpose": "ਉਦੇਸ਼",
    "Mindfulness": "ਸਾਵਧਾਨਤਾ",
    "Daily Routine": "ਰੋਜ਼ਾਨਾ ਰੁਟੀਨ",
    "Weather": "ਮੌਸਮ",
    "Feelings": "ਭਾਵਨਾਵਾਂ",
    "Food": "ਭੋਜਨ",
    "Health": "ਸਿਹਤ",
    "Work": "ਕਮ੍ਮ",
    "Technology": "ਤਕਨਾਲੋਜੀ",
    "Nature": "ਕੁਦਰਤ",
    "Animals": "ਜਾਨਵਰ",
    "Colors": "ਰੰਗ",
    "Directions": "ਦਿਸ਼ਾਵਾਂ",
    "Body Parts": "ਸਰੀਰ ਦੇ ਅੰਗ",
    "Clothes": "ਕਪਡ਼ੇ",
    "Music": "ਸੰਗੀਤ",
    "Sports": "ਖੇਡਾਂ",
    "Holidays": "ਛੁਟ੍ਟੀਆਂ",
    "Education": "ਸਿੱਖਿਆ",
    "Culture": "ਸਭਿਆਚਾਰ",
    "Finance": "ਵਿੱਤ",
    "Relationships": "ਰਿਸ਼ਤੇ"
}

ENGLISH_VOICE = "en-US-GuyNeural"
NATIVE_VOICE = ""

PHRASE_HISTORY_FILE = HISTORY_DIR / "all_generated_phrases.json"
RECENT_CATEGORIES_FILE = HISTORY_DIR / "recent_categories.json"
MAX_RECENT_CATEGORIES = 25


def load_phrase_history():
    if PHRASE_HISTORY_FILE.exists():
        with open(PHRASE_HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"phrases": [], "last_updated": None}


def save_phrase_history(data):
    data["last_updated"] = datetime.now().isoformat()
    with open(PHRASE_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def is_phrase_used(english_phrase):
    history = load_phrase_history()
    english_lower = english_phrase.lower().strip()
    for p in history.get("phrases", []):
        if p.get("english", "").lower().strip() == english_lower:
            return True
    return False


def add_phrases_to_history(phrases, category):
    history = load_phrase_history()
    lang_key = "punjabi"
    for phrase in phrases:
        history["phrases"].append({
            "english": phrase["english"],
            lang_key: phrase[lang_key],
            "transliteration": phrase.get("transliteration", ""),
            "category": category,
            "generated_at": datetime.now().isoformat()
        })
    save_phrase_history(history)
    print(f"[history] Added {len(phrases)} phrases to history (total: {len(history['phrases'])})")


def load_recent_categories():
    if RECENT_CATEGORIES_FILE.exists():
        with open(RECENT_CATEGORIES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"recent_categories": [], "last_updated": None}


def save_recent_categories(data):
    data["last_updated"] = datetime.now().isoformat()
    with open(RECENT_CATEGORIES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_available_category():
    recent_data = load_recent_categories()
    recent = recent_data.get("recent_categories", [])
    available = [cat for cat in CATEGORIES_ENGLISH if cat not in recent]
    if not available:
        recent_data["recent_categories"] = recent[-5:]
        save_recent_categories(recent_data)
        available = [cat for cat in CATEGORIES_ENGLISH if cat not in recent_data["recent_categories"]]
        print(f"[rotation] All categories used recently - cleared old ones, {len(available)} available")
    selected = random.choice(available)
    recent.append(selected)
    if len(recent) > MAX_RECENT_CATEGORIES:
        recent = recent[-MAX_RECENT_CATEGORIES:]
    recent_data["recent_categories"] = recent
    save_recent_categories(recent_data)
    print(f"[rotation] Selected '{selected}' ({len(available)} available, {len(recent)} in recent history)")
    return selected


def generate_phrases(category_english: str, num_phrases: int = 5) -> list:
    category_native = CATEGORIES_NATIVE[category_english]
    max_attempts = 3

    history = load_phrase_history()
    recent_english = [p["english"] for p in history.get("phrases", []) if p.get("category") == category_english][-30:]

    for attempt in range(max_attempts):
        try:
            import requests
            url = "https://gen.pollinations.ai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {POLLINATIONS_API_KEY}",
                "Content-Type": "application/json"
            }

            avoid_text = ""
            if recent_english:
                avoid_text = "\nABSOLUTELY AVOID these already-used phrases:\n" + "\n".join(f"- {p}" for p in recent_english)

            prompt = f"""Create {num_phrases * 6} unique and creative {category_english} phrases for English speakers learning Punjabi.{avoid_text}

IMPORTANT RULES FOR NATURAL SPEECH:
1. Keep phrases SHORT (5-12 words max per language)
2. Add NATURAL PAUSES using commas (e.g., "Dream big, start small")
3. Use punctuation for breathing room in TTS
4. Avoid long run-on sentences
5. Each phrase should be speakable in 3-5 seconds
6. Punjabi text should be CLEAN - use standard Punjabi script
7. Do NOT include multiple versions or slashes - just ONE clean Punjabi translation
8. Transliteration should be in Roman script for pronunciation
9. BE CREATIVE AND VARIED - do NOT repeat themes from the avoid list

For each phrase:
1. English phrase (with commas for natural pauses)
2. Punjabi translation (in Punjabi script)
3. Transliteration (Roman script pronunciation)

Return as JSON array:
[{{"english": "...", "punjabi": "...", "transliteration": "..."}}]

IMPORTANT: Create FRESH, UNIQUE phrases that haven't been used before.
IMPORTANT: Punjabi text must be clean - no slashes, no multiple versions."""

            payload = {
                "model": AI_MODEL,
                "messages": [
                    {"role": "system", "content": "You are a Punjabi teacher. Create short, natural phrases with pauses. Each generation must produce completely different, creative phrases."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": min(0.95 + attempt * 0.03, 1.0)
            }

            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()

            data = response.json()
            content = data["choices"][0]["message"]["content"].strip()

            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            phrases = json.loads(content)

            for p in phrases:
                if "transliteration" not in p and "romaji" in p:
                    p["transliteration"] = p.pop("romaji")
                if "punjabi" not in p:
                    alt_keys = ["punjabi_text", "native", "translation", p.get("language", "")]
                    for k in alt_keys:
                        if k in p:
                            p["punjabi"] = p.pop(k)
                            break
                if "punjabi" not in p:
                    continue

            unique_phrases = []
            for phrase in phrases:
                if len(phrase["english"].split()) > 15:
                    continue
                if not is_phrase_used(phrase["english"]):
                    unique_phrases.append(phrase)
                if len(unique_phrases) >= num_phrases:
                    break

            if len(unique_phrases) >= num_phrases:
                add_phrases_to_history(unique_phrases[:num_phrases], category_english)
                return unique_phrases[:num_phrases]

            print(f"[content] Attempt {attempt + 1}: API returned {len(phrases)} phrases, only {len(unique_phrases)} are new (need {num_phrases})")
            for p in unique_phrases:
                if p["english"] not in recent_english:
                    recent_english.append(p["english"])

        except Exception as e:
            print(f"[content] Attempt {attempt + 1} failed: {e}")

    print("[content] Using fallback phrases...")
    return get_fresh_fallback_phrases(category_english, num_phrases)



def get_fresh_fallback_phrases(category: str, num_phrases: int) -> list:
    """Return simple English fallback phrases when AI generation fails"""
    generic_fallbacks = [
        {"english": "Hello, nice to meet you.", "punjabi": "\u0a38\u0a24\u0a3f \u0a38\u0a4d\u0a30\u0a40 \u0a05\u0a15\u0a3e\u0a32, \u0a24\u0a41\u0a39\u0a3e\u0a28\u0a42\u0a70 \u0a2e\u0a3f\u0a32 \u0a15\u0a47 \u0a16\u0a41\u0a38\u0a3c\u0a40 \u0a39\u0a4b\u0a08\u0964", "transliteration": "Sat Sri Akal, tuh\u0101nu\u1e41 mil ke khush\u012b ho\u012b."},
        {"english": "Thank you very much.", "punjabi": "\u0a24\u0a41\u0a39\u0a3e\u0a21\u0a3e \u0a2c\u0a39\u0a41\u0a24 \u0a2c\u0a39\u0a41\u0a24 \u0a27\u0a70\u0a28\u0a35\u0a3e\u0a26\u0964", "transliteration": "Tuh\u0101\u1e0d\u0101 bahuta bahuta dhanav\u0101d."},
        {"english": "Good morning, have a great day.", "punjabi": "\u0a38\u0a3c\u0a41\u0a2d \u0a38\u0a35\u0a47\u0a30, \u0a24\u0a41\u0a39\u0a3e\u0a21\u0a3e \u0a26\u0a3f\u0a28 \u0a35\u0a27\u0a40\u0a06 \u0a30\u0a39\u0a47\u0964", "transliteration": "Shubha saver, tuh\u0101\u1e0d\u0101 dina vadh\u012b'\u0101 rahe."},
        {"english": "I love learning new languages.", "punjabi": "\u0a2e\u0a48\u0a28\u0a42\u0a70 \u0a28\u0a35\u0a40\u0a06\u0a02 \u0a2d\u0a3e\u0a38\u0a3c\u0a3e\u0a35\u0a3e\u0a02 \u0a38\u0a3f\u0a71\u0a16\u0a23\u0a3e \u0a2a\u0a38\u0a70\u0a26 \u0a39\u0a48\u0964", "transliteration": "Main\u016b\u1e41 nav\u012b'\u0101\u1e41 bh\u0101sh\u0101v\u0101\u1e41 sikha\u1e47\u0101 pasanda hai."},
        {"english": "Never give up on your dreams.", "punjabi": "\u0a06\u0a2a\u0a23\u0a47 \u0a38\u0a41\u0a2a\u0a28\u0a3f\u0a06\u0a02 \u0a28\u0a42\u0a70 \u0a15\u0a26\u0a47 \u0a28\u0a3e \u0a1b\u0a71\u0a21\u0a4b\u0964", "transliteration": "\u0100pa\u1e47e supan'n\u0101\u1e41 n\u016b kade n\u0101 chha\u1e0do."},
        {"english": "Every day is a fresh start.", "punjabi": "\u0a39\u0a30 \u0a26\u0a3f\u0a28 \u0a07\u0a71\u0a15 \u0a28\u0a35\u0a40\u0a02 \u0a38\u0a3c\u0a41\u0a30\u0a42\u0a06\u0a24 \u0a39\u0a48\u0964", "transliteration": "Har dina ika nav\u012b\u1e41 shur\u016b'\u0101t hai."},
        {"english": "Believe in yourself always.", "punjabi": "\u0a39\u0a2e\u0a47\u0a38\u0a3c\u0a3e \u0a06\u0a2a\u0a23\u0a47 \u0a06\u0a2a '\u0a24\u0a47 \u0a35\u0a3f\u0a38\u0a3c\u0a35\u0a3e\u0a38 \u0a30\u0a71\u0a16\u0a4b\u0964", "transliteration": "Hamesh\u0101 \u0101pa\u1e47e \u0101pa 'te vishv\u0101sa rakho."},
        {"english": "Small steps lead to big changes.", "punjabi": "\u0a1b\u0a4b\u0a1f\u0a47 \u0a15\u0a26\u0a2e \u0a35\u0a71\u0a21\u0a47 \u0a2c\u0a26\u0a32\u0a3e\u0a05 \u0a32\u0a3f\u0a06\u0a09\u0a02\u0a26\u0a47 \u0a39\u0a28\u0964", "transliteration": "Chho\u1e6de kadama va\u1e0de badal\u0101'a li'\u0101'unde hana."},
        {"english": "You are stronger than you think.", "punjabi": "\u0a24\u0a41\u0a38\u0a40\u0a02 \u0a1c\u0a3f\u0a70\u0a28\u0a3e \u0a38\u0a4b\u0a1a\u0a26\u0a47 \u0a39\u0a4b \u0a09\u0a38 \u0a24\u0a4b\u0a02 \u0a1c\u0a3c\u0a3f\u0a06\u0a26\u0a3e \u0a2e\u0a1c\u0a3c\u0a2c\u0a42\u0a24 \u0a39\u0a4b\u0964", "transliteration": "Tus\u012b\u1e41 jina sochad\u0113 ho usa t\u014d zi'\u0101d\u0101 mazab\u016bta ho."},
        {"english": "Happiness is a choice, choose it.", "punjabi": "\u0a16\u0a41\u0a38\u0a3c\u0a40 \u0a07\u0a71\u0a15 \u0a1a\u0a4b\u0a23 \u0a39\u0a48, \u0a07\u0a38\u0a28\u0a42\u0a70 \u0a1a\u0a41\u0a23\u0a4b\u0964", "transliteration": "Khush\u012b ika cho\u1e47a hai, isan\u016b chuno."},
        {"english": "What time is it please.", "punjabi": "\u0a15\u0a3f\u0a30\u0a2a\u0a3e \u0a15\u0a30\u0a15\u0a47 \u0a38\u0a2e\u0a3e\u0a02 \u0a15\u0a40 \u0a39\u0a48\u0964", "transliteration": "Kirap\u0101 karake sam\u0101\u1e41 k\u012b hai."},
        {"english": "Where is the train station.", "punjabi": "\u0a30\u0a47\u0a32\u0a35\u0a47 \u0a38\u0a1f\u0a47\u0a38\u0a3c\u0a28 \u0a15\u0a3f\u0a71\u0a25\u0a47 \u0a39\u0a48\u0964", "transliteration": "Relv\u0113 s\u1e6d\u0113shana kidh\u0113 hai."},
        {"english": "How much does this cost.", "punjabi": "\u0a07\u0a38\u0a26\u0a40 \u0a15\u0a40\u0a2e\u0a24 \u0a15\u0a3f\u0a70\u0a28\u0a40 \u0a39\u0a48\u0964", "transliteration": "Isad\u012b k\u012bmata kinan\u012b hai."},
        {"english": "Can you help me please.", "punjabi": "\u0a15\u0a3f\u0a30\u0a2a\u0a3e \u0a15\u0a30\u0a15\u0a47 \u0a2e\u0a47\u0a30\u0a40 \u0a2e\u0a26\u0a26 \u0a15\u0a30 \u0a38\u0a15\u0a26\u0a47 \u0a39\u0a4b\u0964", "transliteration": "Kirap\u0101 karake m\u0113r\u012b madada kara sakad\u0113 ho."},
        {"english": "I would like a coffee please.", "punjabi": "\u0a2e\u0a48\u0a28\u0a42\u0a70 \u0a07\u0a71\u0a15 \u0a15\u0a4c\u0a2b\u0a40 \u0a1a\u0a3e\u0a39\u0a40\u0a26\u0a40 \u0a39\u0a48, \u0a15\u0a3f\u0a30\u0a2a\u0a3e \u0a15\u0a30\u0a15\u0a47\u0964", "transliteration": "Main\u016b\u1e41 ika kauf\u012b ch\u0101h\u012bd\u012b hai, kirap\u0101 karake."},
        {"english": "The food is delicious today.", "punjabi": "\u0a05\u0a71\u0a1c \u0a2d\u0a4b\u0a1c\u0a28 \u0a2c\u0a39\u0a41\u0a24 \u0a38\u0a41\u0a06\u0a26\u0a40 \u0a39\u0a48\u0964", "transliteration": "Aja bh\u014djana bahuta su'\u0101d\u012b hai."},
        {"english": "Have a wonderful weekend.", "punjabi": "\u0a24\u0a41\u0a39\u0a3e\u0a21\u0a3e \u0a35\u0a40\u0a15\u0a48\u0a02\u0a21 \u0a38\u0a3c\u0a3e\u0a28\u0a26\u0a3e\u0a30 \u0a30\u0a39\u0a47\u0964", "transliteration": "Tuh\u0101\u1e0d\u0101 v\u012bka'\u0113\u1e47\u1e0da sh\u0101nad\u0101ra rahe."},
        {"english": "Take care of yourself.", "punjabi": "\u0a06\u0a2a\u0a23\u0a3e \u0a16\u0a3f\u0a06\u0a32 \u0a30\u0a71\u0a16\u0a4b\u0964", "transliteration": "\u0100pa\u1e47\u0101 khi'\u0101la rakho."},
        {"english": "See you tomorrow my friend.", "punjabi": "\u0a15\u0a71\u0a32 \u0a2e\u0a3f\u0a32\u0a26\u0a47 \u0a39\u0a3e\u0a02 \u0a2e\u0a47\u0a30\u0a47 \u0a26\u0a4b\u0a38\u0a24\u0964", "transliteration": "Kala milad\u0113 h\u0101\u1e41 m\u0113r\u0113 d\u014dsta."},
        {"english": "The weather is beautiful outside.", "punjabi": "\u0a2c\u0a3e\u0a39\u0a30 \u0a2e\u0a4c\u0a38\u0a2e \u0a2c\u0a39\u0a41\u0a24 \u0a38\u0a41\u0a70\u0a26\u0a30 \u0a39\u0a48\u0964", "transliteration": "B\u0101hara mausa\u1e41 bahuta sundara hai."},
        {"english": "I am very happy today.", "punjabi": "\u0a2e\u0a48\u0a02 \u0a05\u0a71\u0a1c \u0a2c\u0a39\u0a41\u0a24 \u0a16\u0a41\u0a38\u0a3c \u0a39\u0a3e\u0a02\u0964", "transliteration": "Mai\u1e41 aja bahuta khusha h\u0101\u1e41."},
        {"english": "Learning a language opens new doors.", "punjabi": "\u0a2d\u0a3e\u0a38\u0a3c\u0a3e \u0a38\u0a3f\u0a71\u0a16\u0a23 \u0a28\u0a3e\u0a32 \u0a28\u0a35\u0a47\u0a02 \u0a26\u0a30\u0a35\u0a3e\u0a1c\u0a3c\u0a47 \u0a16\u0a41\u0a71\u0a32\u0a4d\u0a39\u0a26\u0a47 \u0a39\u0a28\u0964", "transliteration": "Bh\u0101sh\u0101 sikha\u1e47a n\u0101la nav\u0113 darav\u0101z\u0113 khulhad\u0113 hana."},
        {"english": "Keep practicing every single day.", "punjabi": "\u0a39\u0a30 \u0a30\u0a4b\u0a1c\u0a3c \u0a05\u0a2d\u0a3f\u0a06\u0a38 \u0a15\u0a30\u0a26\u0a47 \u0a30\u0a39\u0a4b\u0964", "transliteration": "Har r\u014dza abhi'\u0101sa karad\u0113 rah\u014d."},
        {"english": "You can achieve anything you want.", "punjabi": "\u0a24\u0a41\u0a38\u0a40\u0a02 \u0a1c\u0a4b \u0a1a\u0a3e\u0a39\u0a4b \u0a2a\u0a4d\u0a30\u0a3e\u0a2a\u0a24 \u0a15\u0a30 \u0a38\u0a15\u0a26\u0a47 \u0a39\u0a4b\u0964", "transliteration": "Tus\u012b\u1e41 j\u014d ch\u0101h\u014d pr\u0101pata kara sakad\u0113 ho."},
        {"english": "Rest when you are tired.", "punjabi": "\u0a1c\u0a26\u0a4b\u0a02 \u0a25\u0a71\u0a15 \u0a1c\u0a3e\u0a13 \u0a24\u0a3e\u0a02 \u0a06\u0a30\u0a3e\u0a2e \u0a15\u0a30\u0a4b\u0964", "transliteration": "Jad\u014d\u1e41 thaka j\u0101'\u014d t\u0101\u1e41 \u0101r\u0101ma karo."},
        {"english": "Focus on the positive things.", "punjabi": "\u0a38\u0a15\u0a3e\u0a30\u0a3e\u0a24\u0a2e\u0a15 \u0a1a\u0a40\u0a1c\u0a3c\u0a3e\u0a02 '\u0a24\u0a47 \u0a27\u0a3f\u0a06\u0a28 \u0a15\u0a47\u0a02\u0a26\u0a30\u0a3f\u0a24 \u0a15\u0a30\u0a4b\u0964", "transliteration": "Sak\u0101r\u0101tamaka ch\u012bz\u0101\u1e41 'te dhi'\u0101na k\u0113ndrita karo."},
        {"english": "Learn from your mistakes.", "punjabi": "\u0a06\u0a2a\u0a23\u0a40\u0a06\u0a02 \u0a17\u0a32\u0a24\u0a40\u0a06\u0a02 \u0a24\u0a4b\u0a02 \u0a38\u0a3f\u0a71\u0a16\u0a4b\u0964", "transliteration": "\u0100pa\u1e47\u012b'\u0101\u1e41 galat\u012b'\u0101\u1e41 t\u014d sikho."},
        {"english": "Trust the process completely.", "punjabi": "\u0a2a\u0a42\u0a30\u0a40 \u0a24\u0a30\u0a4d\u0a39\u0a3e\u0a02 \u0a2a\u0a4d\u0a30\u0a15\u0a3f\u0a30\u0a3f\u0a06 '\u0a24\u0a47 \u0a2d\u0a30\u0a4b\u0a38\u0a3e \u0a15\u0a30\u0a4b\u0964", "transliteration": "P\u016br\u012b tara\u1e41 prakiri'\u0101 'te bhar\u014ds\u0101 karo."},
        {"english": "Breathe deeply and stay calm.", "punjabi": "\u0a21\u0a42\u0a70\u0a18\u0a40 \u0a38\u0a3e\u0a39 \u0a32\u0a13 \u0a05\u0a24\u0a47 \u0a38\u0a3c\u0a3e\u0a02\u0a24 \u0a30\u0a39\u0a4b\u0964", "transliteration": "\u1e0c\u016b\u1e45gh\u012b s\u0101ha la'\u014d at\u0113 sh\u0101nta rah\u014d."},
        {"english": "Enjoy the little moments in life.", "punjabi": "\u0a1c\u0a40\u0a35\u0a28 \u0a26\u0a47 \u0a1b\u0a4b\u0a1f\u0a47 \u0a2a\u0a32\u0a3e\u0a02 \u0a26\u0a3e \u0a06\u0a28\u0a70\u0a26 \u0a2e\u0a3e\u0a23\u0a4b\u0964", "transliteration": "J\u012bvana d\u0113 chho\u1e6d\u0113 pal\u0101\u1e41 d\u0101 \u0101nanda m\u0101\u1e47\u014d."},
        {"english": "Smile more, worry less.", "punjabi": "\u0a35\u0a71\u0a27 \u0a2e\u0a41\u0a38\u0a15\u0a30\u0a3e\u0a13, \u0a18\u0a71\u0a1f \u0a1a\u0a3f\u0a70\u0a24\u0a3e \u0a15\u0a30\u0a4b\u0964", "transliteration": "Vadha musakar\u0101'\u014d, gha\u1e6da chint\u0101 karo."},
        {"english": "Be kind to everyone you meet.", "punjabi": "\u0a39\u0a30 \u0a15\u0a3f\u0a38\u0a47 \u0a28\u0a3e\u0a32 \u0a26\u0a3f\u0a06\u0a32\u0a42 \u0a2c\u0a23\u0a4b \u0a1c\u0a3f\u0a38\u0a28\u0a42\u0a70 \u0a24\u0a41\u0a38\u0a40\u0a02 \u0a2e\u0a3f\u0a32\u0a26\u0a47 \u0a39\u0a4b\u0964", "transliteration": "Har kis\u0113 n\u0101la di'\u0101l\u016b ba\u1e47\u014d jisan\u016b tus\u012b\u1e41 milad\u0113 ho."},
        {"english": "Help others without expecting anything back.", "punjabi": "\u0a2c\u0a3f\u0a28\u0a3e\u0a02 \u0a15\u0a41\u0a1d \u0a35\u0a3e\u0a2a\u0a38 \u0a09\u0a2e\u0a40\u0a26 \u0a15\u0a40\u0a24\u0a47 \u0a26\u0a42\u0a1c\u0a3f\u0a06\u0a02 \u0a26\u0a40 \u0a2e\u0a26\u0a26 \u0a15\u0a30\u0a4b\u0964", "transliteration": "Bin\u0101\u1e41 kujha v\u0101pasa um\u012bda k\u012bt\u0113 d\u016bji'\u0101\u1e41 d\u012b madada karo."},
        {"english": "Forgive yourself and move forward.", "punjabi": "\u0a06\u0a2a\u0a23\u0a47 \u0a06\u0a2a \u0a28\u0a42\u0a70 \u0a2e\u0a3e\u0a2b\u0a3c \u0a15\u0a30\u0a4b \u0a05\u0a24\u0a47 \u0a05\u0a71\u0a17\u0a47 \u0a35\u0a27\u0a4b\u0964", "transliteration": "\u0100pa\u1e47\u0113 \u0101pa n\u016b m\u0101pha karo at\u0113 a\u1e45g\u0113 vadho."},
        {"english": "Stay strong in difficult times.", "punjabi": "\u0a14\u0a16\u0a47 \u0a38\u0a2e\u0a3f\u0a06\u0a02 \u0a35\u0a3f\u0a71\u0a1a \u0a2e\u0a1c\u0a3c\u0a2c\u0a42\u0a24 \u0a30\u0a39\u0a4b\u0964", "transliteration": "Aukhe sama'i\u1e41 vica mazab\u016bta rah\u014d."},
        {"english": "Every moment is a new beginning.", "punjabi": "\u0a39\u0a30 \u0a2a\u0a32 \u0a07\u0a71\u0a15 \u0a28\u0a35\u0a40\u0a02 \u0a38\u0a3c\u0a41\u0a30\u0a42\u0a06\u0a24 \u0a39\u0a48\u0964", "transliteration": "Har pala ika nav\u012b\u1e41 shur\u016b'\u0101t hai."},
        {"english": "Listen to your heart always.", "punjabi": "\u0a39\u0a2e\u0a47\u0a38\u0a3c\u0a3e \u0a06\u0a2a\u0a23\u0a47 \u0a26\u0a3f\u0a32 \u0a26\u0a40 \u0a38\u0a41\u0a23\u0a4b\u0964", "transliteration": "Hamesh\u0101 \u0101pa\u1e47\u0113 dina d\u012b suno."},
        {"english": "Do what makes you happy.", "punjabi": "\u0a09\u0a39 \u0a15\u0a30\u0a4b \u0a1c\u0a4b \u0a24\u0a41\u0a39\u0a3e\u0a28\u0a42\u0a70 \u0a16\u0a41\u0a38\u0a3c \u0a15\u0a30\u0a26\u0a3e \u0a39\u0a48\u0964", "transliteration": "Oh karo j\u014d tuh\u0101n\u016b\u1e41 khusha karad\u0101 hai."},
        {"english": "Your potential is unlimited.", "punjabi": "\u0a24\u0a41\u0a39\u0a3e\u0a21\u0a40 \u0a38\u0a2e\u0a30\u0a71\u0a25\u0a3e \u0a05\u0a38\u0a40\u0a2e \u0a39\u0a48\u0964", "transliteration": "Tuh\u0101\u1e0d\u012b samarath\u0101 as\u012bma hai."},
        {"english": "Be brave and take risks.", "punjabi": "\u0a2c\u0a39\u0a3e\u0a26\u0a30 \u0a2c\u0a23\u0a4b \u0a05\u0a24\u0a47 \u0a1c\u0a4b\u0a16\u0a2e \u0a32\u0a13\u0964", "transliteration": "Bah\u0101dura ba\u1e47\u014d at\u0113 j\u014dkama la'\u014d."},
        {"english": "Celebrate your progress every day.", "punjabi": "\u0a39\u0a30 \u0a30\u0a4b\u0a1c\u0a3c \u0a06\u0a2a\u0a23\u0a40 \u0a24\u0a30\u0a71\u0a15\u0a40 \u0a26\u0a3e \u0a1c\u0a38\u0a3c\u0a28 \u0a2e\u0a28\u0a3e\u0a13\u0964", "transliteration": "Har r\u014dza \u0101pa\u1e47\u012b tarakk\u012b d\u0101 jashana man\u0101'\u014d."},
        {"english": "Surround yourself with good people.", "punjabi": "\u0a06\u0a2a\u0a23\u0a47 \u0a06\u0a2a \u0a28\u0a42\u0a70 \u0a1a\u0a70\u0a17\u0a47 \u0a32\u0a4b\u0a15\u0a3e\u0a02 \u0a28\u0a3e\u0a32 \u0a18\u0a47\u0a30\u0a4b\u0964", "transliteration": "\u0100pa\u1e47\u0113 \u0101pa n\u016b cha\u1e45g\u0113 l\u014dk\u0101\u1e41 n\u0101la gh\u0113r\u014d."},
        {"english": "Read books and grow your mind.", "punjabi": "\u0a15\u0a3f\u0a24\u0a3e\u0a2c\u0a3e\u0a02 \u0a2a\u0a5c\u0a4d\u0a39\u0a4b \u0a05\u0a24\u0a47 \u0a06\u0a2a\u0a23\u0a47 \u0a2e\u0a28 \u0a26\u0a3e \u0a35\u0a3f\u0a15\u0a3e\u0a38 \u0a15\u0a30\u0a4b\u0964", "transliteration": "Kit\u0101b\u0101\u1e41 pa\u1e5bh\u014d at\u0113 \u0101pa\u1e47\u0113 mana d\u0101 vik\u0101sa karo."},
        {"english": "Travel and discover new places.", "punjabi": "\u0a2f\u0a3e\u0a24\u0a30\u0a3e \u0a15\u0a30\u0a4b \u0a05\u0a24\u0a47 \u0a28\u0a35\u0a40\u0a06\u0a02 \u0a25\u0a3e\u0a35\u0a3e\u0a02 \u0a26\u0a40 \u0a16\u0a4b\u0a1c \u0a15\u0a30\u0a4b\u0964", "transliteration": "Y\u0101tar\u0101 karo at\u0113 nav\u012b'\u0101\u1e41 th\u0101v\u0101\u1e41 d\u012b kh\u014dja karo."},
        {"english": "Appreciate what you already have.", "punjabi": "\u0a1c\u0a4b \u0a24\u0a41\u0a39\u0a3e\u0a21\u0a47 \u0a15\u0a4b\u0a32 \u0a2a\u0a39\u0a3f\u0a32\u0a3e\u0a02 \u0a39\u0a40 \u0a39\u0a48 \u0a09\u0a38\u0a26\u0a40 \u0a15\u0a26\u0a30 \u0a15\u0a30\u0a4b\u0964", "transliteration": "J\u014d tuh\u0101\u1e0d\u0113 k\u014dla pahil\u0101\u1e41 h\u012b hai usa d\u012b kadara karo."},
        {"english": "Dance like nobody is watching.", "punjabi": "\u0a07\u0a26\u0a3e\u0a02 \u0a28\u0a71\u0a1a\u0a4b \u0a1c\u0a3f\u0a35\u0a47\u0a02 \u0a15\u0a4b\u0a08 \u0a28\u0a39\u0a40\u0a02 \u0a26\u0a47\u0a16 \u0a30\u0a3f\u0a39\u0a3e\u0964", "transliteration": "Id\u0101\u1e41 nach\u014d jiv\u0113\u1e41 k\u014d'\u012b nah\u012b\u1e41 d\u0113kha ri'\u0101."},
        {"english": "Sing from your heart out loud.", "punjabi": "\u0a06\u0a2a\u0a23\u0a47 \u0a26\u0a3f\u0a32 \u0a24\u0a4b\u0a02 \u0a1c\u0a3c\u0a4b\u0a30-\u0a1c\u0a3c\u0a4b\u0a30 \u0a28\u0a3e\u0a32 \u0a17\u0a3e\u0a13\u0964", "transliteration": "\u0100pa\u1e47\u0113 dina t\u014d z\u014dra-z\u014dra n\u0101la g\u0101'\u014d."},
        {"english": "Plant seeds of kindness everywhere.", "punjabi": "\u0a39\u0a30 \u0a1c\u0a17\u0a4d\u0a39\u0a3e \u0a26\u0a3f\u0a06\u0a32\u0a24\u0a3e \u0a26\u0a47 \u0a2c\u0a40\u0a1c \u0a2c\u0a40\u0a1c\u0a4b\u0964", "transliteration": "Har jaga di'\u0101lat\u0101 d\u0113 b\u012bja b\u012bj\u014d."},
        {"english": "Let go of what you cannot control.", "punjabi": "\u0a1c\u0a3f\u0a38\u0a28\u0a42\u0a70 \u0a24\u0a41\u0a38\u0a40\u0a02 \u0a15\u0a70\u0a1f\u0a30\u0a4b\u0a32 \u0a28\u0a39\u0a40\u0a02 \u0a15\u0a30 \u0a38\u0a15\u0a26\u0a47 \u0a09\u0a38\u0a28\u0a42\u0a70 \u0a1b\u0a71\u0a21 \u0a26\u0a3f\u0a13\u0964", "transliteration": "Jisan\u016b tus\u012b\u1e41 ka\u1e47\u1e6dr\u014dla nah\u012b\u1e41 kara sakad\u0113 usanu chha\u1e0da di'\u014d."},
        {"english": "Be present in the here and now.", "punjabi": "\u0a07\u0a25\u0a47 \u0a05\u0a24\u0a47 \u0a39\u0a41\u0a23 \u0a35\u0a3f\u0a71\u0a1a \u0a2e\u0a4c\u0a1c\u0a42\u0a26 \u0a30\u0a39\u0a4b\u0964", "transliteration": "Ith\u0113 at\u0113 hu\u1e47a vica mauj\u016bda rah\u014d."}
    ]
    fresh = [p for p in generic_fallbacks if not is_phrase_used(p["english"])]
    return fresh[:num_phrases]
async def generate_single_audio(text: str, voice: str, output_path: str):
    try:
        import edge_tts
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        return True
    except Exception as e:
        print(f"  TTS error: {e}")
        return False


async def generate_audio_with_retries(text: str, voice: str, output_path: str, max_retries: int = 3):
    import asyncio
    for attempt in range(1, max_retries + 1):
        success = await generate_single_audio(text, voice, output_path)
        if success:
            if Path(output_path).exists() and Path(output_path).stat().st_size > 100:
                return True
            else:
                print(f"    TTS file too small or missing, retrying ({attempt}/{max_retries})...")
                await asyncio.sleep(2 * attempt)
                continue
        else:
            if attempt < max_retries:
                wait = 2 * attempt
                print(f"    TTS retry {attempt}/{max_retries} in {wait}s...")
                await asyncio.sleep(wait)
            else:
                print(f"    TTS failed after {max_retries} attempts, using silence fallback")
                return False
    return False


def generate_all_audio(phrases: list, output_dir: str):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    audio_files = []

    for i, phrase in enumerate(phrases):
        english_file = output_dir / f"english_{i}.mp3"
        native_file = output_dir / f"native_{i}.mp3"
        combined_file = output_dir / f"combined_{i}.mp3"

        print(f"\n  Phrase {i+1}:")
        print(f"    EN: {phrase['english']}")
        print(f"    PA: {phrase['punjabi']}")

        # 1. Try Bhashini first if configured
        try:
            from bhashini_tts import generate_bhashini_audio
            nat_success = generate_bhashini_audio(phrase["punjabi"], "pa", str(native_file))
        except Exception:
            nat_success = False

        # 2. Try gTTS as immediate free zero-key fallback
        if not nat_success:
            try:
                from gtts import gTTS
                tts = gTTS(text=phrase["punjabi"], lang="pa")
                tts.save(str(native_file))
                nat_success = True
                print(f"    - Punjabi: {native_file.name} (via gTTS)")
            except Exception as e:
                print(f"    - gTTS Punjabi error: {e}")
                nat_success = False

        if not nat_success and NATIVE_VOICE:
            nat_success = asyncio.run(generate_audio_with_retries(phrase["punjabi"], NATIVE_VOICE, str(native_file)))

        if nat_success and not (Path(str(native_file)).exists() and Path(str(native_file)).stat().st_size > 500):
            nat_success = False

        if not nat_success:
            print(f"    - Punjabi: SILENCE FALLBACK (TTS failed)")
            cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", "2", str(native_file)]
            subprocess.run(cmd, capture_output=True)

        en_success = asyncio.run(generate_audio_with_retries(phrase["english"], ENGLISH_VOICE, str(english_file)))
        if en_success:
            print(f"    - English: {english_file.name}")
        else:
            print(f"    - English: SILENCE FALLBACK (TTS failed)")
            cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", "2", str(english_file)]
            subprocess.run(cmd, capture_output=True)

        en_duration = get_audio_duration(str(english_file))
        nat_duration = get_audio_duration(str(native_file))
        pause_between = 0.5
        total_duration = nat_duration + pause_between + en_duration

        print(f"    Total: {total_duration:.2f}s (EN: {en_duration:.2f}s + pause: {pause_between}s + PA: {nat_duration:.2f}s)")

        cmd = [
            "ffmpeg", "-y",
            "-i", str(native_file),
            "-i", str(english_file),
            "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[out]",
            "-map", "[out]",
            str(combined_file)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            concat_file = output_dir / f"concat_{i}.txt"
            with open(concat_file, "w", encoding="utf-8") as f:
                f.write(f"file '{native_file.as_posix()}'\n")
                f.write(f"file '{english_file.as_posix()}'\n")
            cmd = [
                "ffmpeg", "-y",
                "-f", "concat", "-safe", "0",
                "-i", str(concat_file),
                "-c:a", "aac",
                str(combined_file)
            ]
            subprocess.run(cmd, capture_output=True)
            if concat_file.exists():
                concat_file.unlink()

        actual_duration = get_audio_duration(str(combined_file))
        print(f"    Combined verified: {actual_duration:.2f}s")

        audio_files.append({
            "index": i,
            "english": str(english_file),
            "native": str(native_file),
            "combined": str(combined_file),
            "duration": actual_duration,
            "en_duration": en_duration,
            "nat_duration": nat_duration
        })

    print(f"\n[audio] Generated {len(audio_files)} phrase audios")
    return audio_files


def get_audio_duration(audio_file: str) -> float:
    if not Path(audio_file).exists():
        return 2.0
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except:
        return 2.0


def create_final_narration(audio_files: list, output_file: str):
    n = len(audio_files)
    print(f"[audio] Combining {n} audio files...")
    concat_file = Path(output_file).parent / "narration_list.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for audio_info in audio_files:
            combined_path = Path(audio_info["combined"])
            if combined_path.exists():
                path_str = str(combined_path.resolve()).replace("\\", "/").replace("'", "'\\''")
                f.write(f"file '{path_str}'\n")
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c:a", "copy", str(output_file)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if concat_file.exists():
        concat_file.unlink()
    if result.returncode == 0 and Path(output_file).exists() and Path(output_file).stat().st_size > 0:
        size = Path(output_file).stat().st_size
        print(f"\n[audio] Final narration: {Path(output_file).name} ({size/1024:.1f} KB)")
        return True
    return False


NOTO_FONT_URL = "https://raw.githubusercontent.com/googlefonts/noto-fonts/main/hinted/ttf/NotoSansGurmukhi/NotoSansGurmukhi-Bold.ttf"
FONTS_DIR = BASE_DIR / "fonts"


def ensure_font():
    font_file = FONTS_DIR / "NotoSansGurmukhi-Bold.ttf"
    if font_file.exists():
        return str(font_file)
    FONTS_DIR.mkdir(exist_ok=True)
    try:
        import urllib.request
        print(f"[font] Downloading {font_file.name}...")
        urllib.request.urlretrieve(NOTO_FONT_URL, str(font_file))
        print(f"[font] Downloaded: {font_file}")
        return str(font_file)
    except Exception as e:
        print(f"[font] Download failed: {e}")
    return None


def create_impressive_background(category_english: str):
    from PIL import Image, ImageDraw

    category_colors = {
    "Greetings": [
        [
            70,
            130,
            180
        ],
        [
            255,
            140,
            0
        ],
        [
            255,
            255,
            0
        ],
        [
            255,
            99,
            71
        ]
    ],
    "Basic Phrases": [
        [
            60,
            179,
            113
        ],
        [
            255,
            215,
            0
        ],
        [
            144,
            238,
            144
        ],
        [
            255,
            140,
            0
        ]
    ],
    "Common Expressions": [
        [
            138,
            43,
            226
        ],
        [
            255,
            20,
            147
        ],
        [
            75,
            0,
            130
        ],
        [
            255,
            105,
            180
        ]
    ],
    "Travel": [
        [
            0,
            191,
            255
        ],
        [
            255,
            255,
            0
        ],
        [
            70,
            130,
            180
        ],
        [
            255,
            215,
            0
        ]
    ],
    "Restaurant": [
        [
            255,
            69,
            0
        ],
        [
            255,
            215,
            0
        ],
        [
            220,
            20,
            60
        ],
        [
            255,
            140,
            0
        ]
    ],
    "Shopping": [
        [
            255,
            105,
            180
        ],
        [
            0,
            100,
            80
        ],
        [
            255,
            192,
            203
        ],
        [
            0,
            200,
            160
        ]
    ],
    "Emergency": [
        [
            255,
            0,
            0
        ],
        [
            139,
            0,
            0
        ],
        [
            255,
            69,
            0
        ],
        [
            220,
            20,
            60
        ]
    ],
    "Family Terms": [
        [
            255,
            182,
            193
        ],
        [
            138,
            43,
            226
        ],
        [
            255,
            160,
            122
        ],
        [
            75,
            0,
            130
        ]
    ],
    "Numbers": [
        [
            255,
            215,
            0
        ],
        [
            0,
            0,
            139
        ],
        [
            255,
            140,
            0
        ],
        [
            70,
            130,
            180
        ]
    ],
    "Time": [
        [
            0,
            0,
            100
        ],
        [
            255,
            255,
            0
        ],
        [
            70,
            130,
            180
        ],
        [
            255,
            215,
            0
        ]
    ],
    "Motivation": [
        [
            138,
            43,
            226
        ],
        [
            75,
            0,
            130
        ],
        [
            255,
            20,
            147
        ],
        [
            147,
            112,
            219
        ]
    ],
    "Love": [
        [
            255,
            0,
            100
        ],
        [
            139,
            0,
            0
        ],
        [
            255,
            105,
            180
        ],
        [
            255,
            192,
            203
        ]
    ],
    "Success": [
        [
            255,
            215,
            0
        ],
        [
            0,
            100,
            0
        ],
        [
            255,
            140,
            0
        ],
        [
            34,
            139,
            34
        ]
    ],
    "Wisdom": [
        [
            0,
            0,
            139
        ],
        [
            255,
            215,
            0
        ],
        [
            70,
            130,
            180
        ],
        [
            255,
            255,
            0
        ]
    ],
    "Happiness": [
        [
            255,
            255,
            0
        ],
        [
            255,
            0,
            255
        ],
        [
            255,
            165,
            0
        ],
        [
            147,
            112,
            219
        ]
    ],
    "Self Improvement": [
        [
            0,
            128,
            0
        ],
        [
            255,
            215,
            0
        ],
        [
            0,
            255,
            0
        ],
        [
            255,
            140,
            0
        ]
    ],
    "Gratitude": [
        [
            255,
            127,
            80
        ],
        [
            75,
            0,
            130
        ],
        [
            255,
            160,
            122
        ],
        [
            138,
            43,
            226
        ]
    ],
    "Friendship": [
        [
            255,
            192,
            203
        ],
        [
            0,
            100,
            80
        ],
        [
            255,
            105,
            180
        ],
        [
            0,
            200,
            160
        ]
    ],
    "Hope": [
        [
            0,
            0,
            100
        ],
        [
            255,
            255,
            0
        ],
        [
            70,
            130,
            180
        ],
        [
            255,
            215,
            0
        ]
    ],
    "Creativity": [
        [
            255,
            0,
            127
        ],
        [
            0,
            0,
            139
        ],
        [
            255,
            20,
            147
        ],
        [
            75,
            0,
            130
        ]
    ],
    "Inner Peace": [
        [
            135,
            206,
            235
        ],
        [
            0,
            0,
            100
        ],
        [
            176,
            224,
            230
        ],
        [
            75,
            0,
            130
        ]
    ],
    "Confidence": [
        [
            255,
            69,
            0
        ],
        [
            0,
            0,
            139
        ],
        [
            255,
            140,
            0
        ],
        [
            70,
            130,
            180
        ]
    ],
    "Perseverance": [
        [
            139,
            69,
            19
        ],
        [
            255,
            215,
            0
        ],
        [
            160,
            82,
            45
        ],
        [
            255,
            140,
            0
        ]
    ],
    "Inspiration": [
        [
            255,
            0,
            255
        ],
        [
            75,
            0,
            130
        ],
        [
            255,
            20,
            147
        ],
        [
            0,
            0,
            139
        ]
    ],
    "Positive Life": [
        [
            50,
            205,
            50
        ],
        [
            255,
            0,
            127
        ],
        [
            144,
            238,
            144
        ],
        [
            255,
            20,
            147
        ]
    ],
    "Courage": [
        [
            178,
            34,
            34
        ],
        [
            255,
            215,
            0
        ],
        [
            220,
            20,
            60
        ],
        [
            255,
            140,
            0
        ]
    ],
    "Kindness": [
        [
            255,
            182,
            193
        ],
        [
            138,
            43,
            226
        ],
        [
            255,
            160,
            122
        ],
        [
            75,
            0,
            130
        ]
    ],
    "Patience": [
        [
            34,
            139,
            34
        ],
        [
            255,
            255,
            0
        ],
        [
            60,
            179,
            113
        ],
        [
            255,
            215,
            0
        ]
    ],
    "Forgiveness": [
        [
            230,
            230,
            250
        ],
        [
            75,
            0,
            130
        ],
        [
            216,
            191,
            216
        ],
        [
            138,
            43,
            226
        ]
    ],
    "Strength": [
        [
            100,
            100,
            100
        ],
        [
            255,
            69,
            0
        ],
        [
            150,
            150,
            150
        ],
        [
            255,
            140,
            0
        ]
    ],
    "Joy": [
        [
            255,
            255,
            0
        ],
        [
            255,
            0,
            127
        ],
        [
            255,
            215,
            0
        ],
        [
            147,
            112,
            219
        ]
    ],
    "Balance": [
        [
            60,
            179,
            113
        ],
        [
            138,
            43,
            226
        ],
        [
            152,
            251,
            152
        ],
        [
            75,
            0,
            130
        ]
    ],
    "Growth": [
        [
            0,
            100,
            0
        ],
        [
            255,
            215,
            0
        ],
        [
            34,
            139,
            34
        ],
        [
            255,
            140,
            0
        ]
    ],
    "Purpose": [
        [
            75,
            0,
            130
        ],
        [
            255,
            215,
            0
        ],
        [
            138,
            43,
            226
        ],
        [
            255,
            140,
            0
        ]
    ],
    "Mindfulness": [
        [
            210,
            180,
            140
        ],
        [
            75,
            0,
            130
        ],
        [
            245,
            245,
            220
        ],
        [
            138,
            43,
            226
        ]
    ]
}

    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT))
    draw = ImageDraw.Draw(img)

    colors = category_colors.get(category_english, [(138, 43, 226), (75, 0, 130), (255, 20, 147), (147, 112, 219)])

    for y in range(VIDEO_HEIGHT):
        ratio = y / VIDEO_HEIGHT
        if ratio < 0.33:
            r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * (ratio * 3))
            g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * (ratio * 3))
            b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * (ratio * 3))
        elif ratio < 0.66:
            r = int(colors[1][0] + (colors[2][0] - colors[1][0]) * ((ratio - 0.33) * 3))
            g = int(colors[1][1] + (colors[2][1] - colors[1][1]) * ((ratio - 0.33) * 3))
            b = int(colors[1][2] + (colors[2][2] - colors[1][2]) * ((ratio - 0.33) * 3))
        else:
            r = int(colors[2][0] + (colors[3][0] - colors[2][0]) * ((ratio - 0.66) * 3))
            g = int(colors[2][1] + (colors[3][1] - colors[2][1]) * ((ratio - 0.66) * 3))
            b = int(colors[2][2] + (colors[3][2] - colors[2][2]) * ((ratio - 0.66) * 3))
        draw.rectangle([(0, y), (VIDEO_WIDTH, y + 1)], fill=(r, g, b))

    for i in range(0, VIDEO_WIDTH, 120):
        for j in range(0, VIDEO_HEIGHT, 120):
            draw.ellipse(
                [(i + 30, j + 30), (i + 90, j + 90)],
                outline=(255, 255, 255, 20),
                width=1
            )

    glow = Image.new('RGBA', (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for radius in range(800, 0, -50):
        alpha = int(30 * (1 - radius / 800))
        glow_draw.ellipse(
            [(VIDEO_WIDTH//2 - radius, VIDEO_HEIGHT//3 - radius),
             (VIDEO_WIDTH//2 + radius, VIDEO_HEIGHT//3 + radius)],
            fill=(255, 255, 255, alpha)
        )

    img = img.convert('RGBA')
    img = Image.alpha_composite(img, glow)
    return img


def find_font(bold=False, size=40, native=False):
    from PIL import ImageFont
    if native:
        font_preferences = [
            str(FONTS_DIR / "NotoSansGurmukhi-Bold.ttf"),
            "C:\\Windows\\Fonts\\raavib.ttf",
            "C:\\Windows\\Fonts\\raavi.ttf",
            "C:\\Windows\\Fonts\\nirmalab.ttf",
            "C:\\Windows\\Fonts\\nirmala.ttc",
            "NotoSansGurmukhi-Bold.ttf",
        ]
    elif bold:
        font_preferences = [
            "segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    else:
        font_preferences = [
            "segoeui.ttf", "arial.ttf", "calibri.ttf", "DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    for font_name in font_preferences:
        try:
            return ImageFont.truetype(font_name, size)
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


def rounded_rect(draw, bbox, radius, fill=None, outline=None, width=1):
    x1, y1, x2, y2 = bbox
    r = min(radius, (x2 - x1) // 2, (y2 - y1) // 2)
    draw.pieslice([x1, y1, x1 + r*2, y1 + r*2], 180, 270, fill=fill)
    draw.pieslice([x2 - r*2, y1, x2, y1 + r*2], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - r*2, x1 + r*2, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - r*2, y2 - r*2, x2, y2], 0, 90, fill=fill)
    draw.rectangle([x1 + r, y1, x2 - r, y2], fill=fill)
    draw.rectangle([x1, y1 + r, x2, y2 - r], fill=fill)


def generate_complete_image(phrase_data: dict, category_english: str, output_path: str, phrase_index: int = 0, total_phrases: int = 5):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("PIL not available. Install: pip install Pillow")
        return None

    ensure_font()
    img = create_impressive_background(category_english)
    draw = ImageDraw.Draw(img)

    SIZE_CATEGORY = 64
    SIZE_NATIVE_L = 100
    SIZE_NATIVE_M = 82
    SIZE_NATIVE_S = 66
    SIZE_ENGLISH = 70
    SIZE_TRANSLITERATION = 48
    SIZE_BRANDING = 50
    SIZE_PROGRESS = 38

    font_category = find_font(bold=True, size=SIZE_CATEGORY)
    font_native_l = find_font(bold=True, size=SIZE_NATIVE_L, native=True)
    font_native_m = find_font(bold=True, size=SIZE_NATIVE_M, native=True)
    font_native_s = find_font(bold=True, size=SIZE_NATIVE_S, native=True)
    font_english = find_font(bold=True, size=SIZE_ENGLISH)
    font_transliteration = find_font(bold=False, size=SIZE_TRANSLITERATION)
    font_branding = find_font(bold=True, size=SIZE_BRANDING)
    font_progress = find_font(bold=False, size=SIZE_PROGRESS)

    native = phrase_data.get("punjabi", "")
    english = phrase_data.get("english", "")
    transliteration = phrase_data.get("transliteration", "")

    def wrap_text(text, font, max_width):
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        return lines

    def pick_native_font(text, max_w):
        for font, name in [(font_native_l, 'L'), (font_native_m, 'M'), (font_native_s, 'S')]:
            lines = wrap_text(text, font, max_w)
            if len(lines) <= 2:
                return font, lines
        return font_native_s, wrap_text(native, font_native_s, max_w)

    def measure_line_h(font):
        b = draw.textbbox((0, 0), "Ag", font=font)
        return b[3] - b[1]

    max_text_w = VIDEO_WIDTH - 180
    cat_native = CATEGORIES_NATIVE.get(category_english, category_english)

    nat_font, nat_lines = pick_native_font(native, max_text_w - 40)
    en_lines = wrap_text(english, font_english, max_text_w)
    trans_lines = wrap_text(transliteration, font_transliteration, max_text_w - 60) if transliteration else []

    nat_lh = measure_line_h(nat_font)
    en_lh = measure_line_h(font_english)
    trans_lh = measure_line_h(font_transliteration)

    nat_box_pad = 35
    en_box_pad = 28
    trans_box_pad = 22

    nat_box_h = len(nat_lines) * nat_lh + nat_box_pad * 2
    en_box_h = len(en_lines) * en_lh + en_box_pad * 2
    trans_box_h = len(trans_lines) * trans_lh + trans_box_pad * 2 if trans_lines else 0

    gap_cat_nat = 50
    gap_nat_en = 35
    gap_en_trans = 30
    gap_trans_prog = 25
    gap_prog_brand = 40
    prog_bar_h = 30

    total_center_h = (0 + gap_cat_nat + nat_box_h + gap_nat_en +
                      en_box_h + gap_en_trans + trans_box_h + gap_trans_prog +
                      prog_bar_h + gap_prog_brand)

    start_y = int((VIDEO_HEIGHT - total_center_h) * 0.38)
    if start_y < 200:
        start_y = 200

    cy = start_y

    # Category bar (rounded)
    cat_text = category_english
    cat_bb = draw.textbbox((0, 0), cat_text, font=font_category)
    cat_tw = cat_bb[2] - cat_bb[0]
    cat_th = cat_bb[3] - cat_bb[1]
    cat_cx = VIDEO_WIDTH // 2
    cat_cy = 185
    cat_pad = 28
    cat_box_x1 = cat_cx - cat_tw // 2 - cat_pad
    cat_box_y1 = cat_cy - cat_th // 2 - cat_pad
    cat_box_x2 = cat_cx + cat_tw // 2 + cat_pad
    cat_box_y2 = cat_cy + cat_th // 2 + cat_pad
    rounded_rect(draw, (cat_box_x1, cat_box_y1, cat_box_x2, cat_box_y2),
                 25, fill=(0, 0, 0, 190))
    draw.text((cat_cx, cat_cy), cat_text,
              fill=(255, 255, 255), font=font_category, anchor="mm",
              stroke_width=2, stroke_fill=(0, 0, 0))

    cy += gap_cat_nat

    # Native phrase (big, prominent)
    nat_margin = 50
    rounded_rect(draw, (nat_margin, cy, VIDEO_WIDTH - nat_margin, cy + nat_box_h), 28,
                 fill=(139, 0, 0, 220))
    for i, line in enumerate(nat_lines):
        ly = cy + nat_box_pad + i * nat_lh + nat_lh // 2
        draw.text((VIDEO_WIDTH // 2, ly), line,
                  fill=(255, 255, 200), font=nat_font, anchor="mm",
                  stroke_width=3, stroke_fill=(60, 0, 0))

    cy += nat_box_h + gap_nat_en

    # English phrase
    en_margin = 70
    rounded_rect(draw, (en_margin, cy, VIDEO_WIDTH - en_margin, cy + en_box_h), 24,
                 fill=(20, 40, 100, 220))
    for i, line in enumerate(en_lines):
        ly = cy + en_box_pad + i * en_lh + en_lh // 2
        draw.text((VIDEO_WIDTH // 2, ly), line,
                  fill=(255, 255, 255), font=font_english, anchor="mm",
                  stroke_width=2, stroke_fill=(0, 0, 40))

    cy += en_box_h + gap_en_trans

    # Transliteration
    if trans_lines:
        trans_margin = 90
        rounded_rect(draw, (trans_margin, cy, VIDEO_WIDTH - trans_margin, cy + trans_box_h), 18,
                     fill=(40, 40, 40, 220))
        for i, line in enumerate(trans_lines):
            ly = cy + trans_box_pad + i * trans_lh + trans_lh // 2
            draw.text((VIDEO_WIDTH // 2, ly), line,
                      fill=(220, 220, 220), font=font_transliteration, anchor="mm",
                      stroke_width=1, stroke_fill=(20, 20, 20))
        cy += trans_box_h + gap_trans_prog
    else:
        cy += gap_trans_prog

    # Progress
    prog_text = f"{phrase_index + 1} / {total_phrases}"
    prog_bb = draw.textbbox((0, 0), prog_text, font=font_progress)
    prog_h = prog_bb[3] - prog_bb[1]
    draw.text((VIDEO_WIDTH // 2, cy + prog_h // 2), prog_text,
              fill=(180, 180, 180), font=font_progress, anchor="mm")

    # Branding (rounded)
    brand_text = "VELOCITY PUNJABI"
    brand_bb = draw.textbbox((0, 0), brand_text, font=font_branding)
    brand_tw = brand_bb[2] - brand_bb[0]
    brand_th = brand_bb[3] - brand_bb[1]
    brand_cx = VIDEO_WIDTH // 2
    brand_cy = VIDEO_HEIGHT - 120
    brand_pad = 32
    brand_box_x1 = brand_cx - brand_tw // 2 - brand_pad
    brand_box_y1 = brand_cy - brand_th // 2 - brand_pad
    brand_box_x2 = brand_cx + brand_tw // 2 + brand_pad
    brand_box_y2 = brand_cy + brand_th // 2 + brand_pad
    rounded_rect(draw, (brand_box_x1, brand_box_y1, brand_box_x2, brand_box_y2),
                 30, fill=(0, 0, 0, 195))
    draw.text((brand_cx, brand_cy), brand_text,
              fill=(255, 215, 0), font=font_branding, anchor="mm",
              stroke_width=2, stroke_fill=(0, 0, 0))

    if img.mode == 'RGBA':
        img = img.convert('RGB')

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, quality=95, optimize=True)
    print(f"  Image: {Path(output_path).name}")
    return output_path


def create_video_from_images_audio(image_files: list, audio_files: list, combined_audio: str, output_file: str):
    print(f"\n[video] Creating video from {len(image_files)} images...")
    print(f"[video] Ensuring complete audio playback and sync...")

    temp_clips = []

    for i, (img_path, audio_info) in enumerate(zip(image_files, audio_files)):
        duration = audio_info['duration']
        print(f"  Image {i+1}/{len(image_files)}: {duration:.2f}s (EN: {audio_info.get('en_duration', 0):.1f}s + PA: {audio_info.get('nat_duration', 0):.1f}s)")

        temp_clip = Path(output_file).parent / f"temp_clip_{i:02d}.mp4"
        temp_clips.append(temp_clip)

        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(img_path),
            "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2,fps={FPS}",
            "-t", str(duration),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "medium",
            str(temp_clip)
        ]
        subprocess.run(cmd, check=True, capture_output=True)

    print("[video] Concatenating clips...")
    temp_video = Path(output_file).parent / "temp_video.mp4"
    concat_file = Path(output_file).parent / "concat_list.txt"

    with open(concat_file, "w") as f:
        for clip in temp_clips:
            f.write(f"file '{clip.resolve().as_posix()}'\n")

    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", str(temp_video)]
    subprocess.run(cmd, check=True, capture_output=True)

    print("[video] Adding audio (ensuring complete playback)...")
    audio_duration = get_audio_duration(combined_audio)
    print(f"[video] Audio duration: {audio_duration:.2f}s")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(temp_video),
        "-i", str(combined_audio),
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(output_file)
    ]
    subprocess.run(cmd, check=True, capture_output=True)

    video_duration = get_audio_duration(str(output_file).replace(".mp4", ".mp4"))
    print(f"[video] Video created: {Path(output_file).name} ({video_duration:.2f}s)")

    for clip in temp_clips:
        if clip.exists():
            clip.unlink()
    if temp_video.exists():
        temp_video.unlink()
    if concat_file.exists():
        concat_file.unlink()


def generate_reel(category_english: str = None):
    if not category_english:
        category_english = get_available_category()

    print(f"\n{'='*80}")
    print(f"Category: {category_english} ({CATEGORIES_NATIVE[category_english]})")
    print(f"{'='*80}\n")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    reel_dir = VIDEO_DIR / f"{category_english}_{timestamp}"
    reel_dir.mkdir(exist_ok=True)

    print("[1/4] Generating unique phrases (checking history)...")
    phrases = generate_phrases(category_english, num_phrases=5)

    for i, phrase in enumerate(phrases, 1):
        print(f"  {i}. {phrase['english']} -> {phrase['punjabi']}")

    print("\n[2/4] Generating images with impressive backgrounds...")
    for i, phrase in enumerate(phrases):
        output_path = reel_dir / f"phrase_{i:02d}.jpg"
        generate_complete_image(phrase, category_english, str(output_path), phrase_index=i, total_phrases=len(phrases))
        print(f"  Image {i+1}: {phrase['english'][:40]}...")

    print("\n[3/4] Generating audio (English + Punjabi with 500ms pause)...")
    audio_files = generate_all_audio(phrases, str(reel_dir))

    final_audio = reel_dir / "narration.mp3"
    create_final_narration(audio_files, str(final_audio))

    print("\n[4/4] Creating video...")
    output_video = reel_dir / "final_reel.mp4"

    image_files = sorted([str(p) for p in reel_dir.glob("phrase_*.jpg")])

    create_video_from_images_audio(
        image_files,
        audio_files,
        str(final_audio),
        str(output_video)
    )

    metadata = {
        "category_english": category_english,
        "category_native": CATEGORIES_NATIVE[category_english],
        "timestamp": timestamp,
        "phrases": phrases,
        "video": str(output_video),
        "audio": str(final_audio)
    }

    with open(reel_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*80}")
    print(f"REEL COMPLETE!")
    print(f"  {reel_dir}")
    print(f"  {output_video.name}")
    print(f"  Branding: VELOCITY PUNJABI")
    print(f"{'='*80}\n")

    return metadata


if __name__ == "__main__":
    print("\n" + "="*80)
    print(f"VELOCITY PUNJABI - FACEBOOK REELS AUTOMATION")
    print("="*80)
    print("\nFEATURES:")
    print("  - Natural pauses with commas (non-robotic TTS)")
    print("  - Perfect audio-video synchronization")
    print("  - Complete audio playback guaranteed")
    print("  - English category names (for learners)")
    print(f"  - VELOCITY PUNJABI branding at bottom")
    print("  - NEVER repeats phrases (permanent history tracking)")
    print(f"\nAVAILABLE CATEGORIES ({len(CATEGORIES_ENGLISH)} total):")
    for i, cat in enumerate(CATEGORIES_ENGLISH, 1):
        print(f"   {i:2d}. {cat} ({CATEGORIES_NATIVE[cat]})")
    print("="*80)

    generate_reel()

    print("\n" + "="*80)
    print("READY FOR DAILY AUTOMATION!")
    print("="*80)
