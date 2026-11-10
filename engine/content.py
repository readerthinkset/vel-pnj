"""AI phrase generation with permanent no-repeat history."""

from __future__ import annotations

import json
import random
import time
from datetime import datetime

import requests

import config
from config import CATEGORIES, CATEGORIES_NATIVE, HISTORY_DIR, MAX_RECENT_CATEGORIES

PHRASE_HISTORY_FILE = HISTORY_DIR / "all_generated_phrases.json"
RECENT_CATEGORIES_FILE = HISTORY_DIR / "recent_categories.json"

PHRASE_KEY = config.LANGUAGE["history_key"]
LANGUAGE_NAME = config.LANGUAGE["name"]
NATIVE_NAME = config.LANGUAGE["native_name"]

# ==== FALLBACK PHRASES START ====
FALLBACK_PHRASES = [
    {"english": "Hello, nice to meet you.", "native": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ, ਤੁਹਾਨੂੰ ਮਿਲ ਕੇ ਖੁਸ਼ੀ ਹੋਈ।", "transliteration": "Sat Sri Akal, tuhānuṁ mil ke khushī hoī."},
    {"english": "Thank you very much.", "native": "ਤੁਹਾਡਾ ਬਹੁਤ ਬਹੁਤ ਧੰਨਵਾਦ।", "transliteration": "Tuhāḍā bahuta bahuta dhanavād."},
    {"english": "Good morning, have a great day.", "native": "ਸ਼ੁਭ ਸਵੇਰ, ਤੁਹਾਡਾ ਦਿਨ ਵਧੀਆ ਰਹੇ।", "transliteration": "Shubha saver, tuhāḍā dina vadhī'ā rahe."},
    {"english": "I love learning new languages.", "native": "ਮੈਨੂੰ ਨਵੀਆਂ ਭਾਸ਼ਾਵਾਂ ਸਿੱਖਣਾ ਪਸੰਦ ਹੈ।", "transliteration": "Mainūṁ navī'āṁ bhāshāvāṁ sikhaṇā pasanda hai."},
    {"english": "Never give up on your dreams.", "native": "ਆਪਣੇ ਸੁਪਨਿਆਂ ਨੂੰ ਕਦੇ ਨਾ ਛੱਡੋ।", "transliteration": "Āpaṇe supan'nāṁ nū kade nā chhaḍo."},
    {"english": "Every day is a fresh start.", "native": "ਹਰ ਦਿਨ ਇੱਕ ਨਵੀਂ ਸ਼ੁਰੂਆਤ ਹੈ।", "transliteration": "Har dina ika navīṁ shurū'āt hai."},
    {"english": "Believe in yourself always.", "native": "ਹਮੇਸ਼ਾ ਆਪਣੇ ਆਪ 'ਤੇ ਵਿਸ਼ਵਾਸ ਰੱਖੋ।", "transliteration": "Hameshā āpaṇe āpa 'te vishvāsa rakho."},
    {"english": "Small steps lead to big changes.", "native": "ਛੋਟੇ ਕਦਮ ਵੱਡੇ ਬਦਲਾਅ ਲਿਆਉਂਦੇ ਹਨ।", "transliteration": "Chhoṭe kadama vaḍe badalā'a li'ā'unde hana."},
    {"english": "You are stronger than you think.", "native": "ਤੁਸੀਂ ਜਿੰਨਾ ਸੋਚਦੇ ਹੋ ਉਸ ਤੋਂ ਜ਼ਿਆਦਾ ਮਜ਼ਬੂਤ ਹੋ।", "transliteration": "Tusīṁ jina sochadē ho usa tō zi'ādā mazabūta ho."},
    {"english": "Happiness is a choice, choose it.", "native": "ਖੁਸ਼ੀ ਇੱਕ ਚੋਣ ਹੈ, ਇਸਨੂੰ ਚੁਣੋ।", "transliteration": "Khushī ika choṇa hai, isanū chuno."},
    {"english": "What time is it please.", "native": "ਕਿਰਪਾ ਕਰਕੇ ਸਮਾਂ ਕੀ ਹੈ।", "transliteration": "Kirapā karake samāṁ kī hai."},
    {"english": "Where is the train station.", "native": "ਰੇਲਵੇ ਸਟੇਸ਼ਨ ਕਿੱਥੇ ਹੈ।", "transliteration": "Relvē sṭēshana kidhē hai."},
    {"english": "How much does this cost.", "native": "ਇਸਦੀ ਕੀਮਤ ਕਿੰਨੀ ਹੈ।", "transliteration": "Isadī kīmata kinanī hai."},
    {"english": "Can you help me please.", "native": "ਕਿਰਪਾ ਕਰਕੇ ਮੇਰੀ ਮਦਦ ਕਰ ਸਕਦੇ ਹੋ।", "transliteration": "Kirapā karake mērī madada kara sakadē ho."},
    {"english": "I would like a coffee please.", "native": "ਮੈਨੂੰ ਇੱਕ ਕੌਫੀ ਚਾਹੀਦੀ ਹੈ, ਕਿਰਪਾ ਕਰਕੇ।", "transliteration": "Mainūṁ ika kaufī chāhīdī hai, kirapā karake."},
    {"english": "The food is delicious today.", "native": "ਅੱਜ ਭੋਜਨ ਬਹੁਤ ਸੁਆਦੀ ਹੈ।", "transliteration": "Aja bhōjana bahuta su'ādī hai."},
    {"english": "Have a wonderful weekend.", "native": "ਤੁਹਾਡਾ ਵੀਕੈਂਡ ਸ਼ਾਨਦਾਰ ਰਹੇ।", "transliteration": "Tuhāḍā vīka'ēṇḍa shānadāra rahe."},
    {"english": "Take care of yourself.", "native": "ਆਪਣਾ ਖਿਆਲ ਰੱਖੋ।", "transliteration": "Āpaṇā khi'āla rakho."},
    {"english": "See you tomorrow my friend.", "native": "ਕੱਲ ਮਿਲਦੇ ਹਾਂ ਮੇਰੇ ਦੋਸਤ।", "transliteration": "Kala miladē hāṁ mērē dōsta."},
    {"english": "The weather is beautiful outside.", "native": "ਬਾਹਰ ਮੌਸਮ ਬਹੁਤ ਸੁੰਦਰ ਹੈ।", "transliteration": "Bāhara mausaṁ bahuta sundara hai."},
    {"english": "I am very happy today.", "native": "ਮੈਂ ਅੱਜ ਬਹੁਤ ਖੁਸ਼ ਹਾਂ।", "transliteration": "Maiṁ aja bahuta khusha hāṁ."},
    {"english": "Learning a language opens new doors.", "native": "ਭਾਸ਼ਾ ਸਿੱਖਣ ਨਾਲ ਨਵੇਂ ਦਰਵਾਜ਼ੇ ਖੁੱਲ੍ਹਦੇ ਹਨ।", "transliteration": "Bhāshā sikhaṇa nāla navē daravāzē khulhadē hana."},
    {"english": "Keep practicing every single day.", "native": "ਹਰ ਰੋਜ਼ ਅਭਿਆਸ ਕਰਦੇ ਰਹੋ।", "transliteration": "Har rōza abhi'āsa karadē rahō."},
    {"english": "You can achieve anything you want.", "native": "ਤੁਸੀਂ ਜੋ ਚਾਹੋ ਪ੍ਰਾਪਤ ਕਰ ਸਕਦੇ ਹੋ।", "transliteration": "Tusīṁ jō chāhō prāpata kara sakadē ho."},
    {"english": "Rest when you are tired.", "native": "ਜਦੋਂ ਥੱਕ ਜਾਓ ਤਾਂ ਆਰਾਮ ਕਰੋ।", "transliteration": "Jadōṁ thaka jā'ō tāṁ ārāma karo."},
    {"english": "Focus on the positive things.", "native": "ਸਕਾਰਾਤਮਕ ਚੀਜ਼ਾਂ 'ਤੇ ਧਿਆਨ ਕੇਂਦਰਿਤ ਕਰੋ।", "transliteration": "Sakārātamaka chīzāṁ 'te dhi'āna kēndrita karo."},
    {"english": "Learn from your mistakes.", "native": "ਆਪਣੀਆਂ ਗਲਤੀਆਂ ਤੋਂ ਸਿੱਖੋ।", "transliteration": "Āpaṇī'āṁ galatī'āṁ tō sikho."},
    {"english": "Trust the process completely.", "native": "ਪੂਰੀ ਤਰ੍ਹਾਂ ਪ੍ਰਕਿਰਿਆ 'ਤੇ ਭਰੋਸਾ ਕਰੋ।", "transliteration": "Pūrī taraṁ prakiri'ā 'te bharōsā karo."},
    {"english": "Breathe deeply and stay calm.", "native": "ਡੂੰਘੀ ਸਾਹ ਲਓ ਅਤੇ ਸ਼ਾਂਤ ਰਹੋ।", "transliteration": "Ḍūṅghī sāha la'ō atē shānta rahō."},
    {"english": "Enjoy the little moments in life.", "native": "ਜੀਵਨ ਦੇ ਛੋਟੇ ਪਲਾਂ ਦਾ ਆਨੰਦ ਮਾਣੋ।", "transliteration": "Jīvana dē chhoṭē palāṁ dā ānanda māṇō."},
    {"english": "Smile more, worry less.", "native": "ਵੱਧ ਮੁਸਕਰਾਓ, ਘੱਟ ਚਿੰਤਾ ਕਰੋ।", "transliteration": "Vadha musakarā'ō, ghaṭa chintā karo."},
    {"english": "Be kind to everyone you meet.", "native": "ਹਰ ਕਿਸੇ ਨਾਲ ਦਿਆਲੂ ਬਣੋ ਜਿਸਨੂੰ ਤੁਸੀਂ ਮਿਲਦੇ ਹੋ।", "transliteration": "Har kisē nāla di'ālū baṇō jisanū tusīṁ miladē ho."},
    {"english": "Help others without expecting anything back.", "native": "ਬਿਨਾਂ ਕੁਝ ਵਾਪਸ ਉਮੀਦ ਕੀਤੇ ਦੂਜਿਆਂ ਦੀ ਮਦਦ ਕਰੋ।", "transliteration": "Bināṁ kujha vāpasa umīda kītē dūji'āṁ dī madada karo."},
    {"english": "Forgive yourself and move forward.", "native": "ਆਪਣੇ ਆਪ ਨੂੰ ਮਾਫ਼ ਕਰੋ ਅਤੇ ਅੱਗੇ ਵਧੋ।", "transliteration": "Āpaṇē āpa nū māpha karo atē aṅgē vadho."},
    {"english": "Stay strong in difficult times.", "native": "ਔਖੇ ਸਮਿਆਂ ਵਿੱਚ ਮਜ਼ਬੂਤ ਰਹੋ।", "transliteration": "Aukhe sama'iṁ vica mazabūta rahō."},
    {"english": "Every moment is a new beginning.", "native": "ਹਰ ਪਲ ਇੱਕ ਨਵੀਂ ਸ਼ੁਰੂਆਤ ਹੈ।", "transliteration": "Har pala ika navīṁ shurū'āt hai."},
    {"english": "Listen to your heart always.", "native": "ਹਮੇਸ਼ਾ ਆਪਣੇ ਦਿਲ ਦੀ ਸੁਣੋ।", "transliteration": "Hameshā āpaṇē dina dī suno."},
    {"english": "Do what makes you happy.", "native": "ਉਹ ਕਰੋ ਜੋ ਤੁਹਾਨੂੰ ਖੁਸ਼ ਕਰਦਾ ਹੈ।", "transliteration": "Oh karo jō tuhānūṁ khusha karadā hai."},
    {"english": "Your potential is unlimited.", "native": "ਤੁਹਾਡੀ ਸਮਰੱਥਾ ਅਸੀਮ ਹੈ।", "transliteration": "Tuhāḍī samarathā asīma hai."},
    {"english": "Be brave and take risks.", "native": "ਬਹਾਦਰ ਬਣੋ ਅਤੇ ਜੋਖਮ ਲਓ।", "transliteration": "Bahādura baṇō atē jōkama la'ō."},
    {"english": "Celebrate your progress every day.", "native": "ਹਰ ਰੋਜ਼ ਆਪਣੀ ਤਰੱਕੀ ਦਾ ਜਸ਼ਨ ਮਨਾਓ।", "transliteration": "Har rōza āpaṇī tarakkī dā jashana manā'ō."},
    {"english": "Surround yourself with good people.", "native": "ਆਪਣੇ ਆਪ ਨੂੰ ਚੰਗੇ ਲੋਕਾਂ ਨਾਲ ਘੇਰੋ।", "transliteration": "Āpaṇē āpa nū chaṅgē lōkāṁ nāla ghērō."},
    {"english": "Read books and grow your mind.", "native": "ਕਿਤਾਬਾਂ ਪੜ੍ਹੋ ਅਤੇ ਆਪਣੇ ਮਨ ਦਾ ਵਿਕਾਸ ਕਰੋ।", "transliteration": "Kitābāṁ paṛhō atē āpaṇē mana dā vikāsa karo."},
    {"english": "Travel and discover new places.", "native": "ਯਾਤਰਾ ਕਰੋ ਅਤੇ ਨਵੀਆਂ ਥਾਵਾਂ ਦੀ ਖੋਜ ਕਰੋ।", "transliteration": "Yātarā karo atē navī'āṁ thāvāṁ dī khōja karo."},
    {"english": "Appreciate what you already have.", "native": "ਜੋ ਤੁਹਾਡੇ ਕੋਲ ਪਹਿਲਾਂ ਹੀ ਹੈ ਉਸਦੀ ਕਦਰ ਕਰੋ।", "transliteration": "Jō tuhāḍē kōla pahilāṁ hī hai usa dī kadara karo."},
    {"english": "Dance like nobody is watching.", "native": "ਇਦਾਂ ਨੱਚੋ ਜਿਵੇਂ ਕੋਈ ਨਹੀਂ ਦੇਖ ਰਿਹਾ।", "transliteration": "Idāṁ nachō jivēṁ kō'ī nahīṁ dēkha ri'ā."},
    {"english": "Sing from your heart out loud.", "native": "ਆਪਣੇ ਦਿਲ ਤੋਂ ਜ਼ੋਰ-ਜ਼ੋਰ ਨਾਲ ਗਾਓ।", "transliteration": "Āpaṇē dina tō zōra-zōra nāla gā'ō."},
    {"english": "Plant seeds of kindness everywhere.", "native": "ਹਰ ਜਗ੍ਹਾ ਦਿਆਲਤਾ ਦੇ ਬੀਜ ਬੀਜੋ।", "transliteration": "Har jaga di'ālatā dē bīja bījō."},
    {"english": "Let go of what you cannot control.", "native": "ਜਿਸਨੂੰ ਤੁਸੀਂ ਕੰਟਰੋਲ ਨਹੀਂ ਕਰ ਸਕਦੇ ਉਸਨੂੰ ਛੱਡ ਦਿਓ।", "transliteration": "Jisanū tusīṁ kaṇṭrōla nahīṁ kara sakadē usanu chhaḍa di'ō."},
    {"english": "Be present in the here and now.", "native": "ਇਥੇ ਅਤੇ ਹੁਣ ਵਿੱਚ ਮੌਜੂਦ ਰਹੋ।", "transliteration": "Ithē atē huṇa vica maujūda rahō."},
]
# ==== FALLBACK PHRASES END ====


def _load_json(path, default):
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return default


def _save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_phrase_history():
    data = _load_json(PHRASE_HISTORY_FILE, {"phrases": [], "last_updated": None})
    data.setdefault("phrases", [])
    return data


def save_phrase_history(data):
    data["last_updated"] = datetime.now().isoformat()
    _save_json(PHRASE_HISTORY_FILE, data)


def is_phrase_used(english):
    english_lower = english.lower().strip()
    for p in load_phrase_history()["phrases"]:
        if p.get("english", "").lower().strip() == english_lower:
            return True
    return False


def _history_native(p):
    for key in (PHRASE_KEY, "vietnamese", "native", "translation", "target"):
        value = p.get(key)
        if value:
            return str(value)
    return ""


def add_phrases_to_history(phrases, category):
    history = load_phrase_history()
    for phrase in phrases:
        history["phrases"].append({
            "english": phrase["english"],
            PHRASE_KEY: phrase["native"],
            "transliteration": phrase.get("transliteration", ""),
            "category": category,
            "generated_at": datetime.now().isoformat(),
        })
    save_phrase_history(history)
    print(f"[content] Saved {len(phrases)} phrases (history total: {len(history['phrases'])})")


def get_available_category():
    data = _load_json(RECENT_CATEGORIES_FILE, {"recent_categories": [], "last_updated": None})
    recent = data.get("recent_categories", [])
    available = [c for c in CATEGORIES if c not in recent]
    if not available:
        recent = recent[-5:]
        available = [c for c in CATEGORIES if c not in recent]
        print("[rotation] Reset recent categories")
    selected = random.choice(available)
    recent.append(selected)
    data["recent_categories"] = recent[-MAX_RECENT_CATEGORIES:]
    data["last_updated"] = datetime.now().isoformat()
    _save_json(RECENT_CATEGORIES_FILE, data)
    print(f"[rotation] Category: {selected} ({len(available)} available)")
    return selected


def _normalize_phrase(item):
    if not isinstance(item, dict):
        return None
    english = str(item.get("english", "")).strip()
    native = str(
        item.get(PHRASE_KEY)
        or item.get("native")
        or item.get("vietnamese")
        or item.get("translation")
        or ""
    ).strip()
    translit = str(item.get("transliteration") or item.get("romanization") or item.get("romaji") or "").strip()
    if not english or not native:
        return None
    if len(english.split()) > 16:
        return None
    if "/" in native or "|" in native:
        native = native.split("/")[0].split("|")[0].strip()
    return {
        "english": english.replace("  ", " ").strip(),
        "native": native.strip(),
        "transliteration": translit.strip().strip("[]"),
    }


def _history_keys(history):
    used_en = set()
    used_nat = set()
    for p in history.get("phrases", []):
        en = str(p.get("english", "")).lower().strip()
        nat = _history_native(p).lower().strip()
        if en:
            used_en.add(en)
        if nat:
            used_nat.add(nat)
    return used_en, used_nat


def generate_phrases(category_english: str, num_phrases: int = 5) -> list:
    category_native = CATEGORIES_NATIVE[category_english]
    history = load_phrase_history()
    used_en, used_nat = _history_keys(history)
    recent_english = [
        p["english"] for p in history["phrases"] if p.get("category") == category_english
    ][-30:]

    models = [config.AI_MODEL]
    if "gemini-fast" not in models:
        models.append("gemini-fast")

    if config.POLLINATIONS_API_KEY:
        for attempt in range(5):
            model = models[0] if attempt < 3 else models[-1]
            try:
                phrases = _request_phrases(category_english, category_native, recent_english, num_phrases, attempt, model)
                unique = []
                for item in phrases:
                    p = _normalize_phrase(item)
                    if not p:
                        continue
                    key_en = p["english"].lower().strip()
                    key_nat = p["native"].lower().strip()
                    if key_en in used_en or key_nat in used_nat:
                        continue
                    if any(key_en == u["english"].lower().strip() for u in unique):
                        continue
                    used_en.add(key_en)
                    used_nat.add(key_nat)
                    unique.append(p)
                    if len(unique) >= num_phrases:
                        break
                if len(unique) >= num_phrases:
                    add_phrases_to_history(unique[:num_phrases], category_english)
                    return unique[:num_phrases]
                print(f"[content] Attempt {attempt + 1}: only {len(unique)} fresh phrases (need {num_phrases})")
            except Exception as exc:  # noqa: BLE001 - network boundary
                print(f"[content] Attempt {attempt + 1} failed ({model}): {exc}")
            time.sleep(1.5 * (attempt + 1))
    else:
        print("[content] No POLLINATIONS_API_KEY, using fallback phrases")

    fresh_fallback = []
    for p in FALLBACK_PHRASES:
        if p["english"].lower().strip() in used_en or p["native"].lower().strip() in used_nat:
            continue
        fresh_fallback.append(p)
    if not fresh_fallback:
        raise RuntimeError("Phrase API unavailable and no unused fallback phrases left; refusing to reuse phrases")
    chosen = fresh_fallback[:num_phrases]
    if len(chosen) < num_phrases:
        print(f"[content] Only {len(chosen)} fresh fallback phrases; building a shorter lesson")
    add_phrases_to_history(chosen, category_english)
    return chosen


def _request_phrases(category_english, category_native, recent_english, num_phrases, attempt, model=None):
    avoid = ""
    if recent_english:
        avoid = "\nDo NOT reuse any of these phrases:\n" + "\n".join(f"- {p}" for p in recent_english)

    prompt = f"""Create {num_phrases * 6} unique {category_english} phrases for English speakers learning {LANGUAGE_NAME}.
{avoid}

Rules:
1. Keep every phrase short and natural (4-11 words in English).
2. Use natural commas for TTS breathing pauses.
3. Each phrase must be speakable in 2-4 seconds.
4. Write clean {LANGUAGE_NAME} in {NATIVE_NAME} with correct accents and orthography. One translation only, no slashes.
5. Transliteration is a friendly Roman-script pronunciation guide for English speakers (not IPA).
6. Vary the sentence patterns and emotions. No duplicates.
7. Phrases must feel like real everyday language, not textbook filler.

Return ONLY a JSON array:
[{{"english": "...", "native": "...", "transliteration": "..."}}]"""

    response = requests.post(
        "https://gen.pollinations.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {config.POLLINATIONS_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": model or config.AI_MODEL,
            "messages": [
                {"role": "system", "content": f"You are a {LANGUAGE_NAME} teacher creating short, natural, varied bilingual phrases. Reply with JSON only."},
                {"role": "user", "content": prompt},
            ],
            "temperature": min(0.95 + attempt * 0.02, 1.0),
        },
        timeout=90,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()

    if "```json" in content:
        content = content.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in content:
        content = content.split("```", 1)[1].split("```", 1)[0].strip()

    start = content.find("[")
    end = content.rfind("]")
    if start >= 0 and end > start:
        content = content[start:end + 1]

    data = json.loads(content)
    if not isinstance(data, list):
        raise ValueError("AI did not return a JSON array")
    return data
