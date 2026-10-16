"""
YouTube Upload Script - VELOCITY PUNJABI
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

load_dotenv()

def get_authenticated_service():
    client_id = (os.getenv('YOUTUBE_CLIENT_ID') or os.getenv('YT_CLIENT_ID', '')).strip()
    client_secret = (os.getenv('YOUTUBE_CLIENT_SECRET') or os.getenv('YT_CLIENT_SECRET', '')).strip()
    refresh_token = (os.getenv('YOUTUBE_REFRESH_TOKEN') or os.getenv('YT_REFRESH_TOKEN', '')).strip()
    if not all([client_id, client_secret, refresh_token]):
        raise ValueError("Missing YouTube credentials")
    creds = Credentials(None, refresh_token=refresh_token, token_uri="https://oauth2.googleapis.com/token", client_id=client_id, client_secret=client_secret, scopes=["https://www.googleapis.com/auth/youtube"])
    try: creds.refresh(Request())
    except Exception as e:
        if "invalid_grant" in str(e).lower(): print("Refresh token expired")
        raise
    return build('youtube', 'v3', credentials=creds)

def generate_video_metadata(category, num_phrases, phrases=None):
    title = f"Odia Learning: {num_phrases} Essential {category} Phrases"
    lines = [f"Learn Odia with VELOCITY PUNJABI!", "", f"Category: {category}", "", f"Master Odia one phrase at a time! Today's {category} lesson:", ""]
    if phrases:
        for i, p in enumerate(phrases[:5], 0):
            lines.append(f"{i+1}. {p['english']}")
            lines.append(f"   {p.get('odia', '')}")
            lines.append(f"   [{p.get('transliteration', '')}]")
            lines.append("")
    lines.extend(["Tip: Repeat each phrase out loud 3 times!", "Like this video if you learned something new!", "Subscribe for daily Odia lessons!", "", f"#learnodia #odialessons #odiaforbeginners #LanguageLearning", f"#odia #Education #Tutorial #dailyodia #{category.replace(' ', '')}", f"#velocityodia #odiaPhrases #SpeakOdia"])
    tags = [f"learn slovak", f"odia lessons", f"odia for beginners", f"odia phrases", "language learning", f"Speak Odia", category.lower(), "education", f"daily Odia", "VELOCITY PUNJABI", f"Odia Learning"]
    return title, "\n".join(lines), tags

def upload_to_youtube(video_path, title, description, tags=None, category_id='22'):
    if tags is None: tags = ['education', 'language learning', hashtag]
    youtube = get_authenticated_service()
    body = {'snippet': {'title': title, 'description': description, 'tags': tags, 'categoryId': category_id}, 'status': {'privacyStatus': 'public', 'selfDeclaredMadeForKids': False}}
    if '#Shorts' not in body['snippet']['description']: body['snippet']['description'] += '\n\n#Shorts'
    media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True, mimetype='video/mp4')
    request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status: print(f"[youtube] Progress: {int(status.progress() * 100)}%")
    print(f"[youtube] Uploaded! ID: {response['id']}")
    return response

def main():
    video_file = Path('final_video.mp4')
    if not video_file.exists(): return
    try: upload_to_youtube(video_path=video_file, title=f"Learn Slovak Daily", description=f"#shorts #learnodia #odia #language #education", tags=[hashtag, 'education', 'language learning'], category_id='22')
    except Exception as e: print(f"[youtube] Failed: {e}"); raise

if __name__ == '__main__': main()
