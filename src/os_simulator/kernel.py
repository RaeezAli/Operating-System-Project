import logging
from typing import List, Optional, Protocol, Any, Tuple
from os_simulator.process import Process, ProcessState
from os_simulator.system_clock import SystemClock

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("OS-Kernel")

class Scheduler(Protocol):
    """Protocol defining the interface for scheduling algorithms."""
    def schedule(self, process_list: List[Process]) -> List[Any]:
        """
        Takes a list of processes and returns the execution order/segments.
        
        Args:
            process_list: List of Process objects to be scheduled.
            
        Returns:
            A list of execution segments (e.g., GanttEntry or similar).
        """
        ...

from os_simulator.memory_management.paging import PagingMemoryManager

class Kernel:
    """
    Central orchestrator for the OS simulator.
    
    The Kernel manages the process table, clock, and orchestrates the simulation
    by delegating scheduling decisions to a pluggable scheduler and managing memory.
    """

    def __init__(self, context_switch_time: int = 0, system_clock: Optional[SystemClock] = None):
        """
        Initializes the Kernel.
        
        Args:
            context_switch_time: Overhead time units added when switching between processes.
            system_clock: Persistent clock instance for tracking simulation time.
        """
        self.process_table: List[Process] = []
        self.ready_queue: List[Process] = []
        self.scheduler: Optional[Scheduler] = None
        self.memory_manager = PagingMemoryManager()
        self.context_switch_time = context_switch_time
        self.system_clock = system_clock if system_clock else SystemClock()
        self.execution_order: List[Any] = []
        logger.info(f"Kernel initialized with Paging Memory Manager. (CS Overhead: {context_switch_time})")

    def add_process(self, process: Process) -> None:
        """
        Adds a new process to the kernel's process table and allocates memory.

        Args:
            process: The Process object to be added.
        """
        # Attempt to allocate memory first
        if self.memory_manager.allocate(process.pid, process.memory_required):
            self.process_table.append(process)
            logger.info(f"Process {process.pid} ({process.name}) added to process table and memory allocated.")
        else:
            logger.error(f"Failed to add Process {process.pid}: Insufficient memory.")

    def set_scheduler(self, scheduler: Scheduler) -> None:
        """
        Dynamically sets or switches the scheduling algorithm.

        Args:
            scheduler: An object implementing the Scheduler protocol.
        """
        self.scheduler = scheduler
        scheduler_name = type(scheduler).__name__
        logger.info(f"Scheduler switched to {scheduler_name}.")

    def dispatch(self) -> List[Tuple[Any, int, int]]:
        """
        Delegates scheduling to the current scheduler and post-processes the timeline
        to include context switching overhead.

        Returns:
            A list of tuples (pid_or_msg, start_time, end_time).
        """
        if not self.scheduler:
            logger.error("Attempted to dispatch without a scheduler set.")
            raise ValueError("No scheduler set. Call set_scheduler() first.")

        logger.info("Dispatching processes to scheduler...")
        
        active_processes = [p for p in self.process_table if p.state != ProcessState.TERMINATED]
        for p in active_processes:
            if p.state == ProcessState.NEW:
                p.update_state(ProcessState.READY)
                self.ready_queue.append(p)

        # 1. Get raw timeline from scheduler
        raw_result = self.scheduler.schedule(active_processes)
        
        # 2. Process timeline: insert context switching overhead
        final_timeline = []
        current_clock = 0
        last_pid = None

        for pid, start, end in raw_result:
            duration = end - start
            
            # Detect idle gap in scheduler's timeline
            if start > current_clock:
                idle_gap = start - current_clock
                for _ in range(idle_gap):
                    self.system_clock.tick(is_busy=False)
                current_clock = start

            # Inject Context Switch if switching processes
            if last_pid is not None and last_pid != pid and self.context_switch_time > 0:
                cs_end = current_clock + self.context_switch_time
                final_timeline.append(("CS", current_clock, cs_end))
                # CPU is 'busy' doing context switching work
                for _ in range(self.context_switch_time):
                    self.system_clock.tick(is_busy=True)
                current_clock = cs_end

            # Add process execution segment
            seg_end = current_clock + duration
            final_timeline.append((pid, current_clock, seg_end))
            # CPU is 'busy' doing process work
            for _ in range(duration):
                self.system_clock.tick(is_busy=True)
            
            current_clock = seg_end
            last_pid = pid

        self.execution_order = final_timeline
        logger.info(f"Dispatch completed. Generated {len(final_timeline)} segments (including overhead).")
        return final_timeline

    def run(self) -> List[Any]:
        """
        Executes the full simulation using the current configuration.

        Returns:
            The final execution log/sequence.
        """
        logger.info("Starting simulation run...")
        try:
            return self.dispatch()
        except Exception as e:
            logger.error(f"Simulation failed: {e}")
            return []

    def reset(self) -> None:
        """
        Resets the kernel state to its initial configuration.
        """
        self.system_clock.reset()
        self.execution_order = []
        self.ready_queue = []
        self.memory_manager.reset()
        for p in self.process_table:
            p.remaining_time = p.burst_time
            p.state = ProcessState.NEW
            p.completion_time = None
            p.waiting_time = 0
            p.turnaround_time = 0
            self.memory_manager.allocate(p.pid, p.memory_required)
            
        logger.info("Kernel state and Memory reset.")

    def __repr__(self) -> str:
        return f"Kernel(processes={len(self.process_table)}, scheduler={type(self.scheduler).__name__ if self.scheduler else 'None'})"
