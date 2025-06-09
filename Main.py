import os
import platform
import datetime
import webbrowser
import pywhatkit
import pyautogui
import time
import threading
import matplotlib.pyplot as plt
from notifypy import Notify
from multiprocessing import Process, Pipe, Lock
import shutil
import socket
import subprocess
import psutil

# Module we created 
from Automations import (
    wake_word_detected,
    set_reminder,
    move_files,
    read_pdf,
    clean_downloads
)

from utils import speak, take_command

from Features import (
    GoogleSearch,
    Alarm,
    DownloadYouTube,
    SpeedTest,
    calculator
)


from Whatsapp import whatsapp_chat_input


# Database imports
from Database.ChatBot.ChatBot import ChatterBot

# ========== Global Setup ==========
speak_lock = threading.Lock()
parent_conn, child_conn = Pipe()
task_list = []  # Dynamic task list for scheduling

# ========== Core Functions ==========

def run_in_thread(func, *args):
    thread = threading.Thread(target=func, args=args)
    thread.start()

# ========== Round Robin Scheduler ==========
def round_robin_scheduling(processes, burst_time, quantum):
    n = len(processes)
    remaining_burst = burst_time[:]
    waiting_time = [0] * n
    turnaround_time = [0] * n
    t = 0
    gantt_chart = []

    while True:
        done = True
        for i in range(n):
            if remaining_burst[i] > 0:
                done = False
                exec_time = min(quantum, remaining_burst[i])
                gantt_chart.append((processes[i], t, t + exec_time))
                t += exec_time
                remaining_burst[i] -= exec_time
                for j in range(n):
                    if j != i and remaining_burst[j] > 0:
                        waiting_time[j] += exec_time
        if done:
            break

    for i in range(n):
        turnaround_time[i] = waiting_time[i] + burst_time[i]

    print("\nProcess\tBurst\tWaiting\tTurnaround")
    for i in range(n):
        print(f"{processes[i]}\t{burst_time[i]}\t{waiting_time[i]}\t{turnaround_time[i]}")

    fig, ax = plt.subplots()
    ax.set_title("Round Robin Gantt Chart")
    ax.set_xlabel("Time")
    ax.set_ylabel("Processes")
    ax.set_yticks(range(len(processes)))
    ax.set_yticklabels(processes)

    for i, (p, start, end) in enumerate(gantt_chart):
        idx = processes.index(p)
        ax.broken_barh([(start, end - start)], (idx - 0.4, 0.8), facecolors=('tab:blue'))

    plt.grid(True)
    plt.show()


# ========== AI Assistant Features ==========
def open_app(name):
    if name == "notepad":
        os.system("notepad")
    elif name == "calculator":
        os.system("calc")
    elif name == "calendar":
        webbrowser.open("https://calendar.google.com")
    elif name == "google":
        webbrowser.open("https://www.google.com/")
    else:
        speak("App not recognized.")


def take_screenshot():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    pyautogui.screenshot(filename)
    speak(f"Screenshot saved as {filename}")

def get_ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    speak(f"Your IP address is {ip}")

def get_battery():
    battery = psutil.sensors_battery()
    percent = battery.percent
    speak(f"Battery is at {percent} percent")

def show_notification(title, message):
    notify = Notify()
    notify.title = title
    notify.message = message
    notify.send()
    
def custom_notification(msg):
    try:
        # Extract message after the word 'notify'
        message = msg.split("notify", 1)[1].strip()
        
        if message:
            show_notification("Jarvis Notification", message)
            speak(f"Notification sent: {message}")
        else:
            speak("Please provide a message after 'notify'.")
    except Exception as e:
        speak("Sorry, I couldn't send the notification.")
        print("Error:", e)

