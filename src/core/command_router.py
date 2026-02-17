import os
import sys

# Add src to path for internal imports if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from automation.web_search import google_search, play_on_youtube, open_url
from automation.system_monitor import get_battery_status, get_ip_address, get_current_time, get_current_date
from automation.file_manager import move_file, clean_downloads
from automation.whatsapp import send_whatsapp_message
from os_simulator.scheduling.models import Process
from os_simulator.scheduling.fcfs import FCFSScheduler
from os_simulator.scheduling.round_robin import RoundRobinScheduler
from utils.visualizer import SchedulerVisualizer
from utils.logger import logger
from apis.wolfram import query_wolfram
from voice.speech_output import speak
from core.assistant import JarvisAssistant

assistant = JarvisAssistant()
pending_processes = []

def route_command(query):
    global pending_processes
    query = query.lower()

    # --- OS Simulator: Scheduling ---
    if "add task" in query:
        try:
            parts = query.split()
            # Format: add task PID burst BURST [arrival ARR]
            pid = parts[2]
            burst = int(parts[4])
            arrival = 0
            if "arrival" in parts:
                arrival = int(parts[parts.index("arrival") + 1])
            
            pending_processes.append(Process(pid=pid, burst_time=burst, arrival_time=arrival))
            speak(f"Process {pid} added to queue.")
            logger.info(f"Process added: {pid} (Burst: {burst}, Arrival: {arrival})")
        except Exception as e:
            speak("Invalid format. Usage: add task [PID] burst [TIME]")
            logger.error(f"Failed to add process: {e}")

    elif "run scheduler" in query:
        if not pending_processes:
            speak("No processes in queue. Add tasks first.")
            return

        try:
            # Choose algorithm
            if "round robin" in query or "rr" in query:
                quantum = 2
                if "quantum" in query:
                    quantum = int(query.split()[-1])
                scheduler = RoundRobinScheduler(quantum=quantum)
                title = f"Round Robin (q={quantum})"
            else:
                scheduler = FCFSScheduler()
                title = "FCFS Scheduling"

            # Load processes and execute
            for p in pending_processes:
                scheduler.add_process(p)
            
            gantt = scheduler.run()
            avg_wait, avg_tat = scheduler.get_average_metrics()
            
            speak(f"Execution complete using {title}. Displaying results.")
            
            # Use visualizer for output
            SchedulerVisualizer.print_metrics(scheduler.processes, avg_wait, avg_tat)
            SchedulerVisualizer.plot_gantt(gantt, title=title)
            
            pending_processes = [] # Clear queue after run
        except Exception as e:
            logger.error(f"Scheduler execution failed: {e}")
            speak("The scheduler encountered a technical error.")

    # --- Automation Commands ---
    elif "open" in query:
        if "notepad" in query: 
            os.system("notepad")
            logger.info("Task completed: Opened Notepad")
        elif "calculator" in query: 
            os.system("calc")
            logger.info("Task completed: Opened Calculator")
        elif "google" in query: 
            open_url("https://google.com")
            logger.info("Task completed: Opened Google in browser")
        else: speak("I'm not sure which app you want to open.")

    elif "search" in query:
        target = query.replace("search", "").strip()
        google_search(target)
        logger.info(f"Task completed: Google Search for '{target}'")
    
    elif "play" in query:
        target = query.replace("play", "").strip()
        play_on_youtube(target)
        logger.info(f"Task completed: Played '{target}' on YouTube")

    elif "whatsapp" in query:
        speak("Who is the contact?")
        contact = input("Contact: ")
        speak("What is the message?")
        msg = input("Message: ")
        send_whatsapp_message(contact, msg)
        logger.info(f"Task completed: Sent WhatsApp message to {contact}")

    # --- System Info ---
    elif "battery" in query: 
        get_battery_status()
        logger.info("Task completed: Checked battery status")
    elif "ip" in query: 
        get_ip_address()
        logger.info("Task completed: Checked IP address")
    elif "time" in query: 
        get_current_time()
        logger.info("Task completed: Checked current time")
    elif "date" in query: 
        get_current_date()
        logger.info("Task completed: Checked current date")

    # --- File Management ---
    elif "clean downloads" in query: 
        clean_downloads()
        logger.info("Task completed: Cleaned Downloads folder")
    elif "move file" in query:
        speak("Source path?")
        src = input("Source: ")
        speak("Destination path?")
        dst = input("Destination: ")
        move_file(src, dst)
        logger.info(f"Task completed: Moved file from {src} to {dst}")

    # --- Calculation ---
    elif "calculate" in query:
        expr = query.replace("calculate", "").strip()
        res = query_wolfram(expr)
        speak(f"The result is {res}")
        logger.info(f"Task completed: Calculated '{expr}' with result '{res}'")

    # --- Chatbot Fallback ---
    else:
        response = assistant.get_response(query)
        speak(response)
