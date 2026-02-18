import sys
import os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
from src.os_simulator.process import Process
from src.os_simulator.scheduling.fcfs import FCFSScheduler
from src.os_simulator.scheduling.round_robin import RoundRobinScheduler
from src.os_simulator.scheduling.priority import PriorityScheduler
from src.os_simulator.comparator import AlgorithmComparator

# Disable verbose logging to keep output clean
logging.basicConfig(level=logging.WARNING)

def run_comparator_demo():
    print(">>> ALGORITHM COMPARISON ENGINE DEMO <<<\n")
    print("Scenarios: FCFS vs Round Robin (Q=2) vs Priority (Non-preemptive)\n")

    # 1. Define Workload
    # Mixture of burst times and priorities
    workload = [
        Process(pid=1, name="P1", arrival_time=0, burst_time=10, priority=3),
        Process(pid=2, name="P2", arrival_time=1, burst_time=4, priority=1), # High priority
        Process(pid=3, name="P3", arrival_time=2, burst_time=6, priority=2),
    ]

    # 2. Setup Schedulers
    schedulers = [
        FCFSScheduler(),
        RoundRobinScheduler(quantum=2),
        PriorityScheduler() # Assumed non-preemptive logic
    ]

    # 3. Run Comparison
    comparator = AlgorithmComparator()
    print("Benchmarking algorithms... (Using CS Overhead = 1)")
    
    comparator.compare(workload, schedulers, context_switch_time=1)

    # 4. Display Results
    comparator.print_comparison_table()
    
    # 5. Export Test
    csv_file = "os_simulator/comparison_results.csv"
    comparator.export_csv(csv_file)
    print(f"Results also exported to: {csv_file}")

if __name__ == "__main__":
    run_comparator_demo()
