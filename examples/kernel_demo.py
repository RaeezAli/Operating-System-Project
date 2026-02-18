import sys
import os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.os_simulator.kernel import Kernel
from src.os_simulator.process import Process
from src.os_simulator.scheduling.fcfs import FCFSScheduler
from src.os_simulator.scheduling.round_robin import RoundRobinScheduler
from src.os_simulator.scheduling.priority import PriorityScheduler

def print_metrics(kernel: Kernel, algorithm_name: str):
    print(f"\n--- Process Metrics after {algorithm_name} ---")
    print(f"{'PID':<5} | {'Name':<10} | {'Arrival':<8} | {'Burst':<6} | {'TAT':<5} | {'WT':<5}")
    print("-" * 55)
    for p in kernel.process_table:
        print(f"{p.pid:<5} | {p.name:<10} | {p.arrival_time:<8} | {p.burst_time:<6} | {p.turnaround_time:<5} | {p.waiting_time:<5}")

def run_upgraded_demo():
    # 1. Initialize Kernel
    kernel = Kernel()
    
    # 2. Add some processes
    kernel.add_process(Process(pid=1, name="Process A", arrival_time=0, burst_time=5, priority=1))
    kernel.add_process(Process(pid=2, name="Process B", arrival_time=2, burst_time=3, priority=5))
    kernel.add_process(Process(pid=3, name="Process C", arrival_time=4, burst_time=1, priority=10))
    
    # --- Scenario 1: FCFS ---
    print("\n" + "="*60)
    print(">>> Scenario 1: FCFS Scheduling (Non-Preemptive)")
    kernel.set_scheduler(FCFSScheduler())
    timeline = kernel.run()
    
    print("\nExecution Timeline:")
    for pid, start, end in timeline:
        print(f"Time {start:02d}-{end:02d}: Process {pid}")
    print_metrics(kernel, "FCFS")
    
    # --- Scenario 2: Priority ---
    print("\n" + "="*60)
    print(">>> Scenario 2: Priority Scheduling (Non-Preemptive)")
    kernel.reset()
    kernel.set_scheduler(PriorityScheduler())
    timeline = kernel.run()
    
    print("\nExecution Timeline:")
    for pid, start, end in timeline:
        print(f"Time {start:02d}-{end:02d}: Process {pid}")
    print_metrics(kernel, "Priority")
    
    # --- Scenario 3: Round Robin ---
    print("\n" + "="*60)
    print(">>> Scenario 3: Round Robin Scheduling (Quantum=2)")
    kernel.reset()
    kernel.set_scheduler(RoundRobinScheduler(quantum=2))
    timeline = kernel.run()
    
    print("\nExecution Timeline:")
    for pid, start, end in timeline:
        print(f"Time {start:02d}-{end:02d}: Process {pid}")
    print_metrics(kernel, "Round Robin")

if __name__ == "__main__":
    run_upgraded_demo()
