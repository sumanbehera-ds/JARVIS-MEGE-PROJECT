import json
import re
import urllib.parse
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def youtube(query):
    return "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query)


music = {
    "2000s hindi": youtube("2000s hindi songs playlist"),
    "2010s bollywood": youtube("2010s bollywood songs playlist"),
    "90s bollywood": youtube("90s bollywood songs playlist"),
    "90s hindi": youtube("90s hindi songs playlist"),
    "acoustic": youtube("acoustic songs playlist"),
    "ambient": youtube("ambient music playlist"),
    "arijit singh": youtube("arijit singh best songs playlist"),
    "atif aslam": youtube("atif aslam best songs playlist"),
    "badshah": youtube("badshah songs playlist"),
    "bhajan": youtube("bhajan playlist"),
    "bollywood": youtube("best bollywood songs playlist"),
    "bollywood dance": youtube("bollywood dance songs playlist"),
    "bollywood romantic": youtube("bollywood romantic songs playlist"),
    "calm": youtube("calm music playlist"),
    "classical": youtube("indian classical music playlist"),
    "coding": youtube("coding music lofi playlist"),
    "coffee house": youtube("coffee house music playlist"),
    "deep focus": youtube("deep focus music playlist"),
    "devotional": youtube("devotional songs playlist"),
    "diljit dosanjh": youtube("diljit dosanjh songs playlist"),
    "english hits": youtube("english hits playlist"),
    "english romantic": youtube("english romantic songs playlist"),
    "focus": youtube("focus music playlist"),
    "gym": youtube("gym workout music playlist"),
    "hanuman chalisa": youtube("hanuman chalisa"),
    "happy": youtube("happy songs playlist"),
    "hindi chill": youtube("hindi chill songs playlist"),
    "hindi hits": youtube("hindi hits playlist"),
    "hindi lofi": youtube("hindi lofi songs playlist"),
    "hindi romantic": youtube("hindi romantic songs playlist"),
    "hindi sad": youtube("hindi sad songs playlist"),
    "indian pop": youtube("indian pop songs playlist"),
    "instrumental": youtube("instrumental music playlist"),
    "jazz": youtube("jazz music playlist"),
    "jubin nautiyal": youtube("jubin nautiyal songs playlist"),
    "kishore kumar": youtube("kishore kumar songs playlist"),
    "kk": youtube("kk songs playlist"),
    "kumar sanu": youtube("kumar sanu songs playlist"),
    "lata mangeshkar": youtube("lata mangeshkar songs playlist"),
    "lofi": youtube("lofi beats playlist"),
    "lofi hindi": youtube("hindi lofi playlist"),
    "meditation": youtube("meditation music playlist"),
    "mohit chauhan": youtube("mohit chauhan songs playlist"),
    "morning": youtube("morning music playlist"),
    "motivation": youtube("motivational songs playlist"),
    "old hindi": youtube("old hindi songs playlist"),
    "odia": youtube("odia songs playlist"),
    "odia bhajan": youtube("odia bhajan playlist"),
    "odia hits": youtube("odia hit songs playlist"),
    "odia romantic": youtube("odia romantic songs playlist"),
    "party": youtube("party songs playlist"),
    "piano": youtube("piano music playlist"),
    "pop": youtube("pop songs playlist"),
    "punjabi": youtube("punjabi songs playlist"),
    "punjabi party": youtube("punjabi party songs playlist"),
    "rain": youtube("rain sounds relaxing music"),
    "rap": youtube("rap songs playlist"),
    "relax": youtube("relaxing music playlist"),
    "retro": youtube("retro hindi songs playlist"),
    "rock": youtube("rock songs playlist"),
    "sad": youtube("sad songs playlist"),
    "sleep": youtube("sleep music playlist"),
    "soft music": youtube("soft music playlist"),
    "sonu nigam": youtube("sonu nigam songs playlist"),
    "spiritual": youtube("spiritual music playlist"),
    "study": youtube("study music playlist"),
    "sufi": youtube("sufi songs playlist"),
    "taylor swift": youtube("taylor swift songs playlist"),
    "travel": youtube("travel songs playlist"),
    "trending": youtube("trending songs india playlist"),
    "workout": youtube("workout music playlist"),
    "yo yo honey singh": youtube("yo yo honey singh songs playlist"),
}


def load_custom_music():
    path = BASE_DIR / "custom_music.json"
    if not path.exists():
        return {}

    try:
        with path.open(encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Could not load custom_music.json: {exc}")
        return {}

    if not isinstance(data, dict):
        print("custom_music.json must contain a JSON object.")
        return {}

    cleaned = {}
    for name, link in data.items():
        if isinstance(name, str) and isinstance(link, str) and name.strip() and link.strip():
            cleaned[normalize_name(name)] = link.strip()
    return cleaned


def normalize_name(name):
    return re.sub(r"\s+", " ", name.strip().lower())


music.update(load_custom_music())


def find_song(name):
    normalized = normalize_name(name)
    if normalized in music:
        return music[normalized]

    compact = re.sub(r"[^a-z0-9]+", "", normalized)
    for saved_name, link in music.items():
        saved_compact = re.sub(r"[^a-z0-9]+", "", saved_name)
        if saved_compact == compact or saved_name in normalized or normalized in saved_name:
            return link

    return None
