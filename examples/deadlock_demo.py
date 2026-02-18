import sys
import os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.os_simulator.deadlock.bankers_algorithm import BankersAlgorithm

def run_bankers_demo():
    print(">>> BANKER'S ALGORITHM DEMO <<<\n")
    
    # 1. Initialize with total resources (e.g., 10 A, 5 B, 7 C)
    total_resources = [10, 5, 7]
    banker = BankersAlgorithm(total_resources)
    
    # 2. Add processes with their Max demands
    # Format: pid, [MaxA, MaxB, MaxC]
    banker.add_process(0, [7, 5, 3])
    banker.add_process(1, [3, 2, 2])
    banker.add_process(2, [9, 0, 2])
    banker.add_process(3, [2, 2, 2])
    banker.add_process(4, [4, 3, 3])
    
    # 3. Initial Allocations (Start state)
    # Simulation: grantor requests for each process to set initial state
    banker.request_resources(0, [0, 1, 0])
    banker.request_resources(1, [2, 0, 0])
    banker.request_resources(2, [3, 0, 2])
    banker.request_resources(3, [2, 1, 1])
    banker.request_resources(4, [0, 0, 2])
    
    print(f"\nInitial Available: {banker.available}")
    
    # 4. Perform a safety check
    is_safe, sequence = banker.safe_state_check()
    print(f"\nIs system in a safe state? {is_safe}")
    if is_safe:
        print(f"Safe sequence found: {sequence}")

    # 5. Request resources (The classic P1 request: [1, 0, 2])
    print("\n--- Process 1 requests [1, 0, 2] ---")
    if banker.request_resources(1, [1, 0, 2]):
        print("RESULT: Request Granted.")
    else:
        print("RESULT: Request Denied (Unsafe State).")

    # 6. Request that leads to unsafe state
    print("\n--- Process 0 requests [3, 3, 0] ---")
    if banker.request_resources(0, [3, 3, 0]):
        print("RESULT: Request Granted.")
    else:
        print("RESULT: Request Denied (Unsafe State).")

    # 7. Release resources
    print("\n--- Process 2 releases all resources ---")
    banker.release_resources(2, [3, 0, 2])
    print(f"Available after release: {banker.available}")
    
    m = banker.get_matrices()
    print(f"\nCurrent Need Matrix for remaining processes:")
    for pid, need in m['need'].items():
        print(f" PID {pid}: {need}")

if __name__ == "__main__":
    run_bankers_demo()
