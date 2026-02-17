import pywhatkit
import webbrowser
from apis.wikipedia_api import get_wiki_summary
from voice.speech_output import speak

def google_search(query):
    """Performs a Google search and optionally reads a Wikipedia summary."""
    speak(f"Searching for {query} on Google.")
    pywhatkit.search(query)
    
    # Try to get a quick wiki summary as well
    summary = get_wiki_summary(query)
    if summary and not "I couldn't find" in summary:
        speak(f"According to Wikipedia: {summary}")

def play_on_youtube(topic):
    """Plays a video on YouTube."""
    speak(f"Playing {topic} on YouTube.")
    pywhatkit.playonyt(topic)

def open_url(url):
    """Opens a specific URL in the default browser."""
    webbrowser.open(url)
