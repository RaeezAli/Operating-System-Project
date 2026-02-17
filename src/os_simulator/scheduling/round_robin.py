from typing import List, Deque
from collections import deque
from .base_scheduler import BaseScheduler, logger
from .models import Process, GanttEntry

class RoundRobinScheduler(BaseScheduler):
    """
    Round Robin (RR) Scheduling implementation.
    Preemptive algorithm utilizing a time quantum.
    """
    
    def __init__(self, quantum: int = 2):
        super().__init__()
        self.quantum = quantum

    def run(self) -> List[GanttEntry]:
        self.gantt_chart = []
        if not self.processes:
            return []

        # Sort by arrival time initially
        queue: Deque[Process] = deque(sorted(self.processes, key=lambda x: x.arrival_time))
        ready_queue: Deque[Process] = deque()
        
        current_time = 0
        completed_count = 0
        n = len(self.processes)

        # Basic RR Loop
        while completed_count < n:
            # Add arriving processes to ready queue
            while queue and queue[0].arrival_time <= current_time:
                ready_queue.append(queue.popleft())

            if not ready_queue:
                if queue:
                    current_time = queue[0].arrival_time
                    continue
                else:
                    break

            p = ready_queue.popleft()
            exec_time = min(p.remaining_time, self.quantum)
            
            self.gantt_chart.append(GanttEntry(pid=p.pid, start_time=current_time, end_time=current_time + exec_time))
            
            current_time += exec_time
            p.remaining_time -= exec_time

            # Check for new arrivals during execution
            while queue and queue[0].arrival_time <= current_time:
                ready_queue.append(queue.popleft())

            if p.remaining_time > 0:
                ready_queue.append(p)
            else:
                p.completion_time = current_time
                completed_count += 1
                logger.info(f"Task completed in simulation: {p.pid}")

        self.calculate_metrics()
        return self.gantt_chart
