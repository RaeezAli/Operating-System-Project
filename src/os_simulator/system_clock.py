import logging

logger = logging.getLogger("System-Clock")

class SystemClock:
    """
    Central timekeeper for the OS simulator.
    Tracks global simulation time and CPU states (busy vs. idle).
    """

    def __init__(self):
        """Initializes the clock with zeroed counters."""
        self.global_time: int = 0
        self.busy_time: int = 0
        self.idle_time: int = 0
        logger.info("System Clock initialized.")

    def tick(self, is_busy: bool = True) -> None:
        """
        Advances the simulation clock by one time unit.
        
        Args:
            is_busy: Boolean indicating if the CPU was executing a process (True)
                     or was idle (False) during this tick.
        """
        self.global_time += 1
        if is_busy:
            self.busy_time += 1
        else:
            self.idle_time += 1
        
        logger.debug(f"Clock Tick: {self.global_time} (Busy: {is_busy})")

    def reset(self) -> None:
        """Resets all clock counters to initial state."""
        self.global_time = 0
        self.busy_time = 0
        self.idle_time = 0
        logger.info("System Clock reset.")

    def get_time(self) -> int:
        """Returns the current global simulation time."""
        return self.global_time

    def get_busy_time(self) -> int:
        """Returns the total number of busy cycles."""
        return self.busy_time

    def get_idle_time(self) -> int:
        """Returns the total number of idle cycles."""
        return self.idle_time

    def get_cpu_utilization(self) -> float:
        """
        Calculates the CPU utilization as a percentage.
        
        Returns:
            The percentage of time the CPU was busy (0.0 to 100.0).
        """
        if self.global_time == 0:
            return 0.0
        return round((self.busy_time / self.global_time) * 100, 2)

    def __str__(self) -> str:
        """Returns a string representation of the clock state."""
        return (f"Clock State: Time={self.global_time}, "
                f"Busy={self.busy_time}, Idle={self.idle_time}, "
                f"Utilization={self.get_cpu_utilization()}%")
