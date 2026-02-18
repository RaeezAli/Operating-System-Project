from typing import List, Tuple
from .base_scheduler import BaseScheduler
from os_simulator.process import Process

class FCFSScheduler(BaseScheduler):
    """
    First-Come, First-Served (FCFS) Scheduling implementation.
    A non-preemptive algorithm where processes are executed in the order of their arrival.
    """

    def schedule(self, process_list: List[Process]) -> List[Tuple[int, int, int]]:
        """
        Calculates execution timeline using FCFS logic.
        """
        if not process_list:
            return []

        # Sort by arrival time
        sorted_processes = sorted(process_list, key=lambda x: x.arrival_time)
        timeline = []
        current_time = 0

        for p in sorted_processes:
            # CPU Idle time handling
            if current_time < p.arrival_time:
                current_time = p.arrival_time
            
            start = current_time
            current_time += p.burst_time
            
            timeline.append((p.pid, start, current_time))
            
            # Update process metadata
            p.calculate_metrics(current_time)

        return timeline

    def calculate_metrics(self, process_list: List[Process]) -> None:
        """
        Metrics are already calculated during the schedule() phase for non-preemptive FCFS.
        This method is kept for interface compliance.
        """
        pass