import sys
import os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.os_simulator.metrics import MetricsCalculator
from src.os_simulator.process import Process, ProcessState
from src.os_simulator.system_clock import SystemClock

def run_metrics_demo():
    print(">>> METRICS ENGINE DEMO <<<\n")
    
    # 1. Setup Mock Data
    # 3 processes
    p1 = Process(pid=1, name="P1", arrival_time=0, burst_time=5)
    p2 = Process(pid=2, name="P2", arrival_time=1, burst_time=3)
    p3 = Process(pid=3, name="P3", arrival_time=2, burst_time=4)
    
    # Mock completion results (as if FCFS with 1 unit CS overhead)
    # Timeline: 
    # [0-5]  PID 1 (Finish 5)
    # [5-6]  CS
    # [6-9]  PID 2 (Finish 9)
    # [9-10] CS
    # [10-14] PID 3 (Finish 14)
    
    p1.calculate_metrics(5) # TAT=5, WT=0
    p2.calculate_metrics(9) # TAT=8, WT=5
    p3.calculate_metrics(14) # TAT=12, WT=8
    
    procs = [p1, p2, p3]
    timeline = [
        (1, 0, 5),
        ("CS", 5, 6),
        (2, 6, 9),
        ("CS", 9, 10),
        (3, 10, 14)
    ]
    
    clock = SystemClock()
    # 14 ticks, all busy (process or CS)
    for _ in range(14):
        clock.tick(is_busy=True)

    # 2. Run Calculator
    calc = MetricsCalculator()
    calc.calculate(procs, timeline, clock)
    
    # 3. Output
    calc.pretty_print()
    
    # Manual Validation Check
    # Avg WT: (0 + 5 + 8) / 3 = 13 / 3 = 4.33
    # Avg TAT: (5 + 8 + 12) / 3 = 25 / 3 = 8.33
    # Avg RT: P1: 0-0=0, P2: 6-1=5, P3: 10-2=8 -> (0+5+8)/3 = 4.33
    # Throughput: 3 / 14 = 0.2142
    
    print("Manual Validation Check:")
    print(f"Expected Avg WT: ~4.33 | Result: {calc.results['avg_waiting_time']}")
    print(f"Expected Avg TAT: ~8.33 | Result: {calc.results['avg_turnaround_time']}")

if __name__ == "__main__":
    run_metrics_demo()
