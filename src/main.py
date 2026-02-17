import os
import sys

# Ensure the src directory is in the path for modular imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from voice.speech_input import take_command
from voice.speech_output import speak
from core.command_router import route_command

def main():
    speak("Jarvis is online. How can I assist you today?")

    while True:
        try:
            # Choice to type or speak
            query = input("Type your command or press Enter to speak (type 'exit' to quit): ").lower().strip()
            
            if not query:
                # If Enter is pressed without typing, use voice input
                query = take_command()
            
            if not query:
                continue

            if query in ["exit", "quit", "bye"]:
                speak("Shutting down the Jarvis OS Simulator. Goodbye!")
                break

            # Route the command to the appropriate module
            route_command(query)
            
        except KeyboardInterrupt:
            speak("Emergency shutdown initiated. Goodbye!")
            break
        except Exception as e:
            print(f"[FATAL ERROR] {e}")
            speak("I've encountered a critical error, but I'm staying online.")

if __name__ == "__main__":
    main()
