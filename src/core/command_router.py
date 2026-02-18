import os
import sys
import re

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.automation.web_search import google_search, play_on_youtube, open_url
from src.automation.system_monitor import get_battery_status, get_ip_address, get_current_time, get_current_date
from src.automation.file_manager import move_file, clean_downloads
from src.automation.whatsapp import send_whatsapp_message
from src.os_simulator.process import Process
from src.os_simulator.scheduling.fcfs import FCFSScheduler
from src.os_simulator.scheduling.round_robin import RoundRobinScheduler
from src.os_simulator.scheduling.priority import PriorityScheduler
from src.os_simulator.scheduling.models import GanttEntry
from src.os_simulator.kernel import Kernel
from src.os_simulator.metrics import MetricsCalculator
from src.os_simulator.comparator import AlgorithmComparator
from src.utils.visualizer import SchedulerVisualizer
from src.utils.logger import logger
from src.apis.wolfram import query_wolfram
from src.voice.speech_output import speak
from src.core.assistant import JarvisAssistant

assistant = JarvisAssistant()
pending_processes = []
last_metrics = None
current_page_algo = "fifo"

def word_to_int(text):
    """Converts common word-numbers to integers."""
    mapping = {
        "zero": 0, "one": 1, "two": 2, "to": 2, "too": 2, "three": 3, 
        "four": 4, "for": 4, "five": 5, "six": 6, "seven": 7, 
        "eight": 8, "nine": 9, "ten": 10
    }
    text = text.lower().strip()
    if text.isdigit():
        return int(text)
    return mapping.get(text, None)

