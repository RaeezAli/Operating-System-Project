from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Process:
    """Represents a process in the OS simulator."""
    pid: str
    burst_time: int
    arrival_time: int = 0
    priority: int = 0
    remaining_time: int = field(init=False)
    completion_time: int = 0
    waiting_time: int = 0
    turnaround_time: int = 0

    def __post_init__(self):
        self.remaining_time = self.burst_time

@dataclass
class GanttEntry:
    """Represents a single segment of process execution in a Gantt chart."""
    pid: str
    start_time: int
    end_time: int
