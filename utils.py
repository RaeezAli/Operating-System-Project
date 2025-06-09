# utils.py
import pyttsx3
import speech_recognition as sr

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Function to speak text
def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# Function to listen to microphone and recognize speech
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        command = r.recognize_google(audio)
        print("User:", command)
    except sr.UnknownValueError:
        speak("Sorry, I didn't get that.")
        return ""
    except sr.RequestError:
        speak("Speech service is down.")
        return ""
    return command.lower()
    