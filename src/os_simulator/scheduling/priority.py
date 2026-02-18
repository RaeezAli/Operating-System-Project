from typing import List, Tuple
from .base_scheduler import BaseScheduler
from os_simulator.process import Process

class PriorityScheduler(BaseScheduler):
    """
    Non-Preemptive Priority Scheduling implementation.
    Executes processes based on their priority level (assuming higher value = higher priority).
    """

    def schedule(self, process_list: List[Process]) -> List[Tuple[int, int, int]]:
        """
        Calculates execution timeline using Priority logic.
        """
        if not process_list:
            return []

        # Note: Non-preemptive priority also needs to consider arrival time.
        # We process whatever is available at current_time with highest priority.
        
        remaining = sorted(process_list, key=lambda x: x.arrival_time)
        timeline = []
        current_time = 0
        completed = []

        while remaining:
            # Get processes that have arrived
            available = [p for p in remaining if p.arrival_time <= current_time]
            
            if not available:
                # CPU Idle
                current_time = remaining[0].arrival_time
                continue
            
            # Select highest priority from available
            # (If priorities are equal, FCFS within that group is implicit by initial sort)
            p = max(available, key=lambda x: x.priority)
            
            start = current_time
            current_time += p.burst_time
            
            timeline.append((p.pid, start, current_time))
            p.calculate_metrics(current_time)
            
            remaining.remove(p)
            completed.append(p)

        return timeline

    def calculate_metrics(self, process_list: List[Process]) -> None:
        """
        Calculates metrics for the process list.
        """
        pass