import random
import logging
from typing import List, Tuple, Dict, Any
from os_simulator.kernel import Kernel
from os_simulator.process import Process
from os_simulator.scheduling.fcfs import FCFSScheduler
from os_simulator.scheduling.round_robin import RoundRobinScheduler
from os_simulator.scheduling.priority import PriorityScheduler

# Reuse the kernel logger or create a specific one
logger = logging.getLogger("Jarvis-Assistant")

class JarvisAssistant:
    """
    Simulated OS Shell and Assistant.
    
    Transforms user natural language commands into OS processes and manages
    the simulated execution flow via the OS Kernel.
    """

    def __init__(self):
        self.kernel = Kernel()
        self.next_pid = 1000
        
        # Mapping command keywords to simulated process resource requirements
        # Format: "keyword": (burst_time, memory_required, base_priority)
        self.command_resource_map: Dict[str, Tuple[int, int, int]] = {
            "search": (5, 512, 1),
            "open": (2, 256, 3),
            "calculate": (4, 128, 2),
            "whatsapp": (3, 640, 4),
            "clean": (6, 1024, 1),
            "play": (8, 2048, 5)
        }

        self.conversations = {
            "hello": ["Hello Sir, I am Jarvis.", "Greetings! How can I assist you?", "Hello! Ready for tasks."],
            "bye": ["Goodbye Sir.", "Powering down. Have a nice day.", "See you later!"],
            "how are you": ["I am functioning within normal parameters.", "Excellent as always!", "Ready to help."],
            "thanks": ["You're very welcome, Sir.", "My pleasure.", "Don't mention it."]
        }
        self.sorry_responses = ["I'm sorry, that is beyond my current abilities.", "I couldn't quite grasp that command."]

    def process_query(self, text: str) -> str:
        """
        Parses user query to determine action: add process, change scheduler, or run.
        """
        text = text.lower()

        # 1. Check for Scheduler switches
        if "round robin" in text:
            self.kernel.set_scheduler(RoundRobinScheduler(quantum=2))
            return "Scheduler switched to Round Robin (Quantum=2)."
        elif "priority" in text:
            self.kernel.set_scheduler(PriorityScheduler())
            return "Scheduler switched to Priority-based scheduling."
        elif "fcfs" in text or "first come" in text:
            self.kernel.set_scheduler(FCFSScheduler())
            return "Scheduler switched to First-Come, First-Served."

        # 2. Check for Execution command
        if "run" in text or "execute" in text or "start simulation" in text:
            if not self.kernel.process_table:
                return "There are no processes in the table. Please add some tasks first."
            
            timeline = self.kernel.run()
            return self._format_execution_summary(timeline)

        # 3. Check for Task commands (Automation keywords)
        for keyword, resources in self.command_resource_map.items():
            if keyword in text:
                p = self._create_process_from_keyword(keyword, resources)
                self.kernel.add_process(p)
                return f"Task '{keyword}' added to the kernel process table (PID: {p.pid})."

        # 4. Check for Conversational response
        for key, responses in self.conversations.items():
            if key in text:
                return random.choice(responses)

        return random.choice(self.sorry_responses)

    def _create_process_from_keyword(self, keyword: str, resources: Tuple[int, int, int]) -> Process:
        """Helper to create a Process object from resource mapping."""
        burst, mem, priority = resources
        p = Process(
            pid=self.next_pid,
            name=keyword.capitalize(),
            arrival_time=0,  # For simplicity, assumed to arrive now
            burst_time=burst,
            priority=priority,
            memory_required=mem
        )
        self.next_pid += 1
        return p

    def _format_execution_summary(self, timeline: List[Tuple[Any, int, int]]) -> str:
        """Formatted summary of the kernel execution."""
        if not timeline:
            return "Execution failed or produced no results."

        summary = ["\n[OS KERNEL EXECUTION COMPLETE]", "-" * 30]
        summary.append(f"Scheduler: {type(self.kernel.scheduler).__name__}")
        summary.append("\nExecution Timeline (PID: Start -> End):")
        
        for pid, start, end in timeline:
            summary.append(f" - {pid}: {start:02d} -> {end:02d}")

        summary.append("\nPerformance Metrics:")
        summary.append(f"{'PID':<6} | {'TAT':<5} | {'WT':<5}")
        for p in self.kernel.process_table:
            summary.append(f"{p.pid:<6} | {p.turnaround_time:<5} | {p.waiting_time:<5}")
        
        summary.append("-" * 30)
        return "\n".join(summary)

    def get_response(self, text: str) -> str:
        """Alias for process_query for legacy compatibility with command_router."""
        return self.process_query(text)
