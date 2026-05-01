import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import musiclibrary
import requests
from openai import OpenAI

r = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "News api key"

def speak(text):
    engine.say(text) 
    engine.runAndWait()
    # time.sleep(0.6)

def aiprocess(command):
    client = OpenAI(
    api_key = "Api key"
    )
    completion = client.chat.completions.create(
    model = 'gpt-3.5-turbo',

    messages = [
        {"role": "system",
            "content": "You are a virtual assistant named Jarvis, skilled like Alexa and Google Assistant."},
        {"role":"user","content":command}
    ]
)
    return (completion.choices[0].message.content)

def processcommand(c):
    c=c.lower()
    # print(c)
    if "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open facebook" in c:
        # speak("Opening Google")
        webbrowser.open("https://www.facebook.com")
    elif "open linkedin" in c:
        # speak("Opening Google")
        webbrowser.open("https://www.linkedin.com")
    elif "open whatsapp" in c:
        # speak("Opening Google")
        webbrowser.open("https://www.whatsapp.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles',[])
            for article in articles:
                speak(article["title"])
    elif "stop" in c or "exit" in c:
        speak("Goodbye!")
       
    else:
        # let the open ai handle this
        output = aiprocess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis....")
   
    # obtain audio from microphone
    print("Recognizing...")
    while True:
        try:
            print("listening for wake word")
            with sr.Microphone() as source:
                # print("Listening...")
                
                audio = r.listen(source,timeout=5,phrase_time_limit=5)
            
            word = r.recognize_google(audio)
            print("hear",word)
            # print("User said:", command)
            if("jarvis" in word.lower()):
                # time.sleep(0.3)
                engine.say("Ya")
                print("jarvic active...")
                # time.sleep(1.5)
               # lisine for command
                with sr.Microphone() as source:
                    
                    audio = r.listen(source,timeout=5)
                    command =r.recognize_google(audio)

                    processcommand(command)


            
        except sr.UnknownValueError:
            speak("Sorry, I couldn't hear properly.")
        except sr.RequestError:
            speak("Network error while recognizing speech.")
        except Exception as e:
            print("Error:", e)
            speak("An error occurred.")
            