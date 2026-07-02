import json
import os
import re
import urllib.parse
import webbrowser
from pathlib import Path

import pyttsx3
import requests
import speech_recognition as sr

from musiclibrary import find_song, music

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv()


BASE_DIR = Path(__file__).resolve().parent
WAKE_WORD = os.getenv("WAKE_WORD", "jarvis").lower()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
NEWS_COUNTRY = os.getenv("NEWS_COUNTRY", "in")

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def int_env(name, default):
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


engine.setProperty("rate", int_env("VOICE_RATE", 175))


def load_custom_mapping(filename):
    path = BASE_DIR / filename
    if not path.exists():
        return {}

    try:
        with path.open(encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Could not load {filename}: {exc}")
        return {}

    if not isinstance(data, dict):
        print(f"{filename} must contain a JSON object.")
        return {}

    cleaned = {}
    for name, link in data.items():
        if isinstance(name, str) and isinstance(link, str) and name.strip() and link.strip():
            cleaned[name.strip().lower()] = link.strip()
    return cleaned


WEB_LINKS = {
    "airbnb": "https://www.airbnb.com",
    "amazon": "https://www.amazon.in",
    "apple": "https://www.apple.com",
    "apple music": "https://music.apple.com",
    "bbc": "https://www.bbc.com/news",
    "bing": "https://www.bing.com",
    "book my show": "https://in.bookmyshow.com",
    "booking": "https://www.booking.com",
    "canva": "https://www.canva.com",
    "chatgpt": "https://chatgpt.com",
    "claude": "https://claude.ai",
    "codepen": "https://codepen.io",
    "coursera": "https://www.coursera.org",
    "cricbuzz": "https://www.cricbuzz.com",
    "devdocs": "https://devdocs.io",
    "discord": "https://discord.com/app",
    "duckduckgo": "https://duckduckgo.com",
    "edge addons": "https://microsoftedge.microsoft.com/addons",
    "facebook": "https://www.facebook.com",
    "flipkart": "https://www.flipkart.com",
    "gemini": "https://gemini.google.com",
    "gmail": "https://mail.google.com",
    "google": "https://www.google.com",
    "google calendar": "https://calendar.google.com",
    "google classroom": "https://classroom.google.com",
    "google contacts": "https://contacts.google.com",
    "google docs": "https://docs.google.com",
    "google drive": "https://drive.google.com",
    "google flights": "https://www.google.com/travel/flights",
    "google forms": "https://forms.google.com",
    "google keep": "https://keep.google.com",
    "google maps": "https://www.google.com/maps",
    "google meet": "https://meet.google.com",
    "google news": "https://news.google.com",
    "google photos": "https://photos.google.com",
    "google sheets": "https://sheets.google.com",
    "google slides": "https://slides.google.com",
    "google translate": "https://translate.google.com",
    "github": "https://github.com",
    "gitlab": "https://gitlab.com",
    "gmail inbox": "https://mail.google.com/mail/u/0/#inbox",
    "hacker news": "https://news.ycombinator.com",
    "hotstar": "https://www.hotstar.com/in",
    "indeed": "https://www.indeed.com",
    "instagram": "https://www.instagram.com",
    "kaggle": "https://www.kaggle.com",
    "khan academy": "https://www.khanacademy.org",
    "leetcode": "https://leetcode.com",
    "linkedin": "https://www.linkedin.com",
    "linkedin jobs": "https://www.linkedin.com/jobs",
    "medium": "https://medium.com",
    "messenger": "https://www.messenger.com",
    "microsoft account": "https://account.microsoft.com",
    "microsoft copilot": "https://copilot.microsoft.com",
    "microsoft learn": "https://learn.microsoft.com",
    "microsoft office": "https://www.office.com",
    "microsoft teams": "https://teams.microsoft.com",
    "myntra": "https://www.myntra.com",
    "netflix": "https://www.netflix.com",
    "news": "https://news.google.com",
    "notion": "https://www.notion.so",
    "naukri": "https://www.naukri.com",
    "ola": "https://www.olacabs.com",
    "onedrive": "https://onedrive.live.com",
    "openai": "https://platform.openai.com",
    "outlook": "https://outlook.live.com",
    "perplexity": "https://www.perplexity.ai",
    "pinterest": "https://www.pinterest.com",
    "prime video": "https://www.primevideo.com",
    "product hunt": "https://www.producthunt.com",
    "quora": "https://www.quora.com",
    "reddit": "https://www.reddit.com",
    "replit": "https://replit.com",
    "spotify": "https://open.spotify.com",
    "stackoverflow": "https://stackoverflow.com",
    "swiggy": "https://www.swiggy.com",
    "telegram": "https://web.telegram.org",
    "trello": "https://trello.com",
    "twitter": "https://x.com",
    "uber": "https://www.uber.com",
    "udemy": "https://www.udemy.com",
    "vscode marketplace": "https://marketplace.visualstudio.com/vscode",
    "whatsapp": "https://web.whatsapp.com",
    "wikipedia": "https://www.wikipedia.org",
    "x": "https://x.com",
    "yahoo mail": "https://mail.yahoo.com",
    "youtube": "https://www.youtube.com",
    "youtube music": "https://music.youtube.com",
    "zomato": "https://www.zomato.com",
}
WEB_LINKS.update(load_custom_mapping("custom_links.json"))


def normalize_key(text):
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def find_website(site_name):
    if site_name in WEB_LINKS:
        return WEB_LINKS[site_name]

    normalized = normalize_key(site_name)
    for saved_name, link in WEB_LINKS.items():
        if normalize_key(saved_name) == normalized:
            return link

    return None


def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()


def open_url(url, label):
    speak(f"Opening {label}")
    webbrowser.open(url)


def google_search(query):
    encoded_query = urllib.parse.quote_plus(query)
    open_url(f"https://www.google.com/search?q={encoded_query}", f"Google search for {query}")


def youtube_search(query):
    encoded_query = urllib.parse.quote_plus(query)
    open_url(f"https://www.youtube.com/results?search_query={encoded_query}", f"YouTube search for {query}")


def ai_process(command):
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return "OpenAI API key is missing. Please set OPENAI_API_KEY in your environment or .env file."

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Jarvis, a concise and helpful desktop voice assistant. "
                    "Keep spoken answers short, practical, and friendly."
                ),
            },
            {"role": "user", "content": command},
        ],
    )
    return completion.choices[0].message.content.strip()


