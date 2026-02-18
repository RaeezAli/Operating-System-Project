import sys
import os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
from src.os_simulator.kernel import Kernel
from src.os_simulator.process import Process
from src.os_simulator.scheduling.fcfs import FCFSScheduler
from src.os_simulator.system_clock import SystemClock

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(message)s')

def run_context_switch_demo():
    print(">>> CONTEXT SWITCHING OVERHEAD DEMO <<<\n")
    
    # 1. Define processes
    p1 = Process(pid=1, name="Process A", arrival_time=0, burst_time=5, memory_required=100)
    p2 = Process(pid=2, name="Process B", arrival_time=0, burst_time=5, memory_required=100)
    
    # 2. Setup Kernel with 2 units of context switch overhead
    cs_overhead = 2
    clock = SystemClock()
    kernel = Kernel(context_switch_time=cs_overhead, system_clock=clock)
    kernel.set_scheduler(FCFSScheduler())
    
    kernel.add_process(p1)
    kernel.add_process(p2)
    
    # 3. Run Simulation
    print(f"Running simulation with CS Overhead = {cs_overhead}...")
    timeline = kernel.run()
    
    # 4. Analyze Results
    print("\nExecution Timeline:")
    for entry in timeline:
        pid, start, end = entry
        label = f"PID {pid}" if isinstance(pid, int) else pid
        print(f" {start:02} -> {end:02} : {label}")
        
    print(f"\nFinal Metrics:")
    print(f"Total Simulation Time: {clock.get_time()} units")
    print(f"CPU Busy Time:        {clock.get_busy_time()} units")
    print(f"CPU Idle Time:        {clock.get_idle_time()} units")
    print(f"CPU Utilization:      {clock.get_cpu_utilization()}%")
    
    # Expected: 2 processes * 5 burst + 1 switch = 10 + 2 = 12 total units.
    # Utilization should be 100% since CS is considered 'busy' CPU work in this simulation.
    
    if clock.get_time() == (5 + 5 + cs_overhead):
        print("\nSUCCESS: Context switch overhead correctly applied to timeline.")
    else:
        print("\nFAILURE: Timeline duration does not match expected overhead.")

if __name__ == "__main__":
    run_context_switch_demo()
