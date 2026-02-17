import pyttsx3
import threading

_speak_lock = threading.Lock()

def speak(text):
    """
    Synthesizes the given text into speech using the SAPI5 driver.
    Initializes a local engine instance to ensure thread safety and driver stability.
    """
    with _speak_lock:
        try:
            print(f"Jarvis: {text}")
            # Re-initialize engine for each call to prevent driver stutters
            engine = pyttsx3.init('sapi5')
            engine.setProperty('rate', 170)
            
            # Set default voice (0 is usually male, 1 is female)
            voices = engine.getProperty('voices')
            if voices:
                engine.setProperty('voice', voices[0].id)
            
            engine.say(text)
            engine.runAndWait()
            # Explicitly stop to release the speaker resource
            engine.stop()
        except Exception as e:
            print(f"[ERROR] Speech synthesis failed: {e}")

# Note: Keeping the signature identical to maintain compatibility with other modules.
