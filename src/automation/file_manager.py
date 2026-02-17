import os
import shutil
from voice.speech_output import speak

def move_file(src, dst):
    """Moves a file from src to dst and announces the result."""
    try:
        if not os.path.exists(src):
            speak("Source file does not exist.")
            return
        shutil.move(src, dst)
        speak(f"Moved file from {os.path.basename(src)} to {dst}")
    except Exception as e:
        print(f"[ERROR] Failed to move file: {e}")
        speak("I encountered an error while moving the file.")

def clean_downloads(path=None):
    """Cleans the Downloads folder (or specified path) of all files."""
    if path is None:
        path = os.path.join(os.path.expanduser("~"), "Downloads")
    
    try:
        files = os.listdir(path)
        if not files:
            speak("The folder is already clean.")
            return

        for filename in files:
            filepath = os.path.join(path, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath)
        
        speak(f"Successfully cleaned folder: {path}")
    except Exception as e:
        print(f"[ERROR] Cleaning failed: {e}")
        speak("I couldn't clean the downloads folder.")
