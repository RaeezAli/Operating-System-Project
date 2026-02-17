import pyttsx3
import threading

# Initialize engine outside the function if needed, or inside with a lock
_engine = pyttsx3.init()
_engine.setProperty('rate', 150)
_speak_lock = threading.Lock()

def speak(text):
    """Synthesizes the given text into speech."""
    with _speak_lock:
        print(f"Jarvis: {text}")
        _engine.say(text)
        _engine.runAndWait()
