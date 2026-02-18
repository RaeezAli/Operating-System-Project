from dataclasses import dataclass
from typing import List, Optional
from src.os_simulator.process import Process

@dataclass
class GanttEntry:
    """Represents a single segment of process execution in a Gantt chart."""
    pid: str
    start_time: int
    end_time: int