# ========== Main Assistant ==========
def main():
    speak("Jarvis is online. How can I help you today?")

    while True:
        query = input("Type your command or press Enter to speak: ").lower()
        if not query:
            query = take_command()

        # ---------- Task Scheduling ----------
        if query.startswith("add task"):
            try:
                parts = query.split()
                name = parts[2]
                burst = int(parts[4])
                task_list.append((name, burst))
                speak(f"Task {name} with burst time {burst} added to the scheduler.")
            except:
                speak("Invalid format. Use: add task Task1 burst 5")

        elif "run scheduler quantum" in query:
            try:
                parts = query.split()
                quantum = int(parts[-1])
                if task_list:
                    processes, bursts = zip(*task_list)
                    round_robin_scheduling(list(processes), list(bursts), quantum)
                    speak("Scheduling completed.")
                else:
                    speak("No tasks to schedule. Please add tasks first.")
            except:
                speak("Invalid format. Use: run scheduler quantum 2")

        # ---------- Productivity ----------
        elif "open" in query:
            apps = {
                "notepad": "notepad",
                "google": "google",
                "chrome": "google",
                "calculator": "calculator",
                "calendar": "calendar"
            }

            for keyword, app in apps.items():
                if keyword in query:
                    speak(f"Opening {keyword.capitalize()}...")
                    run_in_thread(open_app, app)
                    break


        # ---------- Internet Browsing ----------
        elif "search" in query:
            speak("Searching on Google...")
            query = query.replace("search", "")
            run_in_thread(webbrowser.open, f"https://www.google.com/search?q={query}")

        elif "shutdown" in query:
            speak("Shutting down...")
            os.system("shutdown /s /t 1")
        
        elif "play" in query:
            speak("Playing on YouTube...")
            query = query.replace("play", "")
            run_in_thread(pywhatkit.playonyt, query)
      
        elif "list files" in query or "show files" in query or "list file" in query:
            files = os.listdir()
            speak("Files in the current directory are:")
            for f in files:
                print(f)

        elif "open explorer" in query:
            run_in_thread(subprocess.Popen, "explorer")

        # ---------- Multimedia ----------
        elif "screenshot" in query:
            run_in_thread(take_screenshot)

        # ---------- System Utilities ----------
        elif any(kw in query for kw in ["ip address", "battery", "notify", "time", "date"]):
            utilities = {
                "ip address": get_ip,
                "battery": get_battery,
                "notify": lambda: custom_notification(query),
                "time": lambda: speak(f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}"),
                "date": lambda: speak(f"Today's date is {datetime.date.today().strftime('%B %d, %Y')}")
            }

            for key, func in utilities.items():
                if key in query:
                    run_in_thread(func)
                    time.sleep(3)
                    break

        # --- Automation Commands ---
        elif "set reminder" in query:
            try:
                speak("What should I remind you?")
                message = input("Reminder message: ")
                speak("After how many seconds?")
                delay = int(input("Seconds: "))
                run_in_thread(set_reminder, message, delay)
            except:
                speak("Failed to set reminder.")
                
        elif "send whatsapp message" in query or "send message" in query or "whatsapp" in query:
            whatsapp_chat_input()


        elif "read pdf" in query:
            speak("Enter PDF file path:")
            path = input("PDF Path: ")
            run_in_thread(read_pdf, path)

        elif "move file" in query:
            speak("Enter source file path:")
            src = input("Source: ")
            speak("Enter destination folder path:")
            dst = input("Destination: ")
            run_in_thread(move_files, src, dst)

        elif "clean downloads" in query:
            path = os.path.join(os.path.expanduser("~"), "Downloads")
            speak("Cleaning Downloads folder...")
            run_in_thread(clean_downloads, path)

        # ---------- Features ----------
        elif "google search" in query or "search on google" in query:
            speak("Searching Google...")
            run_in_thread(GoogleSearch, query)
            

        elif "set alarm" in query:
            speak("Setting alarm...")
            run_in_thread(Alarm, query)

        elif "download video" in query or "download youtube video" in query:
            speak("Downloading video...")
            run_in_thread(DownloadYouTube)

        elif "internet speed" in query or "speed test" in query:
            speak("Running internet speed test...")
            run_in_thread(SpeedTest)

        elif any(x in query for x in ["plus", "minus", "add", "subtract", "multiply", "divide"]):
            run_in_thread(calculator, query)


        # ---------- Exit ----------
        else:

            if 'bye' in query:
                break

            elif 'exit' in query:
                break

            elif 'go' in query:
                break
            
            else:
                speak(ChatterBot(query))


# ========== Entry Point ==========
if __name__ == "__main__":
    main()
