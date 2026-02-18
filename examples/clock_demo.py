import sys
import os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.os_simulator.system_clock import SystemClock

# Set up logging for the demo
logging.basicConfig(level=logging.INFO, format='%(name)s - %(message)s')

def run_clock_demo():
    print(">>> SYSTEM CLOCK & CPU UTILIZATION DEMO <<<\n")
    
    # 1. Initialize Clock
    clock = SystemClock()
    
    # 2. Simulate CPU activity
    print("Simulating CPU activity...")
    # 5 units of busy work
    for _ in range(5):
        clock.tick(is_busy=True)
    
    # 3 units of idle time
    for _ in range(3):
        clock.tick(is_busy=False)
        
    # 2 more units of busy work
    for _ in range(2):
        clock.tick(is_busy=True)

    # 3. Report Metrics
    print("\nSimulation Metrics:")
    print(f"Total Time:      {clock.get_time()} units")
    print(f"Busy Time:       {clock.get_busy_time()} units")
    print(f"Idle Time:       {clock.get_idle_time()} units")
    print(f"CPU Utilization: {clock.get_cpu_utilization()}%")
    
    print(f"\nString representation: {clock}")

    # 4. Reset and verify
    print("\nResetting clock...")
    clock.reset()
    print(f"Time after reset: {clock.get_time()}")
    print(f"Utilization after reset: {clock.get_cpu_utilization()}%")

if __name__ == "__main__":
    run_clock_demo()
