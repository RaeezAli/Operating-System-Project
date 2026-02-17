import os
import sys

# Ensure the src directory is in the path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from core.command_router import route_command

def test():
    print("--- Testing Chatbot ---")
    route_command("hello")
    
    print("\n--- Testing OS Scheduler ---")
    route_command("add task T1 burst 5")
    route_command("add task T2 burst 3")
    route_command("run scheduler quantum 2")
    
    print("\n--- Testing System Info ---")
    route_command("time")
    route_command("battery")

if __name__ == "__main__":
    test()
