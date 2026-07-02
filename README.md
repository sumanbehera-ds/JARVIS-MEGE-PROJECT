# Jarvis Voice Assistant

Jarvis is a Python desktop voice assistant. It listens for the wake word `jarvis`, opens useful websites, plays music links, reads news headlines, and answers general questions with OpenAI.

## Features

- Wake-word activation
- Speech-to-text voice commands
- Text-to-speech replies
- Website launcher for common links
- YouTube and Google search commands
- Music and playlist shortcuts
- Private custom shortcuts through JSON files
- News headlines through NewsAPI
- AI responses through OpenAI
- Environment-based API key setup

## Quick Start

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create your local `.env` file:

```powershell
Copy-Item .env.example .env
```

4. Add your keys inside `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_newsapi_key_here
OPENAI_MODEL=gpt-4o-mini
NEWS_COUNTRY=in
WAKE_WORD=jarvis
VOICE_RATE=175
```

5. Run Jarvis:

```powershell
python main.py
```

## Voice Commands

Say `jarvis`, wait for Jarvis to answer, then say one of these commands:

- `open youtube`
- `open gmail`
- `open github`
- `open chatgpt`
- `open stackoverflow`
- `open google maps`
- `open google drive`
- `open microsoft office`
- `open microsoft copilot`
- `open linkedin jobs`
- `open leetcode`
- `open kaggle`
- `open naukri`
- `open canva`
- `open replit`
- `open spotify`
- `open youtube music`
- `open wikipedia`
- `open amazon`
- `play lofi`
- `play coding`
- `play bollywood`
- `play arijit singh`
- `play odia hits`
- `play workout`
- `play study`
- `play hindi romantic`
- `search python speech recognition`
- `youtube search relaxing music`
- `list sites`
- `list music`
- `news`
- `help`
- `stop`

## Saved Website Links

Website shortcuts are stored in `WEB_LINKS` inside `main.py`. Add more links like this:

```python
WEB_LINKS = {
    "portfolio": "https://your-portfolio-link.com",
}
```

Jarvis also loads private website shortcuts from `custom_links.json`. Start from the example file:

```powershell
Copy-Item custom_links.example.json custom_links.json
```

Then edit `custom_links.json`:

```json
{
  "my portfolio": "https://example.com",
  "my project": "https://github.com/your-name/your-project"
}
```

## Saved Music Links

Music shortcuts are stored in `musiclibrary.py`. Add more links like this:

```python
music = {
    "focus": "https://www.youtube.com/results?search_query=focus+music",
}
```

If Jarvis cannot find a saved song, it searches YouTube automatically.

Jarvis also loads private music shortcuts from `custom_music.json`. Start from the example file:

```powershell
Copy-Item custom_music.example.json custom_music.json
```

Then edit `custom_music.json`:

```json
{
  "my playlist": "https://www.youtube.com/results?search_query=my+favorite+playlist",
  "focus mix": "https://www.youtube.com/results?search_query=focus+music+playlist"
}
```

## Notes

- Do not commit your real `.env` file.
- `custom_links.json` and `custom_music.json` are ignored by Git so you can keep personal shortcuts private.
- `PyAudio` is required for microphone input. If installation fails on Windows, update pip first with `python -m pip install --upgrade pip`.
- A working internet connection is required for Google speech recognition, OpenAI answers, NewsAPI, and web searches.
