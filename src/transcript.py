import os
import requests
from groq import Groq
from dotenv import load_dotenv
from src.redis_client import (
    get_transcript_from_redis,
    save_transcript_to_redis
)

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


def get_transcript_with_cache(video_id: str) -> str | None:
    cached = get_transcript_from_redis(video_id)

    if cached:
        print("Using Redis cached transcript")
        return cached

    print("Fetching transcript from API")
    text = get_clean_transcript(video_id)

    if not text or len(text.strip()) < 50:
        return None

    save_transcript_to_redis(video_id, text)
    return text



def get_transcript(video_id: str) -> tuple[str | None, str | None]:
    """
    Fetch subtitles from RapidAPI.
    Returns: (transcript_text, language_code)
    """
    url = "https://youtube-v2.p.rapidapi.com/video/subtitles"

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "youtube-v2.p.rapidapi.com"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params={"video_id": video_id},
            timeout=15
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("Failed to fetch transcript:", e)
        return None, None

    if not data.get("is_available") or "subtitles" not in data:
        return None, None

    lang = data.get("lang") or data.get("languageCode")
    text = " ".join(item["text"] for item in data["subtitles"])

    return text.strip(), lang


def translate_to_english(text: str) -> str:
    """
    Translate non-English transcript to English.
    Returns ONLY translated text.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "Translate the following transcript to English ONLY. "
                    "Do not explain anything. "
                    "Return only the translated text."
                )
            },
            {"role": "user", "content": text[:12000]}
        ]
    )
    return response.choices[0].message.content.strip()


def get_clean_transcript(video_id: str) -> str | None:
    """
    Full pipeline:
    - Fetch subtitles
    - If English → return as-is
    - Else → translate to English
    """
    transcript, lang = get_transcript(video_id)

    if transcript is None:
        return None

    if lang and lang.lower().startswith("en"):
        print("Transcript already in English")
        return transcript

    print(f"Translating transcript from '{lang}' to English")
    return translate_to_english(transcript)
