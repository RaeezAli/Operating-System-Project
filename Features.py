import pywhatkit
import wikipedia
import re
import subprocess
import pyautogui
from time import sleep

# Assumes speak() is imported from utils or defined elsewhere
from utils import speak

def GoogleSearch(query):
    replacements = ["jarvis", "what is", "search", "how to", "on", "google", "what do you mean by"]
    query = query.lower()
    for phrase in replacements:
        query = query.replace(phrase, "")
    query = re.sub(r'\s+', ' ', query).strip()

    if not query:
        speak("Sorry, I didn't understand the query.")
        return

    pywhatkit.search(query)

    try:
        search = wikipedia.summary(query, 2)
        speak(f"According to your search: {search}")
    except wikipedia.exceptions.PageError:
        speak("Sorry! The topic might not be on Wikipedia")


def Alarm(query):
    import datetime
    time_now = query.replace("set alarm for ", "").replace("set ", "").replace("alarm ", "").replace("for ", "").replace(" and ", ":")
    Alarm_Time = str(time_now)
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == Alarm_Time:
            speak("Wake up!")
            pyautogui.alert(text='Alarm Time!', title='Alarm', button='OK')
            break
        elif current_time > Alarm_Time:
            break

def DownloadYouTube():
    from pytube import YouTube
    from pyautogui import click, hotkey
    import pyperclip

    sleep(2)
    click(x=942, y=59)
    hotkey('ctrl', 'c')
    value = pyperclip.paste()
    Link = str(value)

    def Download(link):
        url = YouTube(link)
        video = url.streams.first()
        video.download('Downloads')

    Download(Link)
    speak("Downloaded the video. You can check the Downloads folder.")

def SpeedTest():
    subprocess.run(["python", "SpeedTestGui.py"])

def calculator(query):
    term = query.replace("jarvis", "").replace("addition", "+").replace("subtraction", "-")
    term = term.replace("multiplication", "*").replace("division", "/")
    term = term.replace("add", "+").replace("sub", "-").replace("multiply", "*")
    term = term.replace("divided", "/").replace("plus", "+").replace("minus", "-")
    final = str(term)
    try:
        result = eval(final)
        speak(f"Your calculation answer is {result}")
    except:
        speak("Can't fetch details.")