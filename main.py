import speech_recognition as sr
import pyttsx3
import webbrowser
import pywhatkit
import wikipedia
import datetime
import subprocess
import os
import time
import threading
import requests


engine = pyttsx3.init()
engine.setProperty('rate', 180) 


voices = engine.getProperty('voices')

selected_voice = None
for v in voices:
    if (
        ('en_US' in v.id or 'en_US' in v.name or 'english' in v.name.lower()) and
        ('female' in v.name.lower() or 'samantha' in v.id.lower() or 'siri' in v.id.lower())
    ):
        selected_voice = v.id
        break
if not selected_voice:
   
    for v in voices:
        if 'en' in v.id or 'english' in v.name.lower():
            selected_voice = v.id
            break
if selected_voice:
    engine.setProperty('voice', selected_voice)


APP_PATHS = {
    'safari': '/Applications/Safari.app',
    'chrome': '/Applications/Google Chrome.app',
    'google chrome': '/Applications/Google Chrome.app',
    'vscode': '/Applications/Visual Studio Code.app',
    'visual studio code': '/Applications/Visual Studio Code.app',
    'spotify': '/Applications/Spotify.app',
    'zoom': '/Applications/zoom.us.app',
    'discord': '/Applications/Discord.app',
    'notes': '/Applications/Notes.app',
    'calendar': '/Applications/Calendar.app',
    'reminders': '/Applications/Reminders.app',
    'messages': '/Applications/Messages.app',
    'terminal': '/Applications/Utilities/Terminal.app',
    'finder': '/System/Library/CoreServices/Finder.app',
}

# Shortcuts for websites
WEBSITE_SHORTCUTS = {
    'github': 'https://github.com',
    'stackoverflow': 'https://stackoverflow.com',
    'leetcode': 'https://leetcode.com',
    'geeksforgeeks': 'https://www.geeksforgeeks.org',
    'youtube': 'https://youtube.com',
    'spotify': 'https://open.spotify.com',
    'soundcloud': 'https://soundcloud.com',
    'instagram': 'https://instagram.com',
    'facebook': 'https://facebook.com',
    'twitter': 'https://twitter.com',
    'linkedin': 'https://linkedin.com',
    'whatsapp web': 'https://web.whatsapp.com',
}



def speak(text):
    """Speak the given text using TTS and print it."""
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for a voice command and return it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print(f"You: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please repeat.")
        return ""
    except sr.RequestError:
        speak("Sorry, my speech service is down.")
        return ""

def open_app(app_name):
    """Open a macOS application by name."""
    for key in APP_PATHS:
        if key in app_name:
            try:
                subprocess.Popen(["open", APP_PATHS[key]])
                speak(f"Opening {key}.")
                return
            except Exception as e:
                speak(f"Failed to open {key}: {e}")
                return
    speak(f"Sorry, I couldn't find the app {app_name}.")

def close_app(app_name):
    """Close a macOS application by name."""
    for key in APP_PATHS:
        if key in app_name:
            app_proc = key
            try:
                subprocess.call(["osascript", "-e", f'tell application \"{app_proc.title()}\" to quit'])
                speak(f"Closing {key}.")
                return
            except Exception as e:
                speak(f"Failed to close {key}: {e}")
                return
    speak(f"Sorry, I couldn't find the app {app_name}.")

def open_website(site):
    """Open a website by shortcut or URL."""
    for key in WEBSITE_SHORTCUTS:
        if key in site:
            webbrowser.open(WEBSITE_SHORTCUTS[key])
            speak(f"Opening {key}.")
            return
   
    if site.startswith('http'):
        webbrowser.open(site)
        speak(f"Opening {site}.")
    else:
        webbrowser.open(f"https://{site}")
        speak(f"Opening {site}.")

def play_youtube(query):
    """Play a YouTube video or music using pywhatkit."""
    try:
        speak(f"Playing {query} on YouTube.")
        pywhatkit.playonyt(query)
    except Exception as e:
        speak(f"Sorry, I couldn't play {query}: {e}")

