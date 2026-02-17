from typing import List
from .base_scheduler import BaseScheduler, logger
from .models import Process, GanttEntry

class FCFSScheduler(BaseScheduler):
    """
    First-Come, First-Served (FCFS) Scheduling implementation.
    The simplest non-preemptive scheduling algorithm.
    """
    
    def run(self) -> List[GanttEntry]:
        # Reset charts
        self.gantt_chart = []
        
        # Sort by arrival time (FCFS principle)
        sorted_processes = sorted(self.processes, key=lambda x: x.arrival_time)
        
        current_time = 0
        for p in sorted_processes:
            # CPU Idle time handling
            if current_time < p.arrival_time:
                current_time = p.arrival_time
            
            start = current_time
            current_time += p.burst_time
            
            self.gantt_chart.append(GanttEntry(pid=p.pid, start_time=start, end_time=current_time))
            
            # Update process metrics
            p.completion_time = current_time
            logger.info(f"Task completed in simulation: {p.pid}")
            
        self.calculate_metrics()
        return self.gantt_chart