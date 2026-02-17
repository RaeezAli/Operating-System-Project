import speech_recognition as sr

def take_command():
    """Listens for a command from the microphone and returns it as a recognized string."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User: {query}\n")
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("Speech service is down.")
        return ""
    return query.lower()
