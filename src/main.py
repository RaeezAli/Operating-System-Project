import os
import sys
import argparse
import logging
import copy
from typing import List

# Ensure the project root is in the path for modular 'src' imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.voice.speech_input import take_command
from src.voice.speech_output import speak
from src.core.command_router import route_command
from src.os_simulator.kernel import Kernel
from src.os_simulator.process import Process
from src.os_simulator.metrics import MetricsCalculator
from src.os_simulator.comparator import AlgorithmComparator
from src.os_simulator.scheduling.fcfs import FCFSScheduler
from src.os_simulator.scheduling.round_robin import RoundRobinScheduler
from src.os_simulator.scheduling.priority import PriorityScheduler

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("OS-CLI")

def parse_processes(process_str: str) -> List[Process]:
    """Parses processes from string format 'Name:Arrival:Burst:Priority'"""
    procs = []
    try:
        segments = process_str.split(',')
        for i, seg in enumerate(segments):
            parts = seg.split(':')
            name = parts[0]
            arrival = int(parts[1])
            burst = int(parts[2])
            priority = int(parts[3]) if len(parts) > 3 else 0
            procs.append(Process(pid=i+1, name=name, arrival_time=arrival, burst_time=burst, priority=priority))
    except Exception as e:
        logger.error(f"Failed to parse processes: {e}. Format should be 'Name:Arrival:Burst:Priority,...'")
        sys.exit(1)
    return procs

def run_scheduler_cli(args):
    """Handles --mode scheduler"""
    if not args.processes:
        logger.error('Error: --processes "Name:Arrival:Burst:Priority,..." is required for scheduler mode.')
        return

    procs = parse_processes(args.processes)
    
    scheduler = None
    if args.algorithm == 'fcfs':
        scheduler = FCFSScheduler()
    elif args.algorithm == 'rr':
        scheduler = RoundRobinScheduler(quantum=args.quantum)
    elif args.algorithm == 'priority':
        scheduler = PriorityScheduler()
    else:
        logger.error(f"Unsupported algorithm: {args.algorithm}")
        return

    kernel = Kernel(context_switch_time=args.context_switch)
    kernel.set_scheduler(scheduler)
    for p in procs:
        kernel.add_process(p)

    logger.info(f"Running simulation with {args.algorithm.upper()}...")
    timeline = kernel.run()
    
    calc = MetricsCalculator()
    calc.calculate(procs, timeline, kernel.system_clock)
    calc.pretty_print()

def run_compare_cli(args):
    """Handles --mode compare"""
    # Use default workload if none provided
    if args.processes:
        workload = parse_processes(args.processes)
    else:
        logger.info("Using default benchmark workload...")
        workload = [
            Process(1, "P1", 0, 10, 3),
            Process(2, "P2", 1, 4, 1),
            Process(3, "P3", 2, 6, 2)
        ]

    schedulers = [FCFSScheduler(), RoundRobinScheduler(quantum=args.quantum), PriorityScheduler()]
    comparator = AlgorithmComparator()
    comparator.compare(workload, schedulers, context_switch_time=args.context_switch)
    comparator.print_comparison_table()

def run_memory_cli(args):
    """Handles --mode memory (Paging and Segmentation)"""
    from src.os_simulator.memory_management.paging import PagingMemoryManager
    from src.os_simulator.memory_management.segmentation import SegmentationMemoryManager
    
    if args.algorithm == "segmentation":
        logger.info("Running Segmentation Memory Management Demo...")
        mmu = SegmentationMemoryManager(total_memory=65536)
        mmu.allocate(1, [1000, 2000, 500])
        print("\nSegmentation Status (PID 1):")
        print(mmu.get_status(1))
    else:
        logger.info("Running Paging Memory Management Demo...")
        mm = PagingMemoryManager(total_memory=1024, frame_size=256)
        mm.allocate(1, 400) # Allocate 2 pages
        mm.allocate(2, 200) # Allocate 1 page
        print("\nMemory Management Status:")
        import json
        print(json.dumps(mm.get_status(), indent=2))

def run_deadlock_cli(args):
    """Handles --mode deadlock (Banker's Algorithm and Detection)"""
    from src.os_simulator.deadlock.bankers_algorithm import BankersAlgorithm
    from src.os_simulator.deadlock.deadlock_detection import detect_deadlock
    
    if args.algorithm == "detection":
        logger.info("Running Deadlock Detection (Wait-For Graph)...")
        allocation = {0: [1, 0], 1: [0, 1]}
        request = {0: [0, 1], 1: [1, 0]}
        deadlocked = detect_deadlock(allocation, request)
        print(f"Deadlocked Processes: {deadlocked}")
    else:
        logger.info("Running Deadlock Avoidance (Banker's Algorithm)...")
        banker = BankersAlgorithm([10, 5, 7])
        banker.add_process(0, [7, 5, 3])
        banker.request_resources(0, [0, 1, 0])
        is_safe, sequence = banker.safe_state_check()
        print(f"Is system safe? {is_safe}. Sequence: {sequence}")

def interactive_mode():
    """Fallback interactive loop (AI Assistant mode)"""
    speak("Jarvis is online. How can I assist you today?")
    while True:
        try:
            query = input("Type your command or press Enter to speak (type 'exit' to quit): ").lower().strip()
            if not query:
                query = take_command()
            if not query:
                continue
            if query in ["exit", "quit", "bye"]:
                speak("Shutting down the Jarvis OS Simulator. Goodbye!")
                break
            route_command(query)
        except KeyboardInterrupt:
            speak("Emergency shutdown initiated. Goodbye!")
            break
        except Exception as e:
            print(f"[FATAL ERROR] {e}")

def main():
    parser = argparse.ArgumentParser(description="Jarvis OS Simulator CLI")
    parser.add_argument("--mode", choices=["scheduler", "memory", "deadlock", "compare"], help="Simulation mode")
    parser.add_argument("--algorithm", help="Algorithm (e.g., fcfs, rr, priority, segmentation, detection)")
    parser.add_argument("--quantum", type=int, default=2, help="Time quantum for Round Robin")
    parser.add_argument("--context_switch", type=int, default=0, help="Context switch overhead units")
    parser.add_argument("--processes", help="Processes in format 'Name:Arrival:Burst:Priority,...'")

    args = parser.parse_args()

    if args.mode:
        if args.mode == "scheduler":
            run_scheduler_cli(args)
        elif args.mode == "compare":
            run_compare_cli(args)
        elif args.mode == "memory":
            run_memory_cli(args)
        elif args.mode == "deadlock":
            run_deadlock_cli(args)
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
