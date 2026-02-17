try:
    from voice.speech_input import take_command
    from voice.speech_output import speak
    from core.command_router import route_command
    print("Core modules imported successfully.")
except Exception as e:
    print(f"Import failed: {e}")