def send_whatsapp_message(number, message):
    """Send a WhatsApp message using pywhatkit with improved error handling."""
    try:
      
        number = number.strip()
        
      
        import re
        if number.startswith('+'):
          
            clean_number = '+' + re.sub(r'[^\d]', '', number[1:])
        else:
          
            clean_number = re.sub(r'[^\d]', '', number)
            \
            if len(clean_number) == 10:
                clean_number = '+1' + clean_number
            elif len(clean_number) == 11 and clean_number.startswith('1'):
                clean_number = '+' + clean_number
            elif not clean_number.startswith('+'):
                clean_number = '+91' + clean_number  # Default to India if no country code
        
        speak(f"Attempting to send WhatsApp message to {clean_number}...")
        
       
        try:
            webbrowser.open('https://web.whatsapp.com')
            speak("Opening WhatsApp Web. Please make sure you're logged in.")
            time.sleep(2)  
        except Exception as e:
            speak(f"Could not open WhatsApp Web: {e}")
        
       
        try:
            
            pywhatkit.sendwhatmsg_instantly(
                clean_number, 
                message, 
                wait_time=15, 
                tab_close=True,
                close_time=3
            )
            speak(f"Message sent successfully to {clean_number}!")
            return True
        except Exception as e:
            speak(f"pywhatkit failed: {e}")
            
           
            try:
               
                encoded_message = requests.utils.quote(message)
                whatsapp_url = f"https://web.whatsapp.com/send?phone={clean_number}&text={encoded_message}"
                webbrowser.open(whatsapp_url)
                speak(f"Opened WhatsApp Web with your message. Please click send manually.")
                return True
            except Exception as fallback_error:
                speak(f"Fallback method also failed: {fallback_error}")
                return False
                
    except Exception as e:
        speak(f"Failed to send WhatsApp message: {e}")
        speak("Please make sure:")
        speak("1. You have WhatsApp Web open and logged in")
        speak("2. The phone number is correct with country code")
        speak("3. Your internet connection is stable")
        return False

def get_time():
    """Get the current system time."""
    now = datetime.datetime.now().strftime('%I:%M %p')
    speak(f"The time is {now}.")
    return now

def get_date():
    """Get the current system date."""
    today = datetime.datetime.now().strftime('%A, %B %d, %Y')
    speak(f"Today is {today}.")
    return today

def get_weather(city="New York"):
    """Get weather info using OpenWeatherMap API (requires API key)."""
    API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data.get('cod') != 200:
            speak(f"Sorry, I couldn't get weather for {city}.")
            return
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        speak(f"The weather in {city} is {weather} with a temperature of {temp}°C.")
    except Exception as e:
        speak(f"Failed to get weather: {e}")

def search_wikipedia(query):
    """Search Wikipedia and summarize the result."""
    try:
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
    except wikipedia.DisambiguationError as e:
        speak(f"Your query is ambiguous. Did you mean: {e.options[0]}?")
    except Exception as e:
        speak(f"Sorry, I couldn't find information on {query}.")

def set_reminder(reminder, seconds):
    """Set a reminder and notify the user after the specified seconds."""
    def notify():
        time.sleep(seconds)
        speak(f"Reminder: {reminder}")
    threading.Thread(target=notify).start()
    speak(f"Reminder set for {seconds} seconds from now.")

def add_calendar_event(event, date_time):
    """Add an event to the macOS Calendar using AppleScript."""
    try:
        script = f'tell application "Calendar" to make new event at end of events of calendar "Home" with properties {{summary:"{event}", start date:date "{date_time}"}}'
        subprocess.call(["osascript", "-e", script])
        speak(f"Event '{event}' added to your calendar.")
    except Exception as e:
        speak(f"Failed to add event: {e}")

def system_command(action):
    """Perform system actions: shutdown, restart, sleep."""
    try:
        if action == 'shutdown':
            speak("Shutting down the system.")
            os.system('sudo shutdown -h now')
        elif action == 'restart':
            speak("Restarting the system.")
            os.system('sudo shutdown -r now')
        elif action == 'sleep':
            speak("Putting the system to sleep.")
            os.system('pmset sleepnow')
        else:
            speak("Unknown system command.")
    except Exception as e:
        speak(f"Failed to execute system command: {e}")

def tell_joke():
    """Tell a simple hardcoded joke (macOS compatible)."""
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the computer show up at work late? It had a hard drive!",
        "Why do Java developers wear glasses? Because they don't see sharp!",
        "Why was the cell phone wearing glasses? Because it lost its contacts!",
    ]
    import random
    joke = random.choice(jokes)
    speak(joke)



