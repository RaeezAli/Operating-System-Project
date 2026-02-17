import pyautogui
import os
import time

def send_whatsapp_message(contact_name: str, message: str):
    """
    Sends a WhatsApp message using the desktop application.
    Note: Highly dependent on screen coordinates and application state.
    """
    try:
        # Update this path to the correct WhatsApp shortcut location
        # A common location is %LocalAppData%\WhatsApp\WhatsApp.exe
        whatsapp_path = os.path.join(os.environ.get('APPDATA', ''), "Microsoft\\Windows\\Start Menu\\Programs\\WhatsApp.lnk")
        if os.path.exists(whatsapp_path):
             os.startfile(whatsapp_path)
        else:
            print("[WARNING] WhatsApp shortcut not found at standard path. Trying desktop...")
            desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'WhatsApp.lnk')
            if os.path.exists(desktop_path):
                os.startfile(desktop_path)
            else:
                 print("[ERROR] Could not find WhatsApp shortcut.")
                 return

        time.sleep(5)  # Wait for app to open

        # Search for contact (coordinates may need adjustment)
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyautogui.write(contact_name)
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(1)

        # Type and send message
        pyautogui.write(message)
        pyautogui.press('enter')
        
        print(f"[INFO] Message sent to {contact_name}")
    except Exception as e:
        print(f"[ERROR] WhatsApp automation failed: {e}")

def send_whatsapp_web(contact_phone: str, message: str):
    """Sends a WhatsApp message via pywhatkit (Web-based)."""
    import pywhatkit
    try:
        # Current time + 2 minutes
        hour = time.localtime().tm_hour
        minute = time.localtime().tm_min + 2
        pywhatkit.sendwhatmsg(contact_phone, message, hour, minute)
    except Exception as e:
        print(f"[ERROR] WhatsApp Web failed: {e}")
