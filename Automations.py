import os
import shutil
import time
import PyPDF2

# Assumes speak() is imported from utils or defined elsewhere
from utils import speak


# 1. Wake Word Detection (basic placeholder)
def wake_word_detected(command):
    return "jarvis" in command.lower()

# 2. Reminder / Alarm
def set_reminder(message, delay_sec):
    speak(f"Setting reminder in {delay_sec} seconds.")
    time.sleep(delay_sec)
    speak(f"Reminder: {message}")

# 4. File Management
def move_files(src, dst):
    try:
        shutil.move(src, dst)
        speak(f"Moved file from {src} to {dst}")
    except Exception as e:
        speak("Error moving file.")
        print(e)

# 5. PDF Reader
def read_pdf(path):
    try:
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            speak("Reading PDF content.")
            print(text)
            speak(text[:500])  # Speak first 500 chars
    except Exception as e:
        speak("Unable to read PDF.")
        print(e)

# 6. Clean Downloads Folder
def clean_downloads(download_path, keep_extensions=None):
    keep_extensions = keep_extensions or []
    try:
        for filename in os.listdir(download_path):
            if not any(filename.endswith(ext) for ext in keep_extensions):
                filepath = os.path.join(download_path, filename)
                os.remove(filepath)
        speak("Cleaned Downloads folder.")
    except Exception as e:
        speak("Error cleaning folder.")
        print(e)
