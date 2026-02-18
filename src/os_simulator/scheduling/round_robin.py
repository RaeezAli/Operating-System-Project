from typing import List, Tuple, Deque
from collections import deque
from .base_scheduler import BaseScheduler
from os_simulator.process import Process

class RoundRobinScheduler(BaseScheduler):
    """
    Round Robin (RR) Scheduling implementation.
    A preemptive algorithm using a fixed time quantum.
    """

    def __init__(self, quantum: int = 2):
        """
        Initializes RR with a time quantum.
        """
        self.quantum = quantum

    def schedule(self, process_list: List[Process]) -> List[Tuple[int, int, int]]:
        """
        Calculates execution timeline using RR logic with time quantum.
        """
        if not process_list:
            return []

        timeline = []
        # Sort by arrival initially
        arrival_queue: Deque[Process] = deque(sorted(process_list, key=lambda x: x.arrival_time))
        ready_queue: Deque[Process] = deque()
        
        current_time = 0
        completed_count = 0
        n = len(process_list)

        while completed_count < n:
            # Add arriving processes to ready queue
            while arrival_queue and arrival_queue[0].arrival_time <= current_time:
                ready_queue.append(arrival_queue.popleft())

            if not ready_queue:
                if arrival_queue:
                    current_time = arrival_queue[0].arrival_time
                    continue
                else:
                    break

            p = ready_queue.popleft()
            exec_time = min(p.remaining_time, self.quantum)
            
            start = current_time
            current_time += exec_time
            p.remaining_time -= exec_time
            
            timeline.append((p.pid, start, current_time))

            # Add processes that arrive DURING this execution segment
            while arrival_queue and arrival_queue[0].arrival_time <= current_time:
                ready_queue.append(arrival_queue.popleft())

            if p.remaining_time > 0:
                ready_queue.append(p)
            else:
                p.calculate_metrics(current_time)
                completed_count += 1

        return timeline

    def calculate_metrics(self, process_list: List[Process]) -> None:
        """
        Metrics (TAT, WT) are derived automatically when process finishes in schedule().
        """
        pass
