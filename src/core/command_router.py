import os
import sys

# Add src to path for internal imports if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from automation.web_search import google_search, play_on_youtube, open_url
from automation.system_monitor import get_battery_status, get_ip_address, get_current_time, get_current_date
from automation.file_manager import move_file, clean_downloads
from automation.whatsapp import send_whatsapp_message
from os_simulator.scheduling.round_robin import round_robin_scheduling
from os_simulator.scheduling.gantt import plot_gantt_chart
from apis.wolfram import query_wolfram
from voice.speech_output import speak
from core.assistant import JarvisAssistant

assistant = JarvisAssistant()
task_list = []

def route_command(query):
    global task_list
    query = query.lower()

    # --- OS Simulator Commands ---
    if "add task" in query:
        # Expected format: "add task Task1 burst 5"
        try:
            parts = query.split()
            name = parts[2]
            burst = int(parts[4])
            task_list.append((name, burst))
            speak(f"Task {name} with burst {burst} added.")
        except:
            speak("Invalid format. Use: add task [name] burst [time]")

    elif "run scheduler" in query:
        if not task_list:
            speak("Please add some tasks first.")
            return
        try:
            quantum = 2 # Default
            if "quantum" in query:
                quantum = int(query.split()[-1])
            
            processes, bursts = zip(*task_list)
            gantt, wait, turn = round_robin_scheduling(list(processes), list(bursts), quantum)
            speak("Scheduling complete. Generating Gantt chart.")
            plot_gantt_chart(list(processes), gantt)
            task_list = [] # Clear after run
        except Exception as e:
            print(f"Error: {e}")
            speak("Scheduler failed.")

    # --- Automation Commands ---
    elif "open" in query:
        if "notepad" in query: os.system("notepad")
        elif "calculator" in query: os.system("calc")
        elif "google" in query: open_url("https://google.com")
        else: speak("I'm not sure which app you want to open.")

    elif "search" in query:
        google_search(query.replace("search", "").strip())
    
    elif "play" in query:
        play_on_youtube(query.replace("play", "").strip())

    elif "whatsapp" in query:
        speak("Who is the contact?")
        contact = input("Contact: ")
        speak("What is the message?")
        msg = input("Message: ")
        send_whatsapp_message(contact, msg)

    # --- System Info ---
    elif "battery" in query: get_battery_status()
    elif "ip" in query: get_ip_address()
    elif "time" in query: get_current_time()
    elif "date" in query: get_current_date()

    # --- File Management ---
    elif "clean downloads" in query: clean_downloads()
    elif "move file" in query:
        speak("Source path?")
        src = input("Source: ")
        speak("Destination path?")
        dst = input("Destination: ")
        move_file(src, dst)

    # --- Calculation ---
    elif "calculate" in query:
        res = query_wolfram(query.replace("calculate", ""))
        speak(f"The result is {res}")

    # --- Chatbot Fallback ---
    else:
        response = assistant.get_response(query)
        speak(response)