def route_command(query):
    global pending_processes, last_metrics, current_page_algo
    query = query.lower()

    # --- OS Simulator: Scheduling ---
    if "add task" in query:
        try:
            match = re.search(r"add task ([\w\d]+) burst ([\w\d]+)", query)
            if not match:
                raise ValueError("Missing PID or burst")
            
            pid_raw = match.group(1)
            burst_raw = match.group(2)
            
            pid = word_to_int(pid_raw)
            burst = word_to_int(burst_raw)
            
            if pid is None or burst is None:
                raise ValueError(f"Could not parse PID '{pid_raw}' or Burst '{burst_raw}'")

            arrival = 0
            arr_match = re.search(r"arrival ([\w\d]+)", query)
            if arr_match:
                arrival = word_to_int(arr_match.group(1)) or 0
                
            priority = 0
            prio_match = re.search(r"priority ([\w\d]+)", query)
            if prio_match:
                priority = word_to_int(prio_match.group(1)) or 0
            
            p = Process(pid=pid, name=f"P{pid}", arrival_time=arrival, burst_time=burst, priority=priority)
            pending_processes.append(p)
            speak(f"Process {pid} added to queue.")
            logger.info(f"Process added: {pid} (Burst: {burst}, Arrival: {arrival}, Priority: {priority})")
        except Exception as e:
            speak("Invalid format. Please specify PID and burst time clearly.")
            logger.error(f"Failed to add process: {e}")

    elif "remove task" in query:
        try:
            parts = query.split()
            pid_raw = parts[-1]
            pid = word_to_int(pid_raw)
            if pid is None:
                raise ValueError("Could not parse PID")
            
            original_len = len(pending_processes)
            pending_processes = [p for p in pending_processes if p.pid != pid]
            
            if len(pending_processes) < original_len:
                speak(f"Process {pid} removed from queue.")
            else:
                speak(f"Process {pid} not found in queue.")
        except:
            speak("Please specify which PID to remove.")

    elif "list task" in query or "show task" in query:
        if not pending_processes:
            speak("The process queue is currently empty.")
        else:
            speak(f"There are {len(pending_processes)} tasks in the queue.")
            print("\n--- Current Process Queue ---")
            for p in pending_processes:
                print(f"PID: {p.pid}, Burst: {p.burst_time}, Arrival: {p.arrival_time}, Priority: {p.priority}")
            print("----------------------------\n")

    elif "reset simulation" in query:
        pending_processes = []
        last_metrics = None
        speak("Simulation reset. Process queue cleared.")

    elif "show metrics" in query:
        if last_metrics:
            speak("Displaying last calculated metrics.")
            last_metrics.pretty_print()
        else:
            speak("No metrics available. Please run a simulation first.")

    elif "run scheduler" in query or "simulate scheduler" in query:
        if not pending_processes:
            speak("No processes in queue. Add tasks first.")
            return

        try:
            if "round robin" in query or "rr" in query:
                quantum = 2
                q_match = re.search(r"quantum (\d+)", query)
                if q_match:
                    quantum = int(q_match.group(1))
                scheduler = RoundRobinScheduler(quantum=quantum)
                title = f"Round Robin (q={quantum})"
            elif "priority" in query:
                scheduler = PriorityScheduler()
                title = "Priority Scheduling"
            else:
                scheduler = FCFSScheduler()
                title = "FCFS Scheduling"

            kernel = Kernel()
            kernel.set_scheduler(scheduler)
            for p in pending_processes:
                kernel.add_process(p)
            
            speak(f"Running {title} simulation.")
            timeline = kernel.run()
            
            last_metrics = MetricsCalculator()
            last_metrics.calculate(pending_processes, timeline, kernel.system_clock)
            last_metrics.pretty_print()
            
            gantt_entries = [GanttEntry(pid=str(p[0]), start_time=p[1], end_time=p[2]) for p in timeline]
            SchedulerVisualizer.plot_gantt(gantt_entries, title=title)
        except Exception as e:
            logger.error(f"Scheduler failed: {e}")
            speak("I encountered an error running the scheduler.")

    elif "compare scheduler" in query or "comparison" in query:
        speak("Comparing FCFS, Round Robin, and Priority algorithms.")
        workload = pending_processes if pending_processes else [
            Process(1, "P1", 0, 10, 3), Process(2, "P2", 2, 5, 1), Process(3, "P3", 4, 8, 2)
        ]
        schedulers = [FCFSScheduler(), RoundRobinScheduler(quantum=2), PriorityScheduler()]
        comparator = AlgorithmComparator()
        comparator.compare(workload, schedulers)
        comparator.print_comparison_table()
        speak("Comparison complete. Check the console for the table.")

    # --- Deadlock ---
    elif "banker" in query or "safe state" in query:
        from src.os_simulator.deadlock.bankers_algorithm import BankersAlgorithm
        speak("Running Banker's Algorithm for safe state discovery.")
        banker = BankersAlgorithm([10, 5, 7])
        banker.add_process(0, [7, 5, 3])
        banker.add_process(1, [3, 2, 2])
        banker.request_resources(0, [0, 1, 0])
        banker.request_resources(1, [2, 0, 0])
        safe, seq = banker.safe_state_check()
        res = "System is in a SAFE state." if safe else "System is in an UNSAFE state."
        speak(res)
        print(f"Safety Sequence: {seq}")

    elif "detect deadlock" in query:
        from src.os_simulator.deadlock.deadlock_detection import detect_deadlock
        speak("Analyzing resource allocation for deadlocks.")
        allocation = {0: [1, 0], 1: [0, 1]}
        request = {0: [0, 1], 1: [1, 0]}
        deadlocks = detect_deadlock(allocation, request)
        if deadlocks:
            speak(f"Deadlock detected involving processes: {deadlocks}")
        else:
            speak("No deadlocks detected.")

    # --- Memory ---
    elif "simulate paging" in query:
        from src.os_simulator.memory_management.page_replacement import fifo_replacement, lru_replacement, optimal_replacement
        try:
            frames = 3
            f_match = re.search(r"frames (\d+)", query)
            if f_match: frames = int(f_match.group(1))
            
            ref_str = [7, 0, 1, 2, 0, 3, 0, 4] # Default
            if "reference" in query:
                ref_part = query.split("reference")[-1].strip()
                ref_str = [int(x) for x in re.findall(r"\d+", ref_part)]
            
            speak(f"Simulating {current_page_algo.upper()} page replacement with {frames} frames.")
            if current_page_algo == "fifo": res = fifo_replacement(ref_str, frames)
            elif current_page_algo == "lru": res = lru_replacement(ref_str, frames)
            else: res = optimal_replacement(ref_str, frames)
            
            print(f"\n--- Page Replacement Results ({current_page_algo.upper()}) ---")
            print(f"Reference String: {ref_str}")
            print(f"Frames: {frames}")
            print(f"Page Faults: {res['page_faults']}")
            print(f"Page Hits: {res['page_hits']}")
            print(f"Fault Ratio: {res['fault_ratio']}")
            print("------------------------------------------\n")
            speak(f"Simulation complete. {res['page_faults']} page faults occurred.")
        except Exception as e:
            speak("I had trouble parsing the paging parameters.")

    elif "set page algorithm" in query:
        if "fifo" in query: current_page_algo = "fifo"
        elif "lru" in query: current_page_algo = "lru"
        elif "optimal" in query: current_page_algo = "optimal"
        speak(f"Page replacement algorithm set to {current_page_algo.upper()}.")

    elif "run paging" in query: # Simple demo
        from src.os_simulator.memory_management.paging import PagingMemoryManager
        speak("Simulating Paging Memory Management.")
        pm = PagingMemoryManager(1024, 256)
        pm.allocate(1, 400)
        print(pm.get_status())
        speak("Paging simulation complete.")

    elif "segmentation" in query:
        from src.os_simulator.memory_management.segmentation import SegmentationMemoryManager
        speak("Simulating Memory Segmentation.")
        sm = SegmentationMemoryManager(65536)
        sm.allocate(1, [1000, 2000])
        print(sm.get_status(1))
        speak("Segmentation simulation complete.")

    # --- Process Sync ---
    elif "producer consumer" in query:
        from src.os_simulator.process_sync.producer_consumer import run_producer_consumer_demo
        speak("Running Producer-Consumer synchronization demo.")
        run_producer_consumer_demo()

    elif "philosopher" in query:
        from src.os_simulator.process_sync.dining_philosophers import run_dining_demo
        speak("Running Dining Philosophers deadlock avoidance demo.")
        run_dining_demo()

    # --- Automation Commands ---
    elif "open" in query:
        if "notepad" in query: os.system("notepad")
        elif "calculator" in query: os.system("calc")
        elif "google" in query: open_url("https://google.com")
        else: speak("I'm not sure which app you want to open.")

    elif "search" in query:
        target = query.replace("search", "").strip()
        google_search(target)
    
    elif "play" in query:
        target = query.replace("play", "").strip()
        play_on_youtube(target)

    # --- System Info ---
    elif query == "battery" or "check battery" in query: get_battery_status()
    elif query == "ip" or "my ip" in query or "ip address" in query: get_ip_address()
    elif "time" in query: get_current_time()
    elif "date" in query: get_current_date()

    # --- File/Calculations ---
    elif "clean" in query: clean_downloads()
    elif "calculate" in query:
        expr = query.replace("calculate", "").replace("x", "*").strip()
        res = query_wolfram(expr)
        speak(f"The result is {res}")

    # --- Fallback ---
    else:
        response = assistant.get_response(query)
        speak(response)
