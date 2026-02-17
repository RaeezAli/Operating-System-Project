import speech_recognition as sr
from voice.speech_output import speak

def take_command():
    """Listens for a command from the microphone and returns it as a recognized string."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        # Added a 2-second timeout to prevent indefinite blocking if no audio detected
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("[INFO] Listening timed out.")
            return ""

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User: {query}\n")
    except sr.UnknownValueError:
        speak("I'm sorry, I didn't quite catch that. Could you repeat it?")
        return ""
    except sr.RequestError:
        speak("My speech recognition service is currently unavailable.")
        return ""
    except Exception as e:
        print(f"[ERROR] Recognition error: {e}")
        return ""
        
    return query.lower()
