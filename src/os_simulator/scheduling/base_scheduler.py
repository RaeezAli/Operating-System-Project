from abc import ABC, abstractmethod
from typing import List, Tuple
from os_simulator.process import Process

class BaseScheduler(ABC):
    """
    Abstract Base Class for all Scheduling Algorithms.
    
    Provides a standardized interface for scheduling processes and 
    calculating performance metrics. Concrete implementations must 
    define the logic for execution order.
    """

    @abstractmethod
    def schedule(self, process_list: List[Process]) -> List[Tuple[int, int, int]]:
        """
        Calculates the execution order for a given list of processes.
        
        Args:
            process_list: List of Process objects to schedule.
            
        Returns:
            A list of tuples representing the execution timeline:
            [(pid, start_time, end_time), ...]
        """
        pass

    @abstractmethod
    def calculate_metrics(self, process_list: List[Process]) -> None:
        """
        Calculates and updates performance metrics for each process in the list.
        Typically updates Waiting Time and Turnaround Time.
        
        Args:
            process_list: List of Process objects that have completed execution.
        """
        pass