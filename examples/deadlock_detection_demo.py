import sys
import os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
from src.os_simulator.deadlock.deadlock_detection import detect_deadlock

# Configure logging to see the construction of WFG
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def run_detection_demo():
    print(">>> DEADLOCK DETECTION (WAIT-FOR GRAPH) DEMO <<<\n")
    
    # --- Scenario 1: No Deadlock ---
    print("Scenario 1: Safe state (Chain reaction, no cycles)")
    # P0 holds R0, needs R1
    # P1 holds R1, needs R2
    # P2 holds R2, needs nothing
    allocation1 = {
        0: [1, 0, 0],
        1: [0, 1, 0],
        2: [0, 0, 1]
    }
    request1 = {
        0: [0, 1, 0],
        1: [0, 0, 1],
        2: [0, 0, 0]
    }
    
    deadlocked1 = detect_deadlock(allocation1, request1)
    print(f"Deadlocked Processes: {deadlocked1}\n")

    # --- Scenario 2: Simple Deadlock (P0 <-> P1) ---
    print("Scenario 2: Circular wait (P0 holds R0/wants R1, P1 holds R1/wants R0)")
    allocation2 = {
        0: [1, 0],
        1: [0, 1]
    }
    request2 = {
        0: [0, 1],
        1: [1, 0]
    }
    
    deadlocked2 = detect_deadlock(allocation2, request2)
    print(f"Deadlocked Processes: {deadlocked2}\n")

    # --- Scenario 3: Complex Deadlock (P0 -> P1 -> P2 -> P0) ---
    print("Scenario 3: Multi-node circular wait")
    allocation3 = {
        0: [1, 0, 0],
        1: [0, 1, 0],
        2: [0, 0, 1]
    }
    request3 = {
        0: [0, 1, 0],
        1: [0, 0, 1],
        2: [1, 0, 0]
    }
    
    deadlocked3 = detect_deadlock(allocation3, request3)
    print(f"Deadlocked Processes: {deadlocked3}\n")

if __name__ == "__main__":
    run_detection_demo()
