import threading
import time
import random
import logging
from typing import List
from src.os_simulator.process_sync.semaphore import CountingSemaphore

logger = logging.getLogger("Producer-Consumer")

class BoundedBuffer:
    """A thread-safe bounded buffer using semaphores."""
    def __init__(self, size: int):
        self.size = size
        self.buffer: List[int] = []
        
        # Semaphores
        self.mutex = CountingSemaphore(1)      # Binary semaphore for buffer access
        self.empty = CountingSemaphore(size)   # Counts empty slots
        self.full = CountingSemaphore(0)       # Counts full slots

    def produce(self, item: int, producer_id: int):
        """Adds an item to the buffer."""
        self.empty.wait()      # Wait for an empty slot
        with self.mutex:       # Critical section
            self.buffer.append(item)
            logger.info(f"Producer {producer_id} added {item}. Buffer size: {len(self.buffer)}")
        self.full.signal()     # Signal a new full slot

    def consume(self, consumer_id: int) -> int:
        """Removes an item from the buffer."""
        self.full.wait()       # Wait for a full slot
        item = -1
        with self.mutex:       # Critical section
            item = self.buffer.pop(0)
            logger.info(f"Consumer {consumer_id} took {item}. Buffer size: {len(self.buffer)}")
        self.empty.signal()    # Signal a new empty slot
        return item

def producer_task(buffer: BoundedBuffer, producer_id: int, count: int):
    for i in range(count):
        item = random.randint(1, 100)
        buffer.produce(item, producer_id)
        time.sleep(random.uniform(0.1, 0.5))

def consumer_task(buffer: BoundedBuffer, consumer_id: int, count: int):
    for _ in range(count):
        item = buffer.consume(consumer_id)
        time.sleep(random.uniform(0.2, 0.7))

def run_producer_consumer_demo():
    """Demonstrates the Producer-Consumer problem using semaphores."""
    print(">>> PRODUCER-CONSUMER SYNC DEMO <<<\n")
    buffer = BoundedBuffer(size=5)
    
    # Create threads
    p1 = threading.Thread(target=producer_task, args=(buffer, 1, 10), name="Producer-1")
    c1 = threading.Thread(target=consumer_task, args=(buffer, 1, 10), name="Consumer-1")
    
    p1.start()
    c1.start()
    
    p1.join()
    c1.join()
    print("\nDemonstration complete. Buffer correctly synchronized.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(threadName)s] %(message)s')
    run_producer_consumer_demo()