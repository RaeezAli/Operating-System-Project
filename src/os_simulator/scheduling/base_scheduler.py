from abc import ABC, abstractmethod
from typing import List, Tuple
from .models import Process, GanttEntry
from utils.logger import logger

class BaseScheduler(ABC):
    """
    Abstract Base Class for all Scheduling Algorithms.
    Follows the Strategy Pattern to allow extendable algorithms.
    """
    
    def __init__(self):
        self.processes: List[Process] = []
        self.gantt_chart: List[GanttEntry] = []

    def add_process(self, process: Process):
        """Adds a process to the scheduling queue."""
        self.processes.append(process)

    @abstractmethod
    def run(self) -> List[GanttEntry]:
        """
        Executes the scheduling algorithm.
        Must be implemented by concrete subclasses.
        """
        pass

    def calculate_metrics(self):
        """Standard metrics calculation (SOLID: Single Responsibility)."""
        for p in self.processes:
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time

    def get_average_metrics(self) -> Tuple[float, float]:
        """Returns (Average Waiting Time, Average Turnaround Time)."""
        if not self.processes:
            return 0.0, 0.0
        
        total_wait = sum(p.waiting_time for p in self.processes)
        total_tat = sum(p.turnaround_time for p in self.processes)
        n = len(self.processes)
        
        return total_wait / n , total_tat / n