def parse_command(command):
    """Parse the user's command and call the appropriate function."""
    if not command:
        return
    # Conversational responses
    if any(greet in command for greet in ["how are you", "how are you doing", "what's up", "whats up", "hello", "hi", "hey"]):
        speak("I'm just a bunch of Python code, but I'm doing great! How can I help you today?")
        return
    if any(who in command for who in ["who are you", "what are you", "your name"]):
        speak("I'm Jarvis, your macOS voice assistant. Ready to help you with anything!")
        return
    if "thank you" in command or "thanks" in command:
        speak("You're welcome! Let me know if you need anything else.")
        return
    # Flexible app open/close
    if ("open" in command and any(app in command for app in APP_PATHS)) or ("open app" in command):
        for key in APP_PATHS:
            if key in command:
                open_app(key)
                return
        # fallback to original
        if 'open app' in command:
            app_name = command.replace('open app', '').strip()
            open_app(app_name)
            return
    elif ("close" in command and any(app in command for app in APP_PATHS)) or ("close app" in command):
        for key in APP_PATHS:
            if key in command:
                close_app(key)
                return
        if 'close app' in command:
            app_name = command.replace('close app', '').strip()
            close_app(app_name)
            return
    # Website shortcuts
    elif 'open' in command and any(site in command for site in WEBSITE_SHORTCUTS):
        for site in WEBSITE_SHORTCUTS:
            if site in command:
                open_website(site)
                return
    elif 'open' in command and 'website' in command:
        site = command.replace('open website', '').strip()
        open_website(site)
        return
   
    elif 'play' in command and 'youtube' in command:
        query = command.replace('play', '').replace('on youtube', '').strip()
        play_youtube(query)
        return
   
    elif 'send whatsapp' in command or 'whatsapp message' in command or ('whatsapp' in command and 'send' in command):
       
        import re
        
       
        patterns = [
            r'to ([+\d\s\-\(\)]+)[:\- ]+(.+)', 
            r'([+\d\s\-\(\)]+)[:\- ]+(.+)',     # "send whatsapp 1234567890: hello"
            r'to ([+\d\s\-\(\)]+) (.+)',        
        ]
        
        number = None
        message = None
        
        for pattern in patterns:
            match = re.search(pattern, command)
            if match:
                number = match.group(1).strip()
                message = match.group(2).strip()
                break
        
        if number and message:
           
            number = re.sub(r'[\s\-\(\)]', '', number)
            send_whatsapp_message(number, message)
        else:
            speak("Please say: send WhatsApp to [number]: [message]")
            speak("Example: send WhatsApp to +1234567890: Hello there!")
        return
    elif 'time' in command:
        get_time()
        return
    elif 'date' in command:
        get_date()
        return
    elif 'weather' in command:
        if 'in' in command:
            city = command.split('in')[-1].strip()
            get_weather(city)
        else:
            get_weather()
        return
    elif 'wikipedia' in command or 'search' in command:
        if 'wikipedia' in command:
            query = command.replace('wikipedia', '').replace('search', '').strip()
        else:
            query = command.replace('search', '').strip()
        search_wikipedia(query)
        return
    elif 'remind me' in command or 'set reminder' in command:
        try:
            if 'in' in command:
                reminder = command.split('to')[1].split('in')[0].strip()
                seconds = command.split('in')[1].strip().split()[0]
                seconds = int(seconds)
                set_reminder(reminder, seconds)
            else:
                speak("Please specify the time for the reminder.")
        except Exception:
            speak("Please say: remind me to [task] in [seconds] seconds.")
        return
    elif 'add event' in command or 'calendar' in command:
        try:
            event = command.split('event')[1].split('at')[0].strip()
            date_time = command.split('at')[1].strip()
            add_calendar_event(event, date_time)
        except Exception:
            speak("Please say: add event [event] at [YYYY-MM-DD HH:MM]")
        return
    elif 'shutdown' in command:
        system_command('shutdown')
        return
    elif 'restart' in command:
        system_command('restart')
        return
    elif 'sleep' in command:
        system_command('sleep')
        return
    elif 'joke' in command:
        tell_joke()
        return
    elif 'exit' in command or 'quit' in command or 'stop' in command:
        speak("Goodbye! Have a great day.")
        exit(0)
    else:
      
        speak("Sorry, I didn't understand that command. Here are some things you can ask me to do: open Safari, open website GitHub, play music on YouTube, send WhatsApp to [number]: [message], what's the weather in London, search Python on Wikipedia, remind me to drink water in 10 seconds, add event Meeting at 2024-06-01 15:00, tell me a joke, shutdown, restart, sleep, or exit.")


def main():
    speak("Hello! I am Jarvis, your macOS assistant. How can I help you today?")
    while True:
        command = listen()
        parse_command(command)

if __name__ == "__main__":
    main()
