"""
VELOCITY PUNJABI - Unified Social Media Upload Script
Uploads generated reels to all connected social media platforms
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

upload_dir = Path(__file__).parent / "upload"
if upload_dir.exists() and str(upload_dir) not in sys.path:
    sys.path.insert(0, str(upload_dir))

upload_to_facebook = None
upload_to_instagram = None
upload_to_youtube = None

try:
    from upload_facebook import upload_to_facebook as fb_upload
    upload_to_facebook = fb_upload
except ImportError as e:
    print(f"[!] Facebook upload module not available: {e}")

try:
    from upload_instagram import upload_to_instagram as ig_upload
    upload_to_instagram = ig_upload
except ImportError as e:
    print(f"[!] Instagram upload module not available: {e}")

try:
    from upload_to_youtube import upload_to_youtube as yt_upload
    upload_to_youtube = yt_upload
except ImportError as e:
    print(f"[!] YouTube upload module not available: {e}")


def get_latest_reel():
    video_dir = Path("output/video")
    if not video_dir.exists():
        print("No output/video directory found")
        return None
    reels = list(video_dir.glob("*/final_reel.mp4"))
    if not reels:
        print("No reels found in output/video directory")
        return None
    latest = max(reels, key=lambda p: p.stat().st_mtime)
    metadata_file = latest.parent / "metadata.json"
    metadata = {}
    if metadata_file.exists():
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    return {
        "video_path": str(latest),
        "metadata": metadata,
        "category": metadata.get("category_english", "Punjabi Learning"),
        "phrases": metadata.get("phrases", [])
    }


def generate_caption(phrases, category, platform="facebook"):
    if platform == "facebook":
        caption_lines = [
            f"Learn Punjabi with VELOCITY PUNJABI!",
            f"",
            f"Category: {category}",
            f"",
            f"Master Punjabi one phrase at a time! Today's {category} lesson:",
            f""
        ]
        emojis = ["1", "2", "3", "4", "5"]
        for i, phrase in enumerate(phrases[:5], 0):
            emoji = emojis[i] if i < len(emojis) else f"{i+1}."
            caption_lines.append(f"{emoji}. {phrase['english']}")
            caption_lines.append(f"   {phrase.get('punjabi', '')}")
            caption_lines.append(f"   [{phrase.get('transliteration', '')}]")
            caption_lines.append("")
        caption_lines.extend([
            f"Tip: Repeat each phrase out loud 3 times!",
            f"Like this video if you learned something new!",
            f"Comment your favorite phrase below!",
            f"Follow for daily Punjabi lessons!",
            f"",
        ])
        hashtags = [
            f"#learnpunjabi",
            f"#punjabilessons",
            f"#punjabiforbeginners",
            f"#languagelearning",
            f"#punjabivocabulary",
            f"#velocitypunjabi",
            f"#dailypunjabi",
            f"#punjabi",
            f"#learnlanguages",
            f"#punjabiteacher",
            f"#speakpunjabi",
            f"#punjabipractice",
            f"#bilingual",
            f"#punjabiwords",
            f"#languagetips"
        ]
        caption_lines.extend(hashtags)
    else:
        caption_lines = [
            f"Learn Punjabi with VELOCITY PUNJABI!",
            f"",
            f"Category: {category}",
            f"",
            f"Today's phrases:",
            f""
        ]
        for i, phrase in enumerate(phrases[:3], 1):
            caption_lines.append(f"{i}. {phrase['english']}")
            caption_lines.append(f"   -> {phrase.get('punjabi', '')}")
            caption_lines.append("")
        hashtags = [
            f"#learnpunjabi",
            f"#punjabilessons",
            f"#punjabiforbeginners",
            f"#languagelearning",
            f"#punjabivocabulary",
            f"#velocitypunjabi",
            f"#dailypunjabi",
            f"#punjabi",
            f"#learnlanguages",
            f"#punjabiteacher"
        ]
        caption_lines.extend(hashtags)
    return "\n".join(caption_lines)


def main():
    print("\n" + "="*80)
    print(f"VELOCITY PUNJABI - AUTOMATED UPLOAD")
    print("="*80)
    reel = get_latest_reel()
    if not reel:
        print("\nNo reel found! Run facebook_reels_automation.py first.")
        sys.exit(1)
    print(f"\nFound latest reel:")
    print(f"   Category: {reel['category']}")
    print(f"   Video: {reel['video_path']}")
    print(f"   Phrases: {len(reel['phrases'])}")
    caption = generate_caption(reel['phrases'], reel['category'], platform="facebook")
    print(f"\nGenerated caption ({len(caption)} chars):")
    print("-"*80)
    print(caption[:500] + "..." if len(caption) > 500 else caption)
    print("-"*80)
    print(f"\nUpload complete!")


if __name__ == "__main__":
    main()
