from enum import Enum, auto
from typing import Optional

class ProcessState(Enum):
    """Enumeration of possible process states."""
    NEW = auto()
    READY = auto()
    RUNNING = auto()
    WAITING = auto()
    TERMINATED = auto()

class Process:
    """
    Represents a simulated Operating System process.
    
    This class encapsulates all necessary information for process scheduling and
    lifecycle management within the simulator.
    """

    def __init__(
        self,
        pid: int,
        name: str,
        arrival_time: int,
        burst_time: int,
        priority: int = 0,
        memory_required: int = 0
    ):
        """
        Initializes a new Process instance.

        Args:
            pid: Unique Process Identifier.
            name: Human-readable name of the process.
            arrival_time: Time at which the process enters the system.
            burst_time: Total CPU time required by the process.
            priority: Scheduling priority (default 0).
            memory_required: Amount of memory needed by the process (default 0).
        """
        self.pid = pid
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.memory_required = memory_required
        
        # Runtime attributes
        self.state = ProcessState.NEW
        self.remaining_time = burst_time
        
        # Metrics
        self.waiting_time: int = 0
        self.turnaround_time: int = 0
        self.completion_time: Optional[int] = None

    def update_state(self, new_state: ProcessState) -> None:
        """
        Updates the current state of the process.

        Args:
            new_state: The ProcessState to transition to.
        """
        self.state = new_state

    def execute_one_unit(self) -> None:
        """
        Simulates the execution of the process for one time unit.
        Decrements remaining time and updates state to TERMINATED if finished.
        
        Note: This method assumes the caller (scheduler) ensures the process 
        is in the RUNNING state.
        """
        if self.remaining_time > 0:
            self.remaining_time -= 1
            
            if self.remaining_time == 0:
                self.update_state(ProcessState.TERMINATED)

    def is_completed(self) -> bool:
        """
        Checks if the process has finished its execution.

        Returns:
            True if remaining_time is 0, False otherwise.
        """
        return self.remaining_time == 0

    def calculate_metrics(self, current_time: int) -> None:
        """
        Calculates and updates performance metrics for the process.
        Should be called when the process finishes execution.

        Turnaround Time = Completion Time - Arrival Time
        Waiting Time = Turnaround Time - Burst Time

        Args:
            current_time: The time at which the process completed.
        """
        self.completion_time = current_time
        self.turnaround_time = self.completion_time - self.arrival_time
        self.waiting_time = self.turnaround_time - self.burst_time

    def __repr__(self) -> str:
        return (f"Process(pid={self.pid}, name='{self.name}', state={self.state.name}, "
                f"rem={self.remaining_time}, wait={self.waiting_time})")
