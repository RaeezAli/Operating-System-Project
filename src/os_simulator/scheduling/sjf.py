from typing import List
from .base_scheduler import BaseScheduler, logger
from .models import Process, GanttEntry

class SJFScheduler(BaseScheduler):
    """
    Shortest Job First (SJF) Scheduling implementation.
    Non-preemptive algorithm that selects the process with the smallest burst time.
    """
    
    def run(self) -> List[GanttEntry]:
        self.gantt_chart = []
        if not self.processes:
            return []

        # We'll use a copy to avoid mutating the original arrival order during selection
        ready_queue = []
        incoming = sorted(self.processes, key=lambda x: x.arrival_time)
        
        current_time = 0
        completed_count = 0
        n = len(self.processes)

        while completed_count < n:
            # Handle new arrivals
            while incoming and incoming[0].arrival_time <= current_time:
                ready_queue.append(incoming.pop(0))

            if not ready_queue:
                if incoming:
                    current_time = incoming[0].arrival_time
                    continue
                else: break

            # SJF Logic: Sort ready queue by burst time
            ready_queue.sort(key=lambda x: x.burst_time)
            p = ready_queue.pop(0)

            start = current_time
            current_time += p.burst_time
            
            self.gantt_chart.append(GanttEntry(pid=p.pid, start_time=start, end_time=current_time))
            p.completion_time = current_time
            completed_count += 1
            logger.info(f"Task completed in simulation: {p.pid}")

        self.calculate_metrics()
        return self.gantt_chart