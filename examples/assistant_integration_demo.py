import sys
import os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.assistant import JarvisAssistant

def run_interaction_demo():
    assistant = JarvisAssistant()
    
    queries = [
        "Hello Jarvis!",
        "I want to search for OS simulations.",
        "Can you open the web browser?",
        "Please calculate the value of Pi.",
        "Use round robin scheduling.",
        "Now, run the simulation."
    ]

    print(">>> ASSISTANT INTEGRATION DEMO <<<\n")
    
    for query in queries:
        print(f"USER: {query}")
        response = assistant.process_query(query)
        print(f"JARVIS: {response}\n")

if __name__ == "__main__":
    run_interaction_demo()
