import psutil
import socket
import datetime
from voice.speech_output import speak

def get_battery_status():
    """Reports the current battery percentage."""
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        speak(f"System battery is at {percent} percent.")
    else:
        speak("Battery information is unavailable.")

def get_ip_address():
    """Reports the local IP address."""
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    speak(f"Your local IP address is {ip}")

def get_current_time():
    """Reports the current time."""
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {now}")

def get_current_date():
    """Reports today's date."""
    today = datetime.date.today().strftime("%B %d, %Y")
    speak(f"Today is {today}")