def read_news():
    if not NEWS_API_KEY:
        speak("News API key is missing. Please set NEWS_API_KEY in your environment or .env file.")
        return

    try:
        response = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params={"country": NEWS_COUNTRY, "apiKey": NEWS_API_KEY},
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"News error: {exc}")
        speak("I could not fetch the news right now.")
        return

    articles = response.json().get("articles", [])
    if not articles:
        speak("I could not find news headlines right now.")
        return

    speak("Here are the top headlines.")
    for article in articles[:5]:
        title = article.get("title")
        if title:
            speak(title)


def play_music(command):
    song_name = command.replace("play", "", 1).strip()
    if not song_name:
        speak("Please say the song or playlist name after play.")
        return

    link = find_song(song_name)
    if link:
        open_url(link, song_name)
        return

    speak(f"I do not have {song_name} saved. Searching YouTube.")
    youtube_search(song_name)


def open_website(command):
    site_name = command.replace("open", "", 1).strip()
    if not site_name:
        speak("Please say a website name after open.")
        return

    link = find_website(site_name)
    if link:
        open_url(link, site_name)
        return

    if "." in site_name:
        open_url(f"https://{site_name}", site_name)
        return

    speak(f"I do not have {site_name} saved. Searching Google.")
    google_search(site_name)


def tell_help():
    sites = ", ".join(sorted(WEB_LINKS.keys()))
    songs = ", ".join(sorted(music.keys()))
    speak("You can say open, play, search, youtube search, list sites, list music, news, help, or stop.")
    print(f"Saved sites: {sites}")
    print(f"Saved music: {songs}")


def process_command(command):
    command = command.lower().strip()
    print(f"Command: {command}")

    if command in {"stop", "exit", "quit", "shutdown"}:
        speak("Goodbye!")
        return False

    if command in {"help", "what can you do", "commands"}:
        tell_help()
        return True

    if command in {"list sites", "show sites", "website list"}:
        speak(f"I have {len(WEB_LINKS)} website shortcuts. Check the terminal for the full list.")
        print("Saved sites:")
        for name in sorted(WEB_LINKS):
            print(f"- {name}: {WEB_LINKS[name]}")
        return True

    if command in {"list music", "show music", "music list", "song list"}:
        speak(f"I have {len(music)} music shortcuts. Check the terminal for the full list.")
        print("Saved music:")
        for name in sorted(music):
            print(f"- {name}: {music[name]}")
        return True

    if command.startswith("open "):
        open_website(command)
        return True

    if command.startswith("play "):
        play_music(command)
        return True

    if command.startswith("youtube search "):
        youtube_search(command.replace("youtube search", "", 1).strip())
        return True

    if command.startswith("search ") or command.startswith("google "):
        query = command.split(" ", 1)[1].strip()
        if query:
            google_search(query)
        else:
            speak("Please say what you want me to search.")
        return True

    if "news" in command:
        read_news()
        return True

    output = ai_process(command)
    speak(output)
    return True


def listen_once(source, timeout=5, phrase_time_limit=5):
    audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    return recognizer.recognize_google(audio).lower()


def run_assistant():
    speak("Initializing Jarvis.")
    print(f"Listening for wake word: {WAKE_WORD}")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening for wake word...")
                wake_text = listen_once(source)

            print(f"Heard: {wake_text}")
            if WAKE_WORD not in wake_text:
                continue

            speak("Yes?")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                command = listen_once(source, timeout=6, phrase_time_limit=8)

            if not process_command(command):
                break

        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            speak("Sorry, I could not hear properly.")
        except sr.RequestError:
            speak("Network error while recognizing speech.")
        except KeyboardInterrupt:
            speak("Goodbye!")
            break
        except Exception as exc:
            print(f"Error: {exc}")
            speak("An error occurred.")


if __name__ == "__main__":
    run_assistant()
