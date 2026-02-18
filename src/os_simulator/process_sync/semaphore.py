import threading
import logging

logger = logging.getLogger("Semaphore")

class CountingSemaphore:
    """
    A thread-safe implementation of a Counting Semaphore using Python threading.
    
    Provides standard wait() and signal() operations to synchronize process 
    access to a shared pool of resources.
    """

    def __init__(self, initial_value: int = 1):
        """
        Initializes the semaphore with a starting value.
        
        Args:
            initial_value: The initial count (default 1, acting as a Mutex).
        """
        self.value = initial_value
        self.condition = threading.Condition()
        logger.info(f"Counting Semaphore initialized with value: {self.value}")

    def wait(self) -> None:
        """
        The P (Proberen) operation. 
        Decrements the semaphore value. If the value is 0, the thread blocks 
        until a signal() is received.
        """
        with self.condition:
            while self.value <= 0:
                logger.debug(f"Thread {threading.current_thread().name} waiting on semaphore...")
                self.condition.wait()
            
            self.value -= 1
            logger.debug(f"Thread {threading.current_thread().name} acquired semaphore. Value now: {self.value}")

    def signal(self) -> None:
        """
        The V (Verhogen) operation.
        Increments the semaphore value and notifies one waiting thread.
        """
        with self.condition:
            self.value += 1
            logger.debug(f"Thread {threading.current_thread().name} signaled semaphore. Value now: {self.value}")
            self.condition.notify()

    def __enter__(self):
        """Context manager support (standard wait)."""
        self.wait()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager support (standard signal)."""
        self.signal()