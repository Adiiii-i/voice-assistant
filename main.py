# 📦 Jarvis Assistant with WhatsApp Web Messaging, Error-Free Listening, and App Control on Mac

import pyttsx3
import speech_recognition as sr
import datetime
import os
import webbrowser
import pyautogui
import wikipedia
import time
import subprocess

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Male voice
engine.setProperty('rate', 175)

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please speak again.")
            return ""
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except:
        speak("Sorry, I didn't catch that.")
        return ""
    return query.lower()

def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning Aadi!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Aadi!")
    else:
        speak("Good Evening Aadi!")
    speak("I am Jarvis. How may I help you?")

def open_website(site):
    webbrowser.open(site)
    speak(f"Opening {site}")

def open_app(app_name):
    try:
        subprocess.Popen(["open", "-a", app_name])
        speak(f"Opening {app_name}")
    except Exception as e:
        speak(f"Couldn't open {app_name}")

def close_app(app_name):
    try:
        subprocess.call(["osascript", "-e", f'quit app "{app_name}"'])
        speak(f"Closing {app_name}")
    except:
        speak("Unable to close app")

def send_whatsapp_message(name, message):
    speak(f"Sending message to {name}: {message}")
    webbrowser.open("https://web.whatsapp.com")
    time.sleep(15)  # Wait for WhatsApp to load
    pyautogui.hotkey('command', 'f')
    time.sleep(1)
    pyautogui.typewrite(name)
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite(message)
    time.sleep(1)
    pyautogui.press('enter')

# -------------- Main Logic -------------------

wish_me()

while True:
    query = take_command()

    if query == "":
        continue

    if 'open google' in query:
        open_website("https://www.google.com")

    elif 'open youtube' in query:
        open_website("https://www.youtube.com")

    elif 'open whatsapp' in query:
        open_website("https://web.whatsapp.com")

    elif 'search' in query:
        search_query = query.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        speak(f"Searching for {search_query}")

    elif 'send message to' in query:
        try:
            parts = query.replace("send message to", "").strip().split(" saying ")
            contact = parts[0].strip()
            message = parts[1].strip()
            send_whatsapp_message(contact, message)
        except:
            speak("Sorry, I couldn't understand the contact or message.")

    elif 'open safari' in query:
        open_app("Safari")

    elif 'open vs code' in query:
        open_app("Visual Studio Code")

    elif 'close safari' in query:
        close_app("Safari")

    elif 'close whatsapp' in query:
        close_app("WhatsApp")

    elif 'what is' in query or 'who is' in query:
        result = wikipedia.summary(query, sentences=2)
        speak(result)

    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")

    elif 'exit' in query or 'stop' in query or 'bye' in query:
        speak("Goodbye Aadi. Have a nice day!")
        break

    else:
        speak("Sorry, I didn't understand that.")