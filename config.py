"""VELOCITY PUNJABI - language pack, brand and motion design constants."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

OUTPUT_DIR = BASE_DIR / "output"
LESSONS_DIR = OUTPUT_DIR / "lessons"
HISTORY_DIR = OUTPUT_DIR / "history"
SCENE_DIR = BASE_DIR / "scene"

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 30

# ---------------------------------------------------------------- brand

BRAND = "VELOCITY PUNJABI"
BRAND_LOCKUP_TOP = "VELOCITY"
BRAND_LOCKUP_BOTTOM = "PUNJABI"
HANDLE = "@velocitypunjabi"
MASCOT_NAME = "Velo"

# ==== LANGUAGE PACK START ====
LANGUAGE = {
    "code": "pa",
    "name": "Punjabi",
    "native_name": "ਪੰਜਾਬੀ",
    "history_key": "punjabi",
    "english_voice": "en-US-AvaNeural",
    "english_fallback_voice": "en-US-GuyNeural",
    "native_voice": "",
    "native_fallback_voice": "",
    "native_engine": "gtts",
    "native_lang_code": "pa",
    "english_rate": "-2%",
    "native_rate": "-6%",
    "english_pitch": "+0Hz",
    "native_pitch": "+0Hz",
    "native_label": "ਪੰਜਾਬੀ",
    "translit_label": "SAY IT LIKE",
    "greeting": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ!",
    "encouragement": "ਸ਼ਾਨਦਾਰ!",
    "rtl": False,
    "char_tiles": False,
    "script_font": "NotoSansGurmukhi-Bold.ttf",
}
# ==== LANGUAGE PACK END ====

AI_MODEL = os.getenv("AI_MODEL", "gemini-fast")
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "")

# ---------------------------------------------------------------- timing (seconds)

INTRO_DURATION = 4.0
OUTRO_DURATION = 5.2
EN_CARD_IN = 0.55
GAP_EN_NATIVE = 0.5
NATIVE_CARD_LEAD = 0.35
GAP_BEFORE_REPEAT = 0.8
TAIL_HOLD = 1.4
MAX_REEL_DURATION = 88.0

# ---------------------------------------------------------------- palette

INK = "#3C3C3C"
MUTED = "#8A8A8A"
CREAM = "#FFF8E7"
GREEN = "#58CC02"
GREEN_DARK = "#46A302"
GREEN_DEEP = "#3D8F00"
BLUE = "#1CB0F6"
PURPLE = "#A560E8"
ORANGE = "#FF7A00"
RED = "#FF4B4B"
YELLOW = "#F5A700"
TEAL = "#00A889"
PINK = "#E056A0"

PALETTE = [GREEN, BLUE, PURPLE, ORANGE, RED, YELLOW, TEAL, PINK]

# ---------------------------------------------------------------- categories
# (english, native, icon, accent)

# ==== CATEGORY TABLE START ====
CATEGORY_TABLE = [
    ("Greetings", "ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "hand", "#1CB0F6"),
    ("Basic Phrases", "ਮੁੱਢਲੇ ਵਾਕ", "chat", "#58CC02"),
    ("Common Expressions", "ਆਮ ਸਮੀਕਰਨ", "chat", "#1CB0F6"),
    ("Travel", "ਯਾਤਰਾ", "plane", "#1CB0F6"),
    ("Restaurant", "ਰੈਸਟੋਰੈਂਟ", "fork", "#FF7A00"),
    ("Shopping", "ਖਰੀਦਦਾਰੀ", "bag", "#E056A0"),
    ("Emergency", "ਐਮਰਜੈਂਸੀ", "siren", "#FF4B4B"),
    ("Family Terms", "ਪਰਿਵਾਰਕ ਸ਼ਬਦ", "heart", "#E056A0"),
    ("Numbers", "ਨੰਬਰ", "hash", "#A560E8"),
    ("Time", "ਸਮਾਂ", "clock", "#00A889"),
    ("Motivation", "ਪ੍ਰੇਰਣਾ", "rocket", "#A560E8"),
    ("Love", "ਪਿਆਰ", "heart", "#FF4B4B"),
    ("Success", "ਸਫਲਤਾ", "trophy", "#F5A700"),
    ("Wisdom", "ਬੁੱਧੀ", "book", "#A560E8"),
    ("Happiness", "ਖੁਸ਼ੀ", "smile", "#F5A700"),
    ("Self Improvement", "ਸਵੈ-ਸੁਧਾਰ", "leaf", "#58CC02"),
    ("Gratitude", "ਸ਼ੁਕਰਗੁਜ਼ਾਰ", "heart", "#FF7A00"),
    ("Friendship", "ਦੋਸਤੀ", "users", "#00A889"),
    ("Hope", "ਉਮੀਦ", "sun", "#FF7A00"),
    ("Creativity", "ਸਿਰਜਣਾਤਮਕਤਾ", "palette", "#E056A0"),
    ("Inner Peace", "ਅੰਦਰੂਨੀ ਸ਼ਾਂਤੀ", "lotus", "#00A889"),
    ("Confidence", "ਵਿਸ਼ਵਾਸ", "shield", "#1CB0F6"),
    ("Perseverance", "ਦ੍ਰਿੜਤਾ", "mountain", "#FF7A00"),
    ("Inspiration", "ਪ੍ਰੇਰਨਾ", "sparkles", "#A560E8"),
    ("Positive Life", "ਸਕਾਰਾਤਮਕ ਜੀਵਨ", "sun", "#58CC02"),
    ("Courage", "ਹਿੰਮਤ", "shield", "#FF4B4B"),
    ("Kindness", "ਦਿਆਲਤਾ", "heart", "#E056A0"),
    ("Patience", "ਧੀਰਜ", "hourglass", "#00A889"),
    ("Forgiveness", "ਮਾਫੀ", "hands", "#FF7A00"),
    ("Strength", "ਤਾਕਤ", "dumbbell", "#FF4B4B"),
    ("Joy", "ਅਨੰਦ", "smile", "#F5A700"),
    ("Balance", "ਸੰਤੁਲਨ", "scale", "#00A889"),
    ("Growth", "ਵਿਕਾਸ", "sprout", "#58CC02"),
    ("Purpose", "ਉਦੇਸ਼", "target", "#A560E8"),
    ("Mindfulness", "ਸਾਵਧਾਨਤਾ", "lotus", "#00A889"),
    ("Daily Routine", "ਰੋਜ਼ਾਨਾ ਰੁਟੀਨ", "calendar", "#1CB0F6"),
    ("Weather", "ਮੌਸਮ", "cloud", "#1CB0F6"),
    ("Feelings", "ਭਾਵਨਾਵਾਂ", "smile", "#E056A0"),
    ("Food", "ਭੋਜਨ", "fork", "#FF7A00"),
    ("Health", "ਸਿਹਤ", "heart", "#58CC02"),
    ("Work", "ਕਮ੍ਮ", "briefcase", "#1CB0F6"),
    ("Technology", "ਤਕਨਾਲੋਜੀ", "chip", "#A560E8"),
    ("Nature", "ਕੁਦਰਤ", "leaf", "#58CC02"),
    ("Animals", "ਜਾਨਵਰ", "paw", "#FF7A00"),
    ("Colors", "ਰੰਗ", "palette", "#E056A0"),
    ("Directions", "ਦਿਸ਼ਾਵਾਂ", "compass", "#1CB0F6"),
    ("Body Parts", "ਸਰੀਰ ਦੇ ਅੰਗ", "hand", "#00A889"),
    ("Clothes", "ਕਪਡ਼ੇ", "shirt", "#E056A0"),
    ("Music", "ਸੰਗੀਤ", "music", "#A560E8"),
    ("Sports", "ਖੇਡਾਂ", "ball", "#FF7A00"),
    ("Holidays", "ਛੁਟ੍ਟੀਆਂ", "gift", "#FF4B4B"),
    ("Education", "ਸਿੱਖਿਆ", "book", "#1CB0F6"),
    ("Culture", "ਸਭਿਆਚਾਰ", "globe", "#00A889"),
    ("Finance", "ਵਿੱਤ", "coin", "#58CC02"),
    ("Relationships", "ਰਿਸ਼ਤੇ", "users", "#E056A0"),
]
# ==== CATEGORY TABLE END ====

CATEGORIES = [c[0] for c in CATEGORY_TABLE]
CATEGORIES_NATIVE = {c[0]: c[1] for c in CATEGORY_TABLE}
CATEGORY_META = {c[0]: {"native": c[1], "icon": c[2], "accent": c[3]} for c in CATEGORY_TABLE}
MAX_RECENT_CATEGORIES = 25

# ==== HASHTAGS START ====
HASHTAGS = [
    "#learnpunjabi",
    "#punjabilessons",
    "#punjabiforbeginners",
    "#languagelearning",
    "#punjabivocabulary",
    "#velocitypunjabi",
    "#dailypunjabi",
    "#punjabi",
    "#learnlanguages",
    "#speakpunjabi",
    "#bilingual",
    "#languagetips",
]
# ==== HASHTAGS END ====